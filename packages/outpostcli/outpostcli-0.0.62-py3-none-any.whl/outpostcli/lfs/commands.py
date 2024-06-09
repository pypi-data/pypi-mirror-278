# ref: https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/commands/lfs.py
import json
import os
import subprocess
import sys

import click
from outpostkit.repository.lfs.logger import create_lfs_logger

from outpostcli.constants import CLI_BINARY_NAME
from outpostcli.lfs.comms import read_msg, write_msg
from outpostcli.lfs.storage_class import handle_multipart_upload
from outpostcli.utils import click_group


@click_group()
def lfs():
    pass


_log = create_lfs_logger(__name__)

MULTIPART_UPLOAD_COMMAND_NAME = "multipart-upload"
LFS_MULTIPART_UPLOAD_COMMAND = f"lfs {MULTIPART_UPLOAD_COMMAND_NAME}"


# TODO: find a way to register commands like this
# class LfsCommands(BaseHuggingfaceCLICommand):
#     @staticmethod
#     def register_subcommand(parser: _SubParsersAction):
#         parser.add_command(enable_largefiles)
#         parser.add_command(multipart_upload)

@lfs.command(name="enable-largefiles")
@click.argument("path", type=str)
def enable_largefiles(path):
    """Configure your repository to enable upload of files > 5GB"""
    local_path = os.path.abspath(path)

    if not os.path.isdir(local_path):
        click.echo("This does not look like a valid git repo.")
        sys.exit(1)

    subprocess.run(
        f"git config lfs.customtransfer.multipart-basic.path {CLI_BINARY_NAME}".split(),
        check=True,
        cwd=local_path,
    )

    subprocess.run(
        [
            "git",
            "config",
            "lfs.customtransfer.multipart-basic.args",
            f"{LFS_MULTIPART_UPLOAD_COMMAND}",
        ],
        check=True,
        cwd=local_path,
    )

    subprocess.run(
        [
            "git",
            "config",
            "lfs.customtransfer.multipart-basic.concurrent",
            "false",
        ],
        check=True,
        cwd=local_path,
    )

    click.echo("Local repository set up for largefiles")


@lfs.command(name="disable-multipart")
@click.argument("path", type=str)
def enable_largefiles(path):
    """Configure your repository to enable upload of files > 5GB"""
    local_path = os.path.abspath(path)

    if not os.path.isdir(local_path):
        click.echo("This does not look like a valid git repo.")
        sys.exit(1)

    subprocess.check_call(
        "git config --unset lfs.customtransfer.multipart-basic.path".split(),
        cwd=local_path,
    )

    subprocess.check_call(
        ["git", "config", "--unset", "lfs.customtransfer.multipart-basic.args"],
        cwd=local_path,
    )

    subprocess.check_call(
        [
            "git",
            "config",
            "--unset",
            "lfs.customtransfer.multipart-basic.concurrent",
        ],
        cwd=local_path,
    )

    click.echo("multipart upload configs removed.")


@lfs.command(name=MULTIPART_UPLOAD_COMMAND_NAME)
def multipart_upload():
    try:
        """Command called by git lfs directly and is not meant to be called by the user"""
        # ... (rest of the existing code)
        init_msg = json.loads(sys.stdin.readline().strip())

        if not (init_msg.get("event") == "init" and init_msg.get("operation") == "upload"):
            write_msg({"error": {"code": 32, "message": "Wrong lfs init operation"}})
            sys.exit(1)

        _log.info(init_msg)
        # The transfer process should use the information it needs from the
        # initiation structure, and also perform any one-off setup tasks it
        # needs to do. It should then respond on stdout with a simple empty
        # confirmation structure, as follows:
        write_msg({})

        # After the initiation exchange, git-lfs will send any number of
        # transfer requests to the stdin of the transfer process, in a serial sequence.
        while True:
            msg = read_msg()
            if msg is None:
                # When all transfers have been processed, git-lfs will send
                # a terminate event to the stdin of the transfer process.
                # On receiving this message the transfer process should
                # clean up and terminate. No response is expected.
                sys.exit(0)
            handle_multipart_upload(msg)
    except Exception as e:
        _log.error(e, exc_info=True)
        raise

        # _log.info({"parts": parts})

if __name__ == "__main__":
    lfs()
