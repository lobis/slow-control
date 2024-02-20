from __future__ import annotations

from serial.tools import list_ports


def get_ports():
    return [port.device for port in list_ports.comports()]
