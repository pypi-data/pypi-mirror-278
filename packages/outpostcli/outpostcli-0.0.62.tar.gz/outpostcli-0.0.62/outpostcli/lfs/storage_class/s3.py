from multiprocessing import cpu_count
from typing import Any, Dict, List, Literal, Tuple, TypedDict

from hf_transfer import multipart_upload
from outpostkit.repository.lfs.logger import create_lfs_logger

from outpostcli.lfs.comms import write_msg
from outpostcli.lfs.exc import LFSException, ProxyLFSException
from outpostcli.lfs.parallel import multimap
from outpostcli.lfs.part import PartInfo, transfer_part
from outpostcli.lfs.storage_class.utils import (
    abort_multipart_upload,
    complete_multipart_upload,
    try_extracting_part_number,
)
from outpostcli.lfs.types import UploadedPartObject

_log = create_lfs_logger(__name__)


class FileUploadProgress:
    def __init__(self, oid: str) -> None:
        self.progress = 0
        self.oid = oid
        self.chunks = 0

    def update(self, sz: int) -> None:
        self.progress += sz
        self.chunks += 1

        _log.info({"oid": self.oid, "chunk_no": sz})
        write_msg(
            {
                "event": "progress",
                "oid": self.oid,
                "bytesSoFar": self.progress,
                "bytesSinceLast": sz,
            }
        )


class S3UploadActionDetails(TypedDict):
    storage_provider: Literal["s3"]
    chunk_size: str
    abort_url: str


class S3UploadAction(TypedDict):
    href: str
    header: Dict[str, str]
    method: Literal["POST"]


class S3UploadMessage(TypedDict):
    oid: str
    path: str
    action: S3UploadAction


