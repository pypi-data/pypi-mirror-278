#!/usr/bin/env python

import logging
from pathlib import Path

from gsi.constants import LOGGER_NAME


class Logger:
    def __init__(
        self,
        name: str = LOGGER_NAME,
        level: int = logging.INFO,
        formatter: logging.Formatter = None,
    ):
        """Default logging configuration.

        Args:
            name (str, optional): Name of the logger. Defaults to None.
            level (int, optional): Logging level. Defaults to logging.INFO. Valid levels are:
            - logging.DEBUG (10)
            - logging.INFO (20) [default]
            - logging.WARNING (30)
            - logging.ERROR (40)
            - logging.CRITICAL (50)

        Examples:

            ```python
            logger = Logger(name=__name__)
            logger.log("This is an info message.")
            logger.add_file_handler("log.txt")
            logger.log("This is also an info message, but it's written to a file and the console.")
            ```
        """
        super().__init__()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if not formatter:
            self.formatter = logging.Formatter(
                (
                    "%(asctime)s %(name)s %(levelname)s: %(message)s"
                    if level < logging.INFO
                    else "%(message)s"
                ),
                datefmt="[%Y-%m-%d %H:%M:%S]",
            )
        else:
            self.formatter = formatter
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)

    def __repr__(self):
        return f"Logger(name={self.logger.name}, level={self.logger.level})"

    def add_file_handler(self, log_file: str | Path):
        """Add a file handler to the logger.

        Args:
            log_file (str | Path): Path to the log file.
        """
        if isinstance(log_file, str):
            try:
                log_file = Path(log_file)
            except Exception as e:
                self.log(
                    f"Error converting {log_file} to Path: {e}", level=logging.ERROR
                )
                return
        if not log_file.parent.exists():
            log_file.parent.mkdir(parents=True)
        if log_file.exists():
            log_file.unlink()
        file_handler = logging.FileHandler(filename=log_file)
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(self.logger.level)
        self.logger.addHandler(file_handler)

    def log(self, msg: str, level: int = logging.INFO):
        """Log a message.

        Args:
            msg (str): Message to log.
            level (int, optional): Logging level. Defaults to logging.INFO.
        """
        self.logger.log(level, msg)
