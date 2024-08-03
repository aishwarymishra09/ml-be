import os
from io import BytesIO
from typing import Dict
from urllib.parse import urlparse
from botocore.exceptions import ClientError
from src.utils.constants.properties import REMOTE_IMAGE_FILE
from src.utils.exceptions.custon_exceptions import FileNotFound, AwsAccessDenied, ServiceError
from src.utils.helper.aws_config import s3, s3_client
import boto3
from src.utils.logs.logger import logger


def download_image_from_s3(s3_url, local_dir):
    #
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc
    directory_prefix = parsed_url.path.strip('/')
    files = []
    # Get bucket object
    bucket = s3.Bucket(bucket_name)
    try:
        # List objects in the specified directory
        for obj in bucket.objects.filter(Prefix=directory_prefix):
            key = obj.key
            file_name = os.path.basename(key)
            local_path = os.path.join(local_dir, file_name)
            files.append(local_path)
            # Skip directories
            if not file_name:
                continue

            # Create directories if they don't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # Download file from S3
            bucket.download_file(key, local_path)
            logger.info(f"File downloaded successfully to: {local_path}")
        return local_dir, files
    except ClientError as e:
        logger.error(f"#### Error downloading image. Error {e} ####")


def create_s3_inference_file(inf: Dict):
    """creating s3 files url for inference"""
    files = []
    for i in range(1, 4):
        files.append(REMOTE_IMAGE_FILE.format(inf['id'],
                                 inf["request_id"], i))

    return files



def download_s3_file(s3_url, local_path):
    """This function is used to download s3 file from s3_url"""
    # Define the bucket name and file key
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc
    file_key = parsed_url.path.lstrip('/')
    local_file_path = local_path

    # Download the file
    try:
        s3_client.download_file(bucket_name, file_key, local_file_path)
        print("File downloaded successfully.")
        return local_file_path
    except Exception as e:
        print(f"Failed to download the file: {str(e)}")


def save_image(image, path):
    """Uploads an image to an S3 bucket"""
    try:
        s3 = s3_client
        out_img = BytesIO()
        image.save(out_img, format='png')
        out_img.seek(0)
        s3.upload_fileobj(out_img, "rekogniz-training-data", path,
                          ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read', 'ContentDisposition': 'inline'})

    except Exception as e:
        return e
    return True
