from __future__ import annotations

from slow_control.devices.vsr53 import VSR53Device
from slow_control.measure.sensor_types import PressureSensor


class VSR53PressureSensor(PressureSensor):
    def __init__(self, name: str, device: VSR53Device):
        super().__init__(name=name, device=device)

    def _update_measurement(self):
        with self._device as gauge:  # type: VSR53USB
            self._measurement_value = gauge.get_measurement_value()
