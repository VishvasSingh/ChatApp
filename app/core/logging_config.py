from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # don’t disable Flask/other libs
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": LOG_DIR / "app.log",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
}
