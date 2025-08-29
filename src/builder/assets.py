"""
Asset management functionality for the static site generator.
"""

import shutil
from pathlib import Path

def copy_static_assets(template_dir, output_dir, logger):
    """Copy static assets (CSS, favicons, etc.) to output directory."""
    # Copy CSS file
    css_source = template_dir / "style.css"
    css_dest = Path(output_dir) / "style.css"
    if css_source.exists():
        shutil.copy2(css_source, css_dest)
        logger.info(f"✅ Copied CSS file to: {css_dest}")
    else:
        logger.warning(f"CSS file not found: {css_source}")
    
    # Copy favicon files
    favicon_files = [
        "favicon.ico",
        "favicon-16x16.png", 
        "favicon-32x32.png",
        "apple-touch-icon.png",
        "android-chrome-192x192.png",
        "android-chrome-512x512.png"
    ]
    
    for favicon_file in favicon_files:
        favicon_source = template_dir / favicon_file
        favicon_dest = Path(output_dir) / favicon_file
        if favicon_source.exists():
            shutil.copy2(favicon_source, favicon_dest)
            logger.info(f"✅ Copied {favicon_file} to: {favicon_dest}")
        else:
            logger.warning(f"Favicon file not found: {favicon_source}") 