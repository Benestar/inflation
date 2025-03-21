import json
import os
from typing import Optional

from genesis import Genesis

with open("config.json", "r") as f:
    config = json.load(f)

env = {}

with open(".env", "r") as f:
    for line in f.readlines():
        [key, value] = line.split("=", 1)
        env[key] = value

config["username"] = os.getenv("GENESIS_USERNAME", env.get("GENESIS_USERNAME", "GAST"))
config["password"] = os.getenv("GENESIS_PASSWORD", env.get("GENESIS_PASSWORD", "GAST"))

gen = Genesis(**config)


def parse_float(s: str) -> Optional[float]:
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


def parse_month(s: str) -> str:
    return {
        "Januar": "01",
        "Februar": "02",
        "März": "03",
        "April": "04",
        "Mai": "05",
        "Juni": "06",
        "Juli": "07",
        "August": "08",
        "September": "09",
        "Oktober": "10",
        "November": "11",
        "Dezember": "12"
    }.get(s, "00")


def parse_quarter(s: str) -> str:
    return {
        "1. Quartal": "03",
        "2. Quartal": "06",
        "3. Quartal": "09",
        "4. Quartal": "12"
    }.get(s, "00")



@gen.data_table(name="61111-0002", params={"startyear": 1990})
def download_inflation_and_price(data):
    for year, month, price, prev_year, prev_month in data[6:-4]:
        yield [
            year + "-" + parse_month(month) + "-01T00:00:00Z",
            parse_float(price),
            parse_float(prev_year),
            parse_float(prev_month)
        ]


foo = "62221-0002_560361075"

@gen.data_table(name="62221-0002", params={"startyear": 1990})
def download_union_wages(data):
    for sector_id, sector, year, quarter, h_wage, h_wage_extra, m_wage, m_wage_extra, work_time, abs_work_time in data[7:-3]:
        yield [
            year + "-" + parse_quarter(quarter) + "-01T00:00:00Z",
            parse_float(m_wage),
            parse_float(abs_work_time),
            sector
        ]


if __name__ == "__main__":
    download_inflation_and_price()
    download_union_wages()
