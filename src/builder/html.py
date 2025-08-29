"""
Main site building functionality for the static site generator.
"""

import os
from pathlib import Path
from datetime import datetime

from src.templates.loader import load_template
from src.parser.markdown import parse_markdown
from src.config.markdown import MARKDOWN_PATTERN
from src.builder.navigation import generate_navigation, generate_navigation_html
from src.builder.manifest import generate_manifest_json
from src.builder.assets import copy_static_assets
from src.builder.utils import extract_description





def build_site(logger, content_dir, output_dir, template_file):
    """Build the static site with comprehensive logging.
    
    Returns:
        tuple: (successful_conversions, error_count) - Number of successful conversions and errors
    """
    try:
        # Clear output directory
        import shutil
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            logger.info(f"Cleared existing output directory: {output_dir}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Created/verified output directory: {output_dir}")
        
        # Load template
        template = load_template(template_file, logger)
        
        # Copy static assets to output directory
        template_dir = Path(template_file).parent
        copy_static_assets(template_dir, output_dir, logger)
        
        # Generate and write manifest.json
        manifest_content = generate_manifest_json("Jgrove", "Personal website and projects")
        manifest_path = Path(output_dir) / "manifest.json"
        manifest_path.write_text(manifest_content, encoding="utf-8")
        logger.info(f"✅ Generated manifest.json: {manifest_path}")
        
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
                    slug = slug.lower().replace(" ", "_")
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
                        print(dir_path)
                        if str(dir_path) != ".":
                            # File is in a subdirectory, preserve the directory structure
                            output_path = Path(output_dir) / dir_path / slug / "index.html"
                            url_path = f"/{dir_path}/{slug}"
                        else:
                            # File is in root directory
                            output_path = Path(output_dir) / slug / "index.html"
                            url_path = f"/{slug}"
                else:
                    # Generate HTML files directly with same name as markdown files
                    print(rel_path.stem)
                    # For now, skip files without slug - you can add logic here later
                    continue
                
                # Extract or generate description
                description = extract_description(fm, html_body)
                
                pages_info.append({
                    'title': title,
                    'url_path': url_path,
                    'output_path': output_path,
                    'html_body': html_body,
                    'frontmatter': fm,
                    'description': description
                })
                
            except Exception as e:
                logger.error(f"❌ Failed to process {md_file}: {e}")
                error_count += 1
                continue
        
        # Generate navigation structure
        for page in pages_info:
            print(page['url_path'])
            print(page['output_path'])
            print(page['frontmatter'])
            print("--------------------------------")
        base_pages = generate_navigation(pages_info, logger)
        
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
                
                # Generate navigation HTML for this specific page
                navigation_html = generate_navigation_html(base_pages, page_info['url_path'])
                
                # Generate HTML with navigation and description
                html = template.replace("{title}", title).replace("{content}", html_body).replace("{navigation}", navigation_html).replace("{description}", page_info['description'])
                
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