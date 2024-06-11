# sndid/stream.py
"""
sndid-stream

Copyright 2023, 2024 Jeff Moe <moe@spacecruft.org>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import signal
import sys
import argparse
import subprocess
import os


def signal_handler(signum, frame):
    print("\nReceived signal to exit. Cleaning up...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def run_ffmpeg_command(ip, port, time, url):
    """Runs the ffmpeg command with subprocess, handling piping correctly."""
    ffmpeg_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "quiet",
        "-i",
        url,
        "-acodec",
        "pcm_s16le",
        "-ac",
        "1",
        "-vcodec",
        "vnull",
        "-f",
        "wav",
        "-t",
        time,
        "-",
    ]

    nc_cmd = ["nc", "-q", "0", ip, port]

    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)
    subprocess.run(nc_cmd, stdin=ffmpeg_process.stdout, text=True)
    ffmpeg_process.wait()

    if ffmpeg_process.returncode != 0:
        raise subprocess.CalledProcessError(ffmpeg_process.returncode, ffmpeg_cmd)


def main():
    parser = argparse.ArgumentParser(description="Run sndid-stream")
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
        "-t",
        "--time",
        help="Length of segments in seconds (default 60)",
        type=int,
        required=False,
        default="60",
    )
    parser.add_argument("-u", "--url", help="Input url", type=str, required=True)

    args = parser.parse_args()
    IP = args.ip
    PORT = str(args.port)
    TIME = str(args.time)
    URL = args.url

    try:
        while True:
            print("Sending stream...")
            run_ffmpeg_command(IP, PORT, TIME, URL)
    except KeyboardInterrupt:
        print("Exiting on user interrupt.")
    finally:
        print("Script exit cleanup.")


if __name__ == "__main__":
    main()
