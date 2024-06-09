import sched
import threading
import time

class CompositeJobDisposable:
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.executor = threading.Thread(target=self.scheduler.run)
        self.list = []

        def purge():
            self.executor = threading.Thread(target=self.scheduler.run)
            self.executor.start()
            if len(self.list) > 0:
                filtered = [job for job in self.list if job.isCancelled() or job.isCompleted()]
                for job in filtered:
                    self.list.remove(job)

        self.scheduler.enter(120, 1, purge, ())
        self.scheduler.run()

    def add(self, job):
        if job:
            self.list.append(job)

    def remove(self, job):
        self.list.remove(job)

    def cancel(self):
        for job in self.list:
            try:
                if job.isActive():
                    job.cancel()
            except:
                pass
        self.list.clear()
import sched
import threading
import time

class CompositeJobDisposable:
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.executor = threading.Thread(target=self.scheduler.run)
        self.list = []

        def purge():
            self.executor = threading.Thread(target=self.scheduler.run)
            self.executor.start()
            if len(self.list) > 0:
                filtered = [job for job in self.list if job.isCancelled() or job.isCompleted()]
                for job in filtered:
                    self.list.remove(job)

        self.scheduler.enter(120, 1, purge, ())
        self.scheduler.run()

    def add(self, job):
        if job:
            self.list.append(job)

    def remove(self, job):
        self.list.remove(job)

    def cancel(self):
        for job in self.list:
            try:
                if job.isActive():
                    job.cancel()
            except:
                pass
        self.list.clear()
