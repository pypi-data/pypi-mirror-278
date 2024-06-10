# -*- coding: utf-8 -*-
from __future__ import annotations

import multiprocessing as mp
import threading
from abc import abstractmethod

from computer_vision_design_patterns.pipeline import Payload
from loguru import logger


class Stage:
    pass


class ProcessStage(Stage, mp.Process):
    def __init__(self, key: str, output_maxsize: int | None, control_queue: mp.Queue | None):
        super().__init__()
        self.key = key
        self.output_maxsize = output_maxsize
        self.input_queue: mp.Queue[Payload] | None = None
        self.output_queue: mp.Queue[Payload] | None = None
        self.control_queue = control_queue

    def get_from_input_queue(self) -> Payload | None:
        if not self.input_queue.empty():
            return self.input_queue.get()
        return None

    def put_to_output_queue(self, payload: Payload) -> None:
        if self.output_queue is None:
            return

        if self.output_queue.full():
            logger.warning("Queue is full, dropping frame")
            self.output_queue.get()
        self.output_queue.put(payload)

    def link(self, stage: ProcessStage | MultiQueueThreadStage):
        if self.output_queue is None:
            self.output_queue = mp.Queue() if self.output_maxsize is None else mp.Queue(maxsize=self.output_maxsize)

        if isinstance(stage, ProcessStage):
            stage.input_queue = self.output_queue

        elif isinstance(stage, MultiQueueThreadStage):
            stage.input_queues[self.key] = self.output_queue

    @abstractmethod
    def process(self, payload: Payload | None):
        pass

    @abstractmethod
    def run(self) -> None:
        pass


class MultiQueueThreadStage(Stage, threading.Thread):
    def __init__(self, key: str, output_maxsize: int | None, control_queue: mp.Queue | None):
        super().__init__()
        self.key = key
        self.output_maxsize = output_maxsize
        self.input_queues: dict[str, mp.Queue[Payload]] | None = {}
        self.output_queues: dict[str, mp.Queue[Payload]] | None = {}
        self.control_queue = control_queue

        self.stop_event = threading.Event()

    def get_from_input_queue(self, key: str) -> Payload | None:
        queue = self.input_queues.get(key)
        return queue.get() if queue and not queue.empty() else None

    def put_to_output_queue(self, key: str, payload: Payload) -> None:
        queue = self.output_queues.get(key)

        # If the queue exists and is full
        if queue and queue.full():
            logger.warning("Queue is full, dropping payload")
            queue.get()  # Remove an item from the queue to make space

        if queue:
            queue.put(payload)

    def close_queue(self, key: str):
        del self.input_queues[key]
        del self.output_queues[key]

    def link(self, stage: ProcessStage):
        if self.output_queues.get(stage.key) is None:
            self.output_queues[stage.key] = (
                mp.Queue() if self.output_maxsize is None else mp.Queue(maxsize=self.output_maxsize)
            )

        stage.input_queue = self.output_queues[stage.key]

    def terminate(self):
        self.stop_event.set()

    @abstractmethod
    def process(self, key, payload: Payload):
        pass

    @abstractmethod
    def run(self) -> None:
        pass
