from __future__ import annotations

from abc import ABC

from slow_control.measure.sensor import Sensor


class PressureSensor(Sensor, ABC):
    def __init__(self, device):
        super().__init__(device)
        self._sensor_type = "pressure_sensor"
        self._measurement_value: float = 0.0

    def get_insert_sql(self):
        return f"INSERT INTO {self._sensor_type} (time, value) VALUES ({self.measurement_time}, {self.measurement_value})"
