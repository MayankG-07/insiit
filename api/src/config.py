import json


def get_api_config():
    with open(r"../api-config.json", "r") as config_file:
        config = json.load(config_file)
    return config


api_config = get_api_config()
