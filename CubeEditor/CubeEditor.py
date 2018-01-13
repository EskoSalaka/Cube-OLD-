#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt4 import QtCore, QtGui

import cPickle as pickle
import codecs
import os.path
import ConfigParser

from GUI.FilterButton import FilterButton, MultiColorFilterButton
from GUI.CardImageWidget import CardImageWidget
from GUI.QuickStatsCanvas import QuickStatsCanvas
from GUI.CubeEditorMenuBar import CubeEditorMenuBar
from GUI.CubeEditorToolBar import CubeEditorToolBar
from GUI.HookDialog import Ui_HookDialog
from Base.FileHandler import FileHandler
from Base.Cube import Cube

from GUI.CubeList import CubeList

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_CubeEditor(QtGui.QMainWindow):
    """
    A cube editor window. Its quite similar to the mainwindow.
    """
    
    def __init__(self):
        super(Ui_CubeEditor, self).__init__()
        #------------------------------------
        
        self._config = ConfigParser.ConfigParser()
        self._cardReader = FileHandler(self.getDatabase())
        
        #------------------------------------
        self._config.read('Settings\Settings.ini')
        self.setupUi(self)
        
        self.configure(currentCubeSaved=False, currentCubePath='')


#==========================================================================#
#                              Settings handling methods                   #
#==========================================================================#

#-------------------------------------------------------------------------------
    def configure(self, **kwargs):
        """Configures the settings file."""

        for keyword in kwargs.keys():
            self._config.set('Config', keyword, kwargs[keyword] )
            
        with open('Settings\Settings.ini', 'w') as settingsFile:
            self._config.write(settingsFile)
        
#-------------------------------------------------------------------------------
    def getSetting(self, option):
        """
        Returns an option from the settings file under the [Config] section.
        """
        
        return self._config.get('Config', option)

#==========================================================================#
#                              Database handling methods                   #
#==========================================================================#
#-------------------------------------------------------------------------------
    def getDatabase(self):
        """
        Unpickles and returns the Database instance.
        """
        
        return pickle.load(open('Database\MasterBase.pick', 'rb'))

#-------------------------------------------------------------------------------
    def saveDatabase(self, db):
        """
        Pickles the database back to a file located in the Database package.
        """
        
        pickle.dump(db, open('Database\MasterBase.pick', 'wb'))
        self._presetBasicLands()
    
#==========================================================================#
#                              Public  methods                             #
#==========================================================================#
        
#-------------------------------------------------------------------------------
    def transferCardItem(self, cardItem, sender):
        """
        Transfers a CardItem from a list to another.
        """
        
        if cardItem.__class__.__name__ is not 'TreeCardItem' or \
           'Basic Land' in cardItem.type:
            return
        
        if sender == self.cubeList:
            cardItem.remove()
            self.masterBaseList.addCard(cardItem)
            self.statsWidget.removeCardData(cardItem)
        else:
            self.cubeList.addCard(cardItem)
            self.statsWidget.addCardData(cardItem)
            
        self.statsWidget.Update()
        self.refreshNumbers()

#-------------------------------------------------------------------------------
    def newCube(self):
        """
        Cleares the cubeList and starts a new cube.
        """
        
        if not self.getSetting('currentCubeSaved') and \
        self.cubeList.cardCount():
            reply = self._saveCubeNewWarning()
            
            if reply == QtGui.QMessageBox.Yes:
                self.saveCubeAs()
        
        path = self._newCubeDialog()
        
        if path:
            self.clearAll()
            self.configure(currentCubeSaved=True, currentCubePath=path, 
                           lastSaveCubeLoc=os.path.dirname(str(path)))

#-------------------------------------------------------------------------------
    def openCube(self):
        """Opens a cube and loads the contents in the cubeList."""
        
        path = self._openCubeFileDialog()
        
        if path:
            try:
                cube = pickle.load(open(path, 'r'))
            except (IOError, KeyError, EOFError):
                self._cubeFileOpenErrorDialog()
            else:
                self.clearAll()
                cards = cube.getCards()
                self.cubeList.addCards(cards)
                
                for card in cards:
                    self.statsWidget.addCardData(card)
                
                self.refreshNumbers()
                self.configure(currentCubeSaved=True, currentCubePath=path, 
                               lastSaveCubeLoc=os.path.dirname(str(path)))

        
