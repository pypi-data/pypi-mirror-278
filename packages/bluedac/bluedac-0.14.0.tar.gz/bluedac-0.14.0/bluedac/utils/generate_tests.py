import os
import yaml
import shutil
import bluedac
from bluedac.utils.stack_utils import StackUtils

def generate_unit_tests(project_root: str, stack: str):
    used_resources = []
    patterns = {
        "AWS::Lambda::Function": "lambda",
        "AWS::S3::Bucket": "s3",
        "AWS::DynamoDB::GlobalTable": "dynamo",
        "AWS::DynamoDB::Table": "dynamo"
    }

    # Returns true if at least one of "unit", "integration" or "e2e" test type is already generated.
    if any([os.path.exists(f'{os.getcwd()}/tests/{test_type}')
            for test_type in ["unit", "integration", "e2e"]]):
        print("It seems like some tests have already been generated.")

        if input("Do you want to overwrite them? (y/n): ") == "n":
            return


    # os.system() not really suggested, used to freeze execution until synthesis.
    os.system(f"cdk synth {stack} > synth.yaml")

    # Create tests/ dir if not already existing.
    if not os.path.isdir(f"{project_root}/tests/unit"):
        os.makedirs(f"{project_root}/tests/unit", exist_ok=True)

    # YAML loading
    with open(f'{project_root}/synth.yaml') as synth_file:
        synth = yaml.load(synth_file, Loader=yaml.FullLoader)

    # Check which resources are used in the project
    for res in synth['Resources'].values():
        if res['Type'] in patterns.keys() and patterns[res['Type']] not in used_resources:
            used_resources.append(patterns[res['Type']])

    # ------------------- Copying unit tests. ------------------- #        
    for res in used_resources:
        print(f"{res} used... Tests will be generated.")
        shutil.copytree(f"{os.path.dirname(bluedac.__file__)}/tests/unit/{res}", f"{project_root}/tests/unit/{res}",
                        dirs_exist_ok=True)

def generate_integration_tests(project_root: str):
    # ------------------- Copying integration tests. ------------------- #
    shutil.copytree(f"{os.path.dirname(bluedac.__file__)}/tests/integration", f"{project_root}/tests/integration",
                    dirs_exist_ok=True)

def generate_e2e_tests(project_root: str):
# ------------------- Copying end-to-end tests. ------------------- #
    shutil.copytree(f"{os.path.dirname(bluedac.__file__)}/tests/e2e", f"{project_root}/tests/e2e",
                    dirs_exist_ok=True)

def generate_load_tests(project_root: str, stack: str):

    stack_env = input(f"Load test is being generated for {stack} environment, insert a different one if you want to change it: ")
    
    # Split on '-' char and remove last match (actual environment),
    # then re-join them attaching just inserted stack_env (if inserted). 
    stack = '-'.join(stack.split('-')[:-1])+f'-{stack_env}' if stack_env else stack

    artillery_config = {
        "config": {
            "target": StackUtils.retrieve_apigw_endpoint(stack),
            "plugins": [{
                "apdex": {}
            }, {
                "ensure": {}
            }],
            "ensure": {
                "thresholds": {
                    "conditions": [{
                        "expression": "aggregate.apdex.satisfied > aggregate.apdex.tolerated and aggregate.apdex.frustrated < 0.1 * aggregate.apdex.satisfied"
                    }]
                }
            },
            "phases": [{
                "duration": 0,
                "arrivalRate": 0,
                "rampTo": 0,
                "name": ""
            }]
        },
        "scenarios": [{
            "flow": [{
                "loop": [
                    {
                    "get": {"url": 'INSERT_LAMBDA_URL'}
                }, {
                    "post": {"url": 'INSERT_LAMBDA_URL'}
                }
                ], "count": 0
            }]
        }]
    }

    with open(f"{project_root}/artillery-{stack.split('-')[-1]}.yml", "w") as load_test_file:
        load_test_file.write(yaml.dump(artillery_config))

    print(f"Load test has been generated. You can find it at {project_root}/artillery-{stack}.yml")

def generate_tests(project_root: str, stack: str, test_type: str):

    if test_type == "all":
        generate_unit_tests(project_root, stack)
        generate_integration_tests(project_root)
        generate_e2e_tests(project_root)

        print(f"Tests generated. You can check them at {project_root}/tests/")

    else:
        match test_type:
            case "unit":
                generate_unit_tests(project_root, stack)
            case "integration":
                generate_integration_tests(project_root)
            case "e2e":
                generate_e2e_tests(project_root)
            case _:
                print("Test type incorrect. Available choices: 'unit', 'integration', 'e2e'. Leave blank to generate them all.")