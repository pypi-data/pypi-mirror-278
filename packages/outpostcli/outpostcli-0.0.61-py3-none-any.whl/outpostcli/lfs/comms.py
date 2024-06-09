import json
import sys
from typing import Dict, Optional

from outpostkit.repository.lfs.logger import create_lfs_logger

_log = create_lfs_logger(__name__)


def write_msg(msg: Dict):
    """Write out the message in Line delimited JSON."""
    msg_str = json.dumps(msg) + "\n"
    sys.stdout.write(msg_str)
    sys.stdout.flush()


def read_msg() -> Optional[Dict]:
    """Read Line delimited JSON from stdin."""
    msg = json.loads(sys.stdin.readline().strip())
    _log.info(msg)
    if "terminate" in (msg.get("type"), msg.get("event")):
        # terminate message received
        return None

    if msg.get("event") not in ("download", "upload"):
        # logger.critical("Received unexpected message")
        sys.exit(1)

    return msg
