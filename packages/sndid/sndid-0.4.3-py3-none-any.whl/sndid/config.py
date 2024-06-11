# sndid/config.py
"""
config.py

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
