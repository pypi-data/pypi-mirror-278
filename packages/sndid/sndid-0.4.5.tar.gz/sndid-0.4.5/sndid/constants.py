# sndid/constants.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0

# Default values.
# Can be overrided by configuration file or command line options.
import os

N_INPUTS = 2
SEGMENT_LENGTH = 240000
MIN_CONFIDENCE = 0.25
LAT = 40
LON = -105
LOG_LEVEL = "INFO"
SAMPLE_RATE = 48000
OUTPUT_DIR = os.path.expanduser("~/detections")
