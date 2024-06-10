endpoints = {
    "GET": [],
    "POST": [],
    "PUT": [],
    "DELETE": [],
    "PATCH": [],
}  # Dictionary of HTTP methods and their corresponding endpoints


def endpoint(method: str = "POST"):
    def endpoint_decorator(func):
        if method not in endpoints:
            raise ValueError(f"Unsupported HTTP method: {method}")
        endpoints[method].append(func)

    return endpoint_decorator
