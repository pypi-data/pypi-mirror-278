import os
import json
from mitmproxy import http
from pinnacle_cli.constants import (
    HOST,
    PORT,
    PYTHON_PORT,
    DIRECTORY,
    OPENAPI_PORT,
)

METADATA_DIR = os.path.join(os.getenv("PINNACLE_CWD") or "", DIRECTORY, ".metadata")
SERVER_PORTS = {"py": PYTHON_PORT, "openapi": OPENAPI_PORT}


def load_endpoints():
    """
    Load the endpoints from the metadata directory (./.metadata/py_endpoints.json and ./.metadata/js_endpoints.json)

    Returns:
    endpoints: dict - The endpoints for the Python and JavaScript servers in the following format:
        {
            "py": {
                "endpoint_name": "HTTP_METHOD"
            },
            "js": {
                "endpoint_name": ""
            }
        }
    """
    endpoints = {"py": {}, "js": {}}
    with open(f"{METADATA_DIR}/py_endpoints.json", "r") as f:
        endpoints["py"] = json.load(f)
    print(f"See your endpoints here: http://{HOST}:{PORT}/pinnacle/api_docs")

    if endpoints["py"].keys():
        print("Available Python endpoints:")
        for route_name, http_method in endpoints["py"].items():
            print(f"{http_method}: http://{HOST}:{PORT}/{route_name}")

    return endpoints


def request(flow: http.HTTPFlow):
    endpoints = load_endpoints()
    pathname = flow.request.path.replace("/", "", 1)

    if "?" in pathname:
        pathname = pathname.split("?")[0]

    if pathname == "favicon.ico":
        return
    elif pathname == "pinnacle/api_docs":
        flow.request.host = HOST
        flow.request.port = SERVER_PORTS["openapi"]
        flow.request.path = "/docs"
    elif pathname == "openapi.json":
        flow.request.host = HOST
        flow.request.port = SERVER_PORTS["openapi"]
    elif pathname in endpoints["py"]:
        flow.request.host = HOST
        flow.request.port = SERVER_PORTS["py"]
    else:
        raise ValueError(f"Endpoint not found: {flow.request.path}")


load_endpoints()
