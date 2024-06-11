# sndid/list.py
"""
list.py

Copyright 2023, 2024 Jeff Moe <moe@spacecruft.org>
Copyright 2022, 2023, Joe Weiss <joe.weiss@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

https://joeweiss.github.io/birdnetlib/utility-classes/
"""
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from birdnetlib.species import SpeciesList
from datetime import datetime
from datetime import date
import argparse
from contextlib import redirect_stdout, redirect_stderr
import io


def main():
    TODAY = date.today()
    YEAR = TODAY.year
    MONTH = TODAY.month
    DAY = TODAY.day

    parser = argparse.ArgumentParser(description="Run sndid-list")
    parser.add_argument(
        "-t",
        "--latitude",
        help="Latitude (default 40.57)",
        type=str,
        required=False,
        default="40.57",
    )
    parser.add_argument(
        "-n",
        "--longitude",
        help="Longitude (default -105.23)",
        type=str,
        required=False,
        default="-105.23",
    )
    parser.add_argument(
        "-y",
        "--year",
        help="Year (default today)",
        type=int,
        required=False,
        default=YEAR,
    )
    parser.add_argument(
        "-m",
        "--month",
        help="Month (default today)",
        type=int,
        required=False,
        default=MONTH,
    )
    parser.add_argument(
        "-d",
        "--day",
        help="Day (default today)",
        type=int,
        required=False,
        default=DAY,
    )
    parser.add_argument(
        "-g",
        "--geo",
        help="Limit list by geocoordinates (default False)",
        action=argparse.BooleanOptionalAction,
        type=bool,
        required=False,
        default=False,
    )
    parser.add_argument(
        "-c",
        "--cal",
        help="Limit list by calendar date (default False, use with --geo)",
        action=argparse.BooleanOptionalAction,
        type=bool,
        required=False,
        default=False,
    )

    args = parser.parse_args()
    YEAR = args.year
    MONTH = args.month
    DAY = args.day
    LAT = args.latitude
    LON = args.longitude
    GEO = args.geo
    CAL = args.cal

    f = io.StringIO()
    with redirect_stdout(f), redirect_stderr(f):
        species_local = SpeciesList()

    if CAL:
        DATE = datetime(year=YEAR, month=MONTH, day=DAY)
    else:
        DATE = ""

    if GEO:
        with redirect_stdout(f), redirect_stderr(f):
            species_list = species_local.return_list(lat=LAT, lon=LON, date=DATE)
    else:
        with redirect_stdout(f), redirect_stderr(f):
            species_list = species_local.return_list(date=DATE)

    i = 0
    species_sort = ""
    for i in range(0, len(species_list)):
        species_sort = species_sort + (
            species_list[i]["common_name"]
            + ", "
            + species_list[i]["scientific_name"]
            + "\n"
        )
    species_out = sorted(species_sort.split("\n"))

    i = 0
    for i in range(1, len(species_out)):
        print(species_out[i])


if __name__ == "__main__":
    main()
