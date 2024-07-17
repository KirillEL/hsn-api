from fastapi import BackgroundTasks


class Logging:
    def __init__(self, background_tasks: BackgroundTasks):
        background_tasks.add_task(self._send_log)

    async def _send_log(self):
        pass
