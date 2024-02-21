from __future__ import annotations

from slow_control.devices.serial import get_ports


def test_ports():
    ports = get_ports()
    print(ports)
