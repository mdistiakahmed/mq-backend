import os
import yaml


CONFIG_PATH = "config_local.yaml"


def get_config() -> dict:
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), CONFIG_PATH
    )

    with open(file_path, "rt", encoding="utf-8") as file:
        return yaml.load(file, Loader=yaml.FullLoader)


class _Config:

    # DATABASE CONFIG
    @property
    def db_host(self):
        return get_config()["db_config"]["host"]

    @property
    def db_port(self):
        return get_config()["db_config"]["port"]

    @property
    def db_username(self):
        return get_config()["db_config"]["username"]

    @property
    def db_password(self):
        return get_config()["db_config"]["password"]

    @property
    def db_schema(self):
        return get_config()["db_config"]["schema"]

    @property
    def db_name(self):
        return get_config()["db_config"]["db_name"]


CONFIG = _Config()
