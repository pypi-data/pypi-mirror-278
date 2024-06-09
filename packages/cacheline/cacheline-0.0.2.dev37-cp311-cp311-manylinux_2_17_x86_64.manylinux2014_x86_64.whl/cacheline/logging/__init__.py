import atexit
import logging
import multiprocessing
import queue
import sys
import time
from logging import _acquireLock, _releaseLock
from multiprocessing import process
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Union, cast
from urllib.parse import quote_plus, urljoin

import colorlog
import requests
from pythonjsonlogger import jsonlogger

from ._util import should_colorize
from .logger import Logger

if sys.version_info >= (3, 12) and ("taskName" not in jsonlogger.RESERVED_ATTRS):
    jsonlogger.RESERVED_ATTRS = ("taskName", *jsonlogger.RESERVED_ATTRS)


_DEFAULT_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | [%(process)d,%(thread)d] | %(pathname)s:%(lineno)s#%(funcName)s | %(message)s"
_DEFAULT_FORMATTER = (
    colorlog.ColoredFormatter(
        "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s %(reset)s%(pathname)s:%(lineno)d ",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={
            "message": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            }
        },
        style="%",
    )
    if should_colorize(sys.stderr)
    else logging.Formatter(_DEFAULT_FORMAT)
)


def _getHandler():
    return (
        colorlog.StreamHandler(sys.stderr)
        if should_colorize(sys.stderr)
        else logging.StreamHandler(sys.stderr)
    )


def getLogger(
    name: str,
    *,
    handlers: Optional[Union[logging.Handler, Sequence[logging.Handler]]] = None,
    log_path: Optional[Union[str, Path]] = None,
) -> Logger:
    _acquireLock()
    _lc = logging.Logger.manager.loggerClass  # pylint:disable=no-member
    logging.root.manager.setLoggerClass(Logger)  # pylint:disable=no-member
    _logger = logging.getLogger(name)
    if _lc:
        logging.root.manager.setLoggerClass(_lc)  # pylint:disable=no-member
    _releaseLock()
    _logger.propagate = False

    have_stream_handler = False
    if handlers is not None:
        if isinstance(handlers, logging.Handler):
            _logger.addHandler(handlers)
            have_stream_handler = isinstance(handlers, logging.StreamHandler)
        else:
            for handler in handlers:
                _logger.addHandler(handler)
                have_stream_handler = have_stream_handler or isinstance(
                    handler, logging.StreamHandler
                )

    if not have_stream_handler:
        stream_handler = _getHandler()
        formatter = _DEFAULT_FORMATTER
        stream_handler.setFormatter(formatter)
        _logger.addHandler(stream_handler)

    if log_path is not None:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter(_DEFAULT_FORMAT))
        _logger.addHandler(file_handler)

    _logger.setLevel(logging.INFO)
    return cast(Logger, _logger)


logger = getLogger(
    "cacheline.logging",
)


class LoggerLauncher(logging.Handler):
    def __init__(self, push_function: Callable[[str], None]):
        super().__init__()
        self._push_function = push_function
        self.setLevel(logging.INFO)
        formatter = jsonlogger.JsonFormatter(_DEFAULT_FORMAT)
        self.setFormatter(formatter)

    def emit(self, record):
        self._push_function(self.format(record))

    def getLogger(self, name: str) -> Logger:
        _logger = getLogger(name, handlers=self)
        _logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(_DEFAULT_FORMATTER)
        stream_handler.setLevel(logging.DEBUG)
        _logger.addHandler(stream_handler)
        return _logger


def _consumer(_queue, server, key):
    while True:
        item = _queue.get()
        url = urljoin(server, f"LPUSH/{key}/{ quote_plus(item)}")
        try:
            requests.get(
                url,
                timeout=3,
            )
        except requests.RequestException as err:
            logger.exception(
                "Failed to push log to webdis, error: %s, url: %s", err, url
            )


class WebdisLoggerLauncher(LoggerLauncher):
    def __init__(self, server: str, key: str, queue_size=4096, timeout=3):
        super().__init__(self.push)
        self._url = server
        self._key = quote_plus(key)
        self._timeout = timeout
        _queue: "multiprocessing.Queue[str]" = multiprocessing.Queue(queue_size)
        self._queue = _queue

        self._consumer_started = False

    def start(self):
        _queue = self._queue
        server = self._url
        key = self._key

        self._process = multiprocessing.Process(
            target=_consumer, args=(_queue, server, key)
        )
        self._process.daemon = True
        self._process.start()

        self._consumer_started = True

        def wait_finish():
            while not self._queue.empty() and self._process.is_alive():
                time.sleep(1)
                logger.info("Waiting for consumer")
            self._process.terminate()

        atexit.register(wait_finish)

    def push(self, row: str):
        if not self._consumer_started:
            if not getattr(process.current_process(), "_inheriting", False):
                logger.info("🚀 Consumer not started, starting it")
                self.start()
            else:
                logger.info(
                    "Consumer not started, but it's in child process, not starting it"
                )
        try:
            self._queue.put(row, timeout=self._timeout)
        except queue.Full:
            logger.exception(
                "Failed to push log to webdis, queue is full, dropping log %s", row
            )
            if not self._consumer_started:
                self.start()
