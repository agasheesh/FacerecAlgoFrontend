# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

from ui_settingswidget import Ui_SettingsWidget


class SettingsWidget(QtGui.QWidget, Ui_SettingsWidget):

    newUserButtonClicked = QtCore.pyqtSignal()
    removeUserButtonClicked = QtCore.pyqtSignal()
    securityTolChanged = QtCore.pyqtSignal(int)
    techniqueChanged = QtCore.pyqtSignal(unicode)

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.setupUi(self)

        self._updateSecurityTolLabel()

        self.newUserButton.clicked.connect(self.newUserButtonClicked)
        self.removeUserButton.clicked.connect(self.removeUserButtonClicked)
        self.securityTolSlider.valueChanged.connect(self._onSecurityTolChanged)
        self.techniqueCombo.currentIndexChanged.connect( \
            self._onTechniqueComboChanged)

    def _updateSecurityTolLabel(self):
        self.securityTolLabel.setText(self.tr("&Security tolerance: %1%").arg( \
            self.securityTol))

    @QtCore.pyqtSlot(int)
    def _onSecurityTolChanged(self, newValue):
        self._updateSecurityTolLabel()
        self.securityTolChanged.emit(newValue)

    @QtCore.pyqtSlot(int)
    def _onTechniqueComboChanged(self, index):
        self.techniqueChanged.emit(self.selectedTechnique)

    def addUser(self, user):
        user = user.strip()
        if not user: return
        if self.usersList.findItems(user, QtCore.Qt.MatchExactly):
            raise ValueError(self.tr("duplicated user"))
        self.usersList.addItem(user)

    def removeUser(self, user):
        match = self.usersList.findItems(user, QtCore.Qt.MatchExactly)
        if match:
            self.usersList.takeItem(self.usersList.row(match[0]))

    @property
    def users(self):
        return [u.text() for u in self.usersList.findItems("*", \
            QtCore.Qt.MatchWildcard)]

    @users.setter
    def users(self, users):
        self.usersList.clear()
        self.usersList.addItems(filter(len, map(str.strip, set(users))))

    @property
    def selectedUser(self):
        selectedUser = self.usersList.currentItem()
        return selectedUser.text() if selectedUser else None

    @selectedUser.setter
    def selectedUser(self, user):
        match = self.usersList.findItems(user, QtCore.Qt.MatchExactly)
        if match:
            match[0].setSelected(True)

    @property
    def securityTol(self):
        return self.securityTolSlider.value()

    @securityTol.setter
    def securityTol(self, newValue):
        self.securityTolSlider.setValue(newValue)

    def addTechnique(self, technique):
        technique = technique.strip()
        if not technique: return
        if self.techniqueCombo.findText(technique) > -1:
            raise ValueError(self.tr("duplicated technique"))
        self.techniqueCombo.addItem(technique)

    def removeTechnique(self, technique):
        techniqueIndex = self.techniqueCombo.findText(technique)
        if techniqueIndex > -1:
            self.techniqueCombo.removeItem(techniqueIndex)

    @property
    def techniques(self):
        return [self.techniqueCombo.itemText(i) for i in \
            xrange(0, self.techniqueCombo.count())]

    @techniques.setter
    def techniques(self, techniques):
        self.techniqueCombo.clear()
        self.techniqueCombo.addItems(filter(len, map(str.strip, \
            set(techniques))))

    @property
    def selectedTechnique(self):
        return self.techniqueCombo.currentText()

    @selectedTechnique.setter
    def selectedTechnique(self, technique):
        techniqueIndex = self.techniqueCombo.findText(technique)
        if techniqueIndex > -1:
            self.techniqueCombo.setCurrentIndex(techniqueIndex)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    form = SettingsWidget()
    form.show()
    sys.exit(app.exec_())