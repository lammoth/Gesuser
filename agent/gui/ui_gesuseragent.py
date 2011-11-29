# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gesuser_agent.ui'
#
# Created: Thu May 19 13:43:23 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_GesuserAgent(object):
    def setupUi(self, GesuserAgent):
        GesuserAgent.setObjectName("GesuserAgent")
        GesuserAgent.resize(321, 374)
        GesuserAgent.setMinimumSize(QtCore.QSize(321, 374))
        GesuserAgent.setMaximumSize(QtCore.QSize(321, 374))
        self.centralwidget = QtGui.QWidget(GesuserAgent)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.toolsLabel = QtGui.QLabel(self.centralwidget)
        self.toolsLabel.setObjectName("toolsLabel")
        self.gridLayout.addWidget(self.toolsLabel, 0, 0, 1, 1)
        self.toolsList = QtGui.QListWidget(self.centralwidget)
        self.toolsList.setObjectName("toolsList")
        self.gridLayout.addWidget(self.toolsList, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.connectBtn = QtGui.QPushButton(self.centralwidget)
        self.connectBtn.setObjectName("connectBtn")
        self.horizontalLayout_2.addWidget(self.connectBtn)
        self.disconnectBtn = QtGui.QPushButton(self.centralwidget)
        self.disconnectBtn.setObjectName("disconnectBtn")
        self.horizontalLayout_2.addWidget(self.disconnectBtn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        GesuserAgent.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(GesuserAgent)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 321, 23))
        self.menubar.setObjectName("menubar")
        GesuserAgent.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(GesuserAgent)
        self.statusbar.setObjectName("statusbar")
        GesuserAgent.setStatusBar(self.statusbar)

        self.retranslateUi(GesuserAgent)
        QtCore.QMetaObject.connectSlotsByName(GesuserAgent)

    def retranslateUi(self, GesuserAgent):
        GesuserAgent.setWindowTitle(QtGui.QApplication.translate("GesuserAgent", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsLabel.setText(QtGui.QApplication.translate("GesuserAgent", "Tools list", None, QtGui.QApplication.UnicodeUTF8))
        self.connectBtn.setText(QtGui.QApplication.translate("GesuserAgent", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.disconnectBtn.setText(QtGui.QApplication.translate("GesuserAgent", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GesuserAgent = QtGui.QMainWindow()
    ui = Ui_GesuserAgent()
    ui.setupUi(GesuserAgent)
    GesuserAgent.show()
    sys.exit(app.exec_())

