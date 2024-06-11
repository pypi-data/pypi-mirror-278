# sndid/constants.py
"""
constants.py

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
