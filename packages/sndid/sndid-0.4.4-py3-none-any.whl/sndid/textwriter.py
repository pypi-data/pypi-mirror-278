# sndid/textwriter.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
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
