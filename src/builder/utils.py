"""
Utility functions for the static site generator.
"""

import re
from html import unescape

def extract_description(frontmatter, html_content, max_length=160):
    """Extract or generate a meta description for a page.
    
    Args:
        frontmatter: Dictionary containing page metadata
        html_content: The HTML content of the page
        max_length: Maximum length of description (default 160 for SEO)
    
    Returns:
        str: Meta description for the page
    """
    # First, try to get description from frontmatter
    if 'description' in frontmatter:
        description = frontmatter['description']
        if description and len(description) <= max_length:
            return description
    
    # If no description in frontmatter, generate one from content
    # Remove HTML tags and get plain text
    text_content = re.sub(r'<[^>]+>', '', html_content)
    text_content = unescape(text_content)  # Convert HTML entities
    
    # Clean up whitespace
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    
    # Take first sentence or first max_length characters
    if len(text_content) <= max_length:
        return text_content
    
    # Find the first sentence boundary
    sentence_match = re.search(r'^[^.!?]*[.!?]', text_content)
    if sentence_match:
        sentence = sentence_match.group(0)
        if len(sentence) <= max_length:
            return sentence
    
    # If no good sentence boundary, truncate at word boundary
    truncated = text_content[:max_length-3]
    last_space = truncated.rfind(' ')
    if last_space > max_length * 0.7:  # Only use word boundary if it's not too early
        truncated = truncated[:last_space]
    
    return truncated + '...' 