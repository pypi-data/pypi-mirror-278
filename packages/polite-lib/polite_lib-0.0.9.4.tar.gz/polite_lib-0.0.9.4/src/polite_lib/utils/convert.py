"""
    Polite Lib
    Utils
    Convert
        A libary for making common conversions.
    Testing


"""
import math


def bytes_to_human(the_bytes: int) -> str:
    """Take an argument of a bytes and convert that into a human readble understanding of disk size.
    """
    if the_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(the_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(the_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


# End File: polite-lib/src/polite-lib/utils/convert.py
