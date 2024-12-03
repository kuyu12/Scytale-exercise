import logging
from utils.const import LOG_CONFIG_FILE
import yaml
import os
import logging.config

def setupLogger():
    if os.path.exists(LOG_CONFIG_FILE):
        with open(LOG_CONFIG_FILE, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

