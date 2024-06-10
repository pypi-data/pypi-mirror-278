from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pinnacle_cli.constants import DIRECTORY
import json

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_py_openapi_schema() -> Dict[str, Any]:
    openapi_file_path = f"{DIRECTORY}/.metadata/py_openapi.json"
    with open(openapi_file_path, "r") as file:
        py_openapi_dict = json.load(file)

    return py_openapi_dict


py_openapi_schema = create_py_openapi_schema()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    app.openapi_schema = py_openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore (see https://github.com/tiangolo/fastapi/issues/3745)
