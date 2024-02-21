from __future__ import annotations

import asyncio
import threading

import uvicorn
from fastapi import FastAPI

from slow_control.devices.device import Device
from slow_control.measure.sensor import Sensor


class SlowControl:
    def __init__(self):
        self._sensors = dict()
        self._devices = dict()

        self.app = FastAPI()
        self.background_tasks = []
        self._exit = False

    def add_device(self, name: str, device: Device):
        self._devices[name] = device

    def add_sensor(self, name: str, sensor: Sensor):
        self._sensors[name] = sensor

    def get_device(self, name: str) -> Device:
        return self._devices[name]

    def get_sensor(self, name: str) -> Sensor:
        return self._sensors[name]

    def route(self, path):
        def decorator(func):
            self.app.add_api_route(path, func)
            return func

        return decorator

    # TODO: do not block
    def periodic_task(self, interval_seconds):
        def decorator(func):
            async def async_wrapper():
                while not self._exit:
                    asyncio.get_running_loop().run_in_executor(None, func)
                    await asyncio.sleep(interval_seconds)

            self.background_tasks.append(async_wrapper)
            return func

        return decorator

    def run(self, host="localhost", port=8000):
        self._exit = False

        async def run_all():
            tasks = [func() for func in self.background_tasks]
            await asyncio.gather(*tasks)

        thread = threading.Thread(target=asyncio.run, args=(run_all(),))
        thread.start()
        uvicorn.run(self.app, host=host, port=port)

        self._exit = True
        thread.join()
