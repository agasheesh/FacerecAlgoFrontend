# -*- coding: utf-8 -*-

import cv
import cv2
import numpy as np

from PyQt4 import QtCore
from PyQt4 import QtGui


__all__ = ["OpenCVQImage",
           "CameraDevice",
           "CameraWidget"]


class OpenCVQImage(QtGui.QImage):

    def __init__(self, rgbImg):

        assert rgbImg.ndim == 3 and rgbImg.shape[2] == 3, \
            "The input must be a 3-channel image."
        assert rgbImg.dtype == np.uint8, "The input must be an 8-bit image."

        self._imgData = rgbImg.tostring()
        h, w = rgbImg.shape[0:2]
        super(OpenCVQImage, self).__init__(self._imgData, w, h,
                                           QtGui.QImage.Format_RGB888)


class CameraDevice(QtCore.QObject):

    _DEFAULT_FPS = 30

    newFrame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, cameraId=0, mirrored=False, parent=None):
        super(CameraDevice, self).__init__(parent)

        self.mirrored = mirrored

        self._cameraDevice = cv2.VideoCapture(cameraId)
        if not self._cameraDevice.isOpened():
            raise IOError("Could not open camera '%d'.", cameraId)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(1000/self.fps)

        self.paused = False

    @QtCore.pyqtSlot()
    def _queryFrame(self):
        _, frame = self._cameraDevice.read()
        if frame is None:
            return
        if self.mirrored:
            frame = cv2.flip(frame, 1)
        # it's assumed the frame is in BGR format
        self.newFrame.emit(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    @property
    def paused(self):
        return not self._timer.isActive()

    @paused.setter
    def paused(self, p):
        if p:
            self._timer.stop()
        else:
            self._timer.start()

    @property
    def fps(self):
        fps = int(self._cameraDevice.get(cv.CV_CAP_PROP_FPS))
        if not fps > 0:
            fps = self._DEFAULT_FPS
        return fps

    @property
    def frameSize(self):
        w = self._cameraDevice.get(cv.CV_CAP_PROP_FRAME_WIDTH)
        h = self._cameraDevice.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
        return int(w), int(h)

    @frameSize.setter
    def frameSize(self, newSize):
        w, h = newSize
        self._cameraDevice.set(cv.CV_CAP_PROP_FRAME_WIDTH, w)
        self._cameraDevice.set(cv.CV_CAP_PROP_FRAME_HEIGHT, h)


class CameraWidget(QtGui.QWidget):

    newFrame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, cameraDevice, parent=None):
        super(CameraWidget, self).__init__(parent)

        self._frame = None

        self._cameraDevice = cameraDevice
        self._cameraDevice.newFrame.connect(self._onNewFrame)

        w, h = self._cameraDevice.frameSize
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

    @QtCore.pyqtSlot(cv.iplimage)
    def _onNewFrame(self, frame):
        self._frame = frame.copy()
        self.newFrame.emit(self._frame)
        self.update()

    def changeEvent(self, e):
        if e.type() == QtCore.QEvent.EnabledChange:
            self._cameraDevice.paused = not self.isEnabled()

    def paintEvent(self, e):
        if self._frame is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), OpenCVQImage(self._frame))


def _main():

    @QtCore.pyqtSlot(cv.iplimage)
    def onNewFrame(frame):
        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR, frame)
        msg = "processed frame"
        h, w = frame.shape[0:2]
        tsize, baseline = cv2.getTextSize(msg, cv2.FONT_HERSHEY_PLAIN, 2, 2)
        tpt = (w - tsize[0]) / 2, (h - tsize[1]) / 2
        cv2.putText(frame, msg, tpt, cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    import sys

    app = QtGui.QApplication(sys.argv)

    cameraDevice = CameraDevice(mirrored=True)

    cameraWidget1 = CameraWidget(cameraDevice)
    cameraWidget1.newFrame.connect(onNewFrame)
    cameraWidget1.show()

    cameraWidget2 = CameraWidget(cameraDevice)
    cameraWidget2.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    _main()