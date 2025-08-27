"""
Main site building functionality for the static site generator.
"""

import os
from pathlib import Path
from datetime import datetime

from src.templates.loader import load_template
from src.parser.markdown import parse_markdown
from src.config.markdown import MARKDOWN_PATTERN

def generate_navigation(pages_info, logger):
    """Generate navigation structure from pages information."""
    # Group pages by their directory structure
    pages_by_dir = {}
    
    for page in pages_info:
        url_path = page['url_path']
        title = page['title']
        
        # Split the URL path into parts
        parts = url_path.strip('/').split('/')
        
        # Create directory key
        if len(parts) == 1:
            # Root level page
            dir_key = "root"
        else:
            # Nested page
            dir_key = "/".join(parts[:-1])
        
        if dir_key not in pages_by_dir:
            pages_by_dir[dir_key] = []
        
        pages_by_dir[dir_key].append({
            'title': title,
            'url': url_path,
            'filename': parts[-1]
        })
    
    logger.debug(f"Pages by directory: {pages_by_dir}")
    return pages_by_dir

def format_display_name(name):
    """Convert underscores to spaces and capitalize each word."""
    return name.replace('_', ' ').title()

def generate_navigation_html(navigation, current_url):
    """Generate HTML for the navigation."""
    html = '<nav class="site-navigation">\n'
    
    # Add root-level links directly
    if "root" in navigation:
        for page in navigation["root"]:
            is_current = page['url'] == current_url
            current_class = ' class="current"' if is_current else ''
            display_title = format_display_name(page["title"])
            html += f'  <a href="{page["url"]}"{current_class}>{display_title}</a>\n'
    
    # Add dropdowns for nested folders
    sorted_dirs = sorted([k for k in navigation.keys() if k != "root"])
    for dir_key in sorted_dirs:
        pages = navigation[dir_key]
        dir_name = dir_key.split('/')[-1]  # Get the last part of the directory path
        display_dir_name = format_display_name(dir_name)
        html += f'  <div class="nav-folder">\n'
        html += f'    <span class="nav-folder-title">{display_dir_name}▼</span>\n'
        html += f'    <div class="nav-folder-dropdown">\n'
        
        for page in pages:
            is_current = page['url'] == current_url
            current_class = ' class="current"' if is_current else ''
            display_title = format_display_name(page["title"])
            html += f'      <a href="{page["url"]}"{current_class}>{display_title}</a>\n'
        
        html += f'    </div>\n'
        html += f'  </div>\n'
    
    html += '</nav>\n'
    
    return html



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
        
        # First pass: collect all page information
        pages_info = []
        error_count = 0
        for md_file in markdown_files:
            try:
                # Parse markdown
                fm, html_body = parse_markdown(md_file, logger)
                
                # Extract metadata
                title = fm.get("title", md_file.stem)
                
                # Determine output path - preserve directory structure
                rel_path = md_file.relative_to(content_dir)
                slug = fm.get("slug")
                
                if slug:
                    # If slug is specified in frontmatter, use it
                    if slug.endswith("/"):
                        output_path = Path(output_dir) / slug / "index.html"
                        url_path = f"/{slug}"
                    elif slug == "index":
                        # Special case: slug "index" should create root index.html
                        output_path = Path(output_dir) / "index.html"
                        url_path = "/"
                    else:
                        # Preserve directory structure when using slug
                        dir_path = rel_path.parent
                        if str(dir_path) != ".":
                            # File is in a subdirectory, preserve the directory structure
                            output_path = Path(output_dir) / dir_path / f"{slug}.html"
                            url_path = f"/{dir_path}/{slug}.html"
                        else:
                            # File is in root directory
                            output_path = Path(output_dir) / f"{slug}.html"
                            url_path = f"/{slug}.html"
                else:
                    # Generate HTML files directly with same name as markdown files
                    if rel_path.stem == "index":
                        # For index.md files, create index.html in the same directory
                        output_path = Path(output_dir) / rel_path.parent / "index.html"
                        url_path = f"/{rel_path.parent}" if str(rel_path.parent) != "." else "/"
                    else:
                        # For other files, create .html file directly
                        output_path = Path(output_dir) / rel_path.parent / f"{rel_path.stem}.html"
                        url_path = f"/{rel_path.parent}/{rel_path.stem}.html" if str(rel_path.parent) != "." else f"/{rel_path.stem}.html"
                
                pages_info.append({
                    'title': title,
                    'url_path': url_path,
                    'output_path': output_path,
                    'html_body': html_body,
                    'frontmatter': fm
                })
                
            except Exception as e:
                logger.error(f"❌ Failed to process {md_file}: {e}")
                error_count += 1
                continue
        
        # Generate navigation structure
        navigation = generate_navigation(pages_info, logger)
        
        # Second pass: build all pages with navigation
        processed_count = 0
        for page_info in pages_info:
            logger.info(f"Processing: {page_info['output_path']}")
            
            try:
                # Extract page information
                title = page_info['title']
                html_body = page_info['html_body']
                output_path = page_info['output_path']
                
                logger.debug(f"Page title: {title}")
                logger.debug(f"Output path: {output_path}")
                
                # Ensure parent directories exist
                output_path.parent.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Created directory structure: {output_path.parent}")
                
                # Generate navigation HTML
                navigation_html = generate_navigation_html(navigation, page_info['url_path'])
                
                # Generate HTML with navigation
                html = template.replace("{title}", title).replace("{content}", html_body).replace("{navigation}", navigation_html)
                
                # Write file
                output_path.write_text(html, encoding="utf-8")
                logger.info(f"✅ Built: {output_path}")
                processed_count += 1
                
            except Exception as e:
                logger.error(f"❌ Failed to process {page_info['output_path']}: {e}")
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