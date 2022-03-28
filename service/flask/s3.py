from os import environ as environment
from os import path
from threading import Lock
import sys
import string
import secrets
# from datetime import datetime
from botocore.exceptions import ClientError
import boto3
from boto3.s3.transfer import TransferConfig

S3_ENDPOINT = environment.get('S3_ENDPOINT',
                              'http://s3bucket.resources.noop.desktop:9000')
S3_BUCKET = environment.get('S3_BUCKET')
AWS_REGION = environment.get('AWS_REGION', 'us-west-2')
DYNAMODB_ENDPOINT = environment.get(
    'DYNAMODB_ENDPOINT', 'http://dynamodbtable.resources.noop.desktop:8000')
DYNAMODB_TABLE = environment.get('DYNAMODB_TABLE', 'DynamoDBTable')

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(path.getsize(filename)) if path.exists(filename) else 0
        self._seen_so_far = 0
        self._lock = Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

s3 = boto3.resource('s3',
    endpoint_url=S3_ENDPOINT,
    region_name=AWS_REGION
)

transfer = TransferConfig(
    multipart_threshold=1024 * 25,
    max_concurrency=10,
    multipart_chunksize=1024 * 25,
    use_threads=True
)

def list_objects():
    return [
        i.key for i in s3.Bucket(S3_BUCKET).objects.all()
    ]

def list_key_objects(key):
    return [
        i.key for i in s3.Bucket(S3_BUCKET).objects.filter(Prefix=f"{key}/")
    ]

def download_object(key, destination):
    try:
        result = s3.Bucket(S3_BUCKET).download_file(
            key,
            destination,
            Config=transfer,
            Callback=ProgressPercentage(destination)
        )
        if path.exists(destination):
            return {
                'path': destination
            }
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return e
        else:
            raise

def get_object(key):
    try:
        object = s3.Object(S3_BUCKET, key).get()
        return object.get('Body', None).read()
    except ClientError as e:
        return e

def upload_object(key, source):
    try:
        s3.Object(S3_BUCKET, key).upload_file(
            source,
            Config=transfer,
            Callback=ProgressPercentage(source)
        )
        return key
    except ClientError as e:
        return e

def delete_object(key):
    try:
        result = s3.Object(S3_BUCKET, key).delete()
        return result
    except ClientError as e:
        return e
