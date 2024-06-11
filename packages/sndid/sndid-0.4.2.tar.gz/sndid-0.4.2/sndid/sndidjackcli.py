# sndid/jackcli.py
"""
jackcli.py

Copyright 2024, Jeff Moe <moe@spacecruft.org>

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

import argparse
import logging
import sys
from sndidjack.sndidjack import SndIdJack
from sndidjack.config import Config
from .__version__ import __version__


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="sndidjack - AI processing JACK Audio Connection Kit."
    )
    parser.add_argument("--config_file", "-c", help="Configuration File name")
    parser.add_argument(
        "--log-level",
        "-L",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
        type=str.upper,
    )
    parser.add_argument("--n-inputs", "-n", type=int, help="Number of inputs")
    parser.add_argument("--segment-length", "-l", type=int, help="Segment length")
    parser.add_argument("--min-confidence", "-m", type=float, help="Minimum confidence")
    parser.add_argument("--lat", "-y", type=float, help="Latitude")
    parser.add_argument("--lon", "-x", type=float, help="Longitude")
    parser.add_argument("--output-dir", "-o", help="Output directory for detections")
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s {__version__}"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    config_file = args.config_file
    config = Config.load_config(config_file)

    if not config_file:
        config = Config.set_defaults({})

    for key, value in vars(args).items():
        if value is not None:
            config[key] = value

    logging.basicConfig(
        level=config["log_level"],
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    logging.debug("Starting SndIdJack with configuration: %s", config)

    sndidjack = SndIdJack(config)
    sndidjack.main()


if __name__ == "__main__":
    main()
