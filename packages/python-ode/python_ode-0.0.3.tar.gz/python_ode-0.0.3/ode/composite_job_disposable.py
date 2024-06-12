import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List

class CompositeJobDisposable:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.jobs: List[asyncio.Task] = []
        # asyncio.create_task(self.purge())

    def add(self, job: asyncio.Task):
        if job:
            self.executor.submit(self.jobs.append, job)

    def remove(self, job: asyncio.Task):
        self.executor.submit(self.jobs.remove, job)

    def cancel(self):
        def _cancel_all():
            for job in self.jobs:
                if not job.done():
                    job.cancel()
            self.jobs.clear()

        self.executor.submit(_cancel_all)

    async def purge(self):
        while True:
            await asyncio.sleep(120)
            if self.jobs:
                completed = [job for job in self.jobs if job.done()]
                for job in completed:
                    self.jobs.remove(job)