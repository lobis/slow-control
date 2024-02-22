from __future__ import annotations

from slow_control import SlowControl
from slow_control.database.database import Database
from slow_control.devices.vsr53 import VSR53Device
from slow_control.measure.vsr53 import VSR53Sensor

slow_control = SlowControl()

pressure_gauge = VSR53Device(name="pressure_pipe", port="COM5")

slow_control.add_device(pressure_gauge)

slow_control.add_sensor(VSR53Sensor(name="pressure_one", device=pressure_gauge))
slow_control.add_sensor(VSR53Sensor(name="pressure_two", device=pressure_gauge))

database = Database(
    dbname="postgres",
    user="postgres",
    password="password",
    host="localhost",
    port=5432,
)

database.connect()


@slow_control.route("/")
async def root():
    return "slow-control"


@slow_control.route("/devices")
async def devices():
    return list(slow_control._devices.keys())


@slow_control.route("/sensors")
async def sensors():
    sensors_with_data = {
        sensor_name: (sensor.measurement_time_formatted, sensor.measurement_value)
        for sensor_name, sensor in slow_control._sensors.items()
    }
    return sensors_with_data


@slow_control.periodic_task(interval_seconds=5)
def periodic_task():
    for sensor_name, sensor in slow_control.sensors.items():
        sensor.update()
        print(f"{sensor_name}: {sensor}")
        database.execute_query(sensor.get_table_creation_sql())
        database.execute_query(sensor.get_insert_sql())


slow_control.run()

if __name__ == "__main__":
    ...
