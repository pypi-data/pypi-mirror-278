import sys
import boto3
from moto import mock_aws

# By default, resources path is project_root/resources. Edit this, if needed. 
sys.path.append("./resources")

# Customize with your data.
from lambda_file import handler

@mock_aws
def test_object_retrieve_dynamo():
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

    table = dynamo.Table("moto-dynamo")

    table.put_item(
        Item={
            "name": "John",
            "surname": "Doe"
        }
    )

    event = {}
    context = {}

    lambda_response = handler(event, context)

    assert lambda_response["body"]["Item"]["name"] == "John"
