# sndid/segment_analyzer.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
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
