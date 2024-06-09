from dataclasses import dataclass
from functools import wraps
from typing import Optional

import requests
from outpostkit.repository.lfs.logger import create_lfs_logger

_log = create_lfs_logger(__name__)


class LFSException(Exception):
    def __init__(
        self, code: int, message: str, doc_url: Optional[str] = None, *args: object
    ) -> None:
        self.message = message
        self.code = code
        self.doc_url = doc_url
        super().__init__(*args)


@dataclass
class ProxyLFSException:
    message: str
    code: int
    doc_url: Optional[str] = None


def handle_request_errors(prefix: str):
    def handle_request_error(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except requests.exceptions.HTTPError as errh:
                _log.error(errh, exc_info=True)
                return ProxyLFSException(
                    code=errh.response.status_code,
                    message=f"{prefix} HTTPError: {errh.response.text}",
                )
            except requests.exceptions.ConnectionError as errc:
                _log.error(errc, exc_info=True)
                return ProxyLFSException(
                    code=500, message=f"{prefix} Connection Error: {errc.strerror}"
                )
            except requests.exceptions.Timeout as errt:
                _log.error(errt, exc_info=True)
                return ProxyLFSException(
                    code=500, message=f"{prefix} Connection Timed Out: {errt.strerror}"
                )

        return wrapper

    return handle_request_error
