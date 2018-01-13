"""CardImageWindow class module."""

from PyQt4  import QtGui, QtCore


################################################################################
class CardImageWidget(QtGui.QLabel):
    """A window for showing a card image."""

#-------------------------------------------------------------------------------
    def __init__(self, parent, picsFolder, setNames):
        
        QtGui.QLabel.__init__(self, parent)
        
        self.setScaledContents(True)
        
        self._picsFolder = picsFolder
        self._setNames = setNames
        self._currentCard = None
        
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__showContextMenu)


#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __showContextMenu(self, pos):
        """Shows the context menu of the image widget."""

        contextMenu = QtGui.QMenu(self)
        
        contextMenu.addAction('Show backside', self.showBackside)
        contextMenu.addAction('Rotate 180 degrees', self.rotate180)
        
        if not self._currentCard:
            for action in contextMenu.actions():
                action.setEnabled(False)
                
        contextMenu.exec_(self.mapToGlobal(pos))

#-------------------------------------------------------------------------------
    def _cardImagePath(self, card):
        """
        Returns the path to this cards imagefile in the given imagefolder. 
        Uses same format as MWS card image naming.
        """
        

        return ''.join((self._picsFolder, 
                        '\\', 
                        self._setNames[card.mtgSetName], 
                        '\\', 
                        unicode(card.name.replace('/', '')), 
                        card.altArt, 
                        '.full.jpg'))

#==========================================================================#
#                              Public methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def setCardImage(self, card):
        """Sets the image of the card"""
        
        self._currentCard = card
        pixMap = QtGui.QPixmap((self._cardImagePath(card)))
        self.setPixmap(pixMap)
        

#-------------------------------------------------------------------------------
    def showBackside(self):
        """
        Flips over the card and shows the back side of the card. Only relevant 
        if the card is double sided. Otherwise shows the common backside of 
        the card.
        """
        
        if self._currentCard.isDual and \
           'Kamigawa' not in self._currentCard.Set._name:
            backSide = self._currentCard.dualCardName
            path = ''.join((self._picsFolder, '\\', 
                            self._setNames[self._currentCard.mtgSetName], '\\', 
                            backSide, '.full.jpg'))
            
            pixMap = QtGui.QPixmap(path)
            self.setPixmap(pixMap)
            
        else:
            path = 'Icons\\BackSide.jpg'
            pixMap = QtGui.QPixmap(path)
            self.setPixmap(pixMap)
        
#-------------------------------------------------------------------------------
    def rotate180(self):
        """
        Rotates the current card image 180 degrees. Only relevant if the card 
        is one of the Kamigawa block specials.
        """
        
        pixMap = QtGui.QPixmap((self._cardImagePath(self._currentCard)))
        rotateMatrix = QtGui.QMatrix()
        rotateMatrix.rotate(180)
        pixMap = pixMap.transformed(rotateMatrix)
        self.setPixmap(pixMap)
