"""Set-class module."""

import random

################################################################################
class Set:
    """An MTG set class."""

#-------------------------------------------------------------------------------
    def __init__(self, name, setCode, isSpecial):
        
        self._name = name
        self._setCode = setCode
        self._cards = []
        self._basicLands = []
        self._isSpecial = isSpecial
        
        self._generationCardList = []
        
#==========================================================================#
#                              Internal methods                            #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __str__(self):
        """String representation."""
        
        return self._name

#==========================================================================#
#                              Public methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def hasCard(self, **kwargs):
        """Returns True if the specified card is in the set."""
        
        if 'cardId' in kwargs.keys():
            if kwargs['cardId'] in [card.id for card in self._cards]:
                return True
            
        elif 'cardName' in kwargs.keys():
            if kwargs['cardName'] in [card.name for card in self._cards]:
                return True
        else:
            return False

#-------------------------------------------------------------------------------
    def getCard(self, **kwargs):
        """Returns the card if the specified card is in the set."""
        
        if 'cardId' in kwargs.keys():
            if kwargs['cardId'] in [card.id for card in self._cards]:
                for card in self._cards:
                    if kwargs['cardId'] == card.id:
                        return card
                    
        elif 'cardName' in kwargs.keys():
            if kwargs['cardName'] in [card.name for card in self._cards]:
                for card in self._cards:
                    if kwargs['cardName'] == card.name:
                        return card

#-------------------------------------------------------------------------------
    def addCard(self, newCard):
        """
        Adds a card instance to the set. It is safe to try to add duplicate 
        cards to the set. 
        
        Some sets have multiples of the same card only with a different art.
        These are handled by the altArt number of the Card class. The altArt
        variable is for the purpose of showing card images. Eg. if the 
        card(Armor Thrull) has alternative arts in the same set the image
        will be found by the name (Armor Thrull + altArt)
        
        Note, that the boosters are generated from the nonDuplicateCardList
        of the set. If needed, the specific card instances contained in it
        can be switched for the same cards only with a different altArt number.
        """

        if newCard.name in [card.name for card in self._cards]:
            cardCount = [card.name for card in self._cards].count(newCard.name)
            newCard.altArt = str(cardCount + 1)
            
            if cardCount == 1:
                for card in self._cards:
                    if card.name == newCard.name:
                        card.altArt = '1'
        
        else:
            if not 'Basic Land' in newCard.type:
                self._generationCardList.append(newCard)
                
        self._cards.append(newCard)

#-------------------------------------------------------------------------------
    def countUniques(self):
        """Returns the number of unique, nonbasic land cards in the set."""
        
        return len(self._generationCardList)

#-------------------------------------------------------------------------------
    def countAll(self):
        """
        Returns the number of all the cards in the set, including basic
        lands and double/duplicate cards.
        """
        
        return len(self._generationCardList)
    
#-------------------------------------------------------------------------------
    def getCommons(self):
        """Returns all the unique common cards in the set."""
        
        return [card for card in self._generationCardList if 
                card.rarity == 'Common']

#-------------------------------------------------------------------------------
    def getUncommons(self):
        """Returns all the unique uncommon cards in the set."""
        
        return [card for card in self._generationCardList if 
                card.rarity == 'Uncommon']

#-------------------------------------------------------------------------------
    def getRares(self):
        """Returns all the unique rare cards in the set."""
        
        return [card for card in self._generationCardList if 
                card.rarity == 'Rare']

#-------------------------------------------------------------------------------
    def getMythics(self):
        """Returns all the unique mythic rare cards in the set."""
        
        return [card for card in self._generationCardList if 
                card.rarity == 'Mythic Rare']
#-------------------------------------------------------------------------------
    def hasMythics(self):
        """Returns True if the set has Mythic Rares."""
        
        return any(self.getMythics())

