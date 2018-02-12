# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updatedialog.ui'
#
# Created: Sat Jul 20 08:47:27 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from GUI.SetsTreeWidget import SetsTreeWidget
from Updating.MagicCardsInfoParser import MagicCardsInfoParser

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

class UpdateDialog(QtGui.QDialog):
    """
    Largely generated dialog to to update the program database and download images
    online.
    """
    
    #-------------------------------------------------------------------------------
    def __init__(self, parent, mainframeParent):
        """Additional initializer."""
        
        super(UpdateDialog, self).__init__(parent)
        
        #------------------------------------
        self._mainframeParent = mainframeParent
        self._db = self._mainframeParent.getDatabase()
        self._parser = None
        
        #------------------------------------
        self.setupUi(self)
        self.__setup()
        self.show()
        

#==========================================================================#
#                              Private                                     #
#==========================================================================#
#-------------------------------------------------------------------------------
    def __setup(self):
        """
        Sets up the dialog GUI.
        """
        
        self.__connectEvents()
        self.textEdit.setText(self._mainframeParent.getSetting('picsfolder'))

#-------------------------------------------------------------------------------
    def _checkForNewSets(self, dbSetNames, onlineSetNames):
        """
        Compares the set names found online and the set names in the database
        and returns those which the database doesn't have.
        """
        
        return set(onlineSetNames) - set(dbSetNames)
        
#-------------------------------------------------------------------------------
    def _connect(self):
        """
        Connects to gatherer and magiccards.info, and checks is for 
        updates.
        """
        
        self._parser = MagicCardsInfoParser()
        
        if not self._parser.checkConnection():
            title = "Error in connection"
            msg = "Magiccards.info is offline or cannot connect to internet"
            QtGui.QMessageBox.warning(self, title, msg)
            return
        
        onlineMtgSetNames = self._parser.getMtgSetNames()
        self.setsTreeWidget.addMtgSets(onlineMtgSetNames)
        
        dbSetNames = self._db.getMtgSetNames()
        
        newSetNames = self._checkForNewSets(dbSetNames, 
                                            onlineMtgSetNames['All'])
        self.setsTreeWidget.markNewMtgSets(newSetNames)
        
        self.connectButton.setEnabled(False)
        
        text = "<font color='green'>Connected</font>"
        self.magiccardsConnectionLabel.setText(text)
        
        

#-------------------------------------------------------------------------------
    def _updateChosenSets(self):
        """
        Updates the database with the sets chosen in the tree widget.
        """
        
        downloadedSets = []
        chosenItems = self.setsTreeWidget.getCheckedItems()
        
        if not chosenItems:
            return
        
        self._resetProgress()
        
        current = 1
        total = len(chosenItems)
        
        self.progressBar.setMaximum(total)
        self.progressBar_2.setMaximum(total + int(round(0.1 * total)))
        
        for chosenItem in chosenItems:
            QtCore.QCoreApplication.processEvents()
            currentProgressText = 'prossessing Set {current} out of {total}'
            currentProgressText = currentProgressText.format(current=current,
                                                            total=total)
            overallProgressText = 'Prossessing sets'
            self.label_7.setText(currentProgressText)
            self.label_8.setText(overallProgressText)
            
            self.progressBar.setValue(current - 1)
            self.progressBar_2.setValue(current - 1)
            
            QtCore.QCoreApplication.processEvents()
            downloadedSets.append(self._parser.getMtgSet(str(chosenItem.text(0))))
            QtCore.QCoreApplication.processEvents()
            
            current += 1
        
        QtCore.QCoreApplication.processEvents()
        currentProgressText = 'Updating Database'
        overallProgressText = 'Prossessing sets'
        self.label_7.setText(currentProgressText)
        self.label_8.setText(overallProgressText)
        
        self.progressBar.setValue(0)
        self.progressBar_2.setValue(current - 1)
        
        for mtgSet in downloadedSets:
            self._db.addSet(mtgSet)
        
        self._mainframeParent.saveDatabase(self._db)
        self._resetProgress()
            

