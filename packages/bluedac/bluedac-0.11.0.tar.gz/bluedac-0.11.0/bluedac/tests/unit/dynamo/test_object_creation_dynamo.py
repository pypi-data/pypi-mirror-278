import sys
import boto3
from moto import mock_aws

# By default, resources path is project_root/resources. Edit this, if needed. 
sys.path.append("./resources")

# Customize with your data.
from lambda_file import handler

@mock_aws
def test_object_creation_dynamo():
    dynamo = boto3.resource("dynamodb", "us-east-1")

    # Create the DynamoDB table
    dynamo.create_table(
        TableName='moto-dynamo',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'surname',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'surname',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    event = {}
    context = {}

    # Item creation
    handler(event, context)

    table = dynamo.Table("moto-dynamo")
    item = table.get_item(
        Key={
            "name": "John",
            "surname": "Doe"
        }
    )

    assert item["Item"]["name"] == "John"