#-------------------------------------------------------------------------------
    def saveCubeAs(self):
        """Saves the cube from the cubeList in a file."""
        
        if self.getSetting('currentCubePath'):
            path = self.getSetting('currentCubePath')
        else:
            path = self._saveCubeDialog()
            
        if path:
            cube = Cube(self.cubeList.getCards())
            pickle.dump(cube,  open(path, 'wb'))
            self.configure(currentCubeSaved=True, currentCubePath=path, 
                           lastSaveCubeLoc=os.path.dirname(str(path)))


#-------------------------------------------------------------------------------
    def cubeToTxtFile(self):
        """
        Writes a Cube given in a .cube file to a sorted textFile.
        """
        
        if not self.cubeList.cardCount():
            self._emptyCubeWarningDialog()
            return
        
        cube = Cube(self.cubeList.getCards())
        
        textFilePath = self._saveOrganizedCubeTxtFile()
        
        if textFilePath:
            textFile = codecs.open(textFilePath, 'w')
            hookDialog = Ui_HookDialog(self, self)
            
            if hookDialog.exec_():
                hooks = hookDialog.getHooks()
                self._cardReader.cubeToTxtFile(cube, textFile, 
                                               frontHook=hooks[0], 
                                               backHook=hooks[1],
                                               spoilerFrontHook=hooks[2], 
                                               spoilerBackHook=hooks[3])
            else:
                self._cardReader.cubeToTxtFile(cube, textFile)

#-------------------------------------------------------------------------------
    def colorMasterListCards(self):
        """
        Colors the cards in the master list which are 
        already in the cube.
        """
        
        self.masterBaseList.colorCards(self.cubeList._cards.values())
        
#-------------------------------------------------------------------------------
    def deColorMasterListCards(self):
        """
        Uncolors all the cards.
        """
        
        self.masterBaseList.deColorMasterListCards()

#-------------------------------------------------------------------------------
    def readFromMwsFile(self):
        """
        Reads cube data from MWS deck file.
        """
        
        self.masterBaseList.deColorMasterListCards()

#-------------------------------------------------------------------------------
    def readFromTxtFile(self):
        """
        Reads cube data from text file. Uses the filehandler class to look for
        cards and loads them in the cube list.
        """
        
        path = self._openTxtFileDialog()
        
        if path:
            try:
                textFile = codecs.open(path, mode='r', encoding='latin-1')
                cards = self._cardReader.readTextFile(textFile)
            except IOError:
                self._txtFileOpenErrorDialog()
            else:
                if cards[1]:
                    self._errorsInTxtFileDialog(cards)
                    
                if cards[0]:
                    self.cubeList.addCards(cards[0])
                
                for card in cards[0]:
                    self.statsWidget.addCardData(card)
                        
                    self.refreshNumbers()
                    self.configure(currentCubeSaved=False, currentCubePath='')
                else:
                    self._txtFileOpenErrorDialog()


#-------------------------------------------------------------------------------
    def refreshNumbers(self):
        """
        Sets the correct values for the numbers of cards seen on the titles
        of deck and sideboard lists, and also the basic lands spinbox title.
        """
        
        cubeCards = self.masterBaseList.cardCount()
        self.sideBoardBox.setTitle('Master Base({num})'.format(num=cubeCards))
        deckCards = self.cubeList.cardCount()
        self.deckBox.setTitle('Cube({num})'.format(num=deckCards))
        self.statsWidget.Update()

#-------------------------------------------------------------------------------
    def clearAll(self):
        """
        Clears all the cards from each list, and clears the data from 
        statsWidget.
        """
        
        self.cubeList.clearList(delete=True)
        self.cubeList.refreshLayout()
        self.statsWidget.clear()
        self.statsWidget.Update()
        self.refreshNumbers()
        self.configure(currentCubeSaved=False, currentCubePath='')
        
