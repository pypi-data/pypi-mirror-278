"""
    BackBlaze
    Utility for managing files in Backblaze b2

"""
import logging
import os

from minio import Minio as Minny
from minio.error import S3Error


class Minio:

    def __init__(self, minio_url: str = None, access_key: str = None, secret_key: str = None):
        self.minio_url = minio_url
        if not minio_url:
            self.minio_url = os.environ.get("MINIO_URL")
        self.access_key = access_key
        if not self.access_key:
            self.access_key = os.environ.get("MINIO_ACCESS_KEY")
        self.secret_key = secret_key
        if not self.secret_key:
            self.secret_key = os.environ.get("MINIO_SECRET_KEY")
        self.client = None
        self.bucket = None

    def connect(self, bucket_name: str):
        """Connect to Minio server."""
        if not self.minio_url:
            raise ValueError("No MinIO server supplied.")
        if not self.access_key:
            raise ValueError("No MinIO access key supplied.")
        if not self.secret_key:
            raise ValueError("No MinIO secret key supplied.")
        if "https://" in self.minio_url:
            self.minio_url = self.minio_url.replace("https://", "")
        self.client = Minny(self.minio_url, self.access_key, self.secret_key)
        self.bucket = bucket_name

    def upload_file(self, local_phile: str, remote_phile: str = None, content_type: str = None):
        """Upload a photo to MinIo."""
        if not remote_phile:
            remote_phile = local_phile[local_phile.rfind("/") + 1:]

        try:
            self.client.fput_object(
                self.bucket, remote_phile, local_phile, content_type=content_type
            )
            logging.info("Uploaded %s > %s" % (local_phile, remote_phile))
            return True
        except S3Error as e:
            logging.error("Could not upload file: %s to %s. %s" % (local_phile, remote_phile, e))
            return False

# End File: polite-lib/src/polite-lib/file_tools/minio.py
