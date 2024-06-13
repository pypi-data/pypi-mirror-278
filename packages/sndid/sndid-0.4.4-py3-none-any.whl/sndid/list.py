# sndid/list.py
# Copyright 2023, 2024 Jeff Moe <moe@spacecruft.org>
# Copyright 2022, 2023, Joe Weiss <joe.weiss@gmail.com>
# Licensed under the Apache License, Version 2.0

import argparse
import os
from birdnetlib.species import SpeciesList
from contextlib import redirect_stdout, redirect_stderr
from datetime import date

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def parse_arguments():
    today = date.today()
    parser = argparse.ArgumentParser(
        description="sndid-list -- List available species. By default return all. Limit list with date and location options."
    )
    parser.add_argument(
        "-a", "--latitude", help="Latitude (default 40.57)", type=str, default="40.57"
    )
    parser.add_argument(
        "-o",
        "--longitude",
        help="Longitude (default -105.23)",
        type=str,
        default="-105.23",
    )
    parser.add_argument(
        "-y", "--year", help="Year (default today)", type=int, default=today.year
    )
    parser.add_argument(
        "-m", "--month", help="Month (default today)", type=int, default=today.month
    )
    parser.add_argument(
        "-d", "--day", help="Day (default today)", type=int, default=today.day
    )
    parser.add_argument(
        "-t",
        "--threshold",
        help="Threshold value for species list (default 0.0)",
        type=float,
        default=0.0,
    )
    return parser.parse_args()


def get_species_list(args):
    species_local = SpeciesList()

    date_obj = (
        date(year=args.year, month=args.month, day=args.day)
        if args.year and args.month and args.day
        else None
    )
    lat = float(args.latitude) if args.latitude else None
    lon = float(args.longitude) if args.longitude else None

    filtered_species_list = species_local.return_list(
        lat=lat, lon=lon, date=date_obj, threshold=args.threshold
    )

    return filtered_species_list


def format_species_list(species_list):
    return sorted(
        f"{species['common_name']}, {species['scientific_name']}"
        for species in species_list
    )


def main():
    args = parse_arguments()

    with open(os.devnull, "w") as devnull:
        with redirect_stdout(devnull), redirect_stderr(devnull):
            species_list = get_species_list(args)

    species_out = format_species_list(species_list)

    for species in species_out:
        print(species)


if __name__ == "__main__":
    main()
