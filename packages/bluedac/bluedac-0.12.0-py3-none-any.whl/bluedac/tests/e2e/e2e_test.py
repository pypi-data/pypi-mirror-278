import boto3
import requests

"""
Before running the test, ensure to have set project stack name 
(WITH specific environment naming).
"""
stack_name = "INSERT_STACK_NAME"

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

""" Use requests library to make calls and retrieve responses. """
response = requests.post(api_endpoint + lambda_api_path)

""" Define here your assertions. """
assert response.text == 'expected_param'
assert response.status_code == '200'