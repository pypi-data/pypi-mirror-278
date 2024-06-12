"""
    BackBlaze
    Utility for managing files in Backblaze b2

"""
import logging
import os

from b2sdk.v1 import B2Api, InMemoryAccountInfo


class Backblaze:

    def __init__(self, key_id: str = None, api_key: str = None):
        self.key_id = key_id
        if not key_id:
            self.key_id = os.environ.get("B2_KEY_ID")
        self.api_key = api_key
        if not api_key:
            self.api_key = os.environ.get("B2_API_KEY")

    def connect_to_b2(self, bucket: str) -> bool:
        """Conect to the Backblaze api"""
        info = InMemoryAccountInfo()
        self.b2_api = B2Api(info)
        self.b2_api.authorize_account(
            "production",
            self.key_id,
            self.api_key)
        self.bucket = self.b2_api.get_bucket_by_name(bucket)
        return True

    def upload_file(self, local_phile: str, remote_phile: str):
        """Upload a photo to backblaze."""
        success = self.bucket.upload_local_file(
            local_file=local_phile,
            file_name=remote_phile,
        )
        logging.info("Uploaded %s > %s" % (local_phile, remote_phile))
        return success


# End File: polite-lib/src/polite-lib/file_tools/backblaze.py
