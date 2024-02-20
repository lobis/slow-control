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
    def background_task(n=10):
        state["counter"] += n
        print("counter", state["counter"])

    @slow_control.periodic_task(interval_seconds=1)
    def periodic_task():
        print("periodic_task")

    slow_control.run()
