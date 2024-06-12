"""
    Polite Lib
    Url Tools

"""


def strip_protocol(url: str) -> str:
    """Remove the protocol from a URL if it exists."""
    protocols = ["https", "http"]
    for protocol in protocols:
        if f"{protocol}://" in url:
            return url.replace(f"{protocol}://", "")
    return url

# End File: polite-lib/src/polite-lib/utils/url_tools.py
