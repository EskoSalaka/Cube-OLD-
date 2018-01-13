"""The MainWindowMenuBar class module."""

from PyQt4 import QtGui
from StandardGenerationDialog import Ui_Dialog as StandardGenerationDialog
from BasicLandDialog import Ui_LandImageDialog as BasicLandDialog
from SetNameEditorDialog import SetNameEditorDialog
from UpdateDialog import UpdateDialog

################################################################################
class MainWindowMenuBar(QtGui.QMenuBar):
    """menubar for the mainWindow."""

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent):
        """"""
        
        super(MainWindowMenuBar, self).__init__(parent)
        self._mainFrameParent = mainFrameParent
        
        #------------------------
        fileMenu = QtGui.QMenu('&File', self)
        
        exitAction = QtGui.QAction('&Quit', self)        
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self._quit)
        
        saveDeckAction = QtGui.QAction('&Save deck as', self)        
        saveDeckAction.setStatusTip('Save deck as')
        saveDeckAction.triggered.connect(self._saveDeckAs)
        
        openDeckAction = QtGui.QAction('&Open a deck', self)        
        openDeckAction.setStatusTip('Open a deck')
        openDeckAction.triggered.connect(self._openDeck)
        
        fileMenu.addActions([openDeckAction, saveDeckAction])
        fileMenu.addSeparator()
        fileMenu.addActions([exitAction])
        
        #------------------------
        sealedMenu = QtGui.QMenu('&Sealed deck generation', self)
        
        standardAction = QtGui.QAction('&Standard sealed deck', self)        
        standardAction.setStatusTip('Generate a standard booster sealed deck')
        standardAction.triggered.connect(self._standardSealed)
        
        cubeMenu = QtGui.QMenu('&Sealed deck from a cube', self)
        sealedMenu.addMenu(cubeMenu)
        
        fromMWSDeckAction = QtGui.QAction('&.MWSDeck file', self)        
        fromMWSDeckAction.setStatusTip('Generate a sealed deck from a custom cube in MWSDeck format')
        fromMWSDeckAction.triggered.connect(self._cubeSealedFromMWSDeck)
        
        fromCubeFileAction = QtGui.QAction('&.Cube file', self)        
        fromCubeFileAction.setStatusTip('Generate a sealed deck from a custom cube in .cube file')
        fromCubeFileAction.triggered.connect(self._cubeSealedFromCubeFile)
        
        fromTextFileAction = QtGui.QAction('&.txt file', self)        
        fromTextFileAction.setStatusTip('Generate a sealed deck from a custom cube in .txt file')
        fromTextFileAction.triggered.connect(self._cubeSealedFromTextFile)
        
        sealedMenu.addActions([standardAction])
        cubeMenu.addActions([fromMWSDeckAction, fromCubeFileAction, fromTextFileAction])
        
        #------------------------
        settingsMenu = QtGui.QMenu('&Settings', self)
        
        imageFolderAction = QtGui.QAction('&Set image folder', self)        
        imageFolderAction.setStatusTip('Set the folder containing the card images')
        imageFolderAction.triggered.connect(self._imageFolder)
        
        landImageAction = QtGui.QAction('&Set images for basic lands', self)        
        landImageAction.setStatusTip('Set the images for basic lands to use wit hMWS')
        landImageAction.triggered.connect(self._setBasicLandImages)
        
        autoUpdateStatsWidgetAction = QtGui.QAction('&Automatically update the statistics panel', self)        
        autoUpdateStatsWidgetAction.setStatusTip('Update the database')
        autoUpdateStatsWidgetAction.toggled.connect(self._autoUpdateStatsWidgetAction)
        autoUpdateStatsWidgetAction.setCheckable(True)
        
        if self._mainFrameParent.getSetting('autoUpdateStatsWidget'):
            autoUpdateStatsWidgetAction.setChecked(True)
        
        settingsMenu.addActions([imageFolderAction, landImageAction, 
                                 autoUpdateStatsWidgetAction])
        
        
        #------------------------
        databaseMenu = QtGui.QMenu('&Database', self)
        
        updateAction = QtGui.QAction('&Update the database', self)        
        updateAction.setStatusTip('Update the database')
        updateAction.triggered.connect(self._update)
        
        editSetNamesAction = QtGui.QAction('&Edit set names and codes', self)        
        editSetNamesAction.setStatusTip('Edit set names and codes')
        editSetNamesAction.triggered.connect(self._editSetNames)
        
        setCodeFormatMenu = QtGui.QMenu('&Set predefined setcodes for all the sets', self)        
        setCodeFormatMenu.setStatusTip('Set predefined setcodes for all the sets')
        
        mwsSetCodesAction = QtGui.QAction('&MWS setcodes', self)        
        mwsSetCodesAction.setStatusTip('MWS setcodes')
        mwsSetCodesAction.triggered.connect(self._setMwsSetcodes)
        
        wizardsSetCodesAction = QtGui.QAction('&Wizards official setcodes', self)        
        wizardsSetCodesAction.setStatusTip('Wizards official setcodes')
        wizardsSetCodesAction.triggered.connect(self._setWizardsSetcodes)
        
        editSetNamesAction = QtGui.QAction('&Edit set names and codes', self)        
        editSetNamesAction.setStatusTip('Edit set names and codes')
        editSetNamesAction.triggered.connect(self._editSetNames)
        
        formatAction = QtGui.QAction('&Format the database', self)        
        formatAction.setStatusTip('Format the database')
        formatAction.triggered.connect(self._format)
        
        setCodeFormatMenu.addActions([mwsSetCodesAction, wizardsSetCodesAction])
        databaseMenu.addActions([editSetNamesAction, updateAction, formatAction])
        databaseMenu.addMenu(setCodeFormatMenu)
        
        #------------------------
        self.addMenu(fileMenu)
        self.addMenu(sealedMenu)
        self.addMenu(settingsMenu)
        self.addMenu(databaseMenu)
       

