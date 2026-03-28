import logging
import logging.config
import yaml
import os

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    with open("config/logging.yaml", "r") as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)
    return logging.getLogger("RAG")