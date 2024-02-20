from __future__ import annotations

from slow_control import SlowControl


def test_slow_control():
    print("starting test slow-control")

    # Example usage of the framework
    slow_control = SlowControl()

    state = {"counter": 0}

    @slow_control.route("/")
    async def root():
        return state

    @slow_control.background_task
    def background_task():
        while True:
            state["counter"] += 1
            print("counter", state["counter"])
            import time

            time.sleep(1)

    slow_control.run()
