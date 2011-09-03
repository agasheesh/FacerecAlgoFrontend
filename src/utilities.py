# -*- coding: utf-8 -*-

import cv2
import os
import shutil
import uuid


__all__ = ["StopWatch",
           "Enrollment",
           "Enroller",
           "objectDetector",
           "getApplicationPath"]


def getApplicationPath():
    appPath = os.path.join(os.path.expanduser("~"), ".VIISAR",
                           "Face Recognition Platform")
    try:
        if not os.path.exists(appPath):
            os.makedirs(appPath)
    except os.error as e:
        raise IOError("%s: '%s'" % (e.strerror, e.filename))
    return appPath


class StopWatch(object):

    def __init__(self):
        self.start()

    def start(self):
        self._time = cv2.getTickCount()

    @property
    def elapsedTime(self):
        return (cv2.getTickCount() - self._time) / cv2.getTickFrequency()


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


def objectDetector(detectorFilename, minObjRelDim=0.2, maxObjRelDim=1,
                   classifierPyrScaleFactor=1.1, minNeighbors=3,
                   subsamplingScaleFactor=0.4):

    assert minObjRelDim < maxObjRelDim, \
        "'minObjRelDim' must be < 'maxObjRelDim'."
    assert minObjRelDim >= 0 and minObjRelDim < 1, \
        "'minObjRelDim' must be in [0, 1) interval."
    assert maxObjRelDim > 0 and maxObjRelDim <= 1, \
        "'maxObjRelDim' must be in (0, 1] interval."
    assert classifierPyrScaleFactor > 1, \
        "'classifierPyrScaleFactor' must be > 1."
    assert minNeighbors > 0, "'minNeighbors' must be > 0."
    assert subsamplingScaleFactor > 0 and subsamplingScaleFactor <= 1, \
        "'subsamplingScaleFactor' must be in (0, 1] interval."
    sf = subsamplingScaleFactor

    classifier = cv2.CascadeClassifier(detectorFilename)
    if classifier.empty():
        raise ValueError("The detector '%s' could not be loaded." % \
            detectorFilename)

    def detector(img, biggestObj=True):
        assert img.ndim == 2, "The input must be an 1-channel image."

        h, w = img.shape
        subsampledW, subsampledH = int(w*sf), int(h*sf)
        minSubsampledDim = min(subsampledW, subsampledH)
        minObjDim = int(minSubsampledDim*minObjRelDim)
        maxObjDim = int(minSubsampledDim*maxObjRelDim)
        subsampledImg = cv2.resize(img, (subsampledW, subsampledH))

        detectorMode = cv2.CASCADE_FIND_BIGGEST_OBJECT if biggestObj else \
            cv2.CASCADE_DO_CANNY_PRUNING

        objs = classifier.detectMultiScale(subsampledImg,
                                           classifierPyrScaleFactor,
                                           minNeighbors,
                                           detectorMode, (minObjDim, minObjDim))

        ret = []
        for x, y, w, h in objs:
            if max(w, h) > maxObjDim:
                continue
            ret.append((int(x/sf), int(y/sf), int(w/sf), int(h/sf)))
        return ret

    return detector