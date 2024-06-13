# src/my_package/logging_config.py
import logging

logger = logging.getLogger(__name__)

def configure_logging(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    logging.basicConfig(level=level, format=format)
