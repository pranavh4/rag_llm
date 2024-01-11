import yaml


def load_config_file() -> dict:
    with open("./llm_server/resources/config.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return data
