import io
import os
from contextlib import AbstractContextManager
from typing import (
    BinaryIO,
    Optional,
)


class SliceFileObj(AbstractContextManager):
    """
    Utility context manager to read a *slice* of a seekable file-like object as a seekable, file-like object.

    This is NOT thread safe

    Inspired by stackoverflow.com/a/29838711/593036

    Credits to @julien-c

    Args:
        fileobj (`BinaryIO`):
            A file-like object to slice. MUST implement `tell()` and `seek()` (and `read()` of course).
            `fileobj` will be reset to its original position when exiting the context manager.
        seek_from (`int`):
            The start of the slice (offset from position 0 in bytes).
        read_limit (`int`):
            The maximum number of bytes to read from the slice.

    Attributes:
        previous_position (`int`):
            The previous position

    Examples:

    Reading 200 bytes with an offset of 128 bytes from a file (ie bytes 128 to 327):
    ```python
    >>> with open("path/to/file", "rb") as file:
    ...     with SliceFileObj(file, seek_from=128, read_limit=200) as fslice:
    ...         fslice.read(...)
    ```

    Reading a file in chunks of 512 bytes
    ```python
    >>> import os
    >>> chunk_size = 512
    >>> file_size = os.getsize("path/to/file")
    >>> with open("path/to/file", "rb") as file:
    ...     for chunk_idx in range(ceil(file_size / chunk_size)):
    ...         with SliceFileObj(file, seek_from=chunk_idx * chunk_size, read_limit=chunk_size) as fslice:
    ...             chunk = fslice.read(...)

    ```
    """

    def __init__(self, fileobj: BinaryIO, seek_from: int, read_limit: int) -> None:
        self.fileobj = fileobj
        self.seek_from = seek_from
        self.read_limit = read_limit

    def __enter__(self):
        self._previous_position = self.fileobj.tell()
        end_of_stream = self.fileobj.seek(0, os.SEEK_END)
        self._len = min(self.read_limit, end_of_stream - self.seek_from)
        # ^^ The actual number of bytes that can be read from the slice
        self.fileobj.seek(self.seek_from, io.SEEK_SET)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fileobj.seek(self._previous_position, io.SEEK_SET)

    def read(self, n: int = -1) -> bytes:
        pos = self.tell()
        if pos >= self._len:
            return b""
        remaining_amount = self._len - pos
        data = self.fileobj.read(
            remaining_amount if n < 0 else min(n, remaining_amount)
        )
        return data

    def tell(self) -> int:
        return self.fileobj.tell() - self.seek_from

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        start = self.seek_from
        end = start + self._len
        if whence in (os.SEEK_SET, os.SEEK_END):
            offset = start + offset if whence == os.SEEK_SET else end + offset
            offset = max(start, min(offset, end))
            whence = os.SEEK_SET
        elif whence == os.SEEK_CUR:
            cur_pos = self.fileobj.tell()
            offset = max(start - cur_pos, min(offset, end - cur_pos))
        else:
            raise ValueError(f"whence value {whence} is not supported")
        return self.fileobj.seek(offset, whence) - self.seek_from

    def __iter__(self):
        yield self.read(n=4 * 1024 * 1024)


class HTTPException(Exception):
    """A base class for all Outpost exceptions."""

    status_code: int
    message: str
    code: Optional[str] = None

    def __init__(
        self, status_code: int, message: str, code: Optional[str] = None
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"status: {self.status_code}, message: {self.code + ' - '+ self.message if self.code else self.message}"


# def _raise_for_status(resp: httpx.Response):
#     if 400 <= resp.status_code < 600:
#         content_type, _, _ = resp.headers["content-type"].partition(";")
#         # if content_type != "text/event-stream":
#         #     raise ValueError(
#         #         "Expected response Content-Type to be 'text/event-stream', "
#         #         f"got {content_type!r}"
#         #     )
#         try:
#             if content_type == "application/json":
#                 try:
#                     data = resp.json()
#                     if isinstance(data, dict):
#                         raise HTTPException(
#                             status_code=resp.status_code,
#                             message=data.get("message")
#                             or "Request failed without message.",
#                             code=data.get("code"),
#                         ) from None
#                     else:
#                         raise HTTPException(
#                             status_code=resp.status_code,
#                             message=(
#                                 data
#                                 if isinstance(data, str)
#                                 else getattr(
#                                     data, "message", "Request failed without message."
#                                 )
#                             ),
#                         ) from None
#                 except JSONDecodeError as e:
#                     raise HTTPException(
#                         message="Failed to decode json body.", status_code=500
#                     ) from e
#             elif content_type == "text/plain":
#                 raise HTTPException(
#                     status_code=resp.status_code, message=resp.text
#                 )
#             elif content_type == "text/html":
#                 raise HTTPException(
#                     status_code=resp.status_code, message=resp.text
#                 )
#             else:
#                 raise HTTPException(
#                     status_code=resp.status_code,
#                     message=f"Request failed. Unhandled Content Type: {content_type}",
#                 )
#         except Exception:
#             raise
