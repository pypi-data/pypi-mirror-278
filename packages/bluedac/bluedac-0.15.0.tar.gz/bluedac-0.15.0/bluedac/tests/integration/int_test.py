import sys

# By default, resources path is project_root/resources. Edit this, if needed. 
sys.path.append("./resources")

from lambda_file import handler

def integration_test():

    # Fill these, if needed.
    event = {}
    context = {}
    
    integration_response = handler(event, context)

    # Assertions
    assert integration_response["param"] == "expected_value"