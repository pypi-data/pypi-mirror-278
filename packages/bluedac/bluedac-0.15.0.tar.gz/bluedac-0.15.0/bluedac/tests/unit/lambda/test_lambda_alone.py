import sys
from moto import mock_aws

# By default, resources path is project_root/resources. Edit this, if needed. 
sys.path.append("./resources")

from lambda_file import handler

@mock_aws
def test_lambda_alone():

    # Fill these, if needed.
    event = {}
    context = {}
    
    lambda_response = handler(event, context)

    # Assertions
    assert lambda_response["param"] == "expected_value"