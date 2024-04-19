import os
from urllib.parse import urlparse

from src.utils.helper.aws_config import s3
import boto3


def download_image_from_s3(s3_url, local_dir):
    #
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc
    directory_prefix = parsed_url.path.strip('/')

    # Get bucket object
    bucket = s3.Bucket(bucket_name)

    # List objects in the specified directory
    for obj in bucket.objects.filter(Prefix=directory_prefix):
        key = obj.key
        file_name = os.path.basename(key)
        local_path = os.path.join(local_dir, file_name)

        # Skip directories
        if not file_name:
            continue

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Create directories if they don't exist

        # Download file from S3
        bucket.download_file( key, local_path)
        print(f"File downloaded successfully to: {local_path}")
    return local_dir
