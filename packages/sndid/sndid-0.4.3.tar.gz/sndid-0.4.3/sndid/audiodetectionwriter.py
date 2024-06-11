# sndid/audiodetectionwriter.py
"""
audiodetectionwriter.py

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
import queue
import threading
from .detectionswriter import DetectionsWriter


class AudioDetectionWriter:
    def __init__(self, detections_file, detections_dir):
        logging.debug("Initialize AudioDetectionWriter")
        self.detections_writer = DetectionsWriter(detections_file, detections_dir)
        self.detection_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._writer_thread = threading.Thread(target=self._start_writer_thread)
        self._writer_thread.daemon = True
        self._writer_thread.start()

    def write_detections(
        self, recording_data, detections, detection_timestamp, input_index
    ):
        logging.debug("Putting data onto the queue")
        self.detection_queue.put(
            (recording_data, detections, detection_timestamp, input_index)
        )
        logging.debug("write_detections")

    def _write_detections_loop(self):
        while not self._stop_event.is_set():
            try:
                recording_data, detections, detection_timestamp, input_index = (
                    self.detection_queue.get(timeout=1)
                )
                logging.debug("Got data from the queue")
            except queue.Empty:
                continue
            self.detections_writer.write_detections(
                detections, detection_timestamp, input_index
            )
            self.detections_writer.write_audio(
                recording_data, detections, detection_timestamp, input_index
            )
            logging.debug("Wrote data to file")
            self.detection_queue.task_done()
        self.detection_queue.join()

    def _start_writer_thread(self):
        logging.basicConfig(level=logging.DEBUG)
        self._write_detections_loop()

    def stop(self):
        self._stop_event.set()
        self._writer_thread.join()
        logging.debug("Writer stopped")
