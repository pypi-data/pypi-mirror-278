# Copyright (C) 2022 Bjarne von Horn (vh at igh dot de).
#
# This file is part of the PdCom library.
#
# The PdCom library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# The PdCom library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more .
#
# You should have received a copy of the GNU Lesser General Public License
# along with the PdCom library. If not, see <http://www.gnu.org/licenses/>.

from asyncio import Event, Future, get_event_loop
from . import _PdComWrapper as PdComWrapper
from .Variable import Variable
from datetime import timedelta
from numbers import Number
from typing import Any, Optional, Union, AsyncGenerator
from weakref import WeakSet
import numpy
import warnings


class _Subscription(PdComWrapper.Subscription):
    def __init__(
        self,
        subscriber: "SubscriberBase",
        variable: Union[str, PdComWrapper.Variable],
        fut: Future,
        selector: Optional[PdComWrapper.Selector],
    ):
        if isinstance(variable, str):
            super().__init__(
                subscriber._subscriber,
                subscriber._subscriber._process._process,
                variable,
                selector,
            )
        else:
            super().__init__(subscriber._subscriber, variable._v, selector)
        self._pending_subscription_future = fut
        self._value_queue = []

    def _push_value_queue(self, ts):
        self._value_queue.append((self.value, ts))

    def _pop_value_queue(self):
        self._value_queue.pop(0)

    def current_value(self, expected_ts):
        if expected_ts is not None:
            if expected_ts != self._value_queue[0][1]:
                raise RuntimeError(
                    "timestamp mismatch, sample cache has become invalid."
                )
            return self._value_queue[0][0]
        return self.value


class Subscription:
    State = PdComWrapper.Subscription.State
    """State enum of a subscription"""

    def __init__(
        self,
        subscriber: "SubscriberBase",
        variable: Union[str, PdComWrapper.Variable],
        fut: Future,
        selector: Optional[PdComWrapper.Selector],
    ):
        self.subscriber = subscriber
        self._subscription = _Subscription(subscriber, variable, fut, selector)
        subscriber._subscriber._subscriptions.add(self)
        # trigger process to call callbacks in case subscription is already ready
        subscriber._subscriber._process._process.callPendingCallbacks()

    def cancel(self):
        """Cancel a subscription."""
        if self._subscription is not None:
            self._subscription.cancel()
            self._subscription = None

    async def poll(self):
        """Poll an existing subscription.

        This can for example be used to refresh an event-based subscription.
        """
        # FIXME(vh) in case of event or periodic subscription,
        # newValues() may be called prematurely
        self._subscription.poll()
        gen = self.subscriber.newValues(autoclose=False)
        try:
            async for _ in gen:
                return self.value
        finally:
            await gen.aclose()

    async def read(self):
        """Wait for an update and return the new value.

        :return: tuple of (value, timestamp)
        """
        try:
            gen = self.subscriber.newValues(autoclose=False).__aiter__()
            async for ts in gen:
                return (self.value, ts)
        finally:
            await gen.aclose()

    @property
    def value(self):
        """The current value."""
        v = self._subscription.current_value(
            self.subscriber._subscriber.getCurrentTimestamp()
        )
        if v.shape == (1,):
            return v[0]
        else:
            return v

    @property
    def variable(self):
        """The corresponding variable."""
        return Variable(self._subscription.variable)

    @property
    def state(self) -> "Subscription.State":
        """The current state of the subscription."""
        return self._subscription.state

    def __iter__(self):
        """Iterate Row-wise over values."""
        return numpy.nditer(
            self._subscription.current_value(
                self.subscriber._subscriber.getCurrentTimestamp()
            ),
            order="C",
        )


class SubscriptionWithSubscriber(Subscription):
    def newValues(self) -> AsyncGenerator[timedelta, Any]:
        """Iterate over all incoming values.

        This functions an asynchronous generator for the timestamp
        of incoming data.
        In the body of the loop, the :py:attr:`~.Subscription.value`
        attribute belongs to the current timestamp.

        .. code-block:: python

            import pdcom5
            process = pdcom5.Process()
            await process.connect("msr://localhost")
            subscription = await process.subscribe(0.1, "/osc/cos")
            async for timestamp in subscription.newValues():
                print(f"At {timestamp}, cos was {subscription.value}"

        For more details, see :py:meth:`SubscriberBase.newValues()`.

        """
        return self.subscriber.newValues().__aiter__()


