import os
from typing import Dict
from urllib.parse import urlparse
from botocore.exceptions import ClientError

from src.utils.constants.properties import REMOTE_IMAGE_FILE
from src.utils.exceptions.custon_exceptions import FileNotFound, AwsAccessDenied, ServiceError
from src.utils.helper.aws_config import s3
import boto3

from src.utils.logs.logger import logger


def download_image_from_s3(s3_url, local_dir):
    #
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc
    directory_prefix = parsed_url.path.strip('/')

    # Get bucket object
    bucket = s3.Bucket(bucket_name)
    try:
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

            # Download file from S3
            bucket.download_file(key, local_path)
            logger.info(f"File downloaded successfully to: {local_path}")
        return local_dir
    except ClientError as e:
        logger.error(f"#### Error downloading image. Error {e} ####")


def create_s3_inference_file(inf: Dict):
    """creating s3 files url for inference"""
    files = []
    for i in range(1, 4):
        files.append(REMOTE_IMAGE_FILE.format(inf['id'],
                                 inf["request_id"], i))

    return files




