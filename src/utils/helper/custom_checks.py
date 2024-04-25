import os
from urllib.parse import urlparse

from src.utils.exceptions.custon_exceptions import FileNotFound, ServiceError

import boto3
from botocore.exceptions import ClientError
from src.utils.helper.aws_config import s3
from src.utils.logs.logger import logger


def check_s3_file_exists(s3_url):
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc.split('.')[0]
    object_key = parsed_url.path[1:]
    try:
        # Check if the object exists
        s3.head_object(Bucket=bucket_name, Key=object_key)
        logger.info(f"The file '{object_key}' exists in the bucket '{bucket_name}'.")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logger.info(f"The file '{object_key}' does not exist in the bucket '{bucket_name}'.")
            raise FileNotFound(name=s3_url, error_message="file does not exist in the bucket")
        else:
            logger.info(f"An unexpected error occurred: {e}")
            raise ServiceError (name=s3_url, error_message="unexpected error occurred while downloading the file")


def check_aws_credentials():
    pass


def check_model_existence(model_path):
    if os.path.exists(model_path):
        return True
    else:
        raise FileNotFound(name="Inference", error_message="model file not found")
