import os
import sys
import logging
import subprocess

from abc import ABC
from typing import List


def get_immediate_subdirectories(full_path: str, ignore: List=[]) -> List[str]:
    """
    Get all immediate sub-directories for a certain full path.

    Args:
        full_path (str): Path (absolute) to folder to get immediate sub-directories for.
        ignore (List): List of folders to ignore. Defaults to [].

    Returns:
        List: List of immediate sub-directory names.
    """
    if not os.path.isabs(full_path):
        raise ValueError("Parameter full_path must be an Absolute Path!")

    subdirectories = []
    for item in os.scandir(full_path):
        if item.is_dir() and item.name not in ignore:
                subdirectories.append(item.name)

    return subdirectories


class CommandRunner(ABC):
    def run(self, *args, **kwargs) -> subprocess.CompletedProcess:
        """
        Run some CLI command, constructed from args and kwargs.

        Returns:
            subprocess.CompletedProcess: Completed Process, which will contain output
            and exit codes.
        """
        logging.info(f"Command: {args}")
        sys.stdout.flush()

        try:
            return subprocess.run(args, shell=False, check=True, encoding="utf-8", **kwargs)
        except subprocess.CalledProcessError as e:
            logging.error(
                f"""
                Command ran with {args} resulted in an error:
                {e.stdout if e.stdout else ""}
                {e.stderr if e.stderr else ""}
                """
            )
            raise
