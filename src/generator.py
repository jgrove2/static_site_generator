from src.builder.html import build_site
from src.config.default import DEFAULT_CONTENT_DIR
from src.config.default import DEFAULT_OUTPUT_DIR
from src.config.default import DEFAULT_TEMPLATE_FILE
from src.logger.logger import setup_logging
import logging
from datetime import datetime

def generate_site():
    """Generate the static site with comprehensive logging."""
    content_dir = DEFAULT_CONTENT_DIR
    output_dir = DEFAULT_OUTPUT_DIR
    template_file = DEFAULT_TEMPLATE_FILE

    logger = setup_logging(log_level=logging.INFO)

    start_time = datetime.now()
    logger.info("Starting static site build")
    logger.info(f"Content directory: {content_dir}")
    logger.info(f"Output directory: {output_dir}")

    successful_conversions, error_count = build_site(logger, content_dir, output_dir, template_file)

    end_time = datetime.now()
    duration = end_time - start_time

    logger.info(f"Static site build completed in {duration}")

    logger.info("=" * 50)
    logger.info("BUILD SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Build duration: {duration}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Successful conversions: {successful_conversions}")
    logger.info(f"Errors encountered: {error_count}")
    logger.info("=" * 50)