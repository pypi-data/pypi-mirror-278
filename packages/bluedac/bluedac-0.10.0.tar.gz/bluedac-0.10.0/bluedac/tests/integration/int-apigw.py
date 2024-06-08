import os
import boto3
import requests

"""
Before running the test, ensure to set project stack name 
(without specific environment naming).
"""
project_stack_name = ""
stack_name: str = project_stack_name + os.environ['INT_TEST_STACK']

""" Change the lambda function API path accordingly. """
lambda_api_path = "example"

""" Client used to scrape stack resources and get API-GW endpoint URL. """
client = boto3.client("cloudformation")

try:
    response = client.describe_stacks(StackName=stack_name)
except Exception:
    raise Exception('No stack found with that name. Check INT_TEST_STACK for additional informations.')

stack_outputs = response["Stacks"][0]["Outputs"]

""" OutputValue contains API Gateway endpoint URL """
api_endpoint = [output['OutputValue'] for output in stack_outputs if output['OutputValue'].startswith('https://')][0]

response = requests.post(api_endpoint + lambda_api_path)

assert response.text == 'expected_param'
assert response.status_code == '200'