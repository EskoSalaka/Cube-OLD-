# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'standardGenerationDialog.ui'
#
# Created: Thu Dec 06 11:25:20 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(QtGui.QDialog):
    """
    Largely generated dialog to to create standard booster sealed deck pools.
    """
#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent):
        """Additional initializer."""
        
        super(Ui_Dialog, self).__init__(parent)
        
        self._mainFrameParent = mainFrameParent
        db = self._mainFrameParent.getDatabase()
        self._mtgSets = db.getMtgSets()

        self.setupUi(self)
        self._addSets()
        self.show()
        

#==========================================================================#
#                              Private                                     #
#==========================================================================#
#-------------------------------------------------------------------------------
    def _addSets(self):
        """
        Adds all the(usable) mtg sets to the combo box list.
        
        Note, that some sets are too small for generating boosters, so these
        are ignored.
        """
        
        usableSetNames = [mtgSetName for mtgSetName in self._mtgSets.keys() if
                          self._mtgSets[mtgSetName].countUniques() > 100]
        
        self.boosterComboBox.addItems(usableSetNames)

#-------------------------------------------------------------------------------
    def _getCardNumComboBoxes(self):
        """
        Returns a combobox item where the user can choose how many cards a 
        booster will generate.
        """
        
        cardNumComboBox = QtGui.QComboBox()
        rareComboBox = QtGui.QComboBox()
        uncommonComboBox = QtGui.QComboBox()
        
        for item in range(12, 91):
            cardNumComboBox.addItem(str(item))
        
        for item in range(1, 10):
            rareComboBox.addItem(str(item))
        
        for item in range(3, 30):
            uncommonComboBox.addItem(str(item))
        
        
        
        cardNumComboBox.setCurrentIndex(3)
        cardNumComboBox.setMaximumWidth(40)
        
        rareComboBox.setCurrentIndex(0)
        rareComboBox.setMaximumWidth(40)
        
        uncommonComboBox.setCurrentIndex(0)
        uncommonComboBox.setMaximumWidth(40)
        
        return cardNumComboBox, rareComboBox, uncommonComboBox

        
#==========================================================================#
#                              Events                                      #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __connectEvents(self):
        """
        Sets up event handling.
        """
        
        self.addButton.clicked.connect(self._addButtonClicked)
        self.removeButton.clicked.connect(self._removeButtonClicked)
        self.generateButton.clicked.connect(self._generateButtonClicked)
        self.generateButton.pressed.connect(self._generateButtonClicked)
        self.cancelButton.clicked.connect(self._cancelButtonClicked)

#-------------------------------------------------------------------------------
    def _addButtonClicked(self, s):
        """
        Handles clicks to the addButton
        """
        
        treeItem = QtGui.QTreeWidgetItem([unicode(self.boosterComboBox.currentText())])
        comboBoxes = self._getCardNumComboBoxes()
        
        
        self.boosterList.addTopLevelItem(treeItem)
        self.boosterList.setItemWidget(treeItem, 1, comboBoxes[0])
        self.boosterList.setItemWidget(treeItem, 2, comboBoxes[1])
        self.boosterList.setItemWidget(treeItem, 3, comboBoxes[2])

        self.boosterList.resizeColumnToContents(0)
        self.boosterList.resizeColumnToContents(1)
        self.boosterList.resizeColumnToContents(2)
        self.boosterList.resizeColumnToContents(3)
        

#-------------------------------------------------------------------------------
    def _removeButtonClicked(self):
        """
        Handles clicks to the addButton
        """
        currentItem = self.boosterList.currentItem()
        index = self.boosterList.indexOfTopLevelItem(currentItem)
        self.boosterList.takeTopLevelItem(index)
        self.boosterList.resizeColumnToContents(0)
        
#-------------------------------------------------------------------------------
    def _generateButtonClicked(self):
        """
        Handles clicks to the generateButton
        """
        
        setNames = {}
        
        for childIndex in range(self.boosterList.topLevelItemCount()):
            child = self.boosterList.topLevelItem(childIndex)
            setName = unicode(child.text(0))
            numOfCards = int(self.boosterList.itemWidget(child, 1).currentText())
            numOfRares = int(self.boosterList.itemWidget(child, 2).currentText())
            numOfUncommons = int(self.boosterList.itemWidget(child, 3).currentText())
            
            if not setName in setNames:
                setNames[setName] = [(numOfCards, numOfRares, numOfUncommons)]
            else:
                setNames[setName].append((numOfCards, numOfRares, numOfUncommons))

        if not setNames:
            QtGui.QMessageBox.warning(self, 'No boosters chosen', 
                                            'No boosters chosen')
            return

        cards = []
        
        for (setName, packNumDatas) in setNames.iteritems():
            for packNumData in packNumDatas:
                cards.extend(self._mtgSets[setName].getRandomPack(packNumData[0],
                                                                  packNumData[1],
                                                                  packNumData[2]))
        
        self._mainFrameParent.clearAll()
        self._mainFrameParent.sideBoardList.addCards(cards)
        self._mainFrameParent.refreshNumbers()
        self.close()

#-------------------------------------------------------------------------------
    def _cancelButtonClicked(self):
        """
        Handles clicks to the addButton
        """
        
        self.reject()

#==========================================================================#
#                              Generated                                   #
#==========================================================================#

    def setupUi(self, Dialog):
        self._dialog = Dialog
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(312, 431)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setMargin(12)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.boosterList = QtGui.QTreeWidget(Dialog)
        self.boosterList.setObjectName(_fromUtf8("boosterList"))
        self.gridLayout.addWidget(self.boosterList, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.boosterComboBox = QtGui.QComboBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boosterComboBox.sizePolicy().hasHeightForWidth())
        self.boosterComboBox.setSizePolicy(sizePolicy)
        self.boosterComboBox.setMinimumSize(QtCore.QSize(50, 0))
        self.boosterComboBox.setMaximumSize(QtCore.QSize(1000, 1000))
        self.boosterComboBox.setObjectName(_fromUtf8("boosterComboBox"))
        self.gridLayout.addWidget(self.boosterComboBox, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setContentsMargins(12, 0, 12, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.addButton = QtGui.QPushButton(Dialog)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(Dialog)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.horizontalLayout.addWidget(self.removeButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 5, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.generateButton = QtGui.QPushButton(Dialog)
        self.generateButton.setObjectName(_fromUtf8("generateButton"))
        self.horizontalLayout_2.addWidget(self.generateButton)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 1)
        self.boosterComboBox.setMaxVisibleItems(20)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.__connectEvents()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Select packs for sealed deck", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("Dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("Dialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.generateButton.setText(QtGui.QApplication.translate("Dialog", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.boosterList.setColumnCount(4)
        self.boosterList.setIndentation(5)
        self.boosterList.setHeaderLabels(['Set', 'Cards', 'Rares', 'Uncs'])
        header = self.boosterList.header()
        header.setStretchLastSection(False)
