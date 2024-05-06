import base64
import os
from urllib.parse import urlparse

from src.utils.exceptions.custon_exceptions import FileNotFound, ServiceError, MlBaseApiError

import boto3
from botocore.exceptions import ClientError
from src.utils.helper.aws_config import s3_client
from src.utils.logs.logger import logger


def check_s3_file_exists(s3_url):
    s3 = s3_client
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc.split('.')[0]
    object_key = parsed_url.path[1:]
    try:
        # Check if the object exists
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=object_key)
        if response.get('Contents'):
            logger.info(f"The file '{object_key}' exists in the bucket '{bucket_name}'.")
            return True
        else:
            logger.info(f"The file '{object_key}' does not exist in the bucket '{bucket_name}'.")
            return False
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        raise ServiceError(name=s3_url, error_message="unexpected error occurred while downloading the file")


def check_aws_credentials():
    pass


def check_model_existence(model_path):
    if os.path.exists(model_path):
        return True
    else:
        raise FileNotFound(name="Inference", error_message="model file not found")


async def decode_verification_key(encoded):
    try:
        text = base64.b64decode(encoded).decode()

        if text != "rekoGnizTechnologiesPriVaTeLiMeted###1234096896":
            raise ServiceError(name="authentication_failed",
                               error_message="verification key verification failed"
                               )
    except Exception as e:
        raise ServiceError(name="authentication_failed",
                           error_message="provided value is not base64"
                           )


def decode_verification_key_sync(encoded):
    try:
        text = base64.b64decode(encoded).decode()

        if text != "rekoGnizTechnologiesPriVaTeLiMeted###1234096896":
            raise ServiceError(name="authentication_failed",
                               error_message="verification key verification failed"
                               )
    except Exception as e:
        raise ServiceError(name="authentication_failed",
                           error_message="provided value is not base64"
                           )
