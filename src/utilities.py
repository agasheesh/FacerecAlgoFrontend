# -*- coding: utf-8 -*-

import time


class StopWatch(object):

    def __init__(self):
        self.start()

    def start(self):
        self._time = time.time()

    @property
    def elapsed_time(self):
        return (time.time() - self._time) * 1000