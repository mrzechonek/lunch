import logging
import secrets
from contextlib import contextmanager
from contextvars import ContextVar, Token

REQUEST_ID = ContextVar("REQUEST_ID", default=None)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        request_id = REQUEST_ID.get()
        if request_id:
            record.name += f".{request_id}"
        return True


@contextmanager
def request_id_context():
    request_id = secrets.token_urlsafe(8)

    token = REQUEST_ID.set(request_id)
    yield request_id
    REQUEST_ID.reset(token)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"request_id": {"()": RequestIdFilter}},
    "formatters": {
        "text": {
            "()": logging.Formatter,
            "format": "%(asctime)s.%(msecs)03d %(name)-30s %(levelname)-6s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "()": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "text",
            "filters": ["request_id"],
        }
    },
    "root": {"level": logging.DEBUG, "handlers": ["console"]},
}
