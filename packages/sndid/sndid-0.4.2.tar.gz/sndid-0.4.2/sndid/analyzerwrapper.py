# sndid/analyzerwrapper.py
"""
analyzerwrapper.py

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
import io
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from .jack_lazy_loader import jack_lazy_load


class AnalyzerWrapper:
    def __init__(self, config):
        logging.debug("Initializing AnalyzerWrapper")
        Analyzer = jack_lazy_load("birdnetlib.analyzer").Analyzer
        self.config = config
        self.f = io.StringIO()
        self.analyzer = Analyzer()

    def analyze(self, input_index, segment):
        logging.debug(f"Running analyzer for input {input_index + 1}")
        RecordingBuffer = jack_lazy_load("birdnetlib").RecordingBuffer
        with redirect_stdout(self.f), redirect_stderr(self.f):
            recording_timestamp = datetime.now()
            logging.debug(
                f"Creating RecordingBuffer instance for input {input_index + 1}"
            )
            recording = RecordingBuffer(
                self.analyzer,
                segment,
                self.config["sample_rate"],
                lat=self.config["lat"],
                lon=self.config["lon"],
                date=recording_timestamp,
                min_conf=self.config["min_confidence"],
            )
            logging.debug(f"Analyzing RecordingBuffer for input {input_index + 1}")
            recording.analyze()
        if recording.detections:
            logging.info(
                f"Detections for input {input_index + 1}: {recording.detections}"
            )
        return recording, recording_timestamp
