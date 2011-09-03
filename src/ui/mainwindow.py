# -*- coding: utf-8 -*-

import cv2
import numpy as np

from PyQt4 import QtCore
from PyQt4 import QtGui

from ui.camera import CameraDevice
from ui.camera import CameraWidget
from ui.enrollment import EnrollmentWidget
from ui.settings import SettingsWidget
from facerecognizer import FaceRecognizer
from utilities import Enrollment
from utilities import objectDetector


__all__ = ["MainWindow"]


class MainWindow(QtGui.QMainWindow):

    _APP_TITLE = "VIISAR - Face Recognition"
    _LOGO_PATH = "../data/viisar_logo.png"
    _FACE_DETECTOR_PATH = "../data/haarcascade_frontalface_alt2.xml"

    def __init__(self, faceRecognizer, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle(self._APP_TITLE)

        self._centralWidget = QtGui.QWidget(self)
        self._horizontalLayout = QtGui.QHBoxLayout(self._centralWidget)

        self._leftPanelLayout = QtGui.QVBoxLayout()

        self._logo = QtGui.QLabel(self)
        self._logo.setPixmap(QtGui.QPixmap(self._LOGO_PATH))
        self._logo.setAlignment(QtCore.Qt.AlignCenter)
        self._leftPanelLayout.addWidget(self._logo)

        self._faceRecognizer = faceRecognizer
        self._settingsWidget = SettingsWidget(self._centralWidget)
        self._settingsWidget.users = self._faceRecognizer.users
        self._settingsWidget.securityTol = \
            int(self._faceRecognizer.securityTol*100)
        self._settingsWidget.techniques = self._faceRecognizer.techniquesNames
        self._onTechniqueChanged(self._settingsWidget.selectedTechnique)
        self._settingsWidget.newUserButtonClicked.connect(self._enrollmentMode)
        self._settingsWidget.removeUserButtonClicked.connect( \
            self._onRemoveUserButtonClicked)
        self._settingsWidget.securityTolChanged.connect( \
            self._onSecurityTolChanged)
        self._settingsWidget.techniqueChanged.connect( \
            self._onTechniqueChanged)
        self._leftPanelLayout.addWidget(self._settingsWidget)

        self._horizontalLayout.addLayout(self._leftPanelLayout)

        self._verticalLineSep = QtGui.QFrame(self._centralWidget)
        self._verticalLineSep.setFrameShape(QtGui.QFrame.VLine)
        self._verticalLineSep.setFrameShadow(QtGui.QFrame.Sunken)
        self._horizontalLayout.addWidget(self._verticalLineSep)

        self._cameraDevice = CameraDevice(mirrored=True)
        self._faceDetector = objectDetector(self._FACE_DETECTOR_PATH)

        self._rightPanelLayout = QtGui.QStackedLayout()

        self._faceRecognitionWidget = CameraWidget(self._cameraDevice, \
            self._centralWidget)
        self._faceRecognitionWidget.newFrame.connect( \
            self._faceRecognition)
        self._rightPanelLayout.addWidget(self._faceRecognitionWidget)

        self._enrollmentWidget = EnrollmentWidget(self._cameraDevice, \
            self._faceDetector, parent=self._centralWidget)
        self._enrollmentWidget.enrollmentConcluded.connect( \
            self._onEnrollmentConcluded)
        self._enrollmentWidget.enrollmentCanceled.connect( \
            self._faceRecognitionMode)
        self._rightPanelLayout.addWidget(self._enrollmentWidget)

        self._faceRecognitionMode()
        self._horizontalLayout.addLayout(self._rightPanelLayout)

        self.setCentralWidget(self._centralWidget)

    @QtCore.pyqtSlot()
    def _enrollmentMode(self):
        self._faceRecognitionWidget.setEnabled(False)
        self._settingsWidget.setEnabled(False)
        self._enrollmentWidget.setEnabled(True)
        self._rightPanelLayout.setCurrentWidget(self._enrollmentWidget)

    @QtCore.pyqtSlot()
    def _faceRecognitionMode(self):
        self._enrollmentWidget.setEnabled(False)
        self._settingsWidget.setEnabled(True)
        self._faceRecognitionWidget.setEnabled(True)
        self._rightPanelLayout.setCurrentWidget(self._faceRecognitionWidget)

    @QtCore.pyqtSlot()
    def _onRemoveUserButtonClicked(self):
        selectedUser = unicode(self._settingsWidget.selectedUser)
        if selectedUser is not None:
            self._faceRecognizer.removeUser(selectedUser)
            self._settingsWidget.removeUser(selectedUser)

    @QtCore.pyqtSlot(int)
    def _onSecurityTolChanged(self, newValue):
        self._faceRecognizer.securityTol = newValue * 1e-2

    @QtCore.pyqtSlot(unicode)
    def _onTechniqueChanged(self, technique):
        self._faceRecognizer.selectTechniqueByName(unicode(technique))

    @QtCore.pyqtSlot(np.ndarray)
    def _faceRecognition(self, frame):
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        detectedFaces = self._faceDetector(grayFrame, False)
        h, w = frame.shape[0:2]
        for bbox in detectedFaces:
            pt1 = (bbox[0], bbox[1])
            pt2 = (pt1[0] + bbox[2], pt1[1] + bbox[3])
            cv2.rectangle(frame, pt1, pt2, (255, 0, 0), 2)

            confidence, user = self._faceRecognizer.identify(grayFrame, bbox)
            if user is not None:
                msg = "%s (%.2f)" % (user, confidence)
            else:
                msg = "unknown user"

            tsize, _ = cv2.getTextSize(msg, cv2.FONT_HERSHEY_DUPLEX, 1, 1)
            tpt = pt1[0] - (tsize[0] - bbox[2]) / 2, pt2[1] + tsize[1]
            cv2.putText(frame, msg, tpt, cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 0, 0))

    @QtCore.pyqtSlot(Enrollment)
    def _onEnrollmentConcluded(self, enrollment):
        while True:
            userNameDlgRet = QtGui.QInputDialog.getText(self,
                self.tr("Enrollment"), self.tr("Enter an user name:"))
            if not userNameDlgRet[1]:
                enrollment.delete()
                self._faceRecognitionMode()
                break
            try:
                userName = unicode(userNameDlgRet[0]).strip()
                if not userName:
                    QtGui.QMessageBox.warning(self, self.tr("Enrollment error"),
                        self.tr("The user name can't be empty."))
                    continue
                self._faceRecognizer.addUser(userName, enrollment)
                self._settingsWidget.addUser(userName)
                self._faceRecognitionMode()
                break
            except ValueError:
                QtGui.QMessageBox.warning(self, self.tr("Enrollment error"),
                    self.tr("Invalid user name. Check if it's already being "
                        "used."))


def _main():
    import sys
    app = QtGui.QApplication(sys.argv)
    faceRecognizer = FaceRecognizer("./plugins")
    mainWindow = MainWindow(faceRecognizer)
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    _main()