from pathlib import Path

from functools import wraps

from whiffle_client.io import load_yaml_with_include


def load_data(class_type, resource_type=None):
    def wrap(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            data = kwargs.get("data", None)
            if isinstance(data, str) or isinstance(data, Path):
                data = load_yaml_with_include(data, relative_to_file=True)
                data = class_type.from_dict(data)
            elif isinstance(data, dict):
                # Data directly provided as dict
                data = class_type.from_dict(data)
            if data:
                kwargs["data"] = data._get_api_params()
            else:
                raise ValueError("Please provide valid data or path to valid data")
            return func(self, *args, **kwargs)

        return wrapper

    return wrap


def request_ok(func):
    def wrapper(self, *args, **kwargs):
        request = func(self, *args, **kwargs)
        try:
            request.raise_for_status()
            return request
        except Exception:
            raise ValueError(request.json())

    return wrapper
