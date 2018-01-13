"""Card-class module."""

################################################################################
class Card:
    """
    An MTG card class.
    
    id == Unique id number, from database
    Set == set in which the card belongs(a Set instance)
    sets == other sets where this card appears
    altArt == alternative art number(if any). Some cards have alternative pics
    
    The simpleColor and simpleType are for convenient classification for lists.
    Most of the time the only thing needed to know about the card is if its 
    mono- or multicolored, land, creature or a non-creature.
    
    SimpleColor is the cards color in case of monocolored cards and "M" if the 
    card is multicolored. In case of colorless the simpleColor is "C".
    
    SimpleType is only "Creature" if the card is a creature, "Land" and 
    "non-creature" otherwise.
    """

#-------------------------------------------------------------------------------
    def __init__(self, Id, name, mtgSetName, rarity, cost, Type, 
                 isDual=False, dualCardName=None):

        self._id = Id
        self._name = name
        self._mtgSetName = mtgSetName
        self._rarity = rarity
        self._cost = cost
        self._type = Type
        self._altArt = ''
        self._isDual = isDual
        self._dualCardName = dualCardName
        
        if len(self.color) == 0:
            self._simpleColor = 'C'
        elif len(self.color) == 1:
            self._simpleColor = self.color
        else:
            self._simpleColor = 'M'
        
        if 'Land' in Type:
            self._simpleType = 'Land'
        elif 'Creature' in Type:
            self._simpleType = 'Creature'
        else:
            self._simpleType = 'Non-Creature'
        
        if self.getTotalCost() > 5:
            self._simpleCC = 6
        else:
            self._simpleCC = self.getTotalCost()

       
#==========================================================================#
#                              Internal methods                            #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __str__(self):
        """String representation."""
        
        return self._name

#-------------------------------------------------------------------------------
    def __eq__(self, other):
        """
        Called by comparison operations. Basically, a card is same as
        another card if both their name and set are the same.
        """
        
        return self.name == other.name and self.mtgSetName == other.mtgSetName


#==========================================================================#
#                              Public methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def getManaSymbolPaths(self, size='Small'):
        """
        Returns the pathnames of the manasymbols of the card.
        """

        cost = self.cost.replace('//', '')
        cost = [symbol for symbol in cost]
        symbolPaths = []
        
        for _ in range(0, len(cost)):
            symbol = cost.pop(0)
            
            if not cost:
                symbolPath = 'Manasymbols\{size}\\{symbol}.gif'.format(size=size,
                                                                  symbol=symbol)
                symbolPaths.append(symbolPath)
                break
            
            if symbol == '(' or symbol == '{'  and '/' in cost:
                symbol = ''
                symbol = symbol + cost.pop(0)
                cost.pop(0)
                symbol = symbol + cost.pop(0)
                cost.pop(0)
                
                symbolPath = 'Manasymbols\{size}\\{symbol}.gif'.format(size=size,
                                                                  symbol=symbol)
                symbolPaths.append(symbolPath)
                
                if not cost:
                    break
            
            elif symbol.isdigit() and cost[0].isdigit():
                symbol = symbol + cost.pop(0)
                
                symbolPath = 'Manasymbols\{size}\\{symbol}.gif'.format(size=size,
                                                                  symbol=symbol)
                symbolPaths.append(symbolPath)
                
                if not cost:
                    break
            
            else:
                symbolPath = 'Manasymbols\{size}\\{symbol}.gif'.format(size=size,
                                                                  symbol=symbol)
                symbolPaths.append(symbolPath)
                
                if not cost:
                    break
            
        return symbolPaths


#-------------------------------------------------------------------------------
    def getSetSymbolPath(self, size='Small'):
        """
        Returns the set symbol path of the card.
        """
        
        mtgSetName = self.mtgSetName
        rarity = self._rarity
        
        if 'Mythic' in rarity:
            rarity = 'Mythic'
        
        path = 'Setsymbols\{size}\\{mtgSetName}_{rarity}'.format(size=size,
                                                         mtgSetName=mtgSetName,
                                                         rarity=rarity)

            
        
        return path.replace(':', '')

#-------------------------------------------------------------------------------
    def getCardData(self):
        """
        Returns a list of the most important data of the card.
        """
        
        return [self.id, self.name, self.mtgSetName, self.rarity, 
                self.cost, self.type]

#-------------------------------------------------------------------------------
    def getStringCardData(self):
        """
        Returns a list of the most important data of the card as strings.
        """
        
        return [str(self.id), str(self.name), str(self.mtgSetName), 
                str(self.rarity), str(self.cost), str(self.type)]

#==========================================================================#
#                              Properties                                  #
#==========================================================================#

    def getId(self):
        return self._id

    def getName(self):
        return self._name


    def getMtgSetName(self):
        return self._mtgSetName


    def getSets(self):
        return self._sets


    def getRarity(self):
        return self._rarity


    def getCost(self):
        return self._cost
    
    def getType(self):
        return self._type
    
    def getAltArt(self):
        return self._altArt


    def getTotalCost(self):
        cost = self.cost
        totalCost = 0
        
        numbers = filter(lambda x: x.isdigit(), cost)
        alphabets = filter(lambda x: x == 'W' or 
                                     x == 'U' or 
                                     x == 'B' or
                                     x == 'R' or
                                     x == 'G', cost)
        
        if numbers:
            totalCost += int(numbers)
        
        totalCost += cost.count('(')
        totalCost += len(alphabets) - 2 * cost.count('(')
        
        return totalCost
        
    def getColor(self):
        colors = ''
        
        for color in 'WUBRG':
            if color in self.cost:
                colors = colors + color

        return colors
    
    def getSimpleColor(self):
        return self._simpleColor
    
    def getSimpleType(self):
        return self._simpleType
    
    def getSimpleCC(self):
        return self._simpleCC
    
    def isDual(self):
        return self._isDual
    
    def setDual(self, isDual):
        self._isDual = isDual
    
    def getDualCardName(self):
        return self._dualCardName
    
    def setDualCardName(self, dualCardName):
        self._dualCardName = dualCardName

        
#-------------------------------------------------------------------------------
    id = property(getId, None, None)
    name = property(getName, None, None)
    mtgSetName = property(getMtgSetName, None, None)
    sets = property(getSets, None, None)
    rarity = property(getRarity, None, None)
    cost = property(getCost, None, None)
    totalCost = property(getTotalCost, None, None)
    color = property(getColor, None, None)
    type = property(getType, None, None)
    manaSymbolPaths = property(getManaSymbolPaths, None, None)
    altArt = property(getAltArt, None, None)
    simpleColor = property(getSimpleColor, None, None)
    simpleType = property(getSimpleType, None, None)
    simpleCC = property(getSimpleCC, None, None)
    isDual = property(isDual, setDual, None)
    dualCardName = property(getDualCardName, setDualCardName)
    

    