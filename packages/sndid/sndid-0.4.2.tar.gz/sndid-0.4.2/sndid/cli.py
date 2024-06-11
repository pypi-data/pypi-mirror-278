# sndid/cli.py
"""
cli.py

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

https://joeweiss.github.io/birdnetlib/getting-started/
"""


import argparse
import io
import os
import sys
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, date


def parse_args():
    TODAY = date.today()
    YEAR = TODAY.year
    MONTH = TODAY.month
    DAY = TODAY.day

    parser = argparse.ArgumentParser(
        description="Run sndid to identify bird species in audio recordings."
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Input filename to process (default samples/sample.wav)",
        type=str,
        required=False,
        default="samples/sample.wav",
    )
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
        "-c",
        "--confidence",
        help="Minimum Confidence (default 0.50)",
        type=float,
        required=False,
        default="0.50",
    )

    parser.add_argument(
        "-l",
        "--list",
        help="Output as human readable list not terse (default True)",
        action=argparse.BooleanOptionalAction,
        type=bool,
        required=False,
        default=True,
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    today = datetime.today()
    args.year = args.year or today.year
    args.month = args.month or today.month
    args.day = args.day or today.day

    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
        custom_labels_path = "models/analyzer/BirdNET_GLOBAL_6K_V2.4_Labels.txt"
        # Model used 2023-Q4 - 2024-Q1.
        custom_model_path = "models/analyzer/BirdNET_GLOBAL_6K_V2.4_Model_FP32.tflite"
        # Newer than above, but not default in birdnetlib because it hangs. XXX
        # custom_model_path = "models/analyzer/BirdNET_GLOBAL_6K_V2.4_MData_Model_V2_FP16.tflite"
        analyzer = Analyzer(
            classifier_labels_path=custom_labels_path,
            classifier_model_path=custom_model_path,
        )

        recording = Recording(
            analyzer,
            args.input,
            lat=args.latitude,
            lon=args.longitude,
            date=datetime(year=args.year, month=args.month, day=args.day),
            min_conf=args.confidence,
        )

        recording.analyze()

    if args.list:
        i = 0
        species_sort = ""
        for i in range(0, len(recording.detections)):
            species_sort = species_sort + (
                recording.detections[i]["common_name"]
                + ", "
                + recording.detections[i]["scientific_name"]
                + ", "
                + str(recording.detections[i]["start_time"])
                + ", "
                + str(recording.detections[i]["end_time"])
                + ", "
                + str(recording.detections[i]["confidence"])
                + "\n"
            )
        species_out = sorted(species_sort.split("\n"))

        i = 0
        for i in range(1, len(species_out)):
            print(species_out[i])

    else:
        print(recording.detections)


if __name__ == "__main__":
    main()
