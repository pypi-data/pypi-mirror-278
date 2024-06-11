import os
from datadashr.utilities.logger import LogManager
from loguru import logger


PATH = os.path.dirname(os.path.realpath(__file__))
CACHE_DIR = os.path.join(PATH, "data", "cache_dir")
VECTOR_DIR = os.path.join(PATH, "data", "vectors")
CHART_DIR = os.path.join(PATH, "data", "charts", "datadashr.png")
LOG_DIR = os.path.join(PATH, "data", "logs", "datadashr_log.duckdb")

log_manager = LogManager(LOG_DIR, verbose=True)


