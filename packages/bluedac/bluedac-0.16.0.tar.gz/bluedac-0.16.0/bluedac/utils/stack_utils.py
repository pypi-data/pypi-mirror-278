import json
import boto3

class StackUtils():

    @staticmethod
    def get_rs_info(environment: str):
        """Retrieve informations about release strategy from configuration file. """

        with open("bluedac_config.json", "r") as config:
            release_strategy = json.loads(config.read())["release_strategy"][environment]

        return release_strategy
    
    @staticmethod
    def retrieve_apigw_endpoint(stack):

        try:
            response = boto3\
                .client("cloudformation")\
                .describe_stacks(StackName=stack)
        except Exception:
            raise Exception(f"No stack found with that name. Are you sure {stack} is correct? Remember: you must have deployed it first.")
        
        stack_outputs = response["Stacks"][0]["Outputs"]
        api_endpoint = [output['OutputValue'] for output in stack_outputs if output['OutputValue'].startswith('https://')][0]

        if api_endpoint:
            # Query output is in the format: "https://.../" --> need to strip whitespaces, "" and suffix "/". 
            return api_endpoint.strip().strip("\"").removesuffix("/")     
        else:
            print(f"It seems like something went wrong with {stack} retrieving. You must deploy it first.")
            return "INSERT_APIGW_BASE_URL"