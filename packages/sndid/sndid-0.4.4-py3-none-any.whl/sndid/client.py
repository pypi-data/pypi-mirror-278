# sndid/client.py
# Copyright 2023, 2024 Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Run sndid-client")
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
        type=int,
        required=False,
        default="9988",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Input filename to process (default samples/mono.wav)",
        type=str,
        required=False,
        default="samples/mono.wav",
    )

    args = parser.parse_args()
    IP = args.ip
    PORT = str(args.port)
    FILE = args.file

    CMD = "cat" + " " + FILE + " | nc -q 0 " + IP + " " + PORT
    print("Sending " + FILE + " to " + IP + ":" + PORT)
    os.system(CMD)


if __name__ == "__main__":
    main()
