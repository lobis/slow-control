from __future__ import annotations

import propar

from slow_control.devices.bronkhorst import BronkhorstDevice
from slow_control.measure.sensor_types import PressureSensor, PressureSetpointSensor


class BronkhorstPressureSensor(PressureSensor):
    def __init__(self, name: str, device: BronkhorstDevice):
        super().__init__(name=name, device=device)

    def _update_measurement(self):
        with self._device as handler:  # type: propar.instrument
            parameter = handler.readParameter(205)
            print("test param", parameter)


class BronkhorstPressureSetpointSensor(PressureSetpointSensor):
    def __init__(self, name: str, device: BronkhorstDevice):
        super().__init__(name=name, device=device)

    def _update_measurement(self):
        with self._device as handler:  # type: propar.instrument
            parameter = handler.readParameter(205)
            print("test param", parameter)
