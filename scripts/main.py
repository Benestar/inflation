import json
import os
from typing import Optional

from genesis import Genesis

with open("config.json", "r") as f:
    config = json.load(f)

config["username"] = os.getenv("GENESIS_USERNAME", "GAST")
config["password"] = os.getenv("GENESIS_PASSWORD", "GAST")

gen = Genesis(**config)


def parse_float(s: str) -> Optional[float]:
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


@gen.data_table(name="61111-0002", params={"startyear": 1990})
def download_inflation_prev_year(data):
    for year, month, price, prev_year, prev_month in data[6:-4]:
        yield {
            "label": month + " " + year,
            "price": parse_float(price),
            "prev_year": parse_float(prev_year),
            "prev_month": parse_float(prev_month)
        }


if __name__ == "__main__":
    download_inflation_prev_year()
