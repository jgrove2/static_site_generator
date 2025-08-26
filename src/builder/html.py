"""
Main site building functionality for the static site generator.
"""

import os
from pathlib import Path
from datetime import datetime

from src.templates.loader import load_template
from src.parser.markdown import parse_markdown
from src.config.markdown import MARKDOWN_PATTERN

def build_site(logger, content_dir, output_dir, template_file):
    """Build the static site with comprehensive logging.
    
    Returns:
        tuple: (successful_conversions, error_count) - Number of successful conversions and errors
    """
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Created/verified output directory: {output_dir}")
        
        # Load template
        template = load_template(template_file, logger)
        
        # Copy CSS file to output directory
        css_source = Path(template_file).parent / "style.css"
        css_dest = Path(output_dir) / "style.css"
        if css_source.exists():
            import shutil
            shutil.copy2(css_source, css_dest)
            logger.info(f"✅ Copied CSS file to: {css_dest}")
        else:
            logger.warning(f"CSS file not found: {css_source}")
        
        # Find all markdown files
        content_path = Path(content_dir)
        if not content_path.exists():
            logger.error(f"Content directory does not exist: {content_dir}")
            return (0, 1)  # 0 successful, 1 error (content dir not found)
        
        markdown_files = list(content_path.rglob(MARKDOWN_PATTERN))
        logger.info(f"Found {len(markdown_files)} markdown files to process")
        
        if not markdown_files:
            logger.warning("No markdown files found in content directory")
            return (0, 0)  # 0 successful, 0 errors (no files to process)
        
        processed_count = 0
        error_count = 0
        
        for md_file in markdown_files:
            logger.info(f"Processing: {md_file}")
            
            try:
                # Parse markdown
                fm, html_body = parse_markdown(md_file, logger)
                
                # Extract metadata
                title = fm.get("title", md_file.stem)
                logger.debug(f"Page title: {title}")
                
                # Determine output path
                rel_path = md_file.relative_to(content_dir).with_suffix("")
                slug = fm.get("slug", str(rel_path))
                logger.debug(f"Slug: {slug}")
                
                # Create output path
                if slug.endswith("/"):
                    output_path = Path(output_dir) / slug / "index.html"
                else:
                    output_path = Path(output_dir) / slug / "index.html"
                
                logger.debug(f"Output path: {output_path}")
                
                # Ensure parent directories exist
                output_path.parent.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Created directory structure: {output_path.parent}")
                
                # Generate HTML
                html = template.replace("{title}", title).replace("{content}", html_body)
                
                # Write file
                output_path.write_text(html, encoding="utf-8")
                logger.info(f"✅ Built: {output_path}")
                processed_count += 1
                
            except Exception as e:
                logger.error(f"❌ Failed to process {md_file}: {e}")
                error_count += 1
                continue
        
        # Log final summary
        if error_count > 0:
            logger.warning(f"Build completed with {error_count} errors")
        else:
            logger.info("Build completed successfully!")
        
        logger.info(f"Final result: {processed_count} successful conversions, {error_count} errors")
        return (processed_count, error_count)
            
    except Exception as e:
        logger.error(f"Build failed: {e}")
        return (0, 1)  # 0 successful, 1 error (build failed) 