#==========================================================================#
#                              Event handling                              #
#==========================================================================#
#-------------------------------------------------------------------------------
    def closeEvent(self, event):
        """
        Close event handler.
        """
        
        if not self.getSetting('currentCubeSaved') \
        and (self.cubeList.cardCount()):
            reply = self._saveCubeClosingWarning()
        
            if reply == QtGui.QMessageBox.Yes:
                self.saveCubeAs()
                event.accept()
            elif reply == QtGui.QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()


#==========================================================================#
#                              QT dialogs                                  #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _emptyCubeWarningDialog(self):
        """Warning displayed when trying to save a Cube with 0 cards."""
        
        title = "No cards in the cube"
        msg = "Cannot save an empty cube"
        QtGui.QMessageBox.warning(self, title, msg)

#-------------------------------------------------------------------------------
    def _saveCubeClosingWarning(self):
        """Warning displayed when trying to close the app without saving cube"""
        
        title = "Save cube"
        msg = "Save cube before closing?"
        return QtGui.QMessageBox.question(self, title, msg,
                                          QtGui.QMessageBox.Yes, 
                                          QtGui.QMessageBox.No,  
                                          QtGui.QMessageBox.Cancel)

#-------------------------------------------------------------------------------
    def _saveCubeNewWarning(self):
        """
        Warning displayed when trying to create a new cube 
        without saving the current one.
        """
        
        title = "Save cube"
        msg = "Save cube before creating a new one?"
        return QtGui.QMessageBox.question(self, title, msg,
                                          QtGui.QMessageBox.Yes, 
                                          QtGui.QMessageBox.No,  
                                          QtGui.QMessageBox.Cancel)
        

#-------------------------------------------------------------------------------
    def _saveCubeDialog(self):
        """A save cube dialog. Returns path where the cube is to be saved."""
        
        caption = 'Save cube as...'
        fileFilter = '.Cube' 
        loc = self.getSetting('lastSaveCubeLoc')
        
        return QtGui.QFileDialog().getSaveFileName(self, caption, 
                                                   filter=fileFilter,
                                                   directory=loc)

#-------------------------------------------------------------------------------
    def _newCubeDialog(self):
        """A new cube dialog. Returns path where the new cube is to be saved."""
        
        caption = 'Choose location for the new cube...'
        fileFilter = '.Cube' 
        loc = self.getSetting('lastSaveCubeLoc')
        
        return QtGui.QFileDialog().getSaveFileName(self, caption, 
                                                   filter=fileFilter,
                                                   directory=loc)

#-------------------------------------------------------------------------------
    def _saveOrganizedCubeTxtFile(self):
        """A save organized cube text file dialog. Returns saved file path.."""
        
        caption = 'Save cube as...'
        fileFilter = '.txt' 
        loc = self.getSetting('lastSaveDeckLoc')
        
        return QtGui.QFileDialog().getSaveFileName(self, caption, 
                                                   filter=fileFilter,
                                                   directory=loc)
    
#-------------------------------------------------------------------------------
    def _openCubeFileDialog(self):
        """A path dialog for opening .cube decks."""
        
        caption = 'Open a .cube file'
        loc = self.getSetting('lastOpenCubeLoc')
        return QtGui.QFileDialog.getOpenFileName(parent=None, caption=caption,
                                                 directory=loc)

#-------------------------------------------------------------------------------
    def _openTxtFileDialog(self):
        """A path dialog for opening .txt decks."""
        
        caption = 'Open a text file containing a list of cards'
        loc = self.getSetting('lastOpenTxtFileLoc')
        return QtGui.QFileDialog.getOpenFileName(parent=None, caption=caption,
                                                 directory=loc)
    
#-------------------------------------------------------------------------------
    def _MWSfileOpenErrorDialog(self):
        """
        An error dialog displayed when something went wrong with 
        opening a mws deck file.
        """
        
        title = "Error in opening a MWSDeck file"
        msg = "Specified file contains no card data or is corrupted"
        QtGui.QMessageBox.warning(self, title, msg)

#-------------------------------------------------------------------------------
    def _txtFileOpenErrorDialog(self):
        """
        An error dialog displayed when something went wrong with 
        opening a .txt file.
        """
        
        title = "Error in opening a text file"
        msg = "Specified file contains no card data or is corrupted"
        QtGui.QMessageBox.warning(self, title, msg)
        
