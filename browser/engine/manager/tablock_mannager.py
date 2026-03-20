import asyncio


class TabLock:
    def __init__(self):
        self.queue = []
        self.active = False

    async def acquire(self, timeout_ms: int):
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        entry = {
            "future": future,
            "timer": None,
        }

        # timeout handler
        def on_timeout():
            if not future.done():
                try:
                    self.queue.remove(entry)
                except ValueError:
                    pass
                future.set_exception(Exception("Tab lock queue timeout"))

        entry["timer"] = loop.call_later(timeout_ms / 1000, on_timeout)

        self.queue.append(entry)
        self._try_next()

        return await future

    def release(self):
        self.active = False
        self._try_next()

    def _try_next(self):
        if self.active or not self.queue:
            return

        self.active = True
        entry = self.queue.pop(0)

        entry["timer"].cancel()

        if not entry["future"].done():
            entry["future"].set_result(None)

    def drain(self):
        self.active = True

        for entry in self.queue:
            entry["timer"].cancel()
            if not entry["future"].done():
                entry["future"].set_exception(Exception("Tab destroyed"))

        self.queue.clear()

tab_locks = {}