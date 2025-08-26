"""
Markdown parsing functionality for the static site generator.
"""

import yaml
import markdown
from pathlib import Path
from src.config.markdown import MARKDOWN_EXTENSIONS

def parse_markdown(file_path, logger):
    """Parse markdown file with YAML frontmatter and logging."""
    logger.debug(f"Parsing markdown file: {file_path}")
    
    try:
        text = Path(file_path).read_text(encoding="utf-8")
        logger.debug(f"Read {len(text)} characters from {file_path}")
        
        # Extract YAML frontmatter if present
        if text.startswith("---"):
            logger.debug("YAML frontmatter detected")
            parts = text.split("---", 2)
            if len(parts) >= 3:
                _, fm, body = parts
                try:
                    frontmatter = yaml.safe_load(fm)
                    logger.debug(f"Parsed frontmatter: {frontmatter}")
                except yaml.YAMLError as e:
                    logger.warning(f"Failed to parse YAML frontmatter: {e}")
                    frontmatter = {}
            else:
                logger.warning("Malformed YAML frontmatter, treating as regular markdown")
                frontmatter, body = {}, text
        else:
            logger.debug("No YAML frontmatter found")
            frontmatter, body = {}, text
        
        # Convert markdown to HTML
        html_body = markdown.markdown(body, extensions=MARKDOWN_EXTENSIONS)
        logger.debug(f"Converted markdown to HTML ({len(html_body)} characters)")
        
        return frontmatter, html_body
        
    except Exception as e:
        logger.error(f"Failed to parse markdown file {file_path}: {e}")
        raise 