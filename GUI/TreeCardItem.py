""""""
from PyQt4 import QtGui
from Base.Card import Card

################################################################################
class TreeCardItem(Card, QtGui.QTreeWidgetItem):
    """
    An object which is both a Card and a treewidgetitem. It automatically
    sets an image of the card's set as it's icon and it's name as the text.
    Also, the items are sortable by every column.
    """
    

#-------------------------------------------------------------------------------
    def __init__(self, card, manaSymbols, size='Small'):
        
        Card.__init__(self, card.id, card.name, card.mtgSetName, card.rarity, 
                      card.cost, card.type)
        QtGui.QTreeWidgetItem.__init__(self, card.name)

        self.setText(0,unicode( card.name))
        
        self.setData(1, 1, manaSymbols)
        self.setText(1, '')
        
        self.setData(2, 1, QtGui.QPixmap(self.getSetSymbolPath()))
        self.setText(2, '')
        
        self.setText(3, self.color)

        self.setText(4, '')
        self.setData(4, 1, QtGui.QPixmap(self.getTypeSymbolPath()))
        
        self.setText(5, '1')
        
        self.setFont(0, QtGui.QFont('Helvetica [Cronyx]', 10, QtGui.QFont.Bold))
        self.font(0).setFamily('Helvetica [Cronyx]')
        
        self._qty = 1
        self._altArt = card.altArt

#-------------------------------------------------------------------------------
    def __lt__(self, other):
        """
        Reimplemented compare operator for sorting the items with no text
        in certain columns.
        """
        column = self.treeWidget().sortColumn()
        #
        if column == 0 or column == 3:
            return self.text(column) > other.text(column)
        elif column == 1:
            return self.totalCost > other.totalCost
        elif column == 5:
            return self.getQty() > other.getQty()
        elif column == 2:
            if self.mtgSetName == other.mtgSetName:
                return self.rarity > other.rarity
            
            return self.mtgSetName > other.mtgSetName
        else:
            return self.type > other.type
        
#-------------------------------------------------------------------------------
    def add(self):
        """
        Called when another same item is added to the same list. Instead of
        adding another same card to the list, the quantity of this one is
        increased.
        """
        
        self._qty += 1
        self.setText(5, str(self._qty))

#-------------------------------------------------------------------------------
    def remove(self):
        """
        Called when another same item is removed from the list.
        """
        
        self._qty -= 1
        
        if self._qty == 0:
            
            parentList = self.treeWidget()
            del parentList._cards[self.id]
    
            if parentList._layout == 'simpleList':
                parentList.takeTopLevelItem(parentList.indexOfTopLevelItem(self))
            else:
                self.parent().takeChild(self.parent().indexOfChild(self))
        else:
            self.setText(5, str(self._qty))

#-------------------------------------------------------------------------------
    def getQty(self):
        """
        Returns the number of these items.
        """
        
        return self._qty

#-------------------------------------------------------------------------------
    def setQty(self, qty):
        """
        Sets the quantity of th item.
        """
        
        self._qty = qty
        self.setText(5, 'qty')
    
#-------------------------------------------------------------------------------
    def getCompositeClass(self):
        """
        Returns a new base Card class instance of this TreeCardItem instance.
        """
        
        return Card(self.id, self.name, self.mtgSetName, self.rarity, 
                   self.cost, self.type, self.altArt)
        
#-------------------------------------------------------------------------------
    def getTypeSymbolPath(self):
        """
        Returns the number of these items.
        """
        
        if 'Artifact' in self.type:
            return 'Manasymbols\small\Artifact.jpg'
        if 'Land' in self.type:
            return 'Manasymbols\small\Land.gif'
        if 'Sorcery' in self.type:
            return 'Manasymbols\small\Sorcery.jpg'
        if 'Instant' in self.type:
            return 'Manasymbols\small\Instant.jpg'
        if 'Creature' in self.type or 'Summon' in self.type:
            return 'Manasymbols\small\Creature.gif'
        if 'Enchantment' in self.type:
            return 'Manasymbols\small\Enchantment.jpg'
        if 'Planeswalker' in self.type:
            return 'Manasymbols\small\Planeswalker.png'