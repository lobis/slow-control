from __future__ import annotations

from slow_control import SlowControl
from slow_control.database.database import Database

from slow_control.devices.vsr53 import VSR53Device
from slow_control.devices.bronkhorst import BronkhorstDevice

from slow_control.measure.vsr53 import VSR53PressureSensor
from slow_control.measure.bronkhorst import BronkhorstPressureSensor
from slow_control.measure.bronkhorst import BronkhorstPressureSetpointSensor

slow_control = SlowControl()

vsr53_device = VSR53Device(name="pressure_pipe", port="COM5")
bronkhorst_device = BronkhorstDevice(name="other_pressure", port="/dev/cu.usbserial-1110")

slow_control.add_device(vsr53_device)
slow_control.add_device(bronkhorst_device)

slow_control.add_sensor(VSR53PressureSensor(name="pressure_one", device=vsr53_device))
slow_control.add_sensor(VSR53PressureSensor(name="pressure_two", device=vsr53_device))

slow_control.add_sensor(BronkhorstPressureSensor(name="pressure_three", device=bronkhorst_device))
slow_control.add_sensor(BronkhorstPressureSetpointSensor(name="pressure_three_set", device=bronkhorst_device))

database = Database(
    dbname="postgres",
    user="postgres",
    password="password",
    host="localhost",
    port=5432,
)


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


@slow_control.periodic_task(interval_seconds=1)
def periodic_task():
    print(" --- periodic task")
    for sensor_name, sensor in slow_control.sensors.items():
        sensor.update()
        print(f"{sensor_name}: {sensor}")
        # database.execute_query(sensor.get_table_creation_sql())
        # database.execute_query(sensor.get_insert_sql())


if __name__ == "__main__":
    slow_control.run()
