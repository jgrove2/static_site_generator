"""
Template loading functionality for the static site generator.
"""

from pathlib import Path


def load_template(template_file, logger):
    """Load the HTML template with logging."""
    logger.info(f"Loading template from: {template_file}")
    
    try:
        template_path = Path(template_file)
        if not template_path.exists():
            logger.error(f"Template file not found: {template_file}")
            raise FileNotFoundError(f"Template file not found: {template_file}")
        
        template_content = template_path.read_text(encoding="utf-8")
        logger.debug(f"Successfully loaded template ({len(template_content)} characters)")
        return template_content
        
    except Exception as e:
        logger.error(f"Failed to load template: {e}")
        raise 