"""
    Polite Lib
    File Tools
    File Tools
    A collections of tools for working with file systems.

"""
import hashlib
# import logging
# import subprocess
# import tempfile
import os

# from polite_lib.utils import convert
from polite_lib.utils import mathy


def get_size(the_path: str) -> int:
    """Get the size of a file or directory from a given path."""
    if os.path.isdir(the_path):
        return get_directory_size(the_path)
    return os.path.getsize(the_path)


def get_directory_size(directory_path: str) -> int:
    """Get the size of a directory in bytes. Will skip sym linked dirctories.
    Use polite_lib.bytes_to_human to get human readable size.
    :unit-test: TestFileTools::test__get_directory_size()
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def get_filename(file_path: str) -> str:
    """Get the filename from a filepath.
    :unit-test: TestFileTools::test__get_filename()
    """
    if "/" in file_path:
        return file_path[file_path.rfind("/") + 1:]
    else:
        return file_path


def get_extension(file_path: str) -> int:
    """Get the extension of a file based off it's path.
    :unit-test: TestFileTools::test__get_extension()
    """
    if "." not in file_path:
        return None
    dot = file_path.rfind(".")
    if len(file_path) == dot:
        return None
    return file_path[dot + 1:]


def get_hash(file_path: str) -> str:
    """Get the MD5 hash of a given file's contents.
    :unit-test: TestFileTools::test__get_hash()
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError("Path does not exist: %s" % file_path)
    open_file = open(file_path, 'rb').read()
    return hashlib.md5(open_file).hexdigest()


def get_disk_info(path_of_partion: str = "/") -> dict:
    """Get the details of a disk partion, including filesystem size, available bytes and free bytes.
    The method will determine the filesystem no matter how qualified the path is, and return data in
    both bytes and human readable sizes.
    """
    statvfs = os.statvfs(path_of_partion)
    ret = {
        "file_system_size": statvfs.f_frsize * statvfs.f_blocks,
        "file_system_free": statvfs.f_frsize * statvfs.f_bfree,
        "file_system_available": statvfs.f_frsize * statvfs.f_bavail,
    }
    ret["percent_free"] = mathy.percentize(ret["file_system_free"], ret["file_system_size"])
    ret["percent_available"] = mathy.percentize(
        ret["file_system_available"],
        ret["file_system_size"])
    # import ipdb; ipdb.set_trace()
    # ret["file_system_size_human"] = convert.bytes_to_human(["file_system_size"])
    # ret["file_system_free_human"] = convert.bytes_to_human(["file_system_free"])
    # ret["file_system_available_human"] = convert.bytes_to_human(["file_system_available"])
    return ret


# def make_zip(
#         path_to_zip: str,
#         zip_path: str,
#         encryption_pass: str = "",
#         temp_dir: str = "",
#         zip_to_temp_space: bool = False
# ) -> bool:
#     """Create a zip of a file or a directory, with optional encryption password.
#     :param: path_to_zip: The path to zip, either a single file or a directory of files.
#     :param zip_path: Path of the zip to be zipped.
#     :param encryption_pass: (optional) Password to use to encrypt the zipfile.
#     :param temp_dir: Path of the temporary storage location to use.
#     """
#     # Determine if we're zipping a directory or a file.
#     if os.path.isdir(path_to_zip):
#         logging.info(f"Zip - Path {path_to_zip} is a directory")
#         is_dir = True
#     else:
#         logging.info(f"Zip - Path {path_to_zip} is a file")
#         is_dir = False

#     if not temp_dir:
#         temp_dir = tempfile.gettempdir()
#     logging.info(f"Using tempdir: {temp_dir}")

#     # Get temp dir free space and zip space needed
#     if not zip_to_temp_space:
#         temp_dir_space = get_disk_info(temp_dir)
#         zip_dir_size = get_size(path_to_zip)
#         if temp_dir_space["file_system_free"] < zip_dir_size:
#             logging.critical("Cannot create zip, not enough free space on temp dir.")
#             return False

#     zip_landed_dir = os.path.dirname(zip_path)
#     zip_landed_dir_details = get_disk_info(zip_landed_dir)
#     if zip_landed_dir_details["file_system_free"] < zip_dir_size:
#         logging.critical("Cannot create zip, not enough free space on temp dir.")
#         return False

#     local_path = get_last_dir(zip_dir)
#     options = "rq"
#     password = ""
#     if encryption_pass:
#         options = "rqe"
#         password = " -P %s" % encryption_pass
#     subprocess.call('cd %s' % temp_dir_space, shell=True)

#     zip_full_path = os.path.join(self.local['tmp_dir'], zip_path)
    # start = arrow.now()
    # cmd = "cd %s && zip -%s %s %s%s" % (
    #     self.local['tmp_dir'],
    #     options,
    #     zip_full_path,
    #     local_path,
    #     password)
    # print('[%s] Making zip: %s' % (arrow.now(), zip_full_path))
    # subprocess.call(cmd, shell=True)
    # end = arrow.now()
    # self.time_zip = (end - start).seconds
    # self.size_backup_zipped = convert.bytes_to_human(file_tools.get_size(zip_full_path))
    # # self.size_backup_zipped = self._convert_size(self._get_size(zip_full_path))
    # print("[%s] Finished zipping files in %s seconds" % (arrow.now(), self.time_zip))


def get_last_dir(path: str):
    """Get the last segment of a full path
       ie: "/tmp/some-dir/some-other-dir" returns "some-other-dir"
    """
    if '/' not in path:
        return path

    last = path[path.rfind('/') + 1:]
    return last


# End File: politeauthority/polite-lib/src/polite-lib/file_tools/file_tools.py
