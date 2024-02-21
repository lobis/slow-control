from __future__ import annotations

from vsr53 import VSR53USB

from slow_control.devices.device import Device


class VSR53Device(Device):
    def __init__(self, port: str):
        super().__init__()
        self._handler = VSR53USB(port)

    def open(self):
        self._handler.open_communication()
        self._open = True

    def close(self):
        self._handler.close_communication()
        self._open = False
