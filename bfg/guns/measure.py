from contextlib import contextmanager
import time
from collections import namedtuple

Sample = namedtuple(
    'Sample', 'ts,bfg,marker,rt,error,code,delay,scenario,action,ext')


class StopWatch(object):
    def __init__(self, task):
        self.task = task
        self.start_time = time.time()
        self.end_time = self.start_time
        self.error = False
        self.code = None
        self.scenario = None
        self.action = None
        self.ext = {}
        self.stopped = False

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if not self.stopped:
            self.stopped = True
            self.end_time = time.time()

    def set_error(self, code=None):
        if code:
            self.set_code(code)
        self.error = True

    def set_code(self, code):
        self.code = code

    def as_sample(self):
        overall = (self.end_time - self.start_time) * 1000
        return Sample(
            int(self.start_time),
            self.task.bfg,
            self.task.marker,
            overall,
            self.error,
            self.code,
            (self.start_time - self.task.ts) * 1000,
            self.scenario,
            self.action,
            self.ext,
        )


@contextmanager
def measure(task, results):
    sw = StopWatch(task)
    yield sw
    sw.stop()
    results.put(sw.as_sample())
