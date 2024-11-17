# utils/logger.py

import logging
from config import LOG_DIR

def setup_logging(log_level):
    log_file = f"{LOG_DIR}/app.log"
    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, log_level),
        format='%(asctime)s - %(levelname)s - %(message)s',
    )