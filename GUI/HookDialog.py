# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HookDialog.ui'
#
# Created: Tue Mar 19 18:38:34 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_HookDialog(QtGui.QDialog):
    """
    Largely generated dialog to choose optional forum hooks when saving a 
    cube as a text file.
    """
    
    def __init__(self, parent, mainFrameParent):
        """Additional initializer."""
        
        super(Ui_HookDialog, self).__init__(parent)
        self.setupUi(self)
        self.__connectEvents()
    
#==========================================================================#
#                              Events                                      #
#==========================================================================#
#-------------------------------------------------------------------------------
    def __connectEvents(self):
        """
        Sets up event handling for the dialog.
        """
        
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        
#==========================================================================#
#                              Generated                                   #
#==========================================================================#

#==========================================================================#
#                              Other                                       #
#==========================================================================#

#-------------------------------------------------------------------------------
    def getHooks(self):
        """
        Returns the user-specified hooks from the line edits. This method is
        called by the mainwindow if this dialog is accepted.
        """
        
        return str(self.autocardFHookTextEdit.text()), \
               str(self.autocardBHookTextEdit.text()), \
               str(self.spoilerFHookTextEdit.text()), \
               str(self.spoilerBHookTextEdit.text())

#-------------------------------------------------------------------------------
    def setupUi(self, HookDialog):
        HookDialog.setObjectName(_fromUtf8("HookDialog"))
        HookDialog.resize(453, 252)
        HookDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(HookDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.spoilerBHook = QtGui.QLabel(HookDialog)
        self.spoilerBHook.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spoilerBHook.setFont(font)
        self.spoilerBHook.setObjectName(_fromUtf8("spoilerBHook"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.spoilerBHook)
        self.spoilerFHook = QtGui.QLabel(HookDialog)
        self.spoilerFHook.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spoilerFHook.setFont(font)
        self.spoilerFHook.setObjectName(_fromUtf8("spoilerFHook"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.spoilerFHook)
        self.autocardBHookLabel = QtGui.QLabel(HookDialog)
        self.autocardBHookLabel.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.autocardBHookLabel.setFont(font)
        self.autocardBHookLabel.setObjectName(_fromUtf8("autocardBHookLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.autocardBHookLabel)
        self.autocardFHookLabel = QtGui.QLabel(HookDialog)
        self.autocardFHookLabel.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.autocardFHookLabel.setFont(font)
        self.autocardFHookLabel.setObjectName(_fromUtf8("autocardFHookLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.autocardFHookLabel)
        self.autocardFHookTextEdit = QtGui.QLineEdit(HookDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autocardFHookTextEdit.sizePolicy().hasHeightForWidth())
        self.autocardFHookTextEdit.setSizePolicy(sizePolicy)
        self.autocardFHookTextEdit.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.autocardFHookTextEdit.setFont(font)
        self.autocardFHookTextEdit.setObjectName(_fromUtf8("autocardFHookTextEdit"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.autocardFHookTextEdit)
        self.autocardBHookTextEdit = QtGui.QLineEdit(HookDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autocardBHookTextEdit.sizePolicy().hasHeightForWidth())
        self.autocardBHookTextEdit.setSizePolicy(sizePolicy)
        self.autocardBHookTextEdit.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.autocardBHookTextEdit.setFont(font)
        self.autocardBHookTextEdit.setObjectName(_fromUtf8("autocardBHookTextEdit"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.autocardBHookTextEdit)
        self.spoilerFHookTextEdit = QtGui.QLineEdit(HookDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spoilerFHookTextEdit.sizePolicy().hasHeightForWidth())
        self.spoilerFHookTextEdit.setSizePolicy(sizePolicy)
        self.spoilerFHookTextEdit.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spoilerFHookTextEdit.setFont(font)
        self.spoilerFHookTextEdit.setObjectName(_fromUtf8("spoilerFHookTextEdit"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.spoilerFHookTextEdit)
        self.spoilerBHookTextEdit = QtGui.QLineEdit(HookDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spoilerBHookTextEdit.sizePolicy().hasHeightForWidth())
        self.spoilerBHookTextEdit.setSizePolicy(sizePolicy)
        self.spoilerBHookTextEdit.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spoilerBHookTextEdit.setFont(font)
        self.spoilerBHookTextEdit.setObjectName(_fromUtf8("spoilerBHookTextEdit"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.spoilerBHookTextEdit)
        self.verticalLayout.addLayout(self.formLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.line_2 = QtGui.QFrame(HookDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.okButton = QtGui.QPushButton(HookDialog)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(HookDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(HookDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.line = QtGui.QFrame(HookDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)

        self.retranslateUi(HookDialog)
        QtCore.QMetaObject.connectSlotsByName(HookDialog)
        
#-------------------------------------------------------------------------------
    def retranslateUi(self, HookDialog):
        HookDialog.setWindowTitle(_translate("HookDialog", "Specify optional forum hooks", None))
        self.spoilerBHook.setText(_translate("HookDialog", "Spoiler back hook", None))
        self.spoilerFHook.setText(_translate("HookDialog", "Spoiler front hook", None))
        self.autocardBHookLabel.setText(_translate("HookDialog", "Autocard back hook", None))
        self.autocardFHookLabel.setText(_translate("HookDialog", "Autocard front hook", None))
        self.okButton.setText(_translate("HookDialog", "Ok", None))
        self.cancelButton.setText(_translate("HookDialog", "Cancel", None))
        self.label_5.setText(_translate("HookDialog", "You can optionally specify forum autocard hooks which will surround each card name, and spoiler hooks which will surround each section of the text file.", None))

