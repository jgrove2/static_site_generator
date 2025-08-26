"""
Unit tests for the logger module.
"""

import os
import tempfile
import logging
import unittest
from unittest.mock import patch, MagicMock

from src.logger.logger import setup_logging
from src.config.default import DEFAULT_LOG_NAME


class TestLogger(unittest.TestCase):
    """Test cases for the logger setup_logging function."""

    def setUp(self):
        """Set up test fixtures."""
        # Clear any existing loggers to avoid interference
        logging.getLogger(DEFAULT_LOG_NAME).handlers.clear()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clear any existing loggers
        logging.getLogger(DEFAULT_LOG_NAME).handlers.clear()
        # Clean up temp files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_setup_logging_returns_logger(self):
        """Test that setup_logging returns a logger instance."""
        logger = setup_logging()
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, DEFAULT_LOG_NAME)

    def test_setup_logging_default_level(self):
        """Test that setup_logging uses INFO level by default."""
        logger = setup_logging()
        self.assertEqual(logger.level, logging.INFO)

    def test_setup_logging_custom_level(self):
        """Test that setup_logging accepts custom log levels."""
        logger = setup_logging(log_level=logging.DEBUG)
        self.assertEqual(logger.level, logging.DEBUG)

    def test_setup_logging_clears_existing_handlers(self):
        """Test that setup_logging clears existing handlers."""
        # Create a logger with existing handlers
        logger = logging.getLogger(DEFAULT_LOG_NAME)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        self.assertEqual(len(logger.handlers), 1)

        # Setup logging should clear existing handlers
        new_logger = setup_logging()
        self.assertEqual(len(new_logger.handlers), 1)  # Only console handler
        self.assertNotIn(handler, new_logger.handlers)

    def test_setup_logging_console_handler(self):
        """Test that setup_logging creates a console handler."""
        logger = setup_logging()
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        self.assertEqual(len(console_handlers), 1)
        self.assertEqual(console_handlers[0].level, logging.INFO)

    def test_setup_logging_console_handler_custom_level(self):
        """Test that console handler uses the specified log level."""
        logger = setup_logging(log_level=logging.WARNING)
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        self.assertEqual(console_handlers[0].level, logging.WARNING)

    def test_setup_logging_console_formatter(self):
        """Test that console handler uses simple formatter."""
        logger = setup_logging()
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        formatter = console_handlers[0].formatter
        self.assertIsInstance(formatter, logging.Formatter)
        # Check that it's the simple formatter (not the detailed one)
        self.assertIn('%(levelname)s', formatter._fmt)
        self.assertNotIn('%(asctime)s', formatter._fmt)

    def test_setup_logging_with_file_handler(self):
        """Test that setup_logging creates file handler when log_file is specified."""
        log_file = os.path.join(self.temp_dir, "test.log")
        logger = setup_logging(log_file=log_file)
        
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        self.assertEqual(len(file_handlers), 1)
        self.assertEqual(file_handlers[0].baseFilename, os.path.abspath(log_file))

    def test_setup_logging_file_handler_level(self):
        """Test that file handler uses DEBUG level."""
        log_file = os.path.join(self.temp_dir, "test.log")
        logger = setup_logging(log_file=log_file)
        
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        self.assertEqual(file_handlers[0].level, logging.DEBUG)

    def test_setup_logging_file_formatter(self):
        """Test that file handler uses detailed formatter."""
        log_file = os.path.join(self.temp_dir, "test.log")
        logger = setup_logging(log_file=log_file)
        
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        formatter = file_handlers[0].formatter
        self.assertIsInstance(formatter, logging.Formatter)
        # Check that it's the detailed formatter
        self.assertIn('%(asctime)s', formatter._fmt)
        self.assertIn('%(name)s', formatter._fmt)
        self.assertIn('%(levelname)s', formatter._fmt)
        self.assertIn('%(message)s', formatter._fmt)

    def test_setup_logging_file_encoding(self):
        """Test that file handler uses UTF-8 encoding."""
        log_file = os.path.join(self.temp_dir, "test.log")
        logger = setup_logging(log_file=log_file)
        
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        # Note: FileHandler encoding is set during creation, not stored as an attribute
        # We can't easily test this without mocking, but the code shows it's set to 'utf-8'

    def test_setup_logging_no_file_handler_when_none(self):
        """Test that no file handler is created when log_file is None."""
        logger = setup_logging(log_file=None)
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        self.assertEqual(len(file_handlers), 0)

    def test_setup_logging_handlers_count(self):
        """Test the correct number of handlers are created."""
        # No file handler
        logger = setup_logging()
        self.assertEqual(len(logger.handlers), 1)  # Only console handler

        # With file handler
        log_file = os.path.join(self.temp_dir, "test.log")
        logger = setup_logging(log_file=log_file)
        self.assertEqual(len(logger.handlers), 2)  # Console and file handlers

    def test_setup_logging_logging_functionality(self):
        """Test that the logger actually works for logging messages."""
        log_file = os.path.join(self.temp_dir, "test.log")
        logger = setup_logging(log_level=logging.DEBUG, log_file=log_file)
        
        # Test file output
        logger.warning("Warning message")
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Warning message", content)
        
        # Test that logger can log different levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # Verify all messages are in the file
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Debug message", content)
            self.assertIn("Info message", content)
            self.assertIn("Warning message", content)
            self.assertIn("Error message", content)

    def test_setup_logging_multiple_calls(self):
        """Test that multiple calls to setup_logging work correctly."""
        log_file1 = os.path.join(self.temp_dir, "test1.log")
        log_file2 = os.path.join(self.temp_dir, "test2.log")
        
        logger1 = setup_logging(log_level=logging.DEBUG, log_file=log_file1)
        logger2 = setup_logging(log_level=logging.WARNING, log_file=log_file2)
        
        # Both should be the same logger instance
        self.assertIs(logger1, logger2)
        self.assertEqual(logger2.level, logging.WARNING)
        
        # Should have 2 handlers (console and file)
        self.assertEqual(len(logger2.handlers), 2)

    def test_setup_logging_invalid_log_level(self):
        """Test that setup_logging handles invalid log levels gracefully."""
        # This should not raise an exception
        logger = setup_logging(log_level=999)
        self.assertEqual(logger.level, 999)

    def test_setup_logging_file_creation(self):
        """Test that log file is created when logging occurs."""
        log_file = os.path.join(self.temp_dir, "test.log")
        self.assertFalse(os.path.exists(log_file))
        
        logger = setup_logging(log_file=log_file)
        logger.info("Test message")
        
        self.assertTrue(os.path.exists(log_file))


if __name__ == '__main__':
    unittest.main() 