import logging
import sys
from typing import Optional

from cacheline.logging import _DEFAULT_FORMATTER, LoggerLauncher, _getHandler, getLogger

_logger = getLogger("cacheline.debug")


def _setup_debug_hook():
    from better_exceptions import hook  # pylint: disable=import-outside-toplevel

    hook()


def _patch_logger(logger: logging.Logger, log_filepath: Optional[str] = None):
    logger.propagate = False
    level = logger.level or logging.DEBUG
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler) and (
            handler.stream == sys.stdout or handler.stream == sys.stderr
        ):
            logger.removeHandler(handler)
        else:
            if not isinstance(handler, LoggerLauncher):
                handler.setLevel(level)
    stream_handler = _getHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(_DEFAULT_FORMATTER)
    logger.addHandler(stream_handler)

    if log_filepath:
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - 🌟 %(message)s - %(pathname)s:%(lineno)d"
            )
        )
        logger.addHandler(file_handler)

    _logger.info("patched logger %s", logger.name)


def _patch_all_logger(log_filepath: Optional[str] = None):
    _patch_logger(logging.getLogger(), log_filepath)
    for name, logger in logging.Logger.manager.loggerDict.items():
        if isinstance(logger, logging.PlaceHolder):
            _logger.info("ignore placeholder %s", name)
            continue
        _patch_logger(logger)


def _setup_debug_logging(log_filepath: Optional[str] = None):
    _patch_all_logger(log_filepath)


def enable_debugger_mode(
    *,
    logging_path: Optional[str] = None,
    better_exceptions: bool = True,
):
    """
    Enable debugger mode.
    Args:
        logging_path: Path to save the logs.
        better_exceptions: Use better_exceptions to print the exception.
    """
    _setup_debug_logging(logging_path)
    if better_exceptions:
        _setup_debug_hook()
