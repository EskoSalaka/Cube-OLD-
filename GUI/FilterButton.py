"""The FilterButton class module."""

from PyQt4 import QtGui, QtCore

################################################################################
class FilterButton(QtGui.QPushButton):
    """
    A PyQt button with some custom procedures added for filtering stuff 
    from cardlists. his same class handles all the filtering except for
    multicolored cards, which belongs to the MultiColorFilterButton class.
    """

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent, filterWord,
                 secondaryList, primaryList):
        
        QtGui.QPushButton.__init__(self, parent=parent)
        
        self._mainFrameParent = mainFrameParent
        self._filterWord = filterWord
        self._secondaryList = secondaryList
        self._primaryList = primaryList
        
        self.clicked.connect(self.__onClicked)
        self.setCheckable(True)
        
        style = """
        FilterButton {
        min-height: 1.5em;
        font: 1em;
        margin: 0 1px 0 1px;
        color: white;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2198c0, stop: 1 #0d5ca6);
        border-style: outset;
        border-radius: 3px;
        border-width: 1px;
        border-color: #0c457e;
        background-image: url(Manasymbols\Small\G.gif);}
                    
        FilterButton:pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #0d5ca6, stop: 1 #2198c0);}
        
        FilterButton:checked {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #0d5ca6, stop: 1 #2198c0);}
        """
        
        self.setStyleSheet(style)

#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __onClicked(self):
        """Handles the clicked event."""
        
        if self._filterWord == 'reset':
                if self._mainFrameParent.whiteButton.isChecked():
                    self._mainFrameParent.whiteButton.click()
                if self._mainFrameParent.blackButton.isChecked():
                    self._mainFrameParent.blackButton.click()
                if self._mainFrameParent.redButton.isChecked():
                    self._mainFrameParent.redButton.click()
                if self._mainFrameParent.blueButton.isChecked():
                    self._mainFrameParent.blueButton.click()
                if self._mainFrameParent.greenButton.isChecked():
                    self._mainFrameParent.greenButton.click()
                if self._mainFrameParent.creatureButton.isChecked():
                    self._mainFrameParent.creatureButton.click()
                if self._mainFrameParent.artifactButton.isChecked():
                    self._mainFrameParent.artifactButton.click()
                if self._mainFrameParent.multicolorButton.isChecked():
                    self._mainFrameParent.multicolorButton.reset()
                if self._mainFrameParent.nonCreatureButton.isChecked():
                    self._mainFrameParent.nonCreatureButton.click()
                if self._mainFrameParent.landButton.isChecked():
                    self._mainFrameParent.landButton.click()
                
                self._secondaryList._filters = []
                self._primaryList._filters = []
                    
        if self.isChecked():
            if self._mainFrameParent.sideaboardRadioButton.isChecked():
                self._secondaryList.addFilterWord(self._filterWord)
                    
                    
            elif self._mainFrameParent.deckRadioButton.isChecked():
                self._primaryList.addFilterWord(self._filterWord)
                    
            else:
                self._secondaryList.addFilterWord(self._filterWord)
                self._primaryList.addFilterWord(self._filterWord)
                    
        else:
            if self._mainFrameParent.sideaboardRadioButton.isChecked():
                self._secondaryList.removeFilterWord(self._filterWord)
                    
                    
            elif self._mainFrameParent.deckRadioButton.isChecked():
                self._primaryList.removeFilterWord(self._filterWord)
                    
            else:
                self._secondaryList.removeFilterWord(self._filterWord)
                self._primaryList.removeFilterWord(self._filterWord)
        
        self._secondaryList.applyFilters()
        self._primaryList.applyFilters()


################################################################################
class MultiColorFilterButton(FilterButton):
    """
    Similar to the filterButton-class except sligtly more complcated. It has a
    drop-down menu for choosing which multicolored cards to filter.
    """

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent, secondaryList, primaryList):
        
        QtGui.QPushButton.__init__(self, parent=parent)
        
        self._mainFrameParent = mainFrameParent
        self._filterWord = 'M'
        self._secondaryList = secondaryList
        self._primaryList = primaryList
        
        self.__createMenu()
        self.setCheckable(True)
        
        style = """/* Let's make the size of the button 1,5 times of font size. */
                   min-height: 1.5em;
                   /* Font size just 1.*/
                   font: 1em;
                   /* Margins so that we get a little space on the left and right. */
                   margin: 0 1px 0 1px;
                   /* The font color */ 
                   color: white;
                   /* Here's the background gradient with start point, end point, 
                    stop "percentage" and color, stop percentage and color. */
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                      stop: 0 #2198c0, stop: 1 #0d5ca6);
                    /* We'll round the borders. */
                    border-style: outset;
                    /* Round radius will be 3px */
                    border-radius: 3px;
                    /* Border is only one pixel */
                    border-width: 1px;
                    /* Border color is now set */
                    border-color: #0c457e;
                    """
    
        self.setStyleSheet(style)
        
