"""Implementation of the HTTP backend"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests
from codetiming import Timer

from ..checksums import Checksum
from ..logger import APP_LOGGER_NAME, get_logger
from ._base import XrdsumBackend

log = get_logger(APP_LOGGER_NAME)


@dataclass
class HttpSettings:
    """Settings for the CephFS backend."""

    base_path: str = "/storage/hdfs/checksum"
    server: str = "http://localhost:4935"
    read_size: int = 128


class HttpBackend(XrdsumBackend):
    """Queries checksums over HTTP.
    This assumes the HTTP services has reasonable defaults"""

    def __init__(
        self, file_path: str, read_size: int, **kwargs: dict[str, Any]
    ) -> None:
        """CephFS backend requires at least the file_path and read_size"""
        self.file_path = file_path
        self.settings = HttpSettings(
            read_size=read_size,
            **kwargs,  # type: ignore[arg-type]
        )

    def get_checksum(self, checksum: Checksum) -> Checksum:
        url = f"{self.settings.server}{self.settings.base_path}/{checksum.name}"
        params = {"path": self.file_path}
        with Timer(
            text=f"HTTP checksum retrieval took {{:.3f}}s for {self.file_path}",
            logger=log.timing,
        ):
            response = requests.get(url, params=params, timeout=60 * 5)
        response.raise_for_status()  # This will raise an exception for HTTP errors

        # Assuming the response is a plain text with the checksum
        checksum.value = response.text.strip()
        return checksum

    def store_checksum(self, checksum: Checksum, force: bool = False) -> None:
        """For HTTP, let's keep it simple and assume storage is done on retrieval"""
        log.trace(
            "Calling %s.store_checksum(%s, %s)",
            self.__class__.__name__,
            checksum.name,
            force,
        )
        log.debug("No store_checksum available for %s", self.__class__.__name__)
