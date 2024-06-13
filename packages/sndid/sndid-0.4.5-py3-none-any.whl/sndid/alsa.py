# sndid/alsa.py
# Copyright 2023, 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0

import argparse
import subprocess
from pydantic import BaseModel, validator


class ArgsModel(BaseModel):
    ip: str = "127.0.0.1"
    port: int = 9988
    rate: int = 48000
    time: int = 10

    @validator("port", "rate", "time")
    def validate_int_values(cls, v):
        if v < 0:
            raise ValueError("Integer values must be positive")
        return v


def parse_args() -> ArgsModel:
    parser = argparse.ArgumentParser(description="Run sndid-alsa")
    args = parser.parse_args()
    return ArgsModel(**vars(args))


def run_alsa_stream(ip: str, port: int, rate: int, time: int):
    command = [
        "arecord",
        "--rate",
        str(rate),
        "-f",
        "FLOAT_LE",
        "--max-file-time",
        str(time),
        "|",
        "nc",
        ip,
        str(port),
    ]
    print(f"Streaming ALSA in to {ip}:{port}")
    subprocess.run(" ".join(command), shell=True)


def main():
    args = parse_args()
    run_alsa_stream(args.ip, args.port, args.rate, args.time)


if __name__ == "__main__":
    main()