#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __onClicked(self, sender):
        """All the menu button call for this event."""

        if sender == self._black:
            if self._black.isChecked():
                self._filterWord = self._filterWord + 'B'
            else:
                self._filterWord = self._filterWord.replace('B', '')
        
        if sender == self._white:
            if self._white.isChecked():
                self._filterWord = self._filterWord + 'W'
            else:
                self._filterWord = self._filterWord.replace('W', '')
        
        if sender == self._blue:
            if self._blue.isChecked():
                self._filterWord = self._filterWord + 'U'
            else:
                self._filterWord = self._filterWord.replace('U', '')
        
        if sender == self._red:
            if self._red.isChecked():
                self._filterWord = self._filterWord + 'R'
            else:
                self._filterWord = self._filterWord.replace('R', '')
        
        if sender == self._green:
            if self._green.isChecked():
                self._filterWord = self._filterWord + 'G'
            else:
                self._filterWord = self._filterWord.replace('G', '')
        
        self._secondaryList.removeFilterWord(self._filterWord)
        self._primaryList.removeFilterWord(self._filterWord)
        
        if self.__anyChecked():
            self.setChecked(True)
            if self._mainFrameParent.sideaboardRadioButton.isChecked():
                self._secondaryList.addFilterWord(self._filterWord)
            elif self._mainFrameParent.deckRadioButton.isChecked():
                self._primaryList.addFilterWord(self._filterWord)
            else:
                self._secondaryList.addFilterWord(self._filterWord)
                self._primaryList.addFilterWord(self._filterWord)
        else:
            self.setChecked(False)
        
        self._secondaryList.applyFilters()
        self._primaryList.applyFilters()

#-------------------------------------------------------------------------------
    def __createMenu(self):
        """
        Additional method of the Multicolor filterbutton. Creates a menu
        where the user can choose which colors of the multicolored cards 
        to filter. The filterword it sends to the cardlists starts with
        'M' and continues with colours to be filtered.
        
        for example the filterWord 'MRUW' would filter all the multicolored
        cards with one or more of the colours 'R', 'U' and 'W'.
        """
        
        self._menu = QtGui.QMenu(self)
        
        self._black = QtGui.QAction('Black', self)
        self._black.triggered.connect(self.__black)
        self._black.setCheckable(True)
        
        self._green = QtGui.QAction('Green', self)
        self._green.triggered.connect(self.__green)
        self._green.setCheckable(True)
        
        self._red = QtGui.QAction('Red', self)
        self._red.triggered.connect(self.__red)
        self._red.setCheckable(True)
        
        self._blue = QtGui.QAction('Blue', self)
        self._blue.triggered.connect(self.__blue)
        self._blue.setCheckable(True)
        
        self._white = QtGui.QAction('White', self)
        self._white.triggered.connect(self.__white)
        self._white.setCheckable(True)
        
        self._menu.addActions([self._black, self._green, self._red, 
                               self._blue, self._white])
        self.setMenu(self._menu)
        
#-------------------------------------------------------------------------------
    def __black(self):
        """Black menu action handler"""
        
        self.__onClicked(self._black)
    
#-------------------------------------------------------------------------------
    def __red(self):
        """Red menu action handler"""
        
        self.__onClicked(self._red)

#-------------------------------------------------------------------------------
    def __blue(self):
        """Blue menu action handler"""
        
        self.__onClicked(self._blue)
        
#-------------------------------------------------------------------------------
    def __green(self):
        """Green menu action handler"""
        
        self.__onClicked(self._green)

#-------------------------------------------------------------------------------
    def __white(self):
        """White menu action handler"""
        
        self.__onClicked(self._white)

#-------------------------------------------------------------------------------
    def __anyChecked(self):
        """Returns True if any of the menuactions of the menu is checked."""
        
        for action in self._menu.actions():
            if action.isChecked():
                return True
            
        return False

#-------------------------------------------------------------------------------
    def reset(self):
        """Removes all the filters."""
        
        self._secondaryList.removeFilterWord(self._filterWord)
        self._primaryList.removeFilterWord(self._filterWord)
        self._filterWord = 'M'
        self._white.setChecked(False)
        self._black.setChecked(False)
        self._blue.setChecked(False)
        self._red.setChecked(False)
        self._green.setChecked(False)
        self.setChecked(False)
        