class _Subscriber(PdComWrapper.Subscriber):
    def __init__(self, process, transmission: PdComWrapper.Transmission):
        if isinstance(transmission, timedelta):
            transmission = PdComWrapper.Transmission(transmission)
        elif isinstance(transmission, Number):
            transmission = PdComWrapper.Transmission(timedelta(seconds=transmission))
        super().__init__(transmission)
        self._process = process
        process._process._subscribers.add(self)
        self._newvalues_event: Event = Event()
        self._process_exception = None
        self._subscriptions: WeakSet[Subscription] = WeakSet()
        self._task_is_listening = False
        self._cached_timestamps: list[timedelta] = []

    def stateChanged(self, s: PdComWrapper.Subscription) -> None:
        if s.state == s.State.Active and s._pending_subscription_future is not None:
            if not s._pending_subscription_future.cancelled():
                s._pending_subscription_future.set_result(None)
            s._pending_subscription_future = None
        elif s.state == s.State.Invalid and s._pending_subscription_future is not None:
            if not s._pending_subscription_future.cancelled():
                s._pending_subscription_future.set_exception(
                    PdComWrapper.InvalidSubscription()
                )
            s._pending_subscription_future = None

    def newValues(self, time: timedelta) -> None:
        # this is a virtual function called by C++ PdCom5
        if self._task_is_listening:
            # caching values requested because of "synchronizeNewValues"
            for subscription in self._subscriptions:
                if subscription is not None:
                    subscription._subscription._push_value_queue(time)
            self._cached_timestamps.append(time)
            self._process_exception = None
            self._newvalues_event.set()

    def getCurrentTimestamp(self):
        if not self._task_is_listening:
            return None
        return self._cached_timestamps[0]

    async def synchronizerEnter(self) -> timedelta:
        await self._newvalues_event.wait()
        # raise exception passed by Process._cancel_all_futures
        if self._process_exception is not None:
            raise self._process_exception
        return self._cached_timestamps[0]

    async def synchronizerExit(self):
        # user is done processing current values, so close the window
        self._task_is_listening = False
        self._pop_queue()

    def _pop_queue(self):
        if len(self._cached_timestamps) == 0:
            return
        for sub in self._subscriptions:
            if sub is not None:
                sub._subscription._pop_value_queue()
        self._cached_timestamps.pop(0)
        if len(self._cached_timestamps) == 0:
            self._newvalues_event.clear()

    async def iterNewValues(self, autoclose):
        try:
            while True:
                yield await self.synchronizerEnter()
                self._pop_queue()
        finally:
            await self.synchronizerExit()
            if autoclose:
                for subscription in self._subscriptions:
                    if subscription is not None:
                        subscription.cancel()


class NewValuesSynchronizer:
    def __init__(self, sub: "_Subscriber", autoclose: bool):
        self._subscriber = sub
        if self._subscriber._task_is_listening:
            raise ValueError("do not use the same subscription in multiple tasks")
        self._subscriber._task_is_listening = True
        self._mode = None
        self._autoclose = autoclose
        self._async_iter = None

    async def __aenter__(self) -> timedelta:
        warnings.warn(
            "This API is deprecated and will be removed in PdCom 6. Please use async for",
            FutureWarning,
        )
        if self._mode == "iter":
            raise ValueError("use either async with or async for, not both.")
        self._mode = "with"
        return await self._subscriber.synchronizerEnter()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._subscriber.synchronizerExit()
        return False

    def __aiter__(self):
        if self._mode == "with":
            raise ValueError("use either async with or async for, not both.")
        self._mode = "iter"
        self._async_iter = self._subscriber.iterNewValues(self._autoclose).__aiter__()
        return self._async_iter

    async def aclose(self):
        if self._async_iter is None:
            return
        await self._async_iter.aclose()
        self._async_iter = None


class SubscriberBase:
    def __init__(self, process, transmission: PdComWrapper.Transmission):
        self._subscriber = _Subscriber(process, transmission)

    def newValues(self, autoclose=True) -> AsyncGenerator[timedelta, Any]:
        """Entry point for library users to process incoming data.

        .. versionchanged:: 5.3 Use generator instead of context manager.

        This function returns an asynchronous generator.
        In the body of the :code:`async for` loop, the values of the subscriptions
        assigned to this subscriber are guaranteed to not change.
        If you break out of the loop early,
        all subscriptions are cancelled automatically,
        unless ``autoclose`` is set to False.

        :param autoclose: Close connections when leaving the loop, defaults to True

        The following example shows how to subscribe to two variables with
        a period of one second.

        .. code-block:: python

            import pdcom5
            process = pdcom5.Process()
            await process.connect("msr://localhost")
            subscriber = process.create_subscriber(1.0)
            cos = await subscriber.subscribe("/osc/cos")
            sin = await subscriber.subscribe("/osc/sin")
            async for timestamp in subscriber.newValues():
                print(f"At {timestamp}, cos was {cos.value}" +
                        f" and sin was {sin.value}.")

        Please do not do any blocking operations in the body of the loop,
        like sleeping for a long time. The reason is that the library
        has to cache the incoming values to make sure no data is
        skipped. Also, using the same subscription in multiple concurrent tasks
        is not allowed, for the same reason. Just create one subscriber per task.

        If you want to reuse existing subscriptions and break out of
        the loop early, pay attention to close the generator fully before
        reusing. This can be done using a ``try...finally`` block or by using
        `contextlib.aclosing
        <https://docs.python.org/3.10/library/contextlib.html#contextlib.aclosing>`_.

        .. code-block:: python

            timestamp_gen = subscriber.newValues(autoclose=False)
            try:
                async for timestamp in timestamp_gen:
                    process(timestamp)
                    break
            finally:
                await timestamp_gen.aclose()
                # subscriber.newValues() can now be called again

        """
        return NewValuesSynchronizer(self._subscriber, autoclose)


class Subscriber(SubscriberBase):
    """Variable subscriber.

    This class manages how variables are subscribed and the callback when new
    values are received.

    :param process: Process instance
    :param transmission: Kind of subscription (poll, event based, periodic)
    """

    def __init__(self, process, transmission: PdComWrapper.Transmission):
        super().__init__(process, transmission)

    async def subscribe(
        self,
        variable: Union[str, PdComWrapper.Variable],
        selector: Optional[PdComWrapper.Selector] = None,
    ) -> Subscription:
        """Subscribe to a variable.

        :param variable: Variable to subscribe.
        :param selector: Optional selector to create a view on multidimensional data.

        :return: a Subscription instance.
        """
        fut = get_event_loop().create_future()
        ans = Subscription(self, variable, fut, selector)
        await fut
        return ans
