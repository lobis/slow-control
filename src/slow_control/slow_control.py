from __future__ import annotations

import concurrent.futures

from fastapi import FastAPI


class SlowControl:
    def __init__(self):
        self.app = FastAPI()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    def route(self, path):
        def decorator(func):
            self.app.add_api_route(path, func)
            return func

        return decorator

    def background_task(self, func):
        print("adding background task")
        # run task in the thread pool, start it immediately
        self.executor.submit(func)

    def run(self, host="localhost", port=8000):
        import uvicorn

        uvicorn.run(self.app, host=host, port=port)
