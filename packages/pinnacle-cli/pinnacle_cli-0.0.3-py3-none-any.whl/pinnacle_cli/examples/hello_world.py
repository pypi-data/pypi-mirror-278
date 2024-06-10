from pinnacle_python import endpoint


@endpoint(method="GET")
def hello_world():
    return "Hello World"
