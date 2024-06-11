# sndid/textwriter.py
"""
textwriter.py

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

import logging
import os


class TextWriter:
    def __init__(self, detections_file):
        self.detections_file = detections_file
        logging.debug("TextWriter object created.")

    def write_detections(self, detections, detection_timestamp, input_index):
        detections_dir = os.path.dirname(self.detections_file)
        logging.debug(f"Creating directory: {detections_dir}")
        os.makedirs(detections_dir, exist_ok=True)

        with open(self.detections_file, "a") as file:
            for d in detections:
                file.write(
                    f"{detection_timestamp}, {d['common_name']}, {d['scientific_name']}, {d['confidence']}, Input {input_index + 1}\n"
                )
        logging.debug(f"Detections written to text file: {self.detections_file}")
