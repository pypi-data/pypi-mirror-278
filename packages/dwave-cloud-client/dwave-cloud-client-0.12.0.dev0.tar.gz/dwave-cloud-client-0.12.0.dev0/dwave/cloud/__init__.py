# Copyright 2017 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
import re
import sys
import json
import logging
import datetime
import importlib
import typing

from dwave.cloud.client import Client
from dwave.cloud.solver import Solver
from dwave.cloud.computation import Future
from dwave.cloud.utils import parse_loglevel

__all__ = ['Client', 'Solver', 'Future']


# prevent log output (from library) when logging not configured by user/app
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# add TRACE log level and Logger.trace() method
logging.TRACE = 5
logging.addLevelName(logging.TRACE, "TRACE")

def _trace(logger, message, *args, **kwargs):
    logger.log(logging.TRACE, message, *args, **kwargs)

logging.Logger.trace = _trace


class ISOFormatter(logging.Formatter):
    # target timezone, e.g. `datetime.timezone.utc`, or `None` for naive timestamp
    as_tz: typing.Optional[datetime.timezone] = None

    def __init__(self, *args, as_tz: typing.Optional[datetime.timezone] = None, **kwargs):
        self.as_tz = as_tz
        super().__init__(*args, **kwargs)

    def formatTime(self, record: logging.LogRecord, datefmt: typing.Optional[str] = None) -> str:
        return datetime.datetime.fromtimestamp(record.created, tz=self.as_tz).isoformat()


class FilteredSecretsFormatter(logging.Formatter):
    """Logging formatter that filters out secrets (like Solver API tokens).

    Note: we assume, for easier disambiguation, a secret/token is prefixed with
    a short alphanumeric string, and comprises 40 or more hex digits.
    """

    # prefixed 160-bit+ hex tokens (sapi token format: `A{2,4}-X{40,}`)
    _SAPI_TOKEN_PATTERN = re.compile(
        r'\b([0-9A-Za-z]{2,4}-[0-9A-Fa-f]{3})([0-9A-Fa-f]{34,})([0-9A-Fa-f]{3})\b')
    # 128-bit+ hex tokens (`X{32,}`)
    _HEX_TOKEN_PATTERN = re.compile(
        r'\b([0-9A-Fa-f]{3})([0-9A-Fa-f]{26,})([0-9A-Fa-f]{3})\b')
    # 128-bit uuid tokens (`X{8}-X{4}-X{4}-X{4}-X{12}`)
    _UUID_TOKEN_PATTERN = re.compile(
        r'\b([0-9A-Fa-f]{3})([0-9A-Fa-f]{5}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{9})([0-9A-Fa-f]{3})\b')

    def format(self, record: logging.LogRecord) -> str:
        output = super().format(record)
        output = re.sub(self._SAPI_TOKEN_PATTERN, r'\1...\3', output)
        output = re.sub(self._HEX_TOKEN_PATTERN, r'\1...\3', output)
        output = re.sub(self._UUID_TOKEN_PATTERN, r'\1...\3', output)
        return output


class JSONFormatter(ISOFormatter):
    def format(self, record: logging.LogRecord) -> str:
        super().format(record)
        # filter out message template and potentially unserializable args
        rec = record.__dict__.copy()
        del rec['args']
        del rec['msg']
        return json.dumps(rec)


def configure_logging(logger: typing.Optional[logging.Logger] = None,
                      *,
                      level: int = logging.WARNING,
                      filter_secrets: bool = True,
                      output_stream: typing.Optional[io.IOBase] = None,
                      in_utc: bool = False,
                      structured_output: bool = False,
                      handler_level: typing.Optional[int] = None,
                      additive: bool = False,
                      ) -> logging.Logger:
    """Configure cloud-client's `dwave.cloud` base logger.

    Logging output from the cloud-client is suppressed by default. This utility
    function can be used to quickly setup basic logging from the library.

    .. note::
       This function is currently intended for internal/private use only.

    .. versionadded:: 0.12.0
       Explicit optional logging configuration. Previously, logger was minimally
       configured by default.
    """

    if logger is None:
        logger = logging.getLogger(__name__)
    if output_stream is None:
        output_stream = sys.stderr
    if handler_level is None:
        handler_level = level

    format = dict(
        fmt='%(asctime)s %(name)s %(levelname)s %(threadName)s [%(funcName)s] %(message)s',
        as_tz=datetime.timezone.utc if in_utc else None,
    )

    if structured_output:
        formatter_base = JSONFormatter
    else:
        formatter_base = ISOFormatter

    if filter_secrets:
        class Formatter(FilteredSecretsFormatter, formatter_base):
            pass
    else:
        Formatter = formatter_base

    if not additive:
        # make sure handlers are not accumulated
        while len(logger.handlers):
            logger.removeHandler(logger.handlers[-1])

    formatter = Formatter(**format)
    handler = logging.StreamHandler(stream=output_stream)
    handler.setFormatter(formatter)
    handler.setLevel(handler_level)

    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


# configure logger if DWAVE_LOG_LEVEL present in environment
def _apply_loglevel_from_env(logger):
    if log_level := os.getenv('DWAVE_LOG_LEVEL', os.getenv('dwave_log_level')):
        level = parse_loglevel(log_level)
        log_format = os.getenv('DWAVE_LOG_FORMAT', os.getenv('dwave_log_format', ''))
        structured = log_format.strip().lower() == 'json'
        configure_logging(logger, level=level, structured_output=structured)

_apply_loglevel_from_env(logger)


# alias dwave.cloud.client.{qpu,sw,hybrid} as dwave.cloud.*
def _alias_old_client_submodules():
    for name in ('qpu', 'sw', 'hybrid'):
        # note: create both module and local attribute
        globals()[name] = sys.modules['dwave.cloud.{}'.format(name)] = \
            importlib.import_module('dwave.cloud.client.{}'.format(name))

_alias_old_client_submodules()
