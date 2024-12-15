import boto3
from botocore.exceptions import ClientError


class S3Backend:
    """
    A utility class for managing interactions with AWS S3 for Splunk configurations and logs.
    """

    def __init__(self, bucket_name, region_name="us-east-1"):
        """
        Initializes the S3Backend with the S3 bucket name and AWS region.

        Args:
            bucket_name (str): Name of the S3 bucket.
            region_name (str): AWS region where the bucket is located.
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3", region_name=region_name)

    def upload_file(self, file_path, s3_key):
        """
        Uploads a file to the specified S3 bucket.

        Args:
            file_path (str): Path to the file to upload.
            s3_key (str): The S3 key (path in the bucket) for the uploaded file.

        Returns:
            bool: True if the upload is successful, False otherwise.
        """
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            print(f"Uploaded {file_path} to s3://{self.bucket_name}/{s3_key}")
            return True
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return False

    def download_file(self, s3_key, file_path):
        """
        Downloads a file from the S3 bucket.

        Args:
            s3_key (str): The S3 key (path in the bucket) of the file to download.
            file_path (str): The local file path to save the downloaded file.

        Returns:
            bool: True if the download is successful, False otherwise.
        """
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, file_path)
            print(f"Downloaded s3://{self.bucket_name}/{s3_key} to {file_path}")
            return True
        except ClientError as e:
            print(f"Error downloading file from S3: {e}")
            return False

    def list_files(self, prefix=""):
        """
        Lists all files in the S3 bucket under the specified prefix.

        Args:
            prefix (str): Prefix to filter files in the bucket. Defaults to an empty string.

        Returns:
            list: A list of S3 keys (paths) for the files in the bucket.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            files = [item["Key"] for item in response.get("Contents", [])]
            print(f"Found {len(files)} files under prefix '{prefix}'.")
            return files
        except ClientError as e:
            print(f"Error listing files in S3: {e}")
            return []

    def delete_file(self, s3_key):
        """
        Deletes a file from the S3 bucket.

        Args:
            s3_key (str): The S3 key (path in the bucket) of the file to delete.

        Returns:
            bool: True if the deletion is successful, False otherwise.
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            print(f"Deleted s3://{self.bucket_name}/{s3_key}")
            return True
        except ClientError as e:
            print(f"Error deleting file from S3: {e}")
            return False
