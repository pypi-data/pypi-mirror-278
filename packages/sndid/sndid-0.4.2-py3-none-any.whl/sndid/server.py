# sndid/server.py
"""
sndid-server

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

https://github.com/joeweiss/birdnetlib/blob/main/examples/simple_tcp_server.py
"""

from birdnetlib import RecordingBuffer
from birdnetlib.analyzer import Analyzer
import birdnetlib.wavutils as wavutils
import datetime
import socketserver
import argparse
from contextlib import redirect_stdout, redirect_stderr
import io
import logging
import functools


class TCPHandler(socketserver.StreamRequestHandler):
    def __init__(self, *args, **kwargs):
        self.lat = kwargs.get("lat", None)
        self.lon = kwargs.get("lon", None)
        self.year = kwargs.get("year", None)
        self.month = kwargs.get("month", None)
        self.day = kwargs.get("day", None)
        self.confidence = kwargs.get("confidence", None)
        super().__init__(*args)

    def handle(self):
        f = io.StringIO()
        with redirect_stdout(f), redirect_stderr(f):
            analyzer = Analyzer()
        # Read WAV data from the socket
        for rate, data in wavutils.bufferwavs(self.rfile):
            with redirect_stdout(f), redirect_stderr(f):
                # Make a RecordingBuffer with buffer and rate
                recording = RecordingBuffer(
                    analyzer,
                    data,
                    rate,
                    lat=self.lat,
                    lon=self.lon,
                    date=datetime.datetime(
                        year=self.year, month=self.month, day=self.day
                    ),
                    min_conf=self.confidence,
                )
            with redirect_stdout(f), redirect_stderr(f):
                recording.analyze()
            i = 0
            detections_sort = ""
            for i in range(0, len(recording.detections)):
                detections_sort = detections_sort + (
                    recording.detections[i]["common_name"]
                    + ", "
                    + recording.detections[i]["scientific_name"]
                    + ", "
                    + str(recording.detections[i]["confidence"])
                    + "\n"
                )
            detections_out = sorted(detections_sort.split("\n"))
            i = 0
            for i in range(1, len(detections_out)):
                n = datetime.datetime.now(datetime.timezone.utc).astimezone()
                print(n, detections_out[i])
                logging.info(str(n) + " " + str(detections_out[i]))


def initialize_logging():
    TODAY = datetime.date.today()
    logging.basicConfig(
        filename="sndid.log",
        encoding="utf-8",
        format="%(message)s",
        level=logging.DEBUG,
    )


def start_server():
    TODAY = datetime.date.today()
    YEAR = TODAY.year
    MONTH = TODAY.month
    DAY = TODAY.day

    parser = argparse.ArgumentParser(description="Run sndid-server")
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
        help="Minimum Confidence (default 0.25)",
        type=float,
        required=False,
        default="0.25",
    )

    args = parser.parse_args()

    handler_factory = functools.partial(
        TCPHandler,
        lat=args.latitude,
        lon=args.longitude,
        year=args.year,
        month=args.month,
        day=args.day,
        confidence=args.confidence,
    )

    initialize_logging()

    lat = args.latitude
    lon = args.longitude
    ip = args.ip
    port = args.port
    year = args.year
    month = args.month
    day = args.day
    confidence = args.confidence

    handler_class = functools.partial(
        TCPHandler,
        **{
            "lat": lat,
            "lon": lon,
            "year": year,
            "month": month,
            "day": day,
            "confidence": confidence,
        },
    )

    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        pass

    server = ThreadedTCPServer((args.ip, args.port), handler_factory)

    try:
        n = datetime.datetime.now(datetime.timezone.utc).astimezone()
        print(n, "sndid-server started on", ip + ":" + str(port))
        logging.info(
            n.strftime("%Y-%m-%d %H:%M:%S")
            + " sndid-server started on "
            + args.ip
            + ":"
            + str(args.port)
        )
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


def main():
    start_server()


if __name__ == "__main__":
    main()
