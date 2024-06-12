"""Utilities for CLI commands."""

import logging
from logging import handlers
from pathlib import Path

import click

LEVEL_TO_COLOR: dict[int, str] = {
    logging.DEBUG: "green",
    logging.INFO: "blue",
    logging.WARNING: "yellow",
    logging.ERROR: "magenta",
    logging.CRITICAL: "red",
}


logger = logging.getLogger(__package__.split(".")[0])


class FancyConsoleHandler(logging.StreamHandler):
    """A handler that prints colourful output to stderr."""

    def emit(self, record: logging.LogRecord):
        """Emit a record using ``click.secho``.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline in
        ANSI colours depending on the log level.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.format(record)
            color = LEVEL_TO_COLOR[record.levelno]
            click.secho(msg, color=True, fg=color)
        except RecursionError:  # See issue 36272 in CPython
            raise
        except Exception:  # noqa: BLE001
            self.handleError(record)


def configure_logging(
    console_log_level: int = logging.WARNING,
    log_file: str | Path | None = None,
    file_log_level: int = logging.DEBUG,
) -> None:
    """Configure logging and printing for command-line functions.

    Args:
        console_log_level: The log level for messages printed to the console.
            Defaults to logging.WARNING.
        log_file: The file to which log messages will be sent. Defaults to
            None, in which case, no log messages are sent to a file.
        file_log_level: The log level for messages sent to the log file.
            Defaults to logging.DEBUG.
    """
    logger.setLevel(logging.DEBUG)
    log_format = (
        "%(asctime)s - %(name)s::%(funcName)s::%(lineno)s - "
        "%(levelname)s - %(message)s "
    )
    formatter = logging.Formatter(log_format)

    if log_file is not None:
        fh = handlers.RotatingFileHandler(
            log_file, encoding="utf-8", maxBytes=1e6, backupCount=5
        )
        fh.setLevel(level=file_log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = FancyConsoleHandler()
    stderr_formatter = logging.Formatter("%(message)s")
    ch.setFormatter(stderr_formatter)
    ch.setLevel(level=console_log_level)
    logger.addHandler(ch)
