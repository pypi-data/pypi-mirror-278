# Form implementation generated from reading ui file 'qt/aqt/forms/reposition.ui'
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
        Dialog.resize(299, 229)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.start = QtWidgets.QSpinBox(parent=Dialog)
        self.start.setMinimum(0)
        self.start.setMaximum(1000000)
        self.start.setProperty("value", 0)
        self.start.setObjectName("start")
        self.gridLayout.addWidget(self.start, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.step = QtWidgets.QSpinBox(parent=Dialog)
        self.step.setMinimum(1)
        self.step.setMaximum(10000)
        self.step.setObjectName("step")
        self.gridLayout.addWidget(self.step, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.randomize = QtWidgets.QCheckBox(parent=Dialog)
        self.randomize.setObjectName("randomize")
        self.verticalLayout.addWidget(self.randomize, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.shift = QtWidgets.QCheckBox(parent=Dialog)
        self.shift.setChecked(False)
        self.shift.setObjectName("shift")
        self.verticalLayout.addWidget(self.shift, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore  # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.start, self.step)
        Dialog.setTabOrder(self.step, self.randomize)
        Dialog.setTabOrder(self.randomize, self.shift)
        Dialog.setTabOrder(self.shift, self.buttonBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(tr.browsing_reposition_new_cards())
        self.label_2.setText(tr.browsing_start_position())
        self.label_3.setText(tr.browsing_step())
        self.randomize.setText(tr.browsing_randomize_order())
        self.shift.setText(tr.browsing_shift_position_of_existing_cards())