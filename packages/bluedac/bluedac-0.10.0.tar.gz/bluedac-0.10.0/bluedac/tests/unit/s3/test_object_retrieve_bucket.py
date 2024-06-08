import sys
import boto3
from moto import mock_aws

# By default, resources path is project_root/resources. Edit this, if needed. 
sys.path.append("./resources")

from lambda_file import handler

@mock_aws
def test_object_retrieve_bucket():

    s3 = boto3.resource("s3", "us-east-1")
    s3.create_bucket(Bucket="moto-bucket")
    bucket = s3.Bucket("moto-bucket")

    bucket.put_object(
        Key="key",
        Body="val"
    )

    # Fill these, if needed.
    event = {}
    context = {}

    # Object creation
    handler(event, context)

    body = s3.Object("moto-bucket", "key2").get()["Body"]\
        .read().decode("utf-8")

    # Assertions
    assert body == "val"