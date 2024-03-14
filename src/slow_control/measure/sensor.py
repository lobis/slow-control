from __future__ import annotations

import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from slow_control.devices.device import Device


class Sensor(ABC):
    def __init__(self, *, name: str, device: Device):
        self._device: Device = device
        self._sensor_type: str = ""
        self._name: str = name  # must be globally unique
        self._uuid: str = str(
            uuid.uuid5(uuid.NAMESPACE_DNS, f"sensor:{self._sensor_type}:{self._name}")
        )

        self._measurement_value: any = None
        self._measurement_time: int = 0  # Unix time

    @property
    def name(self) -> str:
        return self._name

    @property
    def uuid(self) -> str:
        return self._uuid

    def __enter__(self):
        self._device.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._device.release()
        return False

    def update(self) -> bool:
        try:
            self._update_measurement()
            self._update_time()
            return True

        except Exception as e:
            print(f"Failed to update {self.name}: {e}")
            return False

        finally:
            self._device.release()

    def __repr__(self):
        return f"{self.measurement_time_formatted} - {self.measurement_value}"
    
    def get_measurement_value(self):
        return self._measurement_value

    @abstractmethod
    def _update_measurement(self) -> None:
        pass

    @abstractmethod
    def get_insert_sql(self) -> str:
        pass

    @abstractmethod
    def _get_table_creation_sql(self) -> str:
        pass

    def get_table_creation_sql(self) -> str:
        return f"""{self._get_table_creation_sql_base()}
{self._get_table_creation_sql()}"""

    def _get_table_creation_sql_base(self) -> str:
        return """CREATE TABLE IF NOT EXISTS devices (id uuid PRIMARY KEY);
CREATE TABLE IF NOT EXISTS sensors (id uuid PRIMARY KEY, device_id uuid, FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE);"""

    @property
    def measurement_value(self):
        return self._measurement_value

    @property
    def measurement_time(self):
        return self._measurement_time

    @property
    def measurement_time_formatted(self):
        timestamp = datetime.utcfromtimestamp(self._measurement_time)
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def measurement_time_datetime(self):
        return datetime.fromtimestamp(self.measurement_time, tz=timezone.utc)

    def _update_time(self):
        self._measurement_time = int(time.time())
