"""
Unit tests for the builder html module.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile


class TestHTMLBuilder(unittest.TestCase):
    """Test cases for the HTML builder module."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        # Clean up temp directory and all its contents
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_html_builder_import(self):
        """Test that the HTML builder module can be imported."""
        try:
            from src.builder.html import build_site
            self.assertTrue(True)  # Import successful
        except ImportError as e:
            self.fail(f"Failed to import build_site: {e}")

    def test_build_site_function_exists(self):
        """Test that the build_site function exists and is callable."""
        from src.builder.html import build_site
        self.assertTrue(callable(build_site))

    def test_build_site_returns_tuple(self):
        """Test that build_site returns a tuple of (successful_conversions, error_count)."""
        from src.builder.html import build_site
        from unittest.mock import MagicMock
        
        # Create a mock logger
        mock_logger = MagicMock()
        
        # Test with non-existent content directory
        result = build_site(mock_logger, "non_existent_dir", self.temp_dir, "templates/base.html")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        successful_conversions, error_count = result
        self.assertIsInstance(successful_conversions, int)
        self.assertIsInstance(error_count, int)

    def test_build_site_content_dir_not_found(self):
        """Test build_site when content directory doesn't exist."""
        from src.builder.html import build_site
        from unittest.mock import MagicMock
        
        mock_logger = MagicMock()
        result = build_site(mock_logger, "non_existent_dir", self.temp_dir, "templates/base.html")
        
        successful_conversions, error_count = result
        self.assertEqual(successful_conversions, 0)
        self.assertEqual(error_count, 1)
        mock_logger.error.assert_called()

    def test_build_site_no_markdown_files(self):
        """Test build_site when no markdown files are found."""
        from src.builder.html import build_site
        from unittest.mock import MagicMock, patch
        
        mock_logger = MagicMock()
        
        # Create an empty content directory
        content_dir = os.path.join(self.temp_dir, "empty_content")
        os.makedirs(content_dir, exist_ok=True)
        
        with patch('src.builder.html.load_template') as mock_load_template:
            mock_load_template.return_value = "<html><title>{title}</title><body>{content}</body></html>"
            
            result = build_site(mock_logger, content_dir, self.temp_dir, "templates/base.html")
            
            successful_conversions, error_count = result
            self.assertEqual(successful_conversions, 0)
            self.assertEqual(error_count, 0)
            mock_logger.warning.assert_called_with("No markdown files found in content directory")

    def test_build_site_successful_conversion(self):
        """Test build_site with successful markdown to HTML conversion."""
        from src.builder.html import build_site
        from unittest.mock import MagicMock, patch
        
        mock_logger = MagicMock()
        
        # Create content directory with a markdown file
        content_dir = os.path.join(self.temp_dir, "content")
        os.makedirs(content_dir, exist_ok=True)
        
        # Create a test markdown file
        md_file = os.path.join(content_dir, "test.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("---\ntitle: Test Page\n---\n\n# Hello World\n\nThis is a test.")
        
        with patch('src.builder.html.load_template') as mock_load_template:
            mock_load_template.return_value = "<html><title>{title}</title><body>{content}</body></html>"
            
            with patch('src.builder.html.parse_markdown') as mock_parse_markdown:
                mock_parse_markdown.return_value = ({"title": "Test Page"}, "<h1>Hello World</h1><p>This is a test.</p>")
                
                result = build_site(mock_logger, content_dir, self.temp_dir, "templates/base.html")
                
                successful_conversions, error_count = result
                self.assertEqual(successful_conversions, 1)
                self.assertEqual(error_count, 0)

    def test_build_site_with_errors(self):
        """Test build_site when some files fail to process."""
        from src.builder.html import build_site
        from unittest.mock import MagicMock, patch
        
        mock_logger = MagicMock()
        
        # Create content directory with markdown files
        content_dir = os.path.join(self.temp_dir, "content")
        os.makedirs(content_dir, exist_ok=True)
        
        # Create test markdown files
        md_file1 = os.path.join(content_dir, "test1.md")
        md_file2 = os.path.join(content_dir, "test2.md")
        
        with open(md_file1, 'w', encoding='utf-8') as f:
            f.write("---\ntitle: Test Page 1\n---\n\n# Hello World 1")
        
        with open(md_file2, 'w', encoding='utf-8') as f:
            f.write("---\ntitle: Test Page 2\n---\n\n# Hello World 2")
        
        with patch('src.builder.html.load_template') as mock_load_template:
            mock_load_template.return_value = "<html><title>{title}</title><body>{content}</body></html>"
            
            with patch('src.builder.html.parse_markdown') as mock_parse_markdown:
                # First file succeeds, second file fails
                mock_parse_markdown.side_effect = [
                    ({"title": "Test Page 1"}, "<h1>Hello World 1</h1>"),
                    Exception("Parse error")
                ]
                
                result = build_site(mock_logger, content_dir, self.temp_dir, "templates/base.html")
                
                successful_conversions, error_count = result
                self.assertEqual(successful_conversions, 1)
                self.assertEqual(error_count, 1)
                mock_logger.error.assert_called()


if __name__ == '__main__':
    unittest.main() 