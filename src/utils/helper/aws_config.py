import boto3
from src.utils.constants.properties import REGION, keys


s3 = boto3.resource(
            's3',
            region_name=REGION,
            aws_access_key_id=keys["ACCESS_KEY_ID"],
            aws_secret_access_key=keys["SECRET_ACCESS_KEY"]
        )

s3_client = boto3.client("s3",
            region_name=REGION,
            aws_access_key_id=keys["ACCESS_KEY_ID"],
            aws_secret_access_key=keys["SECRET_ACCESS_KEY"]
                         )