import json
import pkg_resources
import platformdirs
import yaml
import os

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from whiffle_client.decorators import request_ok


class BaseClient:
    """
    Base class client to connect to Whiffle APIs
    """

    # API variables
    ENDPOINTS_URL: str = ""

    CONFIG_FILE_NAME = "whiffle_config.yaml"
    CONFIG_FILE_PATH_LOCATIONS = [
        f"{platformdirs.user_config_dir('whiffle')}/{CONFIG_FILE_NAME}",  # app path
        f"{CONFIG_FILE_NAME}",  # workdir path
        pkg_resources.resource_filename(
            "whiffle_client", f"resources/{CONFIG_FILE_NAME}"
        ),  # package resource path
    ]

    # Type method
    def __init__(self, access_token=None, url=None, session=None):
        """
        Initialize the client.

        Authentication order:
        1. `access_token` passed when creating class.
        2. token in CONFIG_FILE_PATH_LOCATIONS (JSON format)

        Parameters
        ----------
        access_token : str, optional
            Token for client session auth
        url : str, optional
            Url pointing to API
        """

        if access_token is None:
            config = self.get_config()
            access_token = config["user"]["token"]
        if url is None:
            config = self.get_config()
            url = config["whiffle"]["url"]
        self.server_url = url

        if session is None:
            # More docs: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.Retry
            status_forcelist = (500, 502, 503, 504)
            retry = Retry(
                total=5,  # Total number of retries to allow
                backoff_factor=0.1,  # Incremental time between retry requests
                status_forcelist=status_forcelist,  # A set of integer HTTP status codes that will force a retry on
            )
            adapter = HTTPAdapter(max_retries=retry)
            session = requests.Session()
            session.mount("http://", adapter)
            session.mount("https://", adapter)
        self.session = session

        self.session.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

    def __repr__(self) -> str:
        return f"Whiffle wind client connected to url: {self.server_url}"

    @staticmethod
    def get_config():
        """Gathers client configuration from resources or from user config directory.

        Returns
        -------
        dict
            Dictionary containing the configuration.

        Raises
        ------
        FileNotFoundError
            Raises error if no configuration found
        """
        config = None
        for file_path in BaseClient.CONFIG_FILE_PATH_LOCATIONS:
            try:
                with open(file_path) as file_object:
                    config = yaml.safe_load(file_object)
                if config:
                    break
            except FileNotFoundError:
                continue
        else:
            raise FileNotFoundError(
                f"No valid config found on either of {BaseClient.CONFIG_FILE_PATH_LOCATIONS} locations"
            )

        return config

    @staticmethod
    def set_config(config):
        config_file_path = BaseClient.CONFIG_FILE_PATH_LOCATIONS[0]
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
        with open(config_file_path, "w") as file_object:
            yaml.safe_dump(config, file_object)

    @request_ok
    def get_request(self, url):
        return self.session.get(url)

    @request_ok
    def post_request(self, url, data=None):
        return self.session.post(url, data=json.dumps(data))

    @request_ok
    def put_request(self, url, data=None):
        return self.session.put(url, data=json.dumps(data))

    @request_ok
    def delete_request(self, url):
        return self.session.delete(url)
