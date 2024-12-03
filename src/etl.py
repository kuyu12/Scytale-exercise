import logging
import os

from extract import extract
from load import load
from utils.const import TRANSFORM_OUTPUT_FILE_PATH, ORGANIZATION_VAR_NAME
from utils.logger_utils import setupLogger
from transform import transform

logger = logging.getLogger(__name__)


def main():
    setupLogger()

    try:
        organization = os.environ[ORGANIZATION_VAR_NAME]
        logger.info(f"etl start with: {organization}")
    except KeyError:
        logger.error(f"Environment variable '{ORGANIZATION_VAR_NAME}' not set.")
        return

    # Extract
    logger.info("Starting data extraction")
    extract(organization)
    logger.info("Data extraction completed")

    # Transform
    logger.info("Starting data transformation")
    result = transform(organization)
    logger.info("data transformation completed")

    # Load
    logger.info("Starting data loading")
    load(organization, result)
    logger.info("data loading completed")


if __name__ == "__main__":
    main()
