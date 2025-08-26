"""
Unit tests for the config default module.
"""

import unittest
from src.config.default import (
    DEFAULT_CONTENT_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TEMPLATE_FILE,
    DEFAULT_LOG_NAME,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_FILE
)


class TestDefaultConfig(unittest.TestCase):
    """Test cases for the default configuration constants."""

    def test_default_content_dir(self):
        """Test that DEFAULT_CONTENT_DIR is set correctly."""
        self.assertEqual(DEFAULT_CONTENT_DIR, "content")

    def test_default_output_dir(self):
        """Test that DEFAULT_OUTPUT_DIR is set correctly."""
        self.assertEqual(DEFAULT_OUTPUT_DIR, "dist")

    def test_default_template_file(self):
        """Test that DEFAULT_TEMPLATE_FILE is set correctly."""
        self.assertEqual(DEFAULT_TEMPLATE_FILE, "templates/base.html")

    def test_default_log_name(self):
        """Test that DEFAULT_LOG_NAME is set correctly."""
        self.assertEqual(DEFAULT_LOG_NAME, "static_site_generator")

    def test_default_log_level(self):
        """Test that DEFAULT_LOG_LEVEL is set correctly."""
        self.assertEqual(DEFAULT_LOG_LEVEL, "INFO")

    def test_default_log_file(self):
        """Test that DEFAULT_LOG_FILE is set to None by default."""
        self.assertIsNone(DEFAULT_LOG_FILE)


if __name__ == '__main__':
    unittest.main() 