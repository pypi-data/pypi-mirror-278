"""Zurich Instruments communication protocol bindings."""

from __future__ import annotations
from zhinst.comms._comms import Callback
from zhinst.comms._comms import CapnpContext
from zhinst.comms._comms import DestinationParams
from zhinst.comms._comms import DynamicClient
from zhinst.comms._comms import DynamicEnum
from zhinst.comms._comms import DynamicList
from zhinst.comms._comms import DynamicServer
from zhinst.comms._comms import DynamicStructBase
from zhinst.comms._comms import Fulfiller
from zhinst.comms._comms import LogSeverity
from zhinst.comms._comms import SchemaLoader
from zhinst.comms._comms import errors
from zhinst.comms._comms import init_logs
from . import _comms

__all__ = [
    "Callback",
    "CapnpContext",
    "DEBUG",
    "DestinationParams",
    "DynamicClient",
    "DynamicEnum",
    "DynamicList",
    "DynamicServer",
    "DynamicStructBase",
    "ERROR",
    "Fulfiller",
    "INFO",
    "LogSeverity",
    "STATUS",
    "SchemaLoader",
    "TRACE",
    "WARNING",
    "errors",
    "init_logs",
]
DEBUG: _comms.LogSeverity  # value = <LogSeverity.DEBUG: 1>
ERROR: _comms.LogSeverity  # value = <LogSeverity.ERROR: 5>
INFO: _comms.LogSeverity  # value = <LogSeverity.INFO: 2>
STATUS: _comms.LogSeverity  # value = <LogSeverity.STATUS: 3>
TRACE: _comms.LogSeverity  # value = <LogSeverity.TRACE: 0>
WARNING: _comms.LogSeverity  # value = <LogSeverity.WARNING: 4>
__commit_hash__: str = "f5c7a56f126699ab60ccfef5ca696f3c337a9d3d"
__version__: str = "0.0.1"
