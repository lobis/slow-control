from __future__ import annotations

import threading
import uuid
from abc import abstractmethod


class Device:
    def __init__(self, *, name: str):
        self._name: str = name
        self._uuid: str = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"device:{self._name}"))
        self._lock = threading.Lock()
        self._open: bool = False
        self._handler = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def uuid(self) -> str:
        return self._uuid

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @property
    def is_open(self):
        return self._open

    @property
    def handler(self):
        return self._handler

    def get(self):
        if not self.is_open:
            self.open()

        return self._handler

    def acquire(self):
        self._lock.acquire()
        if not self.is_open:
            self.open()

    def release(self):
        if self.is_open:
            self.close()
        self._lock.release()

    def __enter__(self):
        self.acquire()
        return self.get()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        return False
