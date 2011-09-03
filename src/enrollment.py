# -*- coding: utf-8 -*-

import cv2
import os
import shutil
import uuid

from utilities import getApplicationPath
from utilities import StopWatch


__all__ = ["Enrollment",
           "Enroller"]


class Enrollment(object):

    def __init__(self, id, bboxes):
        self._path = os.path.join(Enroller._BASE_PATH, id)
        self._bboxes = bboxes

    @property
    def id(self):
        return os.path.basename(self._path)

    def getProcessedFaces(self, f):
        ret = []
        for i, bbox in enumerate(self._bboxes):
            path = os.path.join(self._path,
                                "%d.%s" % (i, Enroller._SAMPLES_FORMAT))
            frame = cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            if not frame is None:
                ret.append(f(frame, bbox))
        return ret

    def delete(self):
        shutil.rmtree(self._path, ignore_errors=True)


class Enroller(object):

    _BASE_PATH = os.path.join(getApplicationPath(), "enrollments")
    _SAMPLES_FORMAT = "png"

    def __init__(self, samplesToAcquire=30, intervalBtwSamples=0.5):

        assert samplesToAcquire > 0, "'samplesToAcquire' must be > 0."
        assert intervalBtwSamples > 0, "'intervalBtwSamples' must be > 0."

        self._samplesToAcquire = samplesToAcquire
        self._intervalBtwSamples = intervalBtwSamples

        self._path = os.path.join(self._BASE_PATH, uuid.uuid4().hex)

        try:
            os.makedirs(self._path)
        except os.error as e:
            raise IOError("%s: '%s'" % (e.strerror, e.filename))

        self._bboxes = []
        self._stopWatch = StopWatch()

    def __del__(self):
        if self.progress < 1:
            shutil.rmtree(self._path, ignore_errors=True)

    @property
    def progress(self):
        return float(len(self._bboxes)) / self._samplesToAcquire

    @property
    def enrollment(self):
        if self.progress < 1:
            return None
        return Enrollment(os.path.basename(self._path), self._bboxes)

    def enroll(self, frame, bbox):
        if self.progress < 1 and self._stopWatch.elapsedTime >= \
                self._intervalBtwSamples:
            path = os.path.join(self._path, "%d.%s" % (len(self._bboxes),
                                                       self._SAMPLES_FORMAT))
            if not cv2.imwrite(path, frame):
                raise IOError("Could not enroll sample '%s'." % path)
            self._bboxes.append(bbox)
            self._stopWatch.start()