def s3_multipart_upload(msg: Dict[str, Any]):
    oid = msg["oid"]
    filepath = msg["path"]

    _log.info(msg)

    header: Dict[str, str] = msg["action"]["header"]
    chunk_size = int(header.pop("chunk_size"))
    abort_url = str(header.pop("abort_url"))
    complete_url = msg["action"]["href"]

    # if i can extract part number from url, no need for this.
    # presigned_urls: List[str] = list(header.values())
    # tbf the above can suffice as all the other headers are popped.

    pre_signed_urls: List[Tuple[int, str]] = []
    for k, v in header.items():
        pNo = try_extracting_part_number(k)
        if pNo:
            pre_signed_urls.append((pNo, v))

    sorted_urls = ["" for _ in range(len(pre_signed_urls))]

    for u in pre_signed_urls:
        sorted_urls[u[0] - 1] = u[1]

    _log.info(
        f"Starting S3 multipart upload, oid={oid} num_parts={len(pre_signed_urls)}, chunk_size={chunk_size}"
    )
    parts: List[UploadedPartObject] = []

    cores = cpu_count()
    _log.info({"cores": cores})
    progress_controller = FileUploadProgress(oid)
    try:

        # hf_transfer
        output = multipart_upload(
            file_path=filepath,
            parts_urls=sorted_urls,
            chunk_size=chunk_size,
            max_files=128,
            parallel_failures=127,  # could be removed
            max_retries=5,
            callback=lambda sz: progress_controller.update(sz),
        )

        for _idx, header in enumerate(output):
            etag = header.get("etag")
            if etag is None or etag == "":
                raise ValueError(
                    f"Invalid etag (`{etag}`) returned for part {_idx + 1}"
                )
            _log.info({"part_no": _idx + 1, "etag": etag})
            parts.append(UploadedPartObject(etag=etag, part_number=_idx + 1))
        # write_msg(
        #     {
        #         "event": "progress",
        #         "oid": oid,
        #         "bytesSoFar": bytes_so_far,
        #         "bytesSinceLast": chunk_size,
        #     }
        # )
        # try:
        #     for part_no, signed_url in pre_signed_urls:
        #         part_info = PartInfo(filepath, part_no, chunk_size, signed_url)
        #         resp = transfer_part(part_info)
        #         if isinstance(resp, ProxyLFSException):
        #             raise LFSException(
        #                 code=resp.code,
        #                 message=resp.message,
        #                 doc_url=resp.doc_url,
        #             )
        #         else:
        #             bytes_so_far += chunk_size
        #             # Not precise but that's ok.
        #             write_msg(
        #                 {
        #                     "event": "progress",
        #                     "oid": oid,
        #                     "bytesSoFar": bytes_so_far,
        #                     "bytesSinceLast": chunk_size,
        #                 }
        #             )
        #             parts.append(resp)
        #         pass

        # multi threaded python
        # bytes_so_far = 0
        # with multimap(cores) as pmap:
        #     for resp in pmap(
        #         transfer_part,
        #         (
        #             PartInfo(
        #                 filepath,
        #                 part_no,
        #                 chunk_size,
        #                 signed_url,
        #             )
        #             for (part_no, signed_url) in pre_signed_urls
        #         ),
        #     ):
        #         if isinstance(resp, ProxyLFSException):
        #             raise LFSException(
        #                 code=resp.code,
        #                 message=resp.message,
        #                 doc_url=resp.doc_url,
        #             )
        #         else:
        #             bytes_so_far += chunk_size
        #             # Not precise but that's ok.
        #             write_msg(
        #                 {
        #                     "event": "progress",
        #                     "oid": oid,
        #                     "bytesSoFar": bytes_so_far,
        #                     "bytesSinceLast": chunk_size,
        #                 }
        #             )
        #             parts.append(resp)
        #         pass
        complete_resp = complete_multipart_upload(complete_url, parts)
        if isinstance(complete_resp, ProxyLFSException):
            abort_resp = abort_multipart_upload(abort_url)
            if isinstance(abort_resp, ProxyLFSException):
                write_msg(
                    {
                        "event": "complete",
                        "oid": oid,
                        "error": {
                            "code": abort_resp.code,
                            "message": abort_resp.message,
                            "original_error": {
                                "code": complete_resp.code,
                                "message": complete_resp.message,
                            },
                        },
                    }
                )
            else:
                _log.info(f"aborted multipart upload, oid={oid}")
                write_msg(
                    {
                        "event": "complete",
                        "oid": oid,
                        "error": {
                            "code": complete_resp.code,
                            "message": complete_resp.message,
                        },
                    }
                )
        else:
            _log.info(f"completed multipart upload, oid={oid}")
            write_msg({"event": "complete", "oid": oid})
    except LFSException as e:
        abort_resp = abort_multipart_upload(abort_url)
        if isinstance(abort_resp, ProxyLFSException):
            write_msg(
                {
                    "event": "complete",
                    "oid": oid,
                    "error": {
                        "code": abort_resp.code,
                        "message": abort_resp.message,
                        "original_error": {
                            "code": e.code,
                            "message": e.message,
                        },
                    },
                }
            )
        else:
            _log.info(f"aborted multipart upload, oid={oid}")
            write_msg(
                {
                    "event": "complete",
                    "oid": oid,
                    "error": {"code": e.code, "message": e.message},
                }
            )
    except Exception as e:  # noqa: BLE001
        abort_resp = abort_multipart_upload(abort_url)
        _log.error(e, exc_info=True)
        if isinstance(abort_resp, ProxyLFSException):
            write_msg(
                {
                    "event": "complete",
                    "oid": oid,
                    "error": {
                        "code": abort_resp.code,
                        "message": abort_resp.message,
                        "original_error": {
                            "code": 500,
                            "message": str(e),
                        },
                    },
                }
            )
        else:
            _log.info(f"aborted multipart upload, oid={oid}")
            write_msg(
                {
                    "event": "complete",
                    "oid": oid,
                    "error": {
                        "code": 500,
                        "message": str(e),
                    },
                }
            )
