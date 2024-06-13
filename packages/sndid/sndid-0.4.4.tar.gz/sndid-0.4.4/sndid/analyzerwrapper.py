# sndid/analyzerwrapper.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
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
