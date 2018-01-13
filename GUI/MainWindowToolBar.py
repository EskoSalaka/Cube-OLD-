"""The MainWindowToolBar class module."""

from PyQt4 import QtGui

################################################################################
class MainWindowToolBar(QtGui.QToolBar):
    """Toolbar for the mainWindow."""

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent):
        """"""
        
        super(MainWindowToolBar, self).__init__(parent)
        self._mainFrameParent = mainFrameParent
        
        openAction = QtGui.QAction(QtGui.QIcon('Icons\open.ico'), 'Open deck', self)
        openAction.setStatusTip('Open a deck')
        openAction.triggered.connect(self._open)
        
        saveAction = QtGui.QAction(QtGui.QIcon('Icons\save.ico'), 'Save deck', self)
        saveAction.setStatusTip('Save deck as')
        saveAction.triggered.connect(self._save)
        
        statsAction = QtGui.QAction(QtGui.QIcon('Icons\statistics.ico'), 'Deep analysis', self)
        statsAction.setStatusTip('Deep analysis')
        statsAction.triggered.connect(self._stats)

        resizeAction = QtGui.QAction(QtGui.QIcon('Icons\save2'), 'Resize columns to contents', self)
        resizeAction.setStatusTip('Resize columns to contents')
        resizeAction.triggered.connect(self._resize)
        
        openCubeEditorAction = QtGui.QAction(QtGui.QIcon('Icons\cube'), 'Open cube editor', self)
        openCubeEditorAction.setStatusTip('Open cube editor')
        openCubeEditorAction.triggered.connect(self._openCubeEditor)
        
        refreshAction = QtGui.QAction(QtGui.QIcon('Icons\gtk_refresh'), 'Refresh', self)
        refreshAction.setStatusTip('Refresh the gui')
        refreshAction.triggered.connect(self._refresh)
        
        self.addActions([openAction, saveAction, statsAction, 
                         resizeAction, openCubeEditorAction,refreshAction])
        
        
        
#==========================================================================#
#                              Actions                                     #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _stats(self):
        """Stats action handler. Shows deeper analysis of the deck."""

#-------------------------------------------------------------------------------
    def _open(self):
        """Open action handler. Opens and loads a deck."""
        
        self._mainFrameParent.openMWSDeck()

#-------------------------------------------------------------------------------
    def _resize(self):
        """
        Resize action handler. Resizes the columns of the deck and sideboard
        to contents
        """
        
        self._mainFrameParent.deckList.resizeColumns()
        self._mainFrameParent.sideBoardList.resizeColumns()
        

#-------------------------------------------------------------------------------
    def _save(self):
        """Save action handler. Saves the deck as mwsdeck format."""
        
        self._mainFrameParent.saveDeck()
        
#-------------------------------------------------------------------------------
    def _openCubeEditor(self):
        """OpenCubeEditor action handler. Opens the cube editor.."""
        
        self._mainFrameParent.openCubeEditor()

#-------------------------------------------------------------------------------
    def _refresh(self):
        """Refreshes the GUI."""
        
        self._mainFrameParent.statsWidget.Update()
        self._mainFrameParent.refreshNumbers()