#-------------------------------------------------------------------------------
    def _downloadChosenSetsImages(self):
        """
        Downloads the images of the sets chosen in the tree widget.
        """
        
        chosenItems = self.setsTreeWidget.getCheckedItems()
        
        if not chosenItems:
            return
        
        self._resetProgress()
        total = len(chosenItems)
        current = 0
        
        self.progressBar_2.setMaximum(total)
        
        for chosenItem in chosenItems:
            QtCore.QCoreApplication.processEvents()
            
            setName = str(chosenItem.text(0))
            setCode = str(chosenItem.text(1))
            destFolder = str(self.textEdit.toPlainText())
            
            overAllText = 'Downloading images of {setName} ({current} out of {total})'
            overAllText = overAllText.format(setName=setName,
                                             current=current,
                                             total=total)
            self.label_8.setText(overAllText)
            self.progressBar_2.setValue(current)
            self._parser.downloadMtgSetImages(setCode, destFolder, 
                                              self.progressBar, self.label_7)
            
            QtCore.QCoreApplication.processEvents()
            
            current += 1
        
        QtCore.QCoreApplication.processEvents()
        overAllText = 'Done downloading images'
        overAllText = overAllText.format(setName=setName,
                                         current=current,
                                         total=total)
        self.label_8.setText(overAllText)
        self.progressBar_2.setValue(current)
        QtCore.QCoreApplication.processEvents()
            
        
#-------------------------------------------------------------------------------
    def _setImageFolder(self):
        """
        Sets up the image folder to be used for downloading images. Called
        when the directory chooser dialog button is clicked.
        """
        
        caption = 'Choose a folder for downloading images'
        folder = QtGui.QFileDialog().getExistingDirectory(self, caption)
        
        self.textEdit.setText(folder)
        

#-------------------------------------------------------------------------------
    def _resetProgress(self):
        """
        Resets progressbars back to starting values.
        """
        
        self.progressBar.setMaximum(100)
        self.progressBar_2.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.progressBar_2.setMinimum(0)
        self.progressBar.setValue(0)
        self.progressBar_2.setValue(0)
        self.label_7.setText('-')
        self.label_8.setText('-')
        
#==========================================================================#
#                              Events                                      #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __connectEvents(self):
        """Sets up the event handling."""
        
        self.doneButton.clicked.connect(self.close)
        self.connectButton.clicked.connect(self._connect)
        self.downloadImagesButton.clicked.connect(self._downloadChosenSetsImages)
        self.updateSetsButton.clicked.connect(self._updateChosenSets)
        self.toolButton.clicked.connect(self._setImageFolder)
        
        self.setsTreeWidget.itemChanged.connect(self.__itemChanged)
        self.comboBox.activated.connect(self.__comboBoxActivated)

#-------------------------------------------------------------------------------
    def __itemChanged(self, item, column):
        """Called when an item in the setsTreeWidget is changed."""
        
        if any(self.setsTreeWidget.getCheckedItems()):
            self.downloadImagesButton.setEnabled(True)
            self.updateSetsButton.setEnabled(True)
        
        else:
            self.downloadImagesButton.setEnabled(False)
            self.updateSetsButton.setEnabled(False)

#-------------------------------------------------------------------------------
    def __comboBoxActivated(self, index):
        """Called when an item in the combobox is chosen by the user."""
        
        if index ==  0:
            self.setsTreeWidget.unCheckAll()
        elif index ==  1:
            self.setsTreeWidget.unCheckAll()
            self.setsTreeWidget.checkAll()
        elif index ==  2:
            self.setsTreeWidget.unCheckAll()
            self.setsTreeWidget.checkNewMtgSets()
        elif index ==  3:
            self.setsTreeWidget.unCheckAll()
            self.setsTreeWidget.checkExpansions()
        elif index ==  4:
            self.setsTreeWidget.unCheckAll()
            self.setsTreeWidget.checkCoreSets()
        elif index ==  5:
            self.setsTreeWidget.unCheckAll()
            self.setsTreeWidget.checkSpecials()
        
        
