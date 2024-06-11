# sndid/sndidjack.py
"""
sndidjack.py

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

import concurrent.futures
import io
import jack
import json
import logging
import numpy as np
import os
import queue
import sys
import threading
from .audiodetectionwriter import AudioDetectionWriter
from .segment_analyzer import SegmentAnalyzer
from .detectionswriter import DetectionsWriter
from .analyzerwrapper import AnalyzerWrapper
from .__version__ import __version__


class SndIdJack:
    def __init__(self, config):
        logging.debug(f"{sys.argv[0].split('/')[-1]} {__version__}")
        self.config = config
        logging.debug(f"Configuration loaded: {json.dumps(self.config, indent=4)}")
        self.segment_length = self.config["segment_length"]
        self.n_inputs = self.config["n_inputs"]
        self.sample_rate = self.config["sample_rate"]
        self.detections_file = os.path.join(self.config["output_dir"], "detections.txt")
        self.detections_dir = self.config["output_dir"]
        logging.debug(f"Creating detection writer for file: {self.detections_file}")
        self.detection_writer = AudioDetectionWriter(
            self.detections_file, self.detections_dir
        )
        self.min_confidence = config["min_confidence"]
        self.lat = config["lat"]
        self.lon = config["lon"]
        self.f = io.StringIO()
        logging.debug(f"Initializing {self.n_inputs} segment buffers")
        self.segments = [np.ndarray([1024]) for _ in range(self.n_inputs)]
        self.data_queues = [queue.Queue(maxsize=10) for _ in range(self.n_inputs)]
        logging.debug("Setting up thread event")
        self.event = threading.Event()
        self.clientname = "SndIdJack"
        self.client = jack.Client(self.clientname)
        logging.debug(f"Creating ThreadPoolExecutor with max_workers: {8}")
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        self.detections_writer = DetectionsWriter(
            self.detections_file, self.detections_dir
        )
        self.analyzer_wrapper = AnalyzerWrapper(self.config)

    def register_client(self):
        logging.debug("Registering client inports")
        for i in range(1, self.n_inputs + 1):
            self.client.inports.register(f"input_{i}")

    def segment_data(self, input_index):
        while not self.data_queues[input_index].empty():
            data = self.data_queues[input_index].get()
            self.segments[input_index] = np.append(
                self.segments[input_index], data, axis=0
            )
            if len(self.segments[input_index]) >= self.segment_length:
                segment = self.segments[input_index][: self.segment_length]
                self.executor.submit(self.analyze_segment, input_index, segment)
                logging.debug(
                    f"Submit segment for analysis in a new thread for input {input_index + 1}."
                )
                self.segments[input_index] = self.segments[input_index][
                    self.segment_length :
                ]

    def analyze_segment(self, input_index, segment):
        result = self.segment_analyzer.analyze(input_index, segment)
        if result:
            segment, detections, detection_timestamp = result
            self.detection_writer.detection_queue.put(
                (segment, detections, detection_timestamp, input_index)
            )

    def connect_client(self):
        logging.debug("Connecting client")
        with self.client:
            for i in range(self.n_inputs):
                self.client.connect(
                    f"ardour:Master/audio_out {i+1}", f"SndIdJack:input_{i+1}"
                )
            logging.info("Press Ctrl+C to stop")
            try:
                self.event.wait()
            except KeyboardInterrupt:
                logging.info("Interrupted by user")

    def process(self, frames):
        if len(self.client.inports) != self.n_inputs:
            self._update_data_structures()
        for i, port in enumerate(self.client.inports):
            data = port.get_array()
            self.data_queues[i].put(data)
            self.segment_data(i)

    def _update_data_structures(self):
        self.n_inputs = len(self.client.inports)
        while len(self.segments) < self.n_inputs:
            self.segments.append(np.ndarray([1024]))
        while len(self.data_queues) < self.n_inputs:
            self.data_queues.append(queue.Queue(maxsize=10))

    def shutdown(self, status, reason):
        logging.debug("JACK shutdown")
        logging.debug(f"Status: {status}")
        logging.debug(f"Reason: {reason}")
        self.event.set()

    def main(self):
        @self.client.set_process_callback
        def process_callback(frames):
            # logging.debug("process callback")
            self.process(frames)

        @self.client.set_shutdown_callback
        def shutdown_callback(status, reason):
            logging.debug("shuddown callback")
            self.shutdown(status, reason)

        logging.debug("Setting up segment analyzer and registering client")
        self.segment_analyzer = SegmentAnalyzer(self.analyzer_wrapper)
        self.register_client()
        self.connect_client()
