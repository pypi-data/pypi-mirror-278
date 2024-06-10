import dotenv
from pinnacle_cli.constants import env_path


def write_or_update_pinnacle_env(key: str, value: str):
    dotenv.set_key(env_path, key, value)
