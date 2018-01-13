"""CardPile-class module."""

from PyQt4 import QtCore, QtGui 

################################################################################
class CardPile:
    """
    A class representing a pile of cards in the visual mode canvas. It has
    useful methods of keeping cards in order on top of each other.
    
    The piles topLeft coordinate has to be adjusted after creation, 
    which should allways happen after the first card is inserted into it.
    If there are no cards in a pile it should be deleted immediately.
    The topLeft should stay the same no matter how many cards the pile has. 
    """

#-------------------------------------------------------------------------------
    def __init__(self, parentCanvas):
    
        #------------------------------------
        self._parentCanvas = parentCanvas
        self._cardLabels = []
        self._topLeft = (0, 0)

        #------------------------------------
        

        #------------------------------------

#==========================================================================#
#                              Public methods                              #
#==========================================================================#
#-------------------------------------------------------------------------------
    def addCardLabel(self, cardLabel, index):
        """
        Adds a cardlabel to the pile in a given position.
        """
        
        self._cardLabels.insert(index, cardLabel)
        cardLabel._pile = self
        self._organize()
    
#-------------------------------------------------------------------------------
    def removeCardLabel(self, cardLabel):
        """
        Removes a cardlabel to the pile.
        """
        self._cardLabels.remove(cardLabel)
        self._organize()
        cardLabel.close()
        
        if not self._cardLabels:
            self._parentCanvas._cardPiles.remove(self)
    
#-------------------------------------------------------------------------------
    def cardLabelIndex(self, cardLabel):
        """
        Returns the position of the cardLabel in the pile
        """
        
        return self._cardLabels.index(cardLabel)
    
#-------------------------------------------------------------------------------
    def movePile(self, x, y):
        """
        Moves the whole pile in the location (x, y).
        """
        
        for label in self._cardLabels:
            label.move(x,y)
        
        self._topLeft = (x, y)
        self._organize()
        
#-------------------------------------------------------------------------------
    def getRect(self):
        """
        Returns the rect of the pile. Basically the rects coordinates are the
        top ones of the highest card and bottom ones of the lowest.
        """
        
        if not self._cardLabels:
            return QtCore.QRect()
        
        topRect = self._cardLabels[0].rect()
        bottomRect = self._cardLabels[-1].rect()
        
        QtCore.QRect(topRect.left(), topRect.top(), 
                     topRect.right(), bottomRect.bottom)

#-------------------------------------------------------------------------------
    def getSectionCut(self, sectionIndex):
        """
        Removes and returns aall the cards from section of the cardPile
        given by sectionIndex
        """
        
        cut = self._cardLabels[sectionIndex:]
        
        for cardLabel in self._cardLabels[sectionIndex:]:
            self._cardLabels.remove(cardLabel)
            cardLabel.close()
        
        self._organize()
        
        if sectionIndex == 0:
            self._parentCanvas._cardPiles.remove(self)
        
        return cut
        
#-------------------------------------------------------------------------------
    def intersects(self, rect):
        """
        Returns all the CardLabels of the pile which rects intersect with 
        given rect.
        """
        
        return [label for label in self._cardLabels if
                label.rect().intersects(rect)]

#-------------------------------------------------------------------------------
    def sortByName(self):
        """
        Sorts the pile's cards by name.
        """
        
        pass

#-------------------------------------------------------------------------------
    def getPileStats(self, event):
        """
        Returns the stats of the cards in the Pile.
        """
        
#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _organize(self):
        """
        Organizes the cards in the pile in a neat order. Moves sections of 
        the pile up or down to replace or plug a hole and raises the cards
        in order the way that one only sees the title from underneath other
        cards
        """
        
        for index in range(len(self._cardLabels)):
            label = self._cardLabels[index]
            label.move(self._topLeft[0], self._topLeft[1] + 20 * index)
            label.raise_()
            


#==========================================================================#
#                              Internal methods                            #
#==========================================================================#

#==========================================================================#
#                              Properties                                  #
#==========================================================================#