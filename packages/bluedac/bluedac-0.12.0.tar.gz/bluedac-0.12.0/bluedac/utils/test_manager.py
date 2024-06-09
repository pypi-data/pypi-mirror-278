import os
import subprocess
import json
from bluedac.utils.generate_unit_int_tests import generate_unit_int_tests
from bluedac.utils.generate_load_tests import generate_load_tests

def test_manager(argument: list):
    try:
        with open(f"{os.getcwd()}/bluedac_config.json", "r") as config:
            json_config = json.loads(config.read())
            coverage = json_config["min_test_coverage"]
    except:
        print("Coverage not specified in configuration file. It has been set to 0.")
        coverage = 0

    # Three different stacks, since they're the same we're gonna choose first one (testing, probably).
    if argument and argument[0] == '--generate':
        if os.path.exists(f'{os.getcwd()}/cdk.json'):

            # Scrape of 'cdk ls' output, choosing first elem of list results in 'testing' stack.
            cdk_ls_process = subprocess.run(["cdk", "ls"], capture_output=True) 
            stack = [stack for stack in cdk_ls_process.stdout.decode("ascii").split("\n")][0]
        else:
            print("An error occurred. You must be in your project's root directory.")
            exit()

        if len(argument) > 1:
            match argument[1]:
                case "unit":
                    generate_unit_int_tests(os.getcwd(), stack)
                case "load":
                    generate_load_tests(os.getcwd(), stack)                            
        else:
            generate_unit_int_tests(os.getcwd(), stack)
            generate_load_tests(os.getcwd(), stack)

    # There's at least a parameter (user specified a type of test)
    elif argument:
        subprocess.run(["python", "-m", "pytest",
                        f"--cov-fail-under={coverage}" if argument[0] == "unit" else "", 
                        "--cov=./resources", 
                        f"tests/{argument[0]}/"])
    else:
        subprocess.run(["python", "-m", "pytest",
                        f"--cov-fail-under={coverage}", 
                        "--cov=./resources",
                        "tests/"])