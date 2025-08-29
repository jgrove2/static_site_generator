"""
Navigation functionality for the static site generator.
"""

def generate_navigation(pages_info, logger):
    """Generate navigation structure from pages information."""
    # Group pages by their directory structure
    base_pages = []
    
    for page in pages_info:
        url_path = page['url_path']
        title = page['title']
        
        # Split the URL path into parts
        parts = url_path.strip('/').split('/')
        
        # Check if this is a base-level page (no directory structure)
        if len(parts) == 1:
            # Base level page - add to base_pages list
            base_pages.append({
                'title': title,
                'url': url_path,
                'filename': parts[-1] if parts[-1] else 'index'
            })
    
    return base_pages

def format_display_name(name):
    """Convert underscores to spaces and capitalize each word."""
    return name.replace('_', ' ').title()

def generate_navigation_html(base_pages, current_url):
    """Generate HTML for the navigation."""
    base_pages.sort(key=lambda x: x['title'])
    html = '<nav class="site-navigation">\n'

    html += '<div class="nav-logo"><a href="/">Jgrove</a></div>\n'

    html += '<div class="nav-links">'
    
    # Add direct links for base pages first
    if base_pages:
        for page in base_pages:
            is_current = page['url'] == current_url
            current_class = ' class="current"' if is_current else ''
            display_title = format_display_name(page["title"])
            html += f'  <a href="{page["url"]}"{current_class}>{display_title}</a>\n'
    
        html += f'  <div class="nav-folder">\n'
        html += f'    <span class="nav-folder-title"></span>\n'
        html += f'    <div class="nav-folder-dropdown">\n'
        for page in base_pages:
            is_current = page['url'] == current_url
            current_class = ' class="current"' if is_current else ''
            display_title = format_display_name(page["title"])
            html += f'      <a href="{page["url"]}"{current_class}>{display_title}</a>\n'
            
        html += f'    </div>\n'
        html += f'  </div>\n'
    
    html += '</div>\n'
    html += '</nav>\n'
    
    return html 