# sndid/audiodetectionwriter.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import logging
import queue
import threading
from typing import Any, Tuple
from .detectionswriter import DetectionsWriter


class AudioDetectionWriter:
    def __init__(
        self, detections_file: str, detections_dir: str, max_queue_size: int = 1000
    ):
        logging.debug("Initialize AudioDetectionWriter")
        self.detections_writer = DetectionsWriter(detections_file, detections_dir)
        self.detection_queue = queue.Queue(maxsize=max_queue_size)
        self._stop_event = threading.Event()
        self._start_writer_thread()

    def __del__(self):
        self.stop()

    def write_detections(
        self,
        recording_data: Any,
        detections: Any,
        detection_timestamp: float,
        input_index: int,
    ):
        logging.debug("Putting data onto the queue")
        try:
            self.detection_queue.put_nowait(
                (recording_data, detections, detection_timestamp, input_index)
            )
        except queue.Full:
            logging.warning("Detection queue is full, skipping detection")

    def _write_detections_loop(self):
        while not self._stop_event.is_set():
            try:
                data = self.detection_queue.get(timeout=1)
                logging.debug("Got data from the queue")
                recording_data, detections, detection_timestamp, input_index = data
                self.detections_writer.write_detections(
                    detections, detection_timestamp, input_index
                )
                self.detections_writer.write_audio(
                    recording_data, detections, detection_timestamp, input_index
                )
                logging.debug("Wrote data to file")
            except queue.Empty:
                continue

    def _start_writer_thread(self):
        logging.basicConfig(level=logging.DEBUG)
        self._writer_thread = threading.Thread(
            target=self._write_detections_loop, daemon=True
        )
        self._writer_thread.start()

    def stop(self):
        self._stop_event.set()
        self._writer_thread.join()
        self.detections_writer.flush()
        logging.debug("Writer stopped")

    def flush(self):
        self.detections_writer.flush()
