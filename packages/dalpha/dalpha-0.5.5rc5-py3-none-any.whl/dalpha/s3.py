import io
import os
import time
import requests
import boto3
from dalpha.logging import logger
from dalpha.logging.events import Event

s3_client = boto3.client('s3')

def download_from_url(url):
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise Exception(f"can't download from url {r.status_code} : {r.text}")
    else:
        return io.BytesIO(r.content)

def download_from_s3(bucket, key, download_path):
    try:
        s3_client.download_file(bucket, key, download_path)
    except Exception as e:
        raise Exception(f"failed to download from s3\n{e}")
    
def upload_s3(upload_path, bucket, key = None, account_id = None):
    if key is None and account_id is not None:
        if not isinstance(account_id, int): raise TypeError('account_id is not a int')
        key = f"channel_id={account_id}/{time.strftime('y=%Y/m=%m/d=%d', time.localtime(time.time()))}/{os.path.basename(upload_path)}"
    try:
        s3_client.upload_file(upload_path, bucket, key)
        logger.info(
            message = f"uploaded to s3://{bucket}/{key}",
            event = Event.UPLOAD_S3,
        )
        return os.path.join(f"https://{bucket}.s3.ap-northeast-2.amazonaws.com", key)
    except Exception as e:
        raise Exception(f"failed to upload s3\n{e}")

def upload_s3_image(pil_image, bucket, img_save_name = None, key = None, account_id = None):
    '''
    pil_image : PIL.Image
    bucket : S3에 업로드할 버킷 이름
    img_save_name : S3에 저장될 이미지 파일 이름
    key : S3에 저장될 이미지 파일 경로
    account_id : S3에 저장될 이미지 파일 경로에 포함될 account_id
    '''
    img_byte_arr = io.BytesIO()
    if img_save_name is None and key is None:
        raise ValueError("img_save_name or key is required")
    if img_save_name is not None:
        if not isinstance(account_id, int): raise TypeError('account_id is not a int')
        output_file_extension = img_save_name.split('.')[-1]
        key = f"channel_id={account_id}/{time.strftime('y=%Y/m=%m/d=%d', time.localtime(time.time()))}/{img_save_name}"
    else:
        output_file_extension = key.split('.')[-1]
    
    pil_image.save(img_byte_arr, format=str(output_file_extension).upper())
    img_byte_arr = img_byte_arr.getvalue()
    
    try:
        s3_client.put_object(Body=img_byte_arr, Bucket=bucket, Key=key)
        logger.info(
            message = f"uploaded to s3://{bucket}/{key}",
            event = Event.UPLOAD_S3,
        )
        return os.path.join(f"https://{bucket}.s3.ap-northeast-2.amazonaws.com", key)
    except Exception as e:
        raise Exception(f"failed to upload s3\n{e}")
