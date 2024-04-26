from io import BytesIO
from typing import Dict

import boto3
from PIL import Image


def upload_img_to_s3(bucket_name, object_name, s3_client, numpy_image):
    """Uploads an image to an S3 bucket"""
    try:
        s3 = boto3.resource(
            's3',
            region_name=REGION,
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_ACCESS_KEY
        )
        img = Image.fromarray(numpy_image).convert('RGB')
        out_img = BytesIO()
        img.save(out_img, format='png')
        out_img.seek(0)
        s3_client.Bucket(bucket_name).put_object(Key=object_name, Body=out_img, ContentType='image/png', ACL='public-read')
    except Exception as e:
        return e
    return True


def making_prompts(train:Dict):
    """Creates prompts for training data"""

    train['class_prompt'] =  f'a photo of {train["class_name"]}'
    train['instance_prompt'] = f'a photo of {train["modifier_token"]} {train["class_name"]}'
    return train