# Form implementation generated from reading ui file 'qt/aqt/forms/stats.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from aqt.utils import tr



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(607, 556)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.web = AnkiWebView(parent=Dialog)
        self.web.setProperty("url", QtCore.QUrl("about:blank"))
        self.web.setObjectName("web")
        self.verticalLayout.addWidget(self.web)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(16, 6, 16, 6)
        self.horizontalLayout_3.setSpacing(8)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groups = QtWidgets.QRadioButton(parent=self.groupBox_2)
        self.groups.setText("deck")
        self.groups.setChecked(True)
        self.groups.setObjectName("groups")
        self.horizontalLayout_2.addWidget(self.groups, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.all = QtWidgets.QRadioButton(parent=self.groupBox_2)
        self.all.setText("collection")
        self.all.setObjectName("all")
        self.horizontalLayout_2.addWidget(self.all, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.month = QtWidgets.QRadioButton(parent=self.groupBox)
        self.month.setText("1 month")
        self.month.setChecked(True)
        self.month.setObjectName("month")
        self.horizontalLayout.addWidget(self.month, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.year = QtWidgets.QRadioButton(parent=self.groupBox)
        self.year.setText("1 year")
        self.year.setObjectName("year")
        self.horizontalLayout.addWidget(self.year, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.life = QtWidgets.QRadioButton(parent=self.groupBox)
        self.life.setText("deck life")
        self.life.setObjectName("life")
        self.horizontalLayout.addWidget(self.life, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 4, -1, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.deckArea = QtWidgets.QWidget(parent=Dialog)
        self.deckArea.setObjectName("deckArea")
        self.horizontalLayout_4.addWidget(self.deckArea, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore  # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(tr.statistics_title())
from aqt.webview import AnkiWebView