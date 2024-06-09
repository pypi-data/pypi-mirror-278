import inquirer
import os

from bluedac.utils.save_config import save_config

def init():
    # If user inputs repo name containing '.' or '/', re-ask him another name.
    while True:
        repo_name: str = input("Insert repository name: ")

        if "." in repo_name or "/" in repo_name:
            print("Invalid input. Avoid using '.' or '/' in repository's name.")
        else:
            break

    # -------------------- Language selection -------------------- # 
    languages = [
        inquirer.List(
            "language",
            message="Select project's main programming language:",
            choices=["Python", "Javascript", "Typescript", "Go", "Java", "C#"],
        ),
    ]
    language: str = inquirer.prompt(languages)["language"]

    # C# 'converted' to csharp in CDK init, else the lowercase version of the choice. 
    language = "csharp" if language == "C#" else language.lower()

    # -------------------- Branching strategy selection -------------------- # 
    branching_strategies = [
        inquirer.List(
            "branching_strategy",
            message="What branching strategy do you want to use?",
            choices=["Trunk Based Development", "GitFlow"],
        ),
    ]
    branching_strategy: str = inquirer.prompt(branching_strategies)["branching_strategy"]

    # Name refactoring
    branching_strategy = "tbd" if branching_strategy == "Trunk Based Development" else "gitflow"

    try:
        # Create project directory and cd into it.
        project_dir_path: str = f"{os.getcwd()}/{repo_name}"
        os.mkdir(project_dir_path)
        os.chdir(project_dir_path)
    except FileExistsError:
        print("Error. Directory '$repo_name' already exists.")

    # Launching CDK init command to initialize project structure.
    os.system(f"cdk init app --language {language} 2>/dev/null")

    # Saving BlueDAC configuration to JSON file
    save_config(repo_name, language, branching_strategy)

    # # -------------- Adding dependencies -------------- #
    with open("requirements.txt", "a") as reqs:
        reqs.write("bluedac \n")
        reqs.write("pyyaml \n")
        reqs.write("moto[s3, lambda] \n")
        reqs.write("pytest \n")
        reqs.write("pytest-cov \n")

    print("""
Repository $repo_name initialized with $project_lang as programming language.
Your project's configuration has been defined in $(pwd)/bluedac_config.json.

Next steps:
1. Inspect <project_root>/bluedac_config.json for eventual misconfigurations.
2. 'dac confirm' to confirm your project's configuration.
3. 'source .venv/bin/activate; pip install -r ./requirements.txt' to install dependencies.
4. Write some code.
5. 'dac test --generate' to generate boilerplate tests.
6. 'dac test' to launch tests. Optionally, you can specify the resources to test (e.g. 'dac test buckets').
    
Have fun with your new project! 💻      
    """)
