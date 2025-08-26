---
title: About This Site
date: 2024-01-15
tags: [about, info]
slug: about
---

# About This Site

This static site is built using a Python-based static site generator with comprehensive logging.

## How It Works

The build process includes detailed logging at every step:

1. **File Discovery**: Logs all markdown files found
2. **Template Loading**: Logs template loading and validation
3. **Markdown Parsing**: Logs frontmatter parsing and markdown conversion
4. **File Generation**: Logs each HTML file created
5. **Build Summary**: Provides a complete summary of the build process

## Logging Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about the build process
- **WARNING**: Non-critical issues
- **ERROR**: Critical errors that prevent successful builds

## Example Log Output

```
INFO: Starting static site build
INFO: Content directory: content
INFO: Output directory: dist
INFO: Loading template from: templates/base.html
INFO: Found 2 markdown files to process
INFO: Processing: content/index.md
INFO: ✅ Built: dist/index/index.html
INFO: Processing: content/about.md
INFO: ✅ Built: dist/about/index.html
INFO: ==================================================
INFO: BUILD SUMMARY
INFO: ==================================================
INFO: Total files processed: 2
INFO: Errors encountered: 0
INFO: Build duration: 0:00:00.123456
INFO: Output directory: dist
INFO: ==================================================
INFO: Build completed successfully!
```

## Configuration

You can control logging behavior with command line arguments:

- `--log-level DEBUG|INFO|WARNING|ERROR`
- `--log-file path/to/logfile.log`
- `--verbose` (shorthand for DEBUG level)