#-------------------------------------------------------------------------------
    def getRandomMythics(self, numOfCards, duplicates=False):
        """
        Returns a specified number of random Mythic Rares from the set. 
        Optionally can be set not to return duplicates.
        
        If the number of cards is larger than the number of mythics, 
        then only 
        """
        
        mythics = self.getMythics()
        
        if duplicates:
            return [random.choice(mythics) for _ in range(numOfCards)]
        else:
            try:
                return random.sample(mythics, numOfCards)
            except ValueError:
                return [random.choice(mythics) for _ in range(numOfCards)]

#-------------------------------------------------------------------------------
    def getRandomRares(self, numOfCards, duplicates=False):
        """
        Returns a specified number of random Rares from the set. Optionally 
        can be set not to return duplicates.
        """
        
        rares = self.getRares()
        
        if duplicates:
            return [random.choice(rares) for _ in range(numOfCards)]
        else:
            try:
                return random.sample(rares, numOfCards)
            except ValueError:
                return [random.choice(rares) for _ in range(numOfCards)]
        
#-------------------------------------------------------------------------------
    def getRandomUncommons(self, numOfCards, duplicates=False):
        """
        Returns a specified number of random uncommons from the set. 
        Optionally can be set not to return duplicates.
        """
        
        uncommons = self.getUncommons()
        
        if duplicates:
            return [random.choice(uncommons) for _ in range(numOfCards)]
        else:
            try:
                return random.sample(uncommons, numOfCards)
            except ValueError:
                return [random.choice(uncommons) for _ in range(numOfCards)]
                

#-------------------------------------------------------------------------------
    def getRandomCommons(self, numOfCards, duplicates=False):
        """
        Returns a specified number of random commons from the set. 
        Optionally can be set not to return duplicates.
        """
        
        commons = self.getCommons()
        
        if duplicates:
            return [random.choice(commons) for _ in range(numOfCards)]
        else:
            try:
                return random.sample(commons, numOfCards)
            except ValueError:
                return [random.choice(commons) for _ in range(numOfCards)]

#-------------------------------------------------------------------------------
    def getRandomPack(self, numOfCards, numOfRares=None, numOfUncommons=None):
        """
        Returns a bunch of random cards simulationg a booster or a starter pack.
        The number of cards in the pack along with the number of rares,
        uncommons and commons can be specified. 
        
        The number of rares/mythics, commons and uncommons is determined the way 
        that there will be one rare, three uncommons and rest commons for each 
        14 cards, if the numbers are not specified.
        
        This way the function can be used to get almost any sort of booster or
        a starter pack without needing to specify the number of rares, 
        uncommons and commons seperately.
        """
        
        
        if not numOfRares:
            numOfRares = int(round(numOfCards / 14.0))
        
        if not numOfUncommons:
            numOfUncommons =  3 * int(round(numOfCards / 14.0))
        
        numOfCommons = numOfCards - numOfRares - numOfUncommons
        
        commons = self.getRandomCommons(numOfCommons)
        uncommons = self.getRandomUncommons(numOfUncommons)
        
        if self.hasMythics and random.randint(0, 7) == 0:
            rares = self.getRandomMythics(numOfRares)
        else:
            rares = self.getRandomRares(numOfRares)
        
        return commons + uncommons + rares

#-------------------------------------------------------------------------------
    def switchAltArt(self):
        """
        Switches a specific card Instance in the nonDuplicateCardList for
        another same card with different altArt number. This way one can 
        control which image to use with a card if it has alternative image(s).
        """
        
        pass
        
#==========================================================================#
#                              Properties                                  #
#==========================================================================#

    def getName(self):
        return self._name

    def getSetCode(self):
        return self._setCode

    def getCards(self):
        return self._cards

    def getIsSpecial(self):
        return self._isSpecial
    
    def getBasicLands(self):
        return self._basicLands

    name = property(getName, None, None, "Name of the set")
    setCode = property(getSetCode, None, None, "Short version of the set's name")
    cards = property(getCards, None, None, "List of Card instances belonging in the set.")
    hasMythics = property(hasMythics, None, None, "True if the set has Mythic Rares")
    isSpecial = property(getIsSpecial, None, None, "True if the set is a non-standard set.")
    basicLands = property(getBasicLands, None, None, "Returns the basic lands of the set, if any")
