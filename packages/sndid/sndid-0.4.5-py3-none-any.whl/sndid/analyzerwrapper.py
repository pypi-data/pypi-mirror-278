# sndid/analyzerwrapper.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import logging
import io
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from typing import Any, Dict, Union
from pydantic import BaseModel, Field, validator
from .jack_lazy_loader import jack_lazy_load


class Config(BaseModel):
    sample_rate: int = Field(..., gt=0)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    min_confidence: float = Field(..., ge=0, le=1)

    @validator("sample_rate", "min_confidence")
    def not_negative(cls, v):
        if v < 0:
            raise ValueError("Value must be non-negative")
        return v


class AnalyzerWrapper:
    def __init__(self, config: Dict[str, Union[int, float]]) -> None:
        self.config = Config(**config)
        self.Analyzer = jack_lazy_load("birdnetlib.analyzer").Analyzer
        self.RecordingBuffer = jack_lazy_load("birdnetlib").RecordingBuffer
        self.analyzer = self.Analyzer()

    def analyze(self, input_index: int, segment: Any) -> None:
        logging.debug(f"Running analyzer for input {input_index + 1}")
        with io.StringIO() as f, redirect_stdout(f), redirect_stderr(f):
            recording_timestamp = datetime.now()
            logging.debug(
                f"Creating RecordingBuffer instance for input {input_index + 1}"
            )
            recording = self.RecordingBuffer(
                self.analyzer,
                segment,
                self.config.sample_rate,
                lat=self.config.lat,
                lon=self.config.lon,
                date=recording_timestamp,
                min_conf=self.config.min_confidence,
            )
            logging.debug(f"Analyzing RecordingBuffer for input {input_index + 1}")
            recording.analyze()

        if recording.detections:
            logging.info(
                f"Detections for input {input_index + 1}: {recording.detections}"
            )
        return recording, recording_timestamp
