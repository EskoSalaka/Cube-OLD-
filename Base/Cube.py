"""Cube class module."""

import random
from collections import defaultdict

################################################################################
class Cube:
    """
    A list of cards representing a cube. It is similar to the Set class
    but is simpler and has less methods.
    """

#-------------------------------------------------------------------------------
    def __init__(self, cards):
        
        self._cards = cards
        

#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#==========================================================================#
#                              Public methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def addCard(self, card):
        """Adds a card to the cube."""
        
        self._cards.append(card)

#-------------------------------------------------------------------------------
    def getSealed(self, numOfCards=90, duplicates=False):
        """Returns a sealed deck pool with given properties"""
        
        if duplicates:
            return [random.choice(self._cards) for _ in range(numOfCards)]
        else:
            return random.sample(self._cards, numOfCards)

#-------------------------------------------------------------------------------
    def getSortedCards(self):
        """
        Returns a dictionary of the cube's cards sorted by first color,
        second type and third manacost.
        
        For instance black creatures with converted manacost 3 are found
        by sortedCards["B"]["Creatures"][3]
        """
        
        sortedCards = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        counter = 0
        for card in self._cards:
            sortedCards[card.simpleColor][card.simpleType][card.simpleCC].append(card)
            counter = counter + 1

        return sortedCards

#-------------------------------------------------------------------------------
    def getCards(self):
        """
        Returns a simple list pf cards in the cube.
        """
        
        return self._cards
        