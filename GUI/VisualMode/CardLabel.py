"""CardLabel-class module."""

from PyQt4 import QtCore, QtGui 


################################################################################
class CardLabel(QtGui.QLabel):
    """
    A QLabel class representing a card that you can move around on a desktop.
    """

#-------------------------------------------------------------------------------
    def __init__(self, cardData, parent, setNames, picsFolder, pile=None):
        
        QtGui.QLabel.__init__(self, parent=parent)
        
        #------------------------------------
        self._cardData = cardData
        self._pile = pile
        self._setNames = setNames
        self._picsFolder = picsFolder
        
        #------------------------------------
        #Setting the cards pixmap by using thepicsfolder location 
        #and setnames
        cardImageLoc = ''.join((picsFolder, 
                                '\\', 
                                setNames[str(self._cardData[2])], 
                                '\\', 
                                unicode(self._cardData[1].replace('/', '')), 
                                '', 
                                '.full.jpg'))
        
        self.setPixmap(QtGui.QPixmap(cardImageLoc).scaledToWidth(150, QtCore.Qt.SmoothTransformation))
        
        #------------------------------------

#==========================================================================#
#                              Public methods                              #
#==========================================================================#
#-------------------------------------------------------------------------------
    def getCardData(self):
        """
        Returns a list of the most important data of the card.
        """
        
        return self._cardData

#-------------------------------------------------------------------------------
    def positionInPile(self):
        """
        Returns the position of the card in its pile.
        """
        
        return self._pile.cardLabelIndex(self)
    

#-------------------------------------------------------------------------------
    def getPile(self):
        """
        Returns the pile the card is in.
        """
        
        return self._pile

#-------------------------------------------------------------------------------
    def getCopy(self):
        """
        Returns the pile the card is in.
        """

        return CardLabel(self._cardData, self.parent(), self._setNames, 
                         self._picsFolder, self._pile)


        
#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#==========================================================================#
#                              Internal methods                            #
#==========================================================================#

#==========================================================================#
#                              Properties                                  #
#==========================================================================#