#==========================================================================#
#                              Generated                                   #
#==========================================================================#
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(719, 512)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setMargin(10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.connectButton = QtGui.QPushButton(Dialog)
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.horizontalLayout.addWidget(self.connectButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.downloadImagesButton = QtGui.QPushButton(Dialog)
        self.downloadImagesButton.setEnabled(False)
        self.downloadImagesButton.setObjectName(_fromUtf8("downloadImagesButton"))
        self.horizontalLayout.addWidget(self.downloadImagesButton)
        self.updateSetsButton = QtGui.QPushButton(Dialog)
        self.updateSetsButton.setEnabled(False)
        self.updateSetsButton.setObjectName(_fromUtf8("updateSetsButton"))
        self.horizontalLayout.addWidget(self.updateSetsButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.doneButton = QtGui.QPushButton(Dialog)
        self.doneButton.setObjectName(_fromUtf8("doneButton"))
        self.horizontalLayout.addWidget(self.doneButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(250, 50))
        self.groupBox.setMaximumSize(QtCore.QSize(200, 3000))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout_3.addWidget(self.comboBox, 0, 0, 1, 1)
        self.setsTreeWidget = SetsTreeWidget(self.groupBox, self._db)
        self.setsTreeWidget.setHeaderLabels(['Set', 'Code'])
        self.setsTreeWidget.setMinimumSize(QtCore.QSize(0, 300))
        self.setsTreeWidget.setObjectName(_fromUtf8("setsTreeWidget"))
        self.setsTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout_3.addWidget(self.setsTreeWidget, 1, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 150))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 200))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.progressBar_2 = QtGui.QProgressBar(self.groupBox_2)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName(_fromUtf8("progressBar_2"))
        self.gridLayout_4.addWidget(self.progressBar_2, 3, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_4.addWidget(self.label_7, 0, 1, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.groupBox_2)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_4.addWidget(self.progressBar, 1, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 2, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 3, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.horizontalLayout_2.addWidget(self.radioButton_2)
        self.radioButton = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton.setEnabled(False)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.horizontalLayout_2.addWidget(self.radioButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.groupBox_3)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_2.addWidget(self.textEdit, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.toolButton = QtGui.QToolButton(self.groupBox_3)
        self.toolButton.setMinimumSize(QtCore.QSize(25, 25))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout_2.addWidget(self.toolButton, 0, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setMinimumSize(QtCore.QSize(300, 70))
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 60))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_4)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.magiccardsLabel = QtGui.QLabel(self.groupBox_4)
        self.magiccardsLabel.setObjectName(_fromUtf8("magiccardsLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.magiccardsLabel)
        self.magiccardsConnectionLabel = QtGui.QLabel(self.groupBox_4)
        self.magiccardsConnectionLabel.setObjectName(_fromUtf8("magiccardsConnectionLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.magiccardsConnectionLabel)
        self.gathererLabel = QtGui.QLabel(self.groupBox_4)
        self.gathererLabel.setObjectName(_fromUtf8("gathererLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.gathererLabel)
        self.gathererConnectionLabel = QtGui.QLabel(self.groupBox_4)
        self.gathererConnectionLabel.setObjectName(_fromUtf8("gathererConnectionLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.gathererConnectionLabel)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Update sets and download images", None))
        self.connectButton.setText(_translate("Dialog", "Connect", None))
        self.downloadImagesButton.setText(_translate("Dialog", "Download Images", None))
        self.updateSetsButton.setText(_translate("Dialog", "Update Sets", None))
        self.doneButton.setText(_translate("Dialog", "Done", None))
        self.groupBox.setTitle(_translate("Dialog", "Sets", None))
        self.comboBox.setItemText(0, _translate("Dialog", "None", None))
        self.comboBox.setItemText(1, _translate("Dialog", "All Sets", None))
        self.comboBox.setItemText(2, _translate("Dialog", "New", None))
        self.comboBox.setItemText(3, _translate("Dialog", "Expansions", None))
        self.comboBox.setItemText(4, _translate("Dialog", "Core Sets", None))
        self.comboBox.setItemText(5, _translate("Dialog", "Specials & Other", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Progress", None))
        self.label_7.setText(_translate("Dialog", "-", None))
        self.label_8.setText(_translate("Dialog", "-", None))
        self.label_9.setText(_translate("Dialog", "Current Progress", None))
        self.label_10.setText(_translate("Dialog", "Overall Progress", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Settings", None))
        self.radioButton_2.setText(_translate("Dialog", "Magiccards.info", None))
        self.radioButton.setText(_translate("Dialog", "Gatherer.Wizards.com(Later)", None))
        self.label_6.setText(_translate("Dialog", "Download Images From:", None))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"> </span></p></body></html>", None))
        self.label_5.setText(_translate("Dialog", "Image Folder:", None))
        self.toolButton.setText(_translate("Dialog", "...", None))
        self.groupBox_4.setTitle(_translate("Dialog", "Connection", None))
        self.magiccardsLabel.setText(_translate("Dialog", "http://magiccards.info:", None))
        self.magiccardsConnectionLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ff0000;\">Offline</span></p></body></html>", None))
        self.gathererLabel.setText(_translate("Dialog", "http://gatherer.wizards.com:", None))
        self.gathererConnectionLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ff0000;\">(To be implemented later)</span></p></body></html>", None))
