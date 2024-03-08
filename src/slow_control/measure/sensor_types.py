from __future__ import annotations

from abc import ABC

from slow_control.devices.device import Device
from slow_control.measure.sensor import Sensor


class PressureSensor(Sensor, ABC):
    def __init__(self, *, name: str, device: Device):
        super().__init__(name=name, device=device)
        self._sensor_type = "pressure_setpoint_sensor"
        self._measurement_value: float = 0.0

    def get_insert_sql(self):
        return f"""INSERT INTO devices (id) VALUES ('{self._device.uuid}') ON CONFLICT DO NOTHING;
INSERT INTO sensors (id) VALUES ('{self.uuid}') ON CONFLICT DO NOTHING;
INSERT INTO {self._sensor_type} (sensor_id, time, value) VALUES ('{self.uuid}', '{self.measurement_time_datetime}', {self.measurement_value});"""

    def _get_table_creation_sql(self):
        return f"""CREATE TABLE IF NOT EXISTS {self._sensor_type} (
    sensor_id uuid,
    time TIMESTAMPTZ,
    value FLOAT,
    PRIMARY KEY (sensor_id, time),
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);"""


class PressureSetpointSensor(Sensor, ABC):
    def __init__(self, *, name: str, device: Device):
        super().__init__(name=name, device=device)
        self._sensor_type = "pressure_setpoint_sensor"
        self._measurement_value: float = 0.0

    def get_insert_sql(self):
        return f"""INSERT INTO devices (id) VALUES ('{self._device.uuid}') ON CONFLICT DO NOTHING;
INSERT INTO sensors (id) VALUES ('{self.uuid}') ON CONFLICT DO NOTHING;
INSERT INTO {self._sensor_type} (sensor_id, time, value) VALUES ('{self.uuid}', '{self.measurement_time_datetime}', {self.measurement_value});"""

    def _get_table_creation_sql(self):
        return f"""CREATE TABLE IF NOT EXISTS {self._sensor_type} (
    sensor_id uuid,
    time TIMESTAMPTZ,
    value FLOAT,
    PRIMARY KEY (sensor_id, time),
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);"""
