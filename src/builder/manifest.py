"""
Manifest generation functionality for the static site generator.
"""

import json

def generate_manifest_json(site_name="Static Site", site_description="A static site generated with Python"):
    """Generate a web app manifest JSON file."""
    manifest = {
        "name": site_name,
        "short_name": site_name.split()[0] if site_name else "Site",
        "description": site_description,
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#00a2e7",
        "orientation": "portrait-primary",
        "scope": "/",
        "lang": "en",
        "icons": [
            {
                "src": "/android-chrome-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/android-chrome-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/apple-touch-icon.png",
                "sizes": "180x180",
                "type": "image/png"
            },
            {
                "src": "/favicon-32x32.png",
                "sizes": "32x32",
                "type": "image/png"
            },
            {
                "src": "/favicon-16x16.png",
                "sizes": "16x16",
                "type": "image/png"
            }
        ]
    }
    return json.dumps(manifest, indent=2) 