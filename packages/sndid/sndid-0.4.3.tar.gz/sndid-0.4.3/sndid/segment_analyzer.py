# sndid/segment_analyzer.py
"""
segment_analyzer.py

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

import threading
import logging


class SegmentAnalyzer(threading.Thread):
    def __init__(self, analyzer_wrapper):
        logging.debug("Initialize SegmentAnalyzer")
        self.analyzer_wrapper = analyzer_wrapper

    def analyze(self, input_index, segment):
        logging.debug(f"SegmentAnalyzer Analyzing segment for input {input_index}")
        recording, detection_timestamp = self.analyzer_wrapper.analyze(
            input_index, segment
        )
        if recording.detections:
            logging.debug(
                f"SegmentAnalyzer detections found in segment for input {input_index}: {recording.detections}"
            )
            return segment, recording.detections, detection_timestamp
        return None
