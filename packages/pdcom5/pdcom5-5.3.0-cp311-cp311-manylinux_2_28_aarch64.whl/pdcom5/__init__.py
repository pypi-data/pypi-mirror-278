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

from .Subscription import SubscriberBase, Subscriber, Subscription, SubscriptionWithSubscriber
from .Process import BroadcastMessage, LoginFailed, ListReply, Process
from .Variable import Variable, TemporaryValueChange
from ._PdComWrapper import (
    ClientStatistics,
    Exception,
    InternalError,
    InvalidArgument,
    InvalidSubscription,
    LoginRequired,
    LogLevel,
    Message,
    NotConnected,
    ProcessGoneAway,
    ProtocolError,
    Selector,
    ScalarSelector,
    Transmission,
)

from ._PdComWrapper import full_version as fv

__all__ = [
    "BroadcastMessage",
    "ClientStatistics",
    "Exception",
    "InternalError",
    "InvalidArgument",
    "InvalidSubscription",
    "LoginFailed",
    "LoginRequired",
    "LogLevel",
    "ListReply",
    "Message",
    "NotConnected",
    "Process",
    "ProcessGoneAway",
    "ProtocolError",
    "Selector",
    "ScalarSelector",
    "SubscriberBase",
    "Subscriber",
    "Subscription",
    "SubscriptionWithSubscriber",
    "TemporaryValueChange",
    "Transmission",
    "Variable",
]

"""Git version hash, from PdCom5 C++ library"""
full_version = fv()
__version__ = "5.3.0"
