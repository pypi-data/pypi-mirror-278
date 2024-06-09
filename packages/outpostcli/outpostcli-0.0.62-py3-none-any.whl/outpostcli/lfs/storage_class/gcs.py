from multiprocessing import cpu_count
from typing import Any, Dict, List, Literal, Tuple, TypedDict

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

_log = create_lfs_logger(__name__)


class GCSUploadActionDetails(TypedDict):
    storage_provider: Literal["gcs"]
    chunk_size: str
    abort_url: str


class GCSUploadAction(TypedDict):
    href: str
    header: Dict[str, str]
    method: Literal["POST"]


class GCSUploadMessage(TypedDict):
    oid: str
    path: str
    action: GCSUploadAction


# def gen_part_url(signed_url: str, part_num: int):
#     return f"{signed_url}&partNumber={part_num}"


# def gen_upload_specific_url(signed_url: str, upload_id: str):
#     return f"{signed_url}&uploadId={upload_id}"

def gcs_multipart_upload(msg: Dict[str, Any]):
    oid = msg["oid"]
    filepath = msg["path"]

    _log.info(msg)

    # _log.info(f"initiated multipart upload of file {filepath}, upload_id: {upload_id}")
    header = msg["action"]["header"]
    chunk_size = int(header.pop("chunk_size"))
    abort_url = header.pop("abort_url")
    complete_url = msg["action"]["href"]

    # if i can extract part number from url, no need for this.
    # presigned_urls: List[str] = list(header.values())
    # tbf the above can suffice as all the other headers are popped.
    pre_signed_urls: List[Tuple[int, str]] = []
    for k, v in header.items():
        pNo = try_extracting_part_number(k)
        if pNo:
            pre_signed_urls.append((pNo, v))
    _log.info(
        f"Starting multipart upload, oid={oid} num_parts={len(pre_signed_urls)}, chunk_size={chunk_size}"
    )
    parts = []
    cores = cpu_count()
    _log.info({"cores": cores})
    bytes_so_far = 0
    try:
        with multimap(cores) as pmap:
            for resp in pmap(
                transfer_part,
                (
                    PartInfo(
                        filepath,
                        part_no,
                        chunk_size,
                        signed_url,
                    )
                    for (part_no, signed_url) in pre_signed_urls
                ),
            ):
                if isinstance(resp, ProxyLFSException):
                    raise LFSException(
                        code=resp.code,
                        message=resp.message,
                        doc_url=resp.doc_url,
                    )
                else:
                    bytes_so_far += chunk_size
                    # Not precise but that's ok.
                    write_msg(
                        {
                            "event": "progress",
                            "oid": oid,
                            "bytesSoFar": bytes_so_far,
                            "bytesSinceLast": chunk_size,
                        }
                    )
                    parts.append(resp)
                pass
        complete_resp = complete_multipart_upload(complete_url, parts)
        if isinstance(complete_resp, LFSException):
            abort_resp = abort_multipart_upload(abort_url)
            if isinstance(abort_resp, LFSException):
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
        if isinstance(abort_resp, LFSException):
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
        if isinstance(abort_resp, LFSException):
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
