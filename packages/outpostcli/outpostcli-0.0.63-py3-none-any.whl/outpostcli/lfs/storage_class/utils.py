import re
from typing import (
    List,
)

import requests
from outpostkit.repository.lfs.logger import create_lfs_logger
from tenacity import retry, stop_after_attempt, wait_exponential

from outpostcli.lfs.exc import handle_request_errors
from outpostcli.lfs.types import UploadedPartObject

_log = create_lfs_logger(__name__)


def try_extracting_part_number(s: str):
    match = re.match(r"part_(\d+)", s)
    if match:
        return int(match.group(1))
    return None


def part_dict_list_to_xml(multi_parts: List[UploadedPartObject]):
    s = "<CompleteMultipartUpload>\n"
    for part in multi_parts:
        s += "  <Part>\n"
        s += "    <PartNumber>%d</PartNumber>\n" % part["part_number"]
        s += "    <ETag>%s</ETag>\n" % part["etag"]
        s += "  </Part>\n"
    s += "</CompleteMultipartUpload>"
    return s


@handle_request_errors(prefix="CompleteMultipartUpload")
@retry(
    reraise=True,
    stop=stop_after_attempt(4),  # Maximum number of retries
    wait=wait_exponential(multiplier=1, min=1, max=60),  # Exponential backoff
)
def complete_multipart_upload(url: str, parts: List[UploadedPartObject]):
    data = part_dict_list_to_xml(sorted(parts, key=lambda x: x.get("part_number")))
    _log.info({"completion_url": url, "data": data})
    r = requests.post(
        url,
        # headers={"Content-Type": "application/xml"},
        data=data,  # type: ignore
    )
    _log.info((r.status_code, r.text))
    r.raise_for_status()
    return r


@handle_request_errors(prefix="AbortMultipartUpload")
@retry(
    reraise=True,
    stop=stop_after_attempt(4),  # Maximum number of retries
    wait=wait_exponential(multiplier=1, min=1, max=60),  # Exponential backoff
)
def abort_multipart_upload(url: str):
    r = requests.delete(url)
    r.raise_for_status()
    return r
