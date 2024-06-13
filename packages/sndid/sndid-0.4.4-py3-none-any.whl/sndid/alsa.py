# sndid/alsa.py
# Copyright 2023, 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Run sndid-alsa")
    parser.add_argument(
        "-i",
        "--ip",
        help="Server IP address (default 127.0.0.1)",
        type=str,
        required=False,
        default="127.0.0.1",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Server network port (default 9988)",
        type=str,
        required=False,
        default="9988",
    )
    parser.add_argument(
        "-r",
        "--rate",
        help="Rate in Hertz (default 48000)",
        type=str,
        required=False,
        default=48000,
    )
    parser.add_argument(
        "-t",
        "--time",
        help="Length of segments in seconds (default 10)",
        type=str,
        required=False,
        default=10,
    )

    args = parser.parse_args()
    IP = args.ip
    PORT = args.port
    RATE = str(args.rate)
    TIME = str(args.time)

    CMD = (
        "arecord --rate "
        + RATE
        + " -f FLOAT_LE --max-file-time "
        + TIME
        + " | nc "
        + IP
        + " "
        + PORT
    )
    print("Streaming ALSA in to " + IP + ":" + PORT)
    os.system(CMD)


if __name__ == "__main__":
    main()
