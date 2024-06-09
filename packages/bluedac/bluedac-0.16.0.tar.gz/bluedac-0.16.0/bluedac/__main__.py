import sys

from bluedac.scripts.init import init
from bluedac.utils.test_manager import test_manager
from bluedac.utils.build_pipeline import build_pipeline

def launch_dac():
    if len(sys.argv) == 1:
        print(r"""
        ____    _                  _____                _____
        |  _ \  | |                |  __ \      /\      / ____|
        | |_) | | |  _   _    ___  | |  | |    /  \    | |
        |  _ <  | | | | | |  / _ \ | |  | |   / /\ \   | |
        | |_) | | | | |_| | |  __/ | |__| |  / ____ \  | |____
        |____/  |_|  \__,_|  \___| |_____/  /_/    \_\  \_____|
        """)
        print("Use 'help' to retrieve the set of available commands to BlueDAC framework.")

    else:
        match sys.argv[1]:
            case "help":
                print ("""The following arguments are currently available:
    init: Initialize a new project creating relative git repository and AWS CDK infrastructure.
                    
    tests: Launch a set of tests. Must specify set's name as additional parameter.
    Available names are directories' name in project_root/tests. 
    You could also specify '--generate' without any additional parameters 
    to let BlueDAC generate boilerplate tests for you.
                """)
            case "init":
                init()
                
            case "test":
                test_manager(sys.argv[2:] if len(sys.argv) > 2 else "")
                
            case "confirm":
                build_pipeline()
                
            case _:
                print("error: unrecognized argument.")

if __name__ == "__main__":
    launch_dac()