import os
from dotenv import load_dotenv, find_dotenv

cwd = os.getcwd()
env_path = os.path.join(cwd, ".env")
found_dotenv = find_dotenv(env_path)
if found_dotenv:
    load_dotenv(env_path, override=True)

HOST = os.getenv("PINNACLE_HOST", default="localhost")
PORT = int(os.getenv("PINNACLE_PORT", default=8000))
if not (0 <= PORT <= 65535):
    raise ValueError("The provided port number is outside the valid range (0-65535).")
DIRECTORY = os.getenv("PINNACLE_DIRECTORY", default="./pinnacle")
OPENAPI_PORT = int(PORT - 1)
PYTHON_PORT = int(PORT + 1)
