from __future__ import annotations

from pyvsr53dl.vsr53dl import PyVSR53DL

import slow_control


def test_ports():
    ports = slow_control.devices.serial.get_ports()
    print(ports)


# TODO: stuck
def test_vsr53usb():
    port = "COM10"
    address = 1
    sensor = PyVSR53DL(port, address)
    sensor.open_communication()
    device_type = sensor.get_device_type()
    print(device_type)
    sensor.close_communication()
