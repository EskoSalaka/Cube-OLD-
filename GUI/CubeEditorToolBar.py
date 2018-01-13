"""The CubeEditorToolBar class module."""

from PyQt4 import QtGui

################################################################################
class CubeEditorToolBar(QtGui.QToolBar):
    """Toolbar for the mainWindow."""

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent):
        """"""
        
        super(CubeEditorToolBar, self).__init__(parent)
        self._mainFrameParent = mainFrameParent
        
        openAction = QtGui.QAction(QtGui.QIcon('Icons\open.ico'), 'Open cube', self)
        openAction.setStatusTip('Open a cube')
        openAction.triggered.connect(self._open)
        
        saveAction = QtGui.QAction(QtGui.QIcon('Icons\save.ico'), 'Save cube', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save cube as')
        saveAction.triggered.connect(self._save)
        
        statsAction = QtGui.QAction(QtGui.QIcon('Icons\statistics.ico'), 'Deep analysis', self)
        statsAction.setShortcut('Ctrl+A')
        statsAction.setStatusTip('Deep analysis')
        statsAction.triggered.connect(self._stats)
        
        self._colorAction = QtGui.QAction(QtGui.QIcon('Icons\color.ico'), 'Color the cards which are already in the cube', self)
        self._colorAction.setShortcut('Ctrl+D')
        self._colorAction.setStatusTip('Color the cards which are already in the cube')
        self._colorAction.triggered.connect(self._colorCards)

        resizeAction = QtGui.QAction(QtGui.QIcon('Icons\resize.ico'), 'Resize columns to contents', self)
        resizeAction.setShortcut('Ctrl+R')
        resizeAction.setStatusTip('Resize columns to contents')
        resizeAction.triggered.connect(self._resize)
        
        
        self.addActions([openAction, saveAction, statsAction, self._colorAction, resizeAction])
        
        
        
#==========================================================================#
#                              Actions                                     #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _stats(self):
        """Stats action handler. Shows deeper analysis of the cube."""

#-------------------------------------------------------------------------------
    def _open(self):
        """Open action handler. Opens and loads a cube."""
        
        self._mainFrameParent.openCube()

#-------------------------------------------------------------------------------
    def _resize(self):
        """
        Resize action handler. Resizes the columns of the deck and sideboard
        to contents
        """
        
        self._mainFrameParent.cubeList.resizeColumns()
        self._mainFrameParent.masterBaseList.resizeColumns()

#-------------------------------------------------------------------------------
    def _colorCards(self):
        """
        Color cards handler. Colors the cards in the master list which are 
        already in the cube
        """

        self._mainFrameParent.colorMasterListCards()

#-------------------------------------------------------------------------------
    def _save(self):
        """Save action handler. Saves the deck as mwsdeck format."""
        
        self._mainFrameParent.saveCubeAs()