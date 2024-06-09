import os
import yaml
import shutil
import bluedac

def generate_unit_int_tests(project_root: str, stack: str):

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

    # ------------------- Copying integration tests. ------------------- #
    shutil.copytree(f"{os.path.dirname(bluedac.__file__)}/tests/integration", f"{project_root}/tests/integration",
                    dirs_exist_ok=True)

    print(f"Tests generated. You can check them at {project_root}/tests/")