# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingswidget.ui'
#
# Created: Fri Aug 26 20:27:48 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SettingsWidget(object):
    def setupUi(self, SettingsWidget):
        SettingsWidget.setObjectName(_fromUtf8("SettingsWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(SettingsWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.usersLabel = QtGui.QLabel(SettingsWidget)
        self.usersLabel.setText(QtGui.QApplication.translate("SettingsWidget", "<h2>&Users:</h2>", None, QtGui.QApplication.UnicodeUTF8))
        self.usersLabel.setObjectName(_fromUtf8("usersLabel"))
        self.verticalLayout.addWidget(self.usersLabel)
        self.verticalLineSep = QtGui.QFrame(SettingsWidget)
        self.verticalLineSep.setFrameShape(QtGui.QFrame.VLine)
        self.verticalLineSep.setFrameShadow(QtGui.QFrame.Sunken)
        self.verticalLineSep.setObjectName(_fromUtf8("verticalLineSep"))
        self.verticalLayout.addWidget(self.verticalLineSep)
        self.usersList = QtGui.QListWidget(SettingsWidget)
        self.usersList.setObjectName(_fromUtf8("usersList"))
        self.verticalLayout.addWidget(self.usersList)
        self.userButtonsLayout = QtGui.QHBoxLayout()
        self.userButtonsLayout.setObjectName(_fromUtf8("userButtonsLayout"))
        self.newUserButton = QtGui.QPushButton(SettingsWidget)
        self.newUserButton.setText(QtGui.QApplication.translate("SettingsWidget", "&New User", None, QtGui.QApplication.UnicodeUTF8))
        self.newUserButton.setObjectName(_fromUtf8("newUserButton"))
        self.userButtonsLayout.addWidget(self.newUserButton)
        self.removeUserButton = QtGui.QPushButton(SettingsWidget)
        self.removeUserButton.setText(QtGui.QApplication.translate("SettingsWidget", "&Remove User", None, QtGui.QApplication.UnicodeUTF8))
        self.removeUserButton.setObjectName(_fromUtf8("removeUserButton"))
        self.userButtonsLayout.addWidget(self.removeUserButton)
        self.verticalLayout.addLayout(self.userButtonsLayout)
        self.usersLineSep = QtGui.QFrame(SettingsWidget)
        self.usersLineSep.setFrameShape(QtGui.QFrame.HLine)
        self.usersLineSep.setFrameShadow(QtGui.QFrame.Sunken)
        self.usersLineSep.setObjectName(_fromUtf8("usersLineSep"))
        self.verticalLayout.addWidget(self.usersLineSep)
        self.securityTolLabel = QtGui.QLabel(SettingsWidget)
        self.securityTolLabel.setText(QtGui.QApplication.translate("SettingsWidget", "&Security tolerance", None, QtGui.QApplication.UnicodeUTF8))
        self.securityTolLabel.setObjectName(_fromUtf8("securityTolLabel"))
        self.verticalLayout.addWidget(self.securityTolLabel)
        self.securityTolSlider = QtGui.QSlider(SettingsWidget)
        self.securityTolSlider.setMaximum(100)
        self.securityTolSlider.setOrientation(QtCore.Qt.Horizontal)
        self.securityTolSlider.setObjectName(_fromUtf8("securityTolSlider"))
        self.verticalLayout.addWidget(self.securityTolSlider)
        self.techniqueLineSep = QtGui.QFrame(SettingsWidget)
        self.techniqueLineSep.setFrameShape(QtGui.QFrame.HLine)
        self.techniqueLineSep.setFrameShadow(QtGui.QFrame.Sunken)
        self.techniqueLineSep.setObjectName(_fromUtf8("techniqueLineSep"))
        self.verticalLayout.addWidget(self.techniqueLineSep)
        self.techniqueLabel = QtGui.QLabel(SettingsWidget)
        self.techniqueLabel.setText(QtGui.QApplication.translate("SettingsWidget", "&Technique:", None, QtGui.QApplication.UnicodeUTF8))
        self.techniqueLabel.setObjectName(_fromUtf8("techniqueLabel"))
        self.verticalLayout.addWidget(self.techniqueLabel)
        self.techniqueCombo = QtGui.QComboBox(SettingsWidget)
        self.techniqueCombo.setObjectName(_fromUtf8("techniqueCombo"))
        self.verticalLayout.addWidget(self.techniqueCombo)
        self.usersLabel.setBuddy(self.usersList)
        self.securityTolLabel.setBuddy(self.securityTolSlider)
        self.techniqueLabel.setBuddy(self.techniqueCombo)

        self.retranslateUi(SettingsWidget)
        QtCore.QMetaObject.connectSlotsByName(SettingsWidget)

    def retranslateUi(self, SettingsWidget):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SettingsWidget = QtGui.QWidget()
    ui = Ui_SettingsWidget()
    ui.setupUi(SettingsWidget)
    SettingsWidget.show()
    sys.exit(app.exec_())

