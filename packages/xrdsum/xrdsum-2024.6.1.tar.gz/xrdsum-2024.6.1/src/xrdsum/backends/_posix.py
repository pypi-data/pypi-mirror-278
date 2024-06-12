"""Implementation of the HDFS backend."""

# we want non-top-level imports to avoid pulling HDFS dependency early
# pylint: disable=import-outside-toplevel
from __future__ import annotations

from collections.abc import Generator
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import xattr  # type: ignore[import-untyped]
from codetiming import Timer

from ..checksums import Checksum
from ..logger import APP_LOGGER_NAME, get_logger
from ._base import XrdsumBackend

log = get_logger(APP_LOGGER_NAME)

USER = "xrootd"
XATTR_TEMPLATE = "user.xrdsum.{}"


@dataclass
class POSIXSettings:
    """Settings for the POSIX backend."""

    user: str = USER
    read_size: int = 64 * 1024 * 1024


def read_file_in_chunks(
    file_path: str, chunk_size_in_bytes: int
) -> Generator[bytes, None, None]:
    """Reads POSIX file in chunks."""
    client = Path(file_path)
    file_status = client.stat()
    total_size = file_status.st_size
    read_bytes = 0
    log.debug(
        "Reading %s in chunks of %s bytes (out of %s)",
        file_path,
        chunk_size_in_bytes,
        total_size,
    )
    with closing(client.open("rb")) as file_handle:
        while True:
            file_handle.seek(read_bytes)
            chunk = file_handle.read(chunk_size_in_bytes)
            if chunk:
                read_bytes += len(chunk)
                yield chunk
            else:
                return


class POSIXBackend(XrdsumBackend):
    """Implementation of the POSIX backend."""

    settings: POSIXSettings

    def __init__(self, file_path: str, read_size: int, **kwargs: dict[str, Any]):
        """POSIX backend requires at least the file_path and read_size"""
        self.file_path = file_path
        self.settings = POSIXSettings(
            read_size=read_size,
            **kwargs,  # type: ignore[arg-type]
        )

    def _get_xattr(self, xattr_name: str) -> str:
        try:
            xattr_value = xattr.getxattr(self.file_path, attr=xattr_name)
            xattr_value = xattr_value.decode("utf-8")
        except OSError as error:
            # this is OK, just means the xattr does not exist
            log.debug(
                "No checksum found in metadata (%s) for file %s: %s",
                xattr_name,
                self.file_path,
                error,
            )
            return ""
        if xattr_value:
            return str(xattr_value)

        return ""

    def get_checksum(self, checksum: Checksum) -> Checksum:
        # check if file exists
        exists = Path(self.file_path).exists()
        if not exists:
            log.error("File %s does not exist", self.file_path)
            return checksum
        # try to get from metadata
        xattr_name = XATTR_TEMPLATE.format(checksum.name)
        with Timer(
            text=f"POSIX get_xattr took {{:.3f}}s for {self.file_path}",
            logger=log.timing,
        ):
            xattr_value = self._get_xattr(xattr_name)
        if xattr_value:
            log.debug(
                "Found checksum %s in metadata (%s=%s) for file %s",
                checksum.name,
                xattr_name,
                xattr_value,
                self.file_path,
            )
            checksum.value = xattr_value
            return checksum
        # did not find it in metadata, try calculating it
        with Timer(
            text=f"HDFS checksum calculation took {{:.3f}}s for {self.file_path}",
            logger=log.timing,
        ):
            checksum.value = checksum.calculate(
                read_file_in_chunks(self.file_path, self.settings.read_size)
            )

        return checksum

    def store_checksum(self, checksum: Checksum, force: bool = False) -> None:
        if not checksum.value:
            checksum = self.get_checksum(checksum)

        xattr_name = XATTR_TEMPLATE.format(checksum.name)
        xattr_value = self._get_xattr(xattr_name)
        if xattr_value and not force:
            log.debug(
                "Checksum already exists in metadata (%s=%s) for file %s and force=False - not overwriting",
                xattr_name,
                xattr_value,
                self.file_path,
            )
            return
        xattr.setxattr(
            self.file_path,
            xattr_name,
            checksum.value.encode("utf-8"),
        )
