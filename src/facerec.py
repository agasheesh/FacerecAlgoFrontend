# -*- coding: utf-8 -*-

import cv2
import os
import uuid

from utilities import getApplicationPath
from utilities import StopWatch


__all__ = ["Enrollment",
           "Enroller"]


class Enrollment(object):

    def __init__(self, id, samples):
        self.id = id
        self.samples = samples

    def getProcessedFaces(self, f):
        ret = []
        for path, bbox in self.samples.items():
            frame = cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            if frame:
                ret.append(f(frame, bbox))
        return ret


class Enroller(object):

    def __init__(self, samplesToAcquire=30, intervalBtwSamples=0.5):

        assert samplesToAcquire > 0, "'samplesToAcquire' must be > 0."
        assert intervalBtwSamples > 0, "'intervalBtwSamples' must be > 0."

        self._samplesToAcquire = samplesToAcquire
        self._intervalBtwSamples = intervalBtwSamples

        self._path = os.path.join(getApplicationPath(), "enrollments",
                                  uuid.uuid4().hex)

        try:
            os.makedirs(self._path)
        except os.error as e:
            raise IOError("%s: '%s'" % (e.strerror, e.filename))

        self._samples = {}
        self._stopWatch = StopWatch()

    @property
    def progress(self):
        return float(len(self._samples)) / self._samplesToAcquire

    @property
    def enrollment(self):
        if self.progress < 1:
            return None
        return Enrollment(os.path.basename(self._path), self._samples)

    def enroll(self, frame, bbox):
        if self.progress < 1 and self._stopWatch.elapsedTime >= \
                self._intervalBtwSamples:
            path = os.path.join(self._path, "%03d.png" % len(self._samples))
            if not cv2.imwrite(path, frame):
                raise IOError("Could not enroll sample '%s'." % path)
            self._samples[path] = bbox
            self._stopWatch.start()