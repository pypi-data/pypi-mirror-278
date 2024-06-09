from typing import Any, Dict

from outpostcli.lfs.comms import write_msg
from outpostcli.lfs.storage_class.gcs import gcs_multipart_upload
from outpostcli.lfs.storage_class.s3 import s3_multipart_upload


def handle_multipart_upload(msg: Dict[str, Any]):
    storage_provider = msg["action"]["header"].pop("storage_provider")

    if storage_provider == "gcs":
        gcs_multipart_upload(msg)

    elif storage_provider == "s3":
        s3_multipart_upload(msg)
    else:
        write_msg(
            {
                "error": {
                    "code": 500,
                    "message": f"Invalid storage provider: {storage_provider}. Availabe options are `gcs` and `aws`.",
                }
            }
        )
