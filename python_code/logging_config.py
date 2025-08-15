# library
import logging.config


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
