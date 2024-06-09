from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as AWS_Lambda
)

class Bluedac_APIGW(apigateway.RestApi):
    """ BlueDAC adapted version of aws_apigateway's RestApi, with some high-level methods. """

    def __init__(self, stack, api_gw_name):
        super().__init__(stack, api_gw_name)

    def bind_lambda(self, lambda_fun: AWS_Lambda.Function, method_type: str, end_point: str):
        """ Binding this lambda fun to https://apigateway.url/end_point with specified method_type. """

        endpoint = self.root.add_resource(end_point)
        endpoint.add_method(method_type, apigateway.LambdaIntegration(lambda_fun))