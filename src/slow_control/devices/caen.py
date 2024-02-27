from __future__ import annotations

from hvps import Caen

from slow_control.devices.device import Device


class CaenDevice(Device):
    def __init__(self, *, name: str, port: str):
        super().__init__(name=name)
        self._handler = Caen(port=port)

    def open(self):
        self._handler.open()
        self._open = True

    def close(self):
        self._handler.close()
        self._open = False
