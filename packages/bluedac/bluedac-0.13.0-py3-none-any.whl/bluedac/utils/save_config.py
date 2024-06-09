import json
import os
import bluedac

def save_config(repo_name, language, branching_strategy):

    envs = [env for env in input("Declare the environments you want in \
your project (separate them with a single space): ").split(' ')]

    release_strategy = {env: {'name': '', 'interval': 0, 'percentage': 0} for env in envs}

    # Initial configuration
    config = {
        'project_name': repo_name,
        'programming_language': language,
        'branching_strategy': branching_strategy,
        'envs': envs,
        'manual_release_envs': [],
        'min_test_coverage': 0,
        'release_strategy': release_strategy
    }

    with open(f"{os.path.dirname(bluedac.__file__)}/templates/{branching_strategy}_pipeline.json") as file:
        config['pipeline'] = json.loads(file.read())

    # Convert and write config dictionary to JSON file
    with open("bluedac_config.json", "w") as json_output:
        json_output.write(json.dumps(config, indent = 4))
