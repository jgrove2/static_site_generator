# Static Site Generator

A simple Python-based static site generator that converts markdown files to HTML with YAML frontmatter support.

## Features

- Converts markdown files to HTML
- Supports YAML frontmatter for metadata
- Generates static HTML files based on markdown file names and frontmatter
- Ready for Docker deployment on Dokploy

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python static_site_generator.py --input-dir ./markdown --output-dir ./html
```

### Command Line Options

- `--input-dir`: Directory containing markdown files (default: `./markdown`)
- `--output-dir`: Directory to output generated HTML files (default: `./html`)
- `--template`: Path to custom HTML template (optional)

### Markdown File Structure

Your markdown files should include YAML frontmatter at the top:

```markdown
---
title: My Page Title
date: 2024-01-01
tags: [blog, tutorial]
layout: default
---

# Your Markdown Content

This is the main content of your page.
```

## File Naming Convention

- Files are placed based on their filename and frontmatter data
- Example: `blog-post.md` with `layout: blog` will be placed at `blog/blog-post.html`

## Docker Deployment

This project is designed to work with Dokploy. The generated HTML files can be served by any static file server.

## Project Structure

```
static_site_generator/
├── static_site_generator.py    # Main script
├── templates/                  # HTML templates
│   └── default.html
├── markdown/                   # Input markdown files
├── html/                       # Generated HTML files
├── requirements.txt
└── README.md
```