#-------------------------------------------------------------------------------
    def _cubeFileOpenErrorDialog(self):
        """
        An error dialog displayed when something went wrong with 
        opening a .cube deck file.
        """
        
        title = "Error in opening a Cube file"
        msg = "Specified file contains no cube data or is corrupted"
        QtGui.QMessageBox.warning(self, title, msg)

#-------------------------------------------------------------------------------
    def _errorsInTxtFileDialog(self, cards):
        """
        An error dialog displayed when errors are found in scanning a txt file
        for cards.
        """
        
        title = 'Errors in the file'
        msg = "Some lines were rejected possibly because they had spelling errors, comments or other non-card text. You can manually fix these lines in the text file"
                    
        msgBox = QtGui.QMessageBox()
        msgBox.setText(title)
        msgBox.setInformativeText(msg)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        msgBox.setDetailedText(cards[1])
        msgBox.exec_()
        
#==========================================================================#
#                             Generated                                    #
#==========================================================================#
#-------------------------------------------------------------------------------
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1156, 915)
        MainWindow.setMinimumSize(QtCore.QSize(100, 100))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 500, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 2, 1, 1)
        self.sideBoardBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sideBoardBox.sizePolicy().hasHeightForWidth())
        self.sideBoardBox.setSizePolicy(sizePolicy)
        self.sideBoardBox.setMinimumSize(QtCore.QSize(200, 300))
        self.sideBoardBox.setObjectName(_fromUtf8("sideBoardBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.sideBoardBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.masterBaseList = CubeList(self.sideBoardBox, self)
        self.masterBaseList.setObjectName(_fromUtf8("masterBaseList"))
        self.masterBaseList.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout_2.addWidget(self.masterBaseList, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.sideBoardBox, 1, 0, 6, 1)
        self.deckBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deckBox.sizePolicy().hasHeightForWidth())
        self.deckBox.setSizePolicy(sizePolicy)
        self.deckBox.setMinimumSize(QtCore.QSize(200, 300))
        self.deckBox.setObjectName(_fromUtf8("deckBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.deckBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.cubeList = CubeList(self.deckBox, self)
        self.cubeList.setObjectName(_fromUtf8("cubeList"))
        self.cubeList.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout_3.addWidget(self.cubeList, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.deckBox, 1, 1, 6, 1)
        self.statsBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statsBox.sizePolicy().hasHeightForWidth())
        self.statsBox.setSizePolicy(sizePolicy)
        self.statsBox.setMinimumSize(QtCore.QSize(800, 200))
        self.statsBox.setMaximumSize(QtCore.QSize(800, 200))
        self.statsBox.setObjectName(_fromUtf8("statsBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.statsBox)
        self.gridLayout_4.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout_4.setMargin(5)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.statsWidget = QuickStatsCanvas(self.statsBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statsWidget.sizePolicy().hasHeightForWidth())
        self.statsWidget.setSizePolicy(sizePolicy)
        self.statsWidget.setObjectName(_fromUtf8("statsWidget"))
        self.gridLayout_4.addWidget(self.statsWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.statsBox, 0, 0, 1, 2)
        self.cardImageBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.cardImageBox.sizePolicy().hasHeightForWidth())
        self.cardImageBox.setSizePolicy(sizePolicy)
        self.cardImageBox.setMinimumSize(QtCore.QSize(308, 436))
        self.cardImageBox.setMaximumSize(QtCore.QSize(308, 436))
        self.cardImageBox.setBaseSize(QtCore.QSize(200, 200))
        self.cardImageBox.setObjectName(_fromUtf8("cardImageBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.cardImageBox)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setMargin(5)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.cardImageWidget = CardImageWidget(self.cardImageBox, self.getSetting('picsFolder'), self.getDatabase().getMtgSetNames())
        self.cardImageWidget.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.cardImageWidget.setObjectName(_fromUtf8("cardImageWidget"))
        self.verticalLayout_2.addWidget(self.cardImageWidget)
        self.label = QtGui.QLabel(self.cardImageBox)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.gridLayout.addWidget(self.cardImageBox, 0, 2, 2, 1)
        self.cardInfoBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.cardInfoBox.sizePolicy().hasHeightForWidth())
        self.cardInfoBox.setSizePolicy(sizePolicy)
        self.cardInfoBox.setMinimumSize(QtCore.QSize(218, 200))
        self.cardInfoBox.setMaximumSize(QtCore.QSize(208, 16777215))
        self.cardInfoBox.setObjectName(_fromUtf8("cardInfoBox"))
        self.gridLayout_5 = QtGui.QGridLayout(self.cardInfoBox)
        self.gridLayout_5.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setContentsMargins(0, 0, -1, 0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.landButton = FilterButton(self.cardInfoBox, self, 'Land', self.masterBaseList, self.cubeList)
        self.landButton.setObjectName(_fromUtf8("landButton"))
        self.gridLayout_5.addWidget(self.landButton, 6, 1, 1, 1)
        self.blackButton = FilterButton(self.cardInfoBox, self, 'B', self.masterBaseList, self.cubeList)
        self.blackButton.setObjectName(_fromUtf8("blackButton"))
        self.gridLayout_5.addWidget(self.blackButton, 2, 0, 1, 1)
        self.greenButton = FilterButton(self.cardInfoBox, self, 'G', self.masterBaseList, self.cubeList)
        self.greenButton.setObjectName(_fromUtf8("greenButton"))
        self.gridLayout_5.addWidget(self.greenButton, 2, 1, 1, 1)
        self.blueButton = FilterButton(self.cardInfoBox, self, 'U', self.masterBaseList, self.cubeList)
        self.blueButton.setObjectName(_fromUtf8("blueButton"))
        self.gridLayout_5.addWidget(self.blueButton, 3, 0, 1, 1)
        self.redButton = FilterButton(self.cardInfoBox, self, 'R', self.masterBaseList, self.cubeList)
        self.redButton.setObjectName(_fromUtf8("redButton"))
        self.gridLayout_5.addWidget(self.redButton, 2, 2, 1, 1)
        self.multicolorButton = MultiColorFilterButton(self.cardInfoBox, self, self.masterBaseList, self.cubeList)
        self.multicolorButton.setObjectName(_fromUtf8("multicolorButton"))
        self.gridLayout_5.addWidget(self.multicolorButton, 3, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(spacerItem2, 5, 1, 1, 1)
        self.whiteButton = FilterButton(self.cardInfoBox, self, 'W', self.masterBaseList, self.cubeList)
        self.whiteButton.setObjectName(_fromUtf8("whiteButton"))
        self.gridLayout_5.addWidget(self.whiteButton, 3, 1, 1, 1)
        self.resetFiltersButton = FilterButton(self.cardInfoBox, self, 'reset', self.masterBaseList, self.cubeList)
        self.resetFiltersButton.setAutoDefault(False)
        self.resetFiltersButton.setDefault(False)
        self.resetFiltersButton.setCheckable(False)
        self.resetFiltersButton.setFlat(False)
        self.resetFiltersButton.setObjectName(_fromUtf8("resetFiltersButton"))
        self.gridLayout_5.addWidget(self.resetFiltersButton, 11, 0, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(6, -1, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.sideaboardRadioButton = QtGui.QRadioButton(self.cardInfoBox)
        self.sideaboardRadioButton.setChecked(True)
        self.sideaboardRadioButton.setObjectName(_fromUtf8("sideaboardRadioButton"))
        self.horizontalLayout.addWidget(self.sideaboardRadioButton)
        self.deckRadioButton = QtGui.QRadioButton(self.cardInfoBox)
        self.deckRadioButton.setObjectName(_fromUtf8("deckRadioButton"))
        self.horizontalLayout.addWidget(self.deckRadioButton)
        self.bothRadioButton = QtGui.QRadioButton(self.cardInfoBox)
        self.bothRadioButton.setObjectName(_fromUtf8("bothRadioButton"))
        self.horizontalLayout.addWidget(self.bothRadioButton)
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.creatureButton = FilterButton(self.cardInfoBox, self, 'Creature', self.masterBaseList, self.cubeList)
        self.creatureButton.setCheckable(True)
        self.creatureButton.setObjectName(_fromUtf8("creatureButton"))
        self.gridLayout_5.addWidget(self.creatureButton, 6, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(spacerItem3, 8, 1, 1, 1)
        self.artifactButton = FilterButton(self.cardInfoBox, self, 'Artifact', self.masterBaseList, self.cubeList)
        self.artifactButton.setCheckable(True)
        self.artifactButton.setObjectName(_fromUtf8("artifactButton"))
        self.gridLayout_5.addWidget(self.artifactButton, 6, 0, 1, 1)
        self.nonCreatureButton = FilterButton(self.cardInfoBox, self, 'Non-Creature', self.masterBaseList, self.cubeList)
        self.nonCreatureButton.setCheckable(True)
        self.nonCreatureButton.setObjectName(_fromUtf8("nonCreatureButton"))
        self.gridLayout_5.addWidget(self.nonCreatureButton, 7, 0, 1, 3)
        self.gridLayout.addWidget(self.cardInfoBox, 3, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = CubeEditorMenuBar(MainWindow, self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1156, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = CubeEditorToolBar(MainWindow, self)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        style = 'QGroupBox {font-size: 14px; font-weight: bold}'
        self.sideBoardBox.setStyleSheet(style)
        self.deckBox.setStyleSheet(style)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.sideBoardBox.setTitle(QtGui.QApplication.translate("MainWindow", "Sideboard(0)", None, QtGui.QApplication.UnicodeUTF8))
        self.deckBox.setTitle(QtGui.QApplication.translate("MainWindow", "Deck(0)", None, QtGui.QApplication.UnicodeUTF8))
        self.statsBox.setTitle(QtGui.QApplication.translate("MainWindow", "Quick deck statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.cardImageBox.setTitle(QtGui.QApplication.translate("MainWindow", "Card Image", None, QtGui.QApplication.UnicodeUTF8))
        self.cardInfoBox.setTitle(QtGui.QApplication.translate("MainWindow", "Filters", None, QtGui.QApplication.UnicodeUTF8))
        self.landButton.setText(QtGui.QApplication.translate("MainWindow", "Land", None, QtGui.QApplication.UnicodeUTF8))
        self.blackButton.setText(QtGui.QApplication.translate("MainWindow", "Black", None, QtGui.QApplication.UnicodeUTF8))
        self.greenButton.setText(QtGui.QApplication.translate("MainWindow", "Green", None, QtGui.QApplication.UnicodeUTF8))
        self.blueButton.setText(QtGui.QApplication.translate("MainWindow", "Blue", None, QtGui.QApplication.UnicodeUTF8))
        self.redButton.setText(QtGui.QApplication.translate("MainWindow", "Red", None, QtGui.QApplication.UnicodeUTF8))
        self.multicolorButton.setText(QtGui.QApplication.translate("MainWindow", "Multicolor", None, QtGui.QApplication.UnicodeUTF8))
        self.whiteButton.setText(QtGui.QApplication.translate("MainWindow", "White", None, QtGui.QApplication.UnicodeUTF8))
        self.resetFiltersButton.setText(QtGui.QApplication.translate("MainWindow", "Reset filters", None, QtGui.QApplication.UnicodeUTF8))
        self.sideaboardRadioButton.setText(QtGui.QApplication.translate("MainWindow", "Sideboard", None, QtGui.QApplication.UnicodeUTF8))
        self.deckRadioButton.setText(QtGui.QApplication.translate("MainWindow", "Deck", None, QtGui.QApplication.UnicodeUTF8))
        self.bothRadioButton.setText(QtGui.QApplication.translate("MainWindow", "Both", None, QtGui.QApplication.UnicodeUTF8))
        self.creatureButton.setText(QtGui.QApplication.translate("MainWindow", "Creature", None, QtGui.QApplication.UnicodeUTF8))
        self.artifactButton.setText(QtGui.QApplication.translate("MainWindow", "Artifact", None, QtGui.QApplication.UnicodeUTF8))
        self.nonCreatureButton.setText(QtGui.QApplication.translate("MainWindow", "Other Non-Creature Spells", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
