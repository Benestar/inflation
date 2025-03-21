import csv
import functools
import json
import time
from pathlib import Path

import requests


class GenesisNotFound(Exception):
    """
    Exception if the resource could not be found.
    """


class GenesisJobRequired(Exception):
    """
    Exception if a job is required to download a dataset.
    """

    def __init__(self, msg: str):
        self.job_name = msg.split(" ")[-1]


class Genesis:
    """
    Client for the Genesis REST api.
    """

    def __init__(self, base_url: str, data_dir: str, username: str, password: str):
        self.base_url = base_url
        self.data_dir = Path(data_dir)
        self.username = username
        self.password = password

    def _get_request(self, path: str, params: dict = {}):
        params["username"] = self.username
        params["password"] = self.password
        res = requests.get(
            f"{self.base_url}/{path}",
            params=params
        )
        res.raise_for_status()
        return res.json()

    def _get_csv_data(self, path: str, params: dict = {}):
        res = self._get_request(path, params=params)

        if res["Status"]["Code"] == 0:
            csv_str = res["Object"]["Content"]
            return list(csv.reader(csv_str.splitlines(), delimiter=";"))

        if res["Status"]["Code"] == 99:
            raise GenesisJobRequired(res["Status"]["Content"])

        if res["Status"]["Code"] == 104:
            raise GenesisNotFound()

        raise Exception(res["Status"])

    def get_data_result(self, name: str):
        for _ in range(100):
            time.sleep(5)
            try:
                return self._get_csv_data("data/result", {"name": name})
            except GenesisNotFound:
                pass

        raise GenesisNotFound()

    def get_data_table(self, name: str, params: dict = {}):
        try:
            print(f"Download data table: {name}")
            return self._get_csv_data("data/table", {**params, "name": name, "job": True})
        except GenesisJobRequired as e:
            print(f"Download job result: {e.job_name}")
            return self.get_data_result(e.job_name)

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
