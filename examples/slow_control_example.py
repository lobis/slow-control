from __future__ import annotations

from slow_control import SlowControl
from slow_control.database.database import Database

from slow_control.devices.vsr53 import VSR53Device
from slow_control.devices.bronkhorst import BronkhorstDevice

from slow_control.measure.vsr53 import VSR53PressureSensor
from slow_control.measure.bronkhorst import BronkhorstPressureSensor
from slow_control.measure.bronkhorst import BronkhorstPressureSetpointSensor

slow_control = SlowControl()

vsr53_device = VSR53Device(name="pressure_pipe", port="COM3")

slow_control.add_device(vsr53_device)

slow_control.add_sensor(VSR53PressureSensor(name="pressure_one", device=vsr53_device))


database = Database(
    dbname="slow-control",
    user="admin",
    password="admin",
    host="localhost",
    port=45432,
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

# Create a dictionary to store the last 5 pressure values for each sensor
last_5_pressures = {sensor_name: [] for sensor_name in slow_control.sensors.keys()}
@slow_control.periodic_task(interval_seconds=1)
def periodic_task():
    print(" --- periodic task")
    for sensor_name, sensor in slow_control.sensors.items():
        sensor.update()
        current_pressure = sensor.get_measurement_value()
        print(f"GET {sensor_name}: {current_pressure}")
        print(f"{sensor_name}: {sensor}")
        database.execute_query(sensor.get_table_creation_sql())
        database.execute_query(sensor.get_insert_sql())

        # Update the dictionary with the latest pressure value
        last_5_pressures[sensor_name].append(current_pressure)

        # If there are more than 5 values, remove the oldest one
        if len(last_5_pressures[sensor_name]) > 5:
            last_5_pressures[sensor_name].pop(0)

        # Calculate the average of the last 5 values
        average_pressure = sum(last_5_pressures[sensor_name]) / len(last_5_pressures[sensor_name])

        # If the latest value is more than 5% higher than the average, print a warning
        if current_pressure > average_pressure * 1.05:
            print(f"Warning: Pressure from {sensor_name} is more than 5% higher than the average of the last 5 values.")

if __name__ == "__main__":
    slow_control.run()
