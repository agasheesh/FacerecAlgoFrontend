# -*- coding: utf-8 -*-

import time


__all__ = ["StopWatch"]


class StopWatch(object):

    def __init__(self):
        self.start()

    def start(self):
        self._time = time.time()

    @property
    def elapsedTime(self):
        return (time.time() - self._time) * 1000