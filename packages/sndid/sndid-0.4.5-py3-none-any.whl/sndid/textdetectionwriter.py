# sndid/textdetectionwriter.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import logging
import queue
import threading
from .textwriter import TextWriter


class TextDetectionWriter:
    def __init__(self, detections_file, detections_dir):
        logging.debug("Initializing TextDetectionWriter")
        self.text_writer = TextWriter(detections_file)
        self.detection_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._writer_thread = threading.Thread(target=self._write_detections_loop)
        self._writer_thread.daemon = True
        self._writer_thread.start()
        logging.debug("TextDetectionWriter thread started")

    def write_detections(self, detections, detection_timestamp, input_index):
        self.detection_queue.put((detections, detection_timestamp, input_index))
        logging.debug(
            f"TextDetectionWriter detections written to queue: {len(detections)}"
        )

    def _write_detections_loop(self):
        while not self._stop_event.is_set():
            try:
                detections, detection_timestamp, input_index = self.detection_queue.get(
                    timeout=1
                )
                logging.debug("TextDetectionWriter received detections from queue")
            except queue.Empty:
                continue
            self.text_writer.write_detections(
                detections, detection_timestamp, input_index
            )
            logging.debug(
                f"TextDetectionWriter detections written to file: {len(detections)}"
            )

    def stop(self):
        logging.debug("Stopping TextDetectionWriter")
        self._stop_event.set()
        self._writer_thread.join()
