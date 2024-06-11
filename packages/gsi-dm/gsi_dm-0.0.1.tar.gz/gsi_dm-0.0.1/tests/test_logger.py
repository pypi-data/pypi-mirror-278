import pytest
from pathlib import Path
import logging

from gsi.logger import Logger
from gsi.constants import LOGGER_NAME

TEST_LOGFILE = "test.log"


@pytest.fixture(autouse=True)
def cleanup():
    """Fixture to execute asserts before and after a test is run."""
    # Before test
    yield
    # After test
    if Path(TEST_LOGFILE).exists():
        Path(TEST_LOGFILE).unlink()


def test_logger_init():
    """Test that the logger is initialized with the correct attributes."""
    logger = Logger()
    assert logger.logger.name == LOGGER_NAME
    assert logger.logger.level == 20
    assert isinstance(logger.formatter, logging.Formatter)


def test_logger_default_handler():
    """Test that the logger has a default stream handler."""
    logger = Logger()
    assert logger.logger.hasHandlers()
    assert len(logger.logger.handlers) > 0


def test_logger_file_handler():
    """Test that the file handler method adds a file handler to the logger."""
    logger = Logger()
    logger.add_file_handler(TEST_LOGFILE)
    assert Path(TEST_LOGFILE).exists()


def test_logger_file_handler_write():
    logger = Logger()
    logger.add_file_handler(TEST_LOGFILE)
    logger.log("This is a test info message.")
    with open(TEST_LOGFILE, "r") as f:
        assert "This is a test info message." in f.read()
    logger.log("This is a test error message.", level=logging.ERROR)
    with open(TEST_LOGFILE, "r") as f:
        assert "This is a test error message." in f.read()
    # Write a debug message. This should not be written to the log
    # file if the Logger level is set to the default loggin level (INFO).
    logger.log("This is a test debug message.", level=logging.DEBUG)
    with open(TEST_LOGFILE, "r") as f:
        assert "This is a test debug message." not in f.read()
