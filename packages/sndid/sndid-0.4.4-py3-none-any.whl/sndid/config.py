# sndid/config.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import os
import yaml
from .constants import (
    N_INPUTS,
    SEGMENT_LENGTH,
    MIN_CONFIDENCE,
    LAT,
    LON,
    LOG_LEVEL,
    SAMPLE_RATE,
    OUTPUT_DIR,
)


class Config:
    @staticmethod
    def load_config(file_path=None):
        config = {}
        if file_path:
            with open(file_path, "r") as file:
                config = yaml.safe_load(file)
        return Config.set_defaults(config)

    @staticmethod
    def set_defaults(config):
        config["n_inputs"] = int(
            os.getenv("N_INPUTS", config.get("n_inputs", N_INPUTS))
        )
        config["segment_length"] = int(
            os.getenv("SEGMENT_LENGTH", config.get("segment_length", SEGMENT_LENGTH))
        )
        config["min_confidence"] = float(
            os.getenv("MIN_CONFIDENCE", config.get("min_confidence", MIN_CONFIDENCE))
        )
        config["lat"] = float(os.getenv("LAT", config.get("lat", LAT)))
        config["lon"] = float(os.getenv("LON", config.get("lon", LON)))
        config["log_level"] = os.getenv("LOG_LEVEL", config.get("log_level", LOG_LEVEL))
        config["output_dir"] = os.getenv(
            "OUTPUT_DIR", config.get("output_dir", OUTPUT_DIR)
        )
        config["sample_rate"] = int(
            os.getenv("SAMPLE_RATE", config.get("sample_rate", SAMPLE_RATE))
        )
        return config
