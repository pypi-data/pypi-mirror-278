import logging
import sys

import uvicorn.config as uvicorn_config
import uvicorn.logging


def logging_config(log_level: str = "info"):
    """Return new `uvicorn.config.LOGGING_CONFIG` dict."""
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            },
            "webhook": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s[%(name)s]:\t%(message)s",
                "use_colors": None,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "webhook": {
                "formatter": "webhook",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
            "webhook": {"handlers": ["webhook"], "level": log_level.upper(), "propagate": False},
        },
    }

    return LOGGING_CONFIG

logger: logging.Logger = logging.getLogger("webhook")


_formatter = logging.Formatter("%(levelname)s[%(name)s]:\t%(message)s")
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)
_handler.setStream(sys.stderr)
_handler.setLevel(logging.INFO)
logger.addHandler(_handler)
