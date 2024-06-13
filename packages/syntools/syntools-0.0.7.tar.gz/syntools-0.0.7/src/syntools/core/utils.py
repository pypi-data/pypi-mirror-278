import os
import re
import hashlib
import math
import pathlib
from .env import Env


class Utils:
    KB = 1024
    MB = KB * KB
    CHUNK_SIZE = 10 * MB

    @staticmethod
    def os_name():
        return os.name

    @staticmethod
    def patch():
        """Applies patches to packages"""
        if Env.SYNTOOLS_PATCH() is True:
            # On windows this method will lowercase all directory and file names.
            # We do not want this since it changes the data and breaks uploading and comparisons.
            if Utils.os_name() == 'nt':
                from .logging import Logging
                from synapseclient.core import utils
                Logging.info('Patching synapseclient.', console=True)

                def normalize_path(path):
                    """Transforms a path into an absolute path with forward slashes only."""
                    if path is None:
                        return None
                    return re.sub(r'\\', '/', os.path.abspath(path))

                utils.normalize_path = normalize_path

    @staticmethod
    def real_path(path):
        return str(pathlib.Path(path).resolve())

    @staticmethod
    def app_dir():
        """Gets the application's primary directory for the current user.

        Returns:
            Absolute path to the directory.
        """
        return os.path.join(pathlib.Path.home(), '.syntools')

    @staticmethod
    def app_log_dir():
        """Gets the applications primary log directory for the current user.

        Returns:
            Absolute path to the directory.
        """
        return os.path.join(Utils.app_dir(), 'logs')

    @staticmethod
    def app_resumable_queue_dir():
        """Gets the applications primary resumable_queue directory for the current user.

        Returns:
            Absolute path to the directory.
        """
        return os.path.join(Utils.app_dir(), '.resumable_queue')

    @staticmethod
    def expand_path(local_path):
        var_path = os.path.expandvars(local_path)
        expanded_path = os.path.expanduser(var_path)
        return os.path.abspath(expanded_path)

    @staticmethod
    def norm_os_path_sep(path):
        """Normalizes the path separator for the current operating system.

        Args:
            path: Path to normalize.

        Returns:
            Path with normalized path separators.
        """
        if os.sep == '/':
            return path.replace('\\', '/')
        else:
            return path.replace('/', '\\')

    @staticmethod
    def ensure_dirs(local_path):
        """Ensures the directories in local_path exist.

        Args:
            local_path: The local path to ensure.

        Returns:
            None
        """
        if not os.path.isdir(local_path):
            os.makedirs(local_path)

    @staticmethod
    def split_chunk(list, chunk_size):
        """Yield successive n-sized chunks from a list.

        Args:
            list: The list to chunk.
            chunk_size: The max chunk size.

        Returns:
            List of lists.
        """
        for i in range(0, len(list), chunk_size):
            yield list[i:i + chunk_size]

    # Holds the last string that was printed
    __last_print_inplace_len = 0

    @staticmethod
    def print_inplace(msg):
        Utils.print_inplace_reset()
        print(msg, end='\r')
        Utils.__last_print_inplace_len = len(msg)

    @staticmethod
    def print_inplace_reset():
        if Utils.__last_print_inplace_len > 0:
            # Clear the line. Using this method so it works on Windows too.
            print(' ' * Utils.__last_print_inplace_len, end='\r')
            Utils.__last_print_inplace_len = 0

    # Hold the names for pretty printing file sizes.
    PRETTY_SIZE_NAMES = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    @staticmethod
    def pretty_size(size):
        if size > 0:
            i = int(math.floor(math.log(size, 1024)))
            p = math.pow(1024, i)
            s = round(size / p, 2)
        else:
            i = 0
            s = 0
        return '{0} {1}'.format(s, Utils.PRETTY_SIZE_NAMES[i])

    @staticmethod
    def get_md5(local_path):
        md5 = hashlib.md5()
        with open(local_path, mode='rb') as fd:
            while True:
                chunk = fd.read(819200)
                if not chunk:
                    break
                md5.update(chunk)
        return md5.hexdigest()
