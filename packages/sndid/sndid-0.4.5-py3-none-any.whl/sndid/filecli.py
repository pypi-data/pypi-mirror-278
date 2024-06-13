# sndid/cli.py
# Copyright 2023, 2024 Jeff Moe <moe@spacecruft.org>
# Copyright 2022, 2023, Joe Weiss <joe.weiss@gmail.com>
# Licensed under the Apache License, Version 2.0
import argparse
import io
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


class Args(BaseModel):
    confidence: float = Field(
        title="confidence",
        alias="c",
        default=0.3,
        description="Minimum Confidence (default: 0.3)",
    )
    input: str = Field(
        title="input",
        default="samples/sample.wav",
        description="Input filename to process (default: samples/sample.wav)",
        alias="i",
    )
    latitude: str = Field(
        title="latitude",
        alias="a",
        default="40.57",
        description="Latitude (default: 40.57)",
    )
    longitude: str = Field(
        title="longitude",
        alias="o",
        default="-105.23",
        description="Longitude (default: -105.23)",
    )
    year: int = Field(
        title="year",
        alias="y",
        default=datetime.today().year,
        description="Year (default: today's year)",
    )
    month: int = Field(
        title="month",
        alias="m",
        default=datetime.today().month,
        description="Month (default: today's month)",
    )
    day: int = Field(
        title="day",
        alias="d",
        default=datetime.today().day,
        description="Day (default: today's day)",
    )
    list: bool = Field(
        title="list",
        alias="l",
        default=True,
        description="sndid file (default: True)",
    )


def parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Process bird sound file.")

    for field in Args.__fields__.values():
        parser.add_argument(
            f"-{field.alias}",
            f"--{field.title}",
            type=field.annotation,
            default=field.default if field.default is not None else "",
            help=field.description,
        )

    return parser.parse_args()


def main():
    args = parse_args()
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
        custom_labels_path = "models/analyzer/BirdNET_GLOBAL_6K_V2.4_Labels.txt"
        custom_model_path = "models/analyzer/BirdNET_GLOBAL_6K_V2.4_Model_FP32.tflite"
        analyzer = Analyzer(
            classifier_labels_path=custom_labels_path,
            classifier_model_path=custom_model_path,
        )

        recording = Recording(
            analyzer,
            args.input,
            lat=args.latitude,
            lon=args.longitude,
            date=datetime(
                year=args.year or datetime.today().year,
                month=args.month or datetime.today().month,
                day=args.day or datetime.today().day,
            ),
            min_conf=float(args.confidence),
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
