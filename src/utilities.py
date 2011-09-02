# -*- coding: utf-8 -*-

import cv2
import os


__all__ = ["StopWatch",
           "objectDetector",
           "getApplicationPath"]


class StopWatch(object):

    def __init__(self):
        self.start()

    def start(self):
        self._time = cv2.getTickCount()

    @property
    def elapsedTime(self):
        return (cv2.getTickCount() - self._time) / cv2.getTickFrequency()


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

def getApplicationPath():
    appPath = os.path.join(os.path.expanduser("~"), ".VIISAR",
                           "Face Recognition Platform")
    try:
        if not os.path.exists(appPath):
            os.makedirs(appPath)
    except os.error as e:
        raise IOError("%s: '%s'" % (e.strerror, e.filename))
    return appPath