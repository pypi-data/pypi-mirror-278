import json

class StackUtils():

    @staticmethod
    def get_rs_info(environment: str):
        """Retrieve informations about release strategy from configuration file. """

        with open("bluedac_config.json", "r") as config:
            release_strategy = json.loads(config.read())["release_strategy"][environment]

        return release_strategy