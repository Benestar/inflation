import csv
import functools
import json
from pathlib import Path

import requests


class Genesis:
    """
    Client for the Genesis REST api.
    """

    def __init__(self, base_url: str, data_dir: str, username: str, password: str):
        self.base_url = base_url
        self.data_dir = Path(data_dir)
        self.username = username
        self.password = password

    def get_request(self, path: str, params: dict = {}):
        params["username"] = self.username
        params["password"] = self.password
        res = requests.get(
            f"{self.base_url}/{path}",
            params=params
        )
        res.raise_for_status()
        return res.json()

    def get_data_table(self, name: str, params: dict = {}):
        params["name"] = name
        res = self.get_request("data/table", params=params)
        csv_str = res["Object"]["Content"]
        return list(csv.reader(csv_str.splitlines(), delimiter=";"))

    def data_table(self, name: str, params: dict = {}):
        def decorator(fn):
            @functools.wraps(fn)
            def wrapper():
                data = fn(self.get_data_table(name, params))
                self.data_dir.mkdir(parents=True, exist_ok=True)
                with open(self.data_dir / f"data-table-{name}.json", "w") as f:
                    json.dump(list(data), f, indent=2)
                return data
            return wrapper
        return decorator
