from loguru import logger
import sys
import traceback
import json
from datetime import datetime

class JsonLogger:
    def __init__(self):
        logger.remove()
        logger.add(
            sys.stdout,
            format="{message}",
            serialize=True,
            level="DEBUG"
        )

    def log(self, level, message, **kwargs):
        if "exception" in kwargs:
            # Utilizzare direttamente l'oggetto eccezione in loguru
            exception_info = kwargs.pop("exception")
            logger.opt(exception=True).log(level, message)
        else:
            logger.log(level, message)

    def info(self, message):
        self.log("INFO", message)

    def debug(self, message):
        self.log("DEBUG", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message, **kwargs):
        self.log("ERROR", message, **kwargs)

    def critical(self, message):
        self.log("CRITICAL", message)

    def exception(self, message):
        # intercept traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb = "".join(tb)
        self.error(message, exception=tb)

# Uso della classe JsonLogger
if __name__ == "__main__":
    log = JsonLogger()
    log.info("Questo è un messaggio di log informativo.")
    try:
        raise ValueError("Questo è un errore di test")
    except Exception as e:
        log.error("Si è verificato un errore", exception=e)
