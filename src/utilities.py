# -*- coding: utf-8 -*-

import cv


__all__ = ["StopWatch",
           "objectDetector"]


class StopWatch(object):

    def __init__(self):
        self.start()

    def start(self):
        self._time = cv.GetTickCount()

    @property
    def elapsedTime(self):
        return ((cv.GetTickCount() - self._time) / cv.GetTickFrequency()) / 1e6


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

    try:
        classifier = cv.Load(detectorFilename)
    except:
        raise ValueError("The detector could not be loaded.")

    def detector(img, biggestObj=True):
        assert img.nChannels == 1, "The input image must be 1-channel."

        w, h = cv.GetSize(img)
        subsampledW, subsampledH = int(w*sf), int(h*sf)
        minSubsampledDim = min(subsampledW, subsampledH)
        minObjDim = int(minSubsampledDim*minObjRelDim)
        maxObjDim = int(minSubsampledDim*maxObjRelDim)

        subsampledImg = cv.CreateImage((subsampledW, subsampledH), img.depth,
                                       img.nChannels)
        cv.Resize(img, subsampledImg)

        detectorMode = cv.CV_HAAR_FIND_BIGGEST_OBJECT if biggestObj else \
            cv.CV_HAAR_DO_CANNY_PRUNING

        objs = cv.HaarDetectObjects(subsampledImg, classifier,
                                    cv.CreateMemStorage(),
                                    classifierPyrScaleFactor, minNeighbors,
                                    detectorMode, (minObjDim, minObjDim))

        ret = []
        for (x, y, w, h), _ in objs:
            d = w
            if d > maxObjDim:
                continue
            ret.append((int(x/sf), int(y/sf), int(d/sf), int(d/sf)))
        return ret

    return detector