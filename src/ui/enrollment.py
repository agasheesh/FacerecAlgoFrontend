# -*- coding: utf-8 -*-

import cv2
import numpy as np

from PyQt4 import QtCore
from PyQt4 import QtGui

from ui.camera import CameraDevice
from ui.camera import CameraWidget
from facerec import Enroller
from facerec import Enrollment
from utilities import objectDetector


class EnrollmentWidget(QtGui.QWidget):

    enrollmentConcluded = QtCore.pyqtSignal(Enrollment)
    enrollmentCanceled = QtCore.pyqtSignal()

    def __init__(self, cameraDevice, faceDetector, parent=None):
        super(EnrollmentWidget, self).__init__(parent)

        self._verticalLayout = QtGui.QVBoxLayout(self)
        self._verticalLayout.setContentsMargins(0, 0, 0, 0)

        self._cameraWidget = CameraWidget(cameraDevice, parent=self)
        self._cameraWidget.newFrame.connect(self._onNewFrame)
        self._verticalLayout.addWidget(self._cameraWidget)

        self._enrollmentProgressBar = QtGui.QProgressBar(self)
        self._verticalLayout.addWidget(self._enrollmentProgressBar)

        self._buttonsLayout = QtGui.QHBoxLayout()

        self._startEnrollmentButton = QtGui.QPushButton( \
            self.tr('Start &Enrollment'), parent=self)
        self._startEnrollmentButton.clicked.connect(self._startEnrollment)
        self._buttonsLayout.addWidget(self._startEnrollmentButton)

        self._cancelEnrollmentButton = QtGui.QPushButton( \
            self.tr('&Cancel Enrollment'), parent=self)
        self._cancelEnrollmentButton.clicked.connect(self._cancelEnrollment)
        self._buttonsLayout.addWidget(self._cancelEnrollmentButton)

        self._verticalLayout.addLayout(self._buttonsLayout)

        self.setMaximumSize(self.minimumSizeHint())

        self._faceDetector = faceDetector

        self._resetEnrollment()

    def _resetEnrollment(self):
        self._enroller = None
        self._enrollmentProgressBar.setValue(0)
        self._startEnrollmentButton.setEnabled(True)

    @QtCore.pyqtSlot()
    def _startEnrollment(self):
        self._enroller = Enroller()
        self._startEnrollmentButton.setEnabled(False)

    @QtCore.pyqtSlot()
    def _cancelEnrollment(self):
        self._resetEnrollment()
        self.enrollmentCanceled.emit()

    @QtCore.pyqtSlot(np.ndarray)
    def _onNewFrame(self, frame):
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        detectedFace = self._faceDetector(grayFrame)
        if len(detectedFace) == 0:
            return
        detectedFace = detectedFace[0]
        pt1 = (detectedFace[0], detectedFace[1])
        pt2 = (pt1[0] + detectedFace[2], pt1[1] + detectedFace[3])
        cv2.rectangle(frame, pt1, pt2, (255, 0, 0), 2)

        if not self._enroller:
            return

        self._enroller.enroll(grayFrame, detectedFace)
        self._enrollmentProgressBar.setValue(int(self._enroller.progress*100))
        if self._enroller.progress == 1:
            self.enrollmentConcluded.emit(self._enroller.enrollment)
            self._resetEnrollment()


def _main():
    import sys
    app = QtGui.QApplication(sys.argv)
    cameraDevice = CameraDevice(mirrored=True)
    faceDetector = objectDetector("../data/haarcascade_frontalface_alt2.xml")
    enrollmentWidget = EnrollmentWidget(cameraDevice, faceDetector)
    enrollmentWidget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    _main()