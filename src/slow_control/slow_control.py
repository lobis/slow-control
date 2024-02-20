from __future__ import annotations

import concurrent.futures
import time

import uvicorn
from fastapi import FastAPI


class SlowControl:
    def __init__(self):
        self.app = FastAPI()
        self.executor = None
        self.background_tasks = []
        self._exit = False

    def route(self, path):
        def decorator(func):
            self.app.add_api_route(path, func)
            return func

        return decorator

    def background_task(self, func):
        self.background_tasks.append(func)

    # TODO: do not block
    def periodic_task(self, interval_seconds):
        # run a sync function every interval_seconds, exit if _exit is True
        def decorator(func):
            def wrapper():
                while not self._exit:
                    func()
                    time.sleep(interval_seconds)

            self.background_tasks.append(wrapper)
            return wrapper

        return decorator

    def run(self, host="localhost", port=8000):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self._exit = False

        for task in self.background_tasks:
            self.executor.submit(task)

        uvicorn.run(self.app, host=host, port=port)
        self._exit = True
        self.executor.shutdown()
