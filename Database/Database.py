"""Database-class module."""

from collections import defaultdict

################################################################################
class Database:
    """
    A database class, which hold all the mtg cards and sets. The cards are also
    stored seperately in dictionaries by name and by id for more convenient 
    access.
    """

#-------------------------------------------------------------------------------
    def __init__(self):
        self._cardsByName = defaultdict(list)
        self._cardsById = {}
        self._mtgSets = {}

#==========================================================================#
#                              Public methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def addSet(self, mtgSet):
        """
        Adds a new mtgset instance to the database. The cards of the set dont 
        have to be added to the _cardsByName dict seperately, this function 
        automatically does it.
        """

        if self.hasMtgSet(mtgSetName=mtgSet.name):
            return
        
        self._mtgSets[mtgSet.name] = mtgSet
        
        for card in mtgSet.cards:
            self._cardsByName[card.name].append(card)
            self._cardsById[card.id] = card

#-------------------------------------------------------------------------------
    def editSetName(self, origMtgSetName=None, newMtgSetName=None,
                          origMtgSetCode=None, newMtgSetCode=None):
        """
        Changes set name or code.
        """
        
        if origMtgSetName:
            if newMtgSetName:
                try:
                    self.getMtgSet(mtgSetName=origMtgSetName).name = newMtgSetName
                    self._mtgSets[newMtgSetName] = self._mtgSets.pop(origMtgSetName)
                except AttributeError:
                    print '{mtgSetName} not found in the database'.format(mtgSetName=origMtgSetName)
            
            if newMtgSetCode:
                try:
                    self.getMtgSet(mtgSetName=origMtgSetName).setCode = newMtgSetCode
                except AttributeError:
                    print '{mtgSetCode} not found in the database'.format(mtgSetCode=origMtgSetCode)
        
        if origMtgSetCode:
            if newMtgSetName:
                try:
                    self.getMtgSet(mtgSetCode=origMtgSetCode).name = newMtgSetName
                    self._mtgSets[newMtgSetName] = self._mtgSets.pop(origMtgSetName)
                except AttributeError:
                    print '{mtgSetName} not found in the database'.format(mtgSetName=origMtgSetName)
            
            if newMtgSetCode:
                try:
                    self.getMtgSet(mtgSetCode=origMtgSetCode).setCode = newMtgSetCode
                except AttributeError:
                    print '{mtgSetCode} not found in the database'.format(mtgSetCode=origMtgSetCode)
        
        
        
#-------------------------------------------------------------------------------
    def getCards(self, cardName):
        """
        Returns all the cards instances in the database of 
        the given name.
        """
        
        return self._cardsByName[cardName]

#-------------------------------------------------------------------------------
    def getRegularCards(self, cardName):
        """
        Returns all the cards instances in the database of 
        the given name, which belong in regular mtg sets.
        """
        
        regularSetNames = self.getRegularMtgSetNames()
        cards = self.getCards(cardName)
        
        return [card for card in cards if card.mtgSetName in regularSetNames]
                
#-------------------------------------------------------------------------------
    def getAllCards(self, single=True, basicLands=False):
        """
        Returns all the cards instances in the database. If single is True then
        only one of each card will be returned, otherwise all copies. If
        basicLands is True also basic lands will be returned.
        """
        
        if single:
            cards = [cards[-1] for cards in self._cardsByName.values()]
        else:
            cards = self._cardsById.values()
        
        if not basicLands:
            cards = [card for card in cards if not 'Basic Land' in card.type]
        
        return cards
    
#-------------------------------------------------------------------------------
    def getCard(self, cardId):
        """
        Returns a card by the given Id.
        """
        
        return self._cardsById[cardId]
        
#-------------------------------------------------------------------------------
    def hasMtgSet(self, mtgSetName=None, mtgSetCode=None):
        """
        Returns True if the mtg set with the given name or set code is in the
        database, and False otherwise.
        """
        
        if mtgSetName:
            return mtgSetName in self.getMtgSetNames()
        
        elif mtgSetCode:
            return mtgSetCode in [mtgSet.setCode for mtgSet in 
                                  self._mtgSets.values()]
            
        
#-------------------------------------------------------------------------------
    def getMtgSet(self, mtgSetName=None, mtgSetCode=None):
        """
        Returns the set with the given name or code.
        """
        
        if mtgSetName:
            return self._mtgSets[mtgSetName]
        
        elif mtgSetCode:
            for mtgSet in self._mtgSets.values():
                if mtgSetCode == mtgSet.setCode:
                    return mtgSet

#-------------------------------------------------------------------------------
    def getMtgSetNames(self):
        """
        Returns a dictionary of the set names and set codes stored in the 
        database.
        """
        
        mtgSetNames = {}
        
        for mtgSet in self._mtgSets.values():
            mtgSetNames[mtgSet.name] = mtgSet.setCode
        
        return mtgSetNames

#-------------------------------------------------------------------------------
    def getRegularMtgSetNames(self):
        """
        Returns a dictionary of the regular set names and set codes stored in the 
        database.
        """
        
        regularMtgSetNames = {}
        
        for mtgSet in self._mtgSets.values():
            if not mtgSet.isSpecial:
                regularMtgSetNames[mtgSet.name] = mtgSet.setCode
        
        return regularMtgSetNames

#-------------------------------------------------------------------------------
    def getMtgSets(self):
        """
        Returns a dictionary of all the mtg sets in the database.
        """
        
        return self._mtgSets
        
#-------------------------------------------------------------------------------
    def hasCard(self, cardName):
        """
        Returns True if a card with the given name is in the database and false
        otherwise.
        """
        
        return cardName in self._cardsByName.keys()
        
#-------------------------------------------------------------------------------
    def format(self):
        """
        Empties the database of everything
        """
        
        self._cardsByName = defaultdict(list)
        self._cardsById = {}
        self._mtgSets = {}

#-------------------------------------------------------------------------------
    def deleteMtgSet(self):
        """
        Removes a specified set from the database.
        """
        
#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#==========================================================================#
#                              Internal methods                            #
#==========================================================================#

#==========================================================================#
#                              Properties                                  #
#==========================================================================#
