# sndid/detectionswriter.py
"""
detectionswriter.py

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
from .textwriter import TextWriter
from .audiowriter import AudioWriter


class DetectionsWriter:
    def __init__(self, detections_file, detections_dir):
        logging.debug("Initializing DetectionsWriter")
        self.text_writer = TextWriter(detections_file)
        self.audio_writer = AudioWriter(detections_dir)
        self.detection_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._writer_thread = threading.Thread(target=self._write_detections_loop)
        self._writer_thread.daemon = True
        logging.debug("Starting DetectionsWriter thread.")
        self._writer_thread.start()

    def write_detections(self, detections, detection_timestamp, input_index):
        self.detection_queue.put((detections, detection_timestamp, input_index))
        logging.debug(f"DetectionsWriter detections added to queue: {len(detections)}")

    def _write_detections_loop(self):
        while not self._stop_event.is_set():
            try:
                detections, detection_timestamp, input_index = self.detection_queue.get(
                    timeout=1
                )
                logging.debug("Detections received from queue to DetectionsWriter.")
            except queue.Empty:
                continue
            self.text_writer.write_detections(
                detections, detection_timestamp, input_index
            )

    def write_audio(self, recording_data, detections, detection_timestamp, input_index):
        self.audio_writer.write_audio(
            recording_data, detections, detection_timestamp, input_index
        )
        logging.debug("Audio written from DetectionsWriter.")

    def stop(self):
        self._stop_event.set()
        logging.debug("Waiting for DetectionsWriter thread to finish.")
        self._writer_thread.join()
        logging.debug("DetectionsWriter thread stopped.")
