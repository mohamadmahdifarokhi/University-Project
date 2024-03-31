from typing import BinaryIO, Any
from uuid import uuid4
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from fastapi import UploadFile
from boto3 import client

load_dotenv()


class BotoClient:
    """
    A class for interacting with AWS S3 using the Boto3 library.

    Attributes:
        AWS_ACCESS_KEY_ID (str): AWS access key ID.
        AWS_SECRET_ACCESS_KEY (str): AWS secret access key.
        AWS_S3_ENDPOINT_URL (str): AWS S3 endpoint URL.
        AWS_STORAGE_BUCKET_NAME (str): AWS S3 bucket name.
        AWS_SERVICE_NAME (str): AWS service name.
        OVERWRITE_EXISTING_FILES (bool): Flag to determine if existing files should be overwritten.

    Methods:
        __init__(self): Initialize the BotoClient instance.
        write(self, file: BinaryIO, name: str) -> str: Write the input file to the destination and return the link.
        generate_link(self, filename) -> str: Generate a public link for the given filename.
        upload_fileobj(self, file: UploadFile) -> str: Upload a file object and return the public link.
        get_list_of_objects(self) -> list: Get a list of objects in the S3 bucket.
        get_list_of_links(self) -> list: Get a list of public links for objects in the S3 bucket.
        get_path(self, filename) -> str: Get the public path for the given filename.
        generate_new_filename(self, filename) -> str: Generate a new filename to avoid conflicts.
        _check_object_exists(self, key) -> bool: Check if an object with the given key exists.
        get_name(self, name: str) -> str: Get the normalized name of the file.
    """
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_SERVICE_NAME = os.getenv("AWS_SERVICE_NAME", "s3")
    OVERWRITE_EXISTING_FILES = os.getenv("OVERWRITE_EXISTING_FILES", False)

    def __init__(self) -> None:
        """
        Initialize the BotoClient instance.
        """
        self.client = client(
            service_name=self.AWS_SERVICE_NAME,
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            endpoint_url=f"https://{self.AWS_S3_ENDPOINT_URL}",
        )

    def write(self, file: BinaryIO, name: str) -> str:
        """
        Write input file, opened in binary mode, to the destination.

        Args:
            file (BinaryIO): The binary file to write.
            name (str): The name of the file.

        Returns:
            str: The public link to the uploaded file.
        """
        file.seek(0, 0)
        key = self.get_name(name)

        self.client.upload_fileobj(file, self.AWS_STORAGE_BUCKET_NAME, key, ExtraArgs={"ACL": "public-read"})
        link = self.generate_link(key)
        return link

    def generate_link(self, filename: str) -> str:
        """
        Generate a public link for the given filename.

        Args:
            filename (str): The filename.

        Returns:
            str: The public link.
        """
        return f"https://{self.AWS_STORAGE_BUCKET_NAME}.{self.AWS_S3_ENDPOINT_URL}/{filename}"

    def upload_fileobj(self, file: UploadFile) -> str:
        """
        Upload a file object and return the public link.

        Args:
            file (UploadFile): The file object.

        Returns:
            str: The public link to the uploaded file.
        """
        extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid4()}{extension}"
        self.client.upload_fileobj(
            file.file,
            self.AWS_STORAGE_BUCKET_NAME,
            filename,
            ExtraArgs={"ACL": "public-read", "ContentType": file.content_type},
        )
        return self.generate_link(filename)

    def get_list_of_objects(self) -> Any | None:
        """
        Get a list of objects in the S3 bucket.

        Returns:
            list: List of objects in the S3 bucket.
        """
        result = self.client.list_objects_v2(Bucket=self.AWS_STORAGE_BUCKET_NAME)
        if result.get("KeyCount", 0) > 0:
            return result.get("Contents", [])
        return None

    def get_list_of_links(self) -> list:
        """
        Get a list of public links for objects in the S3 bucket.

        Returns:
            list: List of public links.
        """
        result = self.get_list_of_objects()
        return [self.generate_link(item["Key"]) for item in result]

    def get_path(self, filename: str) -> str:
        """
        Get the public path for the given filename.

        Args:
            filename (str): The filename.

        Returns:
            str: The public path.
        """
        key = f"{self.AWS_STORAGE_BUCKET_NAME}/{filename}"
        return f"https://{self.AWS_S3_ENDPOINT_URL}/{key}"

    def generate_new_filename(self, filename: str) -> str:
        """
        Generate a new filename to avoid conflicts.

        Args:
            filename (str): The original filename.

        Returns:
            str: The new filename.
        """
        stem, extension = os.path.splitext(filename)
        counter = 0

        while self._check_object_exists(filename):
            counter += 1
            filename = f"{stem}_{counter}{extension}"

        return filename

    def _check_object_exists(self, key: str) -> bool:
        """
        Check if an object with the given key exists.

        Args:
            key (str): The object key.

        Returns:
            bool: True if the object exists, False otherwise.
        """
        try:
            self.client.head_object(Bucket=self.AWS_STORAGE_BUCKET_NAME, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise

    @classmethod
    def get_name(cls, name: str) -> str:
        """
        Get the normalized name of the file.

        Args:
            name (str): The original name.

        Returns:
            str: The normalized name.
        """
        return name


boto_client = BotoClient()
