
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

class Ui_LandImageDialog(QtGui.QDialog):
    """
    Largely generated dialog to choose and set the basic land images to use
    with MWS.
    """

    def __init__(self, parent, mainFrameParent):
        super(Ui_LandImageDialog, self).__init__(parent)

        self._mainFrameParent = mainFrameParent
        
        db = self._mainFrameParent.getDatabase()
        self._sets = db.getMtgSets()
        self._mtgSetNames = db.getMtgSetNames()
        self._currentLands = {}

        self.setupUi(self)
        self.__connectEvents()
        self._setCurrentLands('Forest')
        self.show()

#==========================================================================#
#                              Events                                      #
#==========================================================================#
#-------------------------------------------------------------------------------
    def __connectEvents(self):
        """
        Sets up event handling for the dialog.
        """

        self.setButton.clicked.connect(self._setButtonClicked)
        self.doneButton.clicked.connect(self._doneButtonClicked)
        self.landComboBox.currentIndexChanged.connect(self._landComboBoxIndexChanged)
        self.imageComboBox.highlighted.connect(self._imageComboBoxHighlighted)

#-------------------------------------------------------------------------------
    def _doneButtonClicked(self):
        """
        Handles clicks to the doneButton. Closes the dialog.
        """

        self.close()

#-------------------------------------------------------------------------------
    def _setButtonClicked(self):
        """
        Handles clicks to the doneButton
        """

        basicLand = self._currentLands[str(self.imageComboBox.currentText())]

        if basicLand.name == 'Forest':
            self._mainFrameParent.configure(Forest=basicLand.id)
        elif basicLand.name == 'Island':
            self._mainFrameParent.configure(Island=basicLand.id)
        elif basicLand.name == 'Plains':
            self._mainFrameParent.configure(Plains=basicLand.id)
        elif basicLand.name == 'Mountain':
            self._mainFrameParent.configure(Mountain=basicLand.id)
        else:
            self._mainFrameParent.configure(Swamp=basicLand.id)

        self._mainFrameParent._presetBasicLands()

#-------------------------------------------------------------------------------
    def _landComboBoxIndexChanged(self, itemIndex):
        """
        Handles the land combo box's index changes.
        """
        
        print self.landComboBox.currentText()

        self._setCurrentLands(str(self.landComboBox.currentText()))

#-------------------------------------------------------------------------------
    def _imageComboBoxHighlighted(self, itemIndex):
        """
        Handles the image combo box's Item highlights.
        """

        card = self._currentLands[str(self.imageComboBox.itemText(itemIndex))]
        self._mainFrameParent.cardImageWidget.setCardImage(card)


#==========================================================================#
#                              Private methods                             #
#==========================================================================#
        
#-------------------------------------------------------------------------------
    def _setCurrentLands(self, basicLandName):
        """
        Sets the specified basic land image paths and names.
        """
        self.imageComboBox.clear()
        basicLands = self._mainFrameParent.getDatabase().getCards(basicLandName)
        
        for basicLand in basicLands:
            mtgSetName = basicLand.mtgSetName
            setCode = self._mtgSetNames[mtgSetName]
            altArt = basicLand.altArt
            
            text = mtgSetName + altArt + '(' + setCode + ')'
            self.imageComboBox.addItem(text)
            self._currentLands[text] = basicLand
            

        self._setCurrentIndex()

#-------------------------------------------------------------------------------
    def _setCurrentIndex(self):
        """
        Sets the index of the land which is already chosen.
        """

        if self.landComboBox.currentText() == 'Forest':
            land = self._mainFrameParent._forest
            
        
        elif self.landComboBox.currentText() == 'Plains':
            land = self._mainFrameParent._plains
        
        elif self.landComboBox.currentText() == 'Island':
            land = self._mainFrameParent._island
        
        elif self.landComboBox.currentText() == 'Mountain':
            land = self._mainFrameParent._mountain
        
        elif self.landComboBox.currentText() == 'Swamp':
            land = self._mainFrameParent._swamp
            
        mtgSetName = land.mtgSetName
        setCode = self._mtgSetNames[mtgSetName]
        altArt = land.altArt
        
        text = mtgSetName + altArt + '(' + setCode + ')'
        index = self.imageComboBox.findText(text)
        print index
        self.imageComboBox.setCurrentIndex(index)
        
        #self._imageComboBoxHighlighted(index)

#==========================================================================#
#                              Generated                                   #
#==========================================================================#
#-------------------------------------------------------------------------------
    def setupUi(self, LandImageDialog):
        LandImageDialog.setObjectName(_fromUtf8("LandImageDialog"))
        LandImageDialog.resize(300, 127)
        self.verticalLayout = QtGui.QVBoxLayout(LandImageDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 30, 10, 10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.landComboBox = QtGui.QComboBox(LandImageDialog)
        self.landComboBox.setObjectName(_fromUtf8("landComboBox"))
        self.landComboBox.addItem(_fromUtf8(""))
        self.landComboBox.addItem(_fromUtf8(""))
        self.landComboBox.addItem(_fromUtf8(""))
        self.landComboBox.addItem(_fromUtf8(""))
        self.landComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.landComboBox)
        self.imageComboBox = QtGui.QComboBox(LandImageDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageComboBox.sizePolicy().hasHeightForWidth())
        self.imageComboBox.setSizePolicy(sizePolicy)
        self.imageComboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.imageComboBox.setObjectName(_fromUtf8("imageComboBox"))
        self.horizontalLayout.addWidget(self.imageComboBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.setButton = QtGui.QPushButton(LandImageDialog)
        self.setButton.setObjectName(_fromUtf8("setButton"))
        self.horizontalLayout.addWidget(self.setButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.line = QtGui.QFrame(LandImageDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.doneButton = QtGui.QPushButton(LandImageDialog)
        self.doneButton.setObjectName(_fromUtf8("doneButton"))
        self.horizontalLayout_3.addWidget(self.doneButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(LandImageDialog)
        self.imageComboBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(LandImageDialog)

    def retranslateUi(self, LandImageDialog):
        LandImageDialog.setWindowTitle(_translate("LandImageDialog", "Set basic land images for MWS decks", None))
        self.landComboBox.setItemText(0, _translate("LandImageDialog", "Forest", None))
        self.landComboBox.setItemText(1, _translate("LandImageDialog", "Island", None))
        self.landComboBox.setItemText(2, _translate("LandImageDialog", "Swamp", None))
        self.landComboBox.setItemText(3, _translate("LandImageDialog", "Plains", None))
        self.landComboBox.setItemText(4, _translate("LandImageDialog", "Mountain", None))
        self.setButton.setText(_translate("LandImageDialog", "Set Image", None))
        self.doneButton.setText(_translate("LandImageDialog", "Done", None))