#==========================================================================#
#                              Actions                                     #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _quit(self):
        """Exits program."""

#-------------------------------------------------------------------------------
    def _standardSealed(self):
        """Opens a dialog for creating a standard booster sealed deck."""
        
        StandardGenerationDialog(self.parent(), self._mainFrameParent)
        
#-------------------------------------------------------------------------------
    def _imageFolder(self):
        """Sets the imagefolder"""
        
        caption='Choose the folder that contains the card images'
        path = QtGui.QFileDialog.getExistingDirectory(caption=caption)
        
        if path:
            self._mainFrameParent.configure(picsFolder=str(path))
            self._mainFrameParent.cardImageWidget._picsFolder = path

#-------------------------------------------------------------------------------
    def _setBasicLandImages(self):
        """Exits program."""
        
        BasicLandDialog(self.parent(), self._mainFrameParent)
        
#-------------------------------------------------------------------------------
    def _saveDeckAs(self):
        """"""
        
        self._mainFrameParent.configure(currentDeckPath='', currentDeckSaved=False)
        self._mainFrameParent.saveDeckAs()
        
#-------------------------------------------------------------------------------
    def _openDeck(self):
        """Opens a deck in mws format and loads the cards in correct lists."""
        
        self._mainFrameParent.openMWSDeck()
        

#-------------------------------------------------------------------------------
    def _cubeSealedFromMWSDeck(self):
        """
        Calls the mainwindows method for creating a cube sealed from an 
        mwsdeckfile.
        """
        
        self._mainFrameParent.cubeSealedFromMWSDeckFile()

#-------------------------------------------------------------------------------
    def _editSetNames(self):
        """
        Opens the set name editor dialog.
        """
        
        SetNameEditorDialog(self._mainFrameParent, 
                            self._mainFrameParent)
        
#-------------------------------------------------------------------------------
    def _update(self):
        """
        Updates the program database from online.
        """
        
        UpdateDialog(self._mainFrameParent, 
                     self._mainFrameParent)

#-------------------------------------------------------------------------------
    def _cubeSealedFromCubeFile(self):
        """
        Calls the mainwindows method for creating a cube sealed from a 
        cube file.
        """
        
        self._mainFrameParent.cubeSealedFromCubeFile()

#-------------------------------------------------------------------------------
    def _cubeSealedFromTextFile(self):
        """
        Calls the mainwindows method for creating a cube sealed from a 
        text file.
        """
        
        self._mainFrameParent.cubeSealedFromTextFile()

#-------------------------------------------------------------------------------
    def _autoUpdateStatsWidgetAction(self, toggled):
        """
        Checks if the option to autoupdate the statswidgetpanel is toggled
        and configures the setting.
        """
        
        if toggled:
            self._mainFrameParent.configure(autoUpdateStatsWidget=1)
        else:
            self._mainFrameParent.configure(autoUpdateStatsWidget='')

#-------------------------------------------------------------------------------
    def _format(self, toggled):
        """
        Formats the database.
        """
        
        title = 'Format database'
        msg = 'Really format the database? This cannot be undone.'
        
        reply = QtGui.QMessageBox.question(self, title, msg,
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.Cancel)
        
        if reply == QtGui.QMessageBox.Yes:
            db = self._mainFrameParent.getDatabase()
            db.format()
            self._mainFrameParent.saveDatabase(db)

#-------------------------------------------------------------------------------
    def _setWizardsSetcodes(self):
        """
        Sets the Wizards official setcodes to all the mtgsets in the database.
        """
        
        

#-------------------------------------------------------------------------------
    def _setMwsSetcodes(self):
        """
        Sets the MWS setcodes to all the mtgsets in the database.
        """
        
        mwsSetCodes = self._mainFrameParent.getMwsSetCodes()
        db = self._mainFrameParent.getDatabase()
        
        for (setName, setCode) in mwsSetCodes.iteritems():
            if db.hasMtgSet(mtgSetName=unicode(setName.title())):
                db.editSetName(origMtgSetName=setName.title(), 
                               newMtgSetCode=setCode.upper())
        
        self._mainFrameParent.saveDatabase(db)
        
        
