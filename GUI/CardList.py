#!/usr/bin/python
# -*- coding: latin-1 -*-

"""CardList class module."""
from collections import defaultdict

from PyQt4 import QtGui, QtCore
from TreeCardItem import TreeCardItem

################################################################################
class CardList(QtGui.QTreeWidget):
    """A listview of cards. """

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent):
        """"""
        
        #-----------------------------------------------
        super(CardList, self).__init__(parent)
        
        self.__setup()
        self.__connectSignals()
        
        #-----------------------------------------------
        self._mainFrameParent = mainFrameParent
        self._cards = {}
        self._layout = 'simpleList'
        self._filters = []
        self._seperatorContainer = defaultdict(defaultdict)
        
        self._db = self._mainFrameParent.getDatabase()
        
        self.__createTopLevelSeperators()
        

#==========================================================================#
#                              Private Methods                             #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __setup(self):
        """Sets up the treewiev with wanted properties."""
        
        self.setColumnCount(6)
        labels = ['Name', 'Cost', 'Set', 'Color', 'Type', 'Qty']
        self.setHeaderLabels(labels)
        
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(self.ExtendedSelection)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setMouseTracking(True)
        #self.setColumnCount(6)
        self.setSortingEnabled(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setIndentation(1)
        #self.setAcceptDrops(True)
        #self.setDragEnabled(True)
        #self.setDragDropOverwriteMode(False)

        
#-------------------------------------------------------------------------------
    def __showContextMenu(self, pos):
        """Shows the context menu of the card list."""
        
        contextMenu = QtGui.QMenu(self)
        
        contextMenu.addAction('Move selected cards to deck/sideboard', self.__transferSelected)
        contextMenu.addAction('Hide selected cards', self.hideSelected)
        
        contextMenu.addSeparator()
        
        seperateMenu1 = QtGui.QMenu('Switch to the same card from another set', self)
        
        currentItem = self.currentItem()
        
        if currentItem:
            sameCards = self._db.getCards(currentItem.name)
            
            for card in sameCards:
                switchAction = QtGui.QAction(self)
                switchAction.setText(card.mtgSetName)
                switchAction.card = card
                seperateMenu1.addAction(switchAction)

        else:
            seperateMenu1.setDisabled(True)
        
        seperateMenu1.triggered.connect(self._switchCard)
        
        contextMenu.addMenu(seperateMenu1)
        
        contextMenu.addSeparator()
        
        seperateMenu2 = QtGui.QMenu('Seperate cards by', self)
        seperateMenu2.addAction('Nothing(show as simple list)', self.simpleList)
        seperateMenu2.addAction('Color', self.seperateByColor)
        seperateMenu2.addAction('Casting cost', self.seperateByCC)
        seperateMenu2.addAction('Type', self.seperateByType)
        contextMenu.addMenu(seperateMenu2)
        
        contextMenu.addSeparator()
        
        contextMenu.addAction('Collapse all seperators', self.__collapseAll)
        contextMenu.addAction('Expand all seperators', self.__expandAll)
        
        contextMenu.addSeparator()
        
        contextMenu.addAction('Discard selected cards', self.__discardSelected)
        
        contextMenu.exec_(self.mapToGlobal(pos))

#-------------------------------------------------------------------------------
    def __createTopLevelSeperators(self):
        """
        Creates the top level items used for seperating cards, and adds them 
        to the seperatorContainer. The container is a dict and with it its easy
        to access each seperator by using keys, which are the same as Cards
        simpleTypes and simpleColors.
        """
        
        seperatorFont = QtGui.QFont('Matrix Bold', 13, QtGui.QFont.Bold)
        
        #-----------------------------------------------
        #Colors
        self._B = QtGui.QTreeWidgetItem('')
        self._B.setText(0, 'Black')
        self._B.setFont(0, seperatorFont)
        self._B.setData(0,1,QtGui.QPixmap('Manasymbols\small\B.gif'))
        
        self._G = QtGui.QTreeWidgetItem('')
        self._G.setText(0, 'Green')
        self._G.setFont(0, seperatorFont)
        self._G.setData(0,1,QtGui.QPixmap('Manasymbols\small\G.gif'))
        
        self._R = QtGui.QTreeWidgetItem('')
        self._R.setText(0, 'Red')
        self._R.setFont(0, seperatorFont)
        self._R.setData(0,1,QtGui.QPixmap('Manasymbols\small\R.gif'))
        
        self._U = QtGui.QTreeWidgetItem('')
        self._U.setText(0, 'Blue')
        self._U.setFont(0, seperatorFont)
        self._U.setData(0,1,QtGui.QPixmap('Manasymbols\small\U.gif'))
        
        self._W = QtGui.QTreeWidgetItem('')
        self._W.setText(0, 'White')
        self._W.setFont(0, seperatorFont)
        self._W.setData(0,1,QtGui.QPixmap('Manasymbols\small\W.gif'))
        
        self._M = QtGui.QTreeWidgetItem('')
        self._M.setText(0, 'Multicolor')
        self._M.setFont(0, seperatorFont)
        
        paths = ['Manasymbols\small\B.gif', 
                 'Manasymbols\small\U.gif',
                 'Manasymbols\small\W.gif', 
                 'Manasymbols\small\R.gif',
                 'Manasymbols\small\G.gif']
        self._M.setData(0,1,QtGui.QPixmap(self.__mergeImages(paths)))
        
        self._artifacts = QtGui.QTreeWidgetItem('')
        self._artifacts.setText(0, 'Colorless/Artifacts')
        self._artifacts.setFont(0, seperatorFont)
        self._artifacts.setData(0,1,QtGui.QPixmap('Manasymbols\small\Artifact.jpg'))
        
        #-----------------------------------------------
        #Casting costs
        self._0CC = QtGui.QTreeWidgetItem('')
        self._0CC.setText(0, '')
        self._0CC.setFont(0, seperatorFont)
        self._0CC.setData(0,1,QtGui.QPixmap('Manasymbols\small\\0.gif'))
        
        self._1CC = QtGui.QTreeWidgetItem('')
        self._1CC.setText(0, '')
        self._1CC.setFont(0, seperatorFont)
        self._1CC.setData(0,1,QtGui.QPixmap('Manasymbols\small\\1.gif'))
        
        self._2CC = QtGui.QTreeWidgetItem('')
        self._2CC.setText(0, '')
        self._2CC.setFont(0, seperatorFont)
        self._2CC.setData(0,1,QtGui.QPixmap('Manasymbols\small\\2.gif'))
        
        self._3CC = QtGui.QTreeWidgetItem('')
        self._3CC.setText(0, '')
        self._3CC.setFont(0, seperatorFont)
        self._3CC.setData(0,1,QtGui.QPixmap('Manasymbols\small\\3.gif'))
        
        self._4CC = QtGui.QTreeWidgetItem('')
        self._4CC.setText(0, '')
        self._4CC.setFont(0, seperatorFont)
        self._4CC.setData(0,1,QtGui.QPixmap('Manasymbols\small\\4.gif'))
        
        self._5CC = QtGui.QTreeWidgetItem('')
        self._5CC.setText(0, '')
        self._5CC.setFont(0, seperatorFont)
        self._5CC.setData(0,1,QtGui.QPixmap('Manasymbols\small\\5.gif'))
        
        paths = ['Manasymbols\small\\6.gif', 'Manasymbols\small\\Plus.png']
        self._6CC = QtGui.QTreeWidgetItem('')
        self._6CC.setText(0, '')
        self._6CC.setFont(0, seperatorFont)
        self._6CC.setData(0,1,QtGui.QPixmap(self.__mergeImages(paths)))
        
        #-----------------------------------------------
        #Types
        self._creatures = QtGui.QTreeWidgetItem('')
        self._creatures.setText(0, 'Creatures')
        self._creatures.setFont(0, seperatorFont)
        self._creatures.setData(0,1,QtGui.QPixmap('Manasymbols\small\Creature.jpg'))
        
        paths = ['Manasymbols\small\Instant.jpg',
                 'Manasymbols\small\Sorcery.jpg',
                 'Manasymbols\small\Enchantment.jpg']
        
        self._nonCreatureSpells = QtGui.QTreeWidgetItem('')
        self._nonCreatureSpells.setText(0, 'Non-creatures')
        self._nonCreatureSpells.setFont(0, seperatorFont)
        self._nonCreatureSpells.setData(0,1,QtGui.QPixmap(self.__mergeImages(paths)))
        
        self._lands = QtGui.QTreeWidgetItem('')
        self._lands.setText(0, 'Lands')
        self._lands.setFont(0, seperatorFont)
        self._lands.setData(0,1,QtGui.QPixmap('Manasymbols\small\Land.jpg'))
        
        
        #-----------------------------------------------
        #Container setup.
        self._seperatorContainer['Color']['W'] = self._W
        self._seperatorContainer['Color']['U'] = self._U
        self._seperatorContainer['Color']['B'] = self._B
        self._seperatorContainer['Color']['R'] = self._R
        self._seperatorContainer['Color']['G'] = self._G
        self._seperatorContainer['Color']['M'] = self._M
        self._seperatorContainer['Color']['C'] = self._artifacts
        
        self._seperatorContainer['Type']['Creature'] = self._creatures
        self._seperatorContainer['Land'] = self._lands
        self._seperatorContainer['Type']['Non-Creature'] = self._nonCreatureSpells
        
        self._seperatorContainer['CC'][0] = self._0CC
        self._seperatorContainer['CC'][1] = self._1CC
        self._seperatorContainer['CC'][2] = self._2CC
        self._seperatorContainer['CC'][3] = self._3CC
        self._seperatorContainer['CC'][4] = self._4CC
        self._seperatorContainer['CC'][5] = self._5CC
        self._seperatorContainer['CC'][6] = self._6CC

#-------------------------------------------------------------------------------
    def __mergeImages(self, imagePaths):
        """
        Combines a list of images into one image. Used for combining manacost 
        images.
        """
        
        firstImage = QtGui.QPixmap(imagePaths[0])
        width = firstImage.width()
        height = firstImage.height()
        
        mergedImage = QtGui.QPixmap(width * len(imagePaths), height)
        bitMap = QtGui.QBitmap(mergedImage)
        bitMap.clear()
        mergedImage.setMask(bitMap)
        painter = QtGui.QPainter(mergedImage)
        
        topleft = (0,0)
        
        for imagePath in imagePaths:
            image = QtGui.QPixmap(imagePath)
            rect = QtCore.QRect(topleft[0], topleft[1], width, height)
            painter.drawPixmap(rect, image, image.rect())
            
            topleft = (topleft[0] + width, topleft[1])
        
        return mergedImage

#-------------------------------------------------------------------------------
    def __cardsToCCSeparators(self):
        """
        Adds all the cards in the list to the top-level casting cost seperators.
        """
        
        for card in self._cards.values():
            if 'Land' in card.type:
                self._lands.addChild(card)
            else:
                self._seperatorContainer['CC'][card.simpleCC].addChild(card)

#-------------------------------------------------------------------------------
    def __cardsToColorSeparators(self):
        """
        Adds all the cards in the list to the top-level color seperators.
        """
        
        for card in self._cards.values():
            if 'Land' in card.type:
                self._lands.addChild(card)
            else:
                self._seperatorContainer['Color'][card.simpleColor].addChild(card)

#-------------------------------------------------------------------------------
    def __cardsToTypeSeparators(self):
        """
        Adds all the cards in the list to the top-level type seperators.
        """
        
        for card in self._cards.values():
            if 'Land' in card.type:
                self._lands.addChild(card)
            else:
                self._seperatorContainer['Type'][card.simpleType].addChild(card)

#-------------------------------------------------------------------------------
    def __CCToTopLevel(self):
        """
        Sets the casting cost seperators as top-level items
        """
        self.addTopLevelItems(self._seperatorContainer['CC'].values())
        self.addTopLevelItem(self._seperatorContainer['Land'])

#-------------------------------------------------------------------------------
    def __colorToTopLevel(self):
        """
        Sets the casting cost seperators as top-level items
        """
        
        self.addTopLevelItems(self._seperatorContainer['Color'].values())
        self.addTopLevelItem(self._seperatorContainer['Land'])

#-------------------------------------------------------------------------------
    def __typeToTopLevel(self):
        """
        Sets the casting cost seperators as top-level items
        """
        
        self.addTopLevelItems(self._seperatorContainer['Type'].values())
        self.addTopLevelItem(self._seperatorContainer['Land'])
    

#==========================================================================#
#                              Event handling                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __connectSignals(self):
        """
        Sets up events handling.
        """
        
        self.itemDoubleClicked.connect(self._onItemDoubleClicked)
        self.itemSelectionChanged.connect(self._onItemSelectionChanged)
        self.customContextMenuRequested.connect(self.__showContextMenu)
        
#-------------------------------------------------------------------------------
    def _onItemDoubleClicked(self, item, column):
        """
        Called when an item is doubleclicked. To be overwritten.
        """
        
        self._mainFrameParent.transferCardItem(item, self)


#-------------------------------------------------------------------------------
    def _onItemSelectionChanged(self):
        """
        Called when a cell is activated
        """
        
        if not self.selectedItems():
            return
        
        selected = self.selectedItems()[-1]
        
        if selected.__class__.__name__ is not 'TreeCardItem':
            return

        self._mainFrameParent.cardImageWidget.setCardImage(selected)
        
#-------------------------------------------------------------------------------
    def __transferSelected(self):
        """
        Sets up events handling.
        """
        
        cardItems = []
        for item in self.selectedItems():
            if item.__class__.__name__ == 'TreeCardItem':
                cardItems.append(item)
        
        self._mainFrameParent.transferCardItems(cardItems, self)


#-------------------------------------------------------------------------------
    def __discardSelected(self):
        """
        Collapses all the top-layer seperators.
        """
        
        msg = 'Are you sure you want to remove the selected cards completely?'
        msgBox = QtGui.QMessageBox()
        msgBox.setText(msg)
        msgBox.setStandardButtons(msgBox.Ok | msgBox.Cancel)
        
        result = msgBox.exec_()
        
        if result == 1024:
            selected = self.selectedItems()
        
            for cardItem in selected:
                cardItem.remove()
                
        self._mainFrameParent.refreshNumbers()
        
        if self == self._mainFrameParent.deckList:
            for cardItem in selected:
                self._mainFrameParent.statsWidget.removeCardData(cardItem)
        
#-------------------------------------------------------------------------------
    def __collapseAll(self):
        """
        Collapses all the top-layer seperators.
        """
        
        for index in range(0, self.topLevelItemCount()):
            self.topLevelItem(index).setExpanded(False)

#-------------------------------------------------------------------------------
    def __expandAll(self):
        """
        Expands all the top-level seperators.
        """
        
        for index in range(0, self.topLevelItemCount()):
            self.topLevelItem(index).setExpanded(True)

#-------------------------------------------------------------------------------
    def __cursorToNextIndex(self):
        """
        Expands all the top-level seperators.
        """
        
        nextIndex = self.moveCursor(self.MoveNext, QtCore.Qt.NoModifier)
        self.setCurrentIndex(nextIndex)

#-------------------------------------------------------------------------------
    def __cursorToPrevIndex(self):
        """
        Expands all the top-level seperators.
        """
        
        prevIndex = self.moveCursor(self.MovePrevious, QtCore.Qt.NoModifier)
        self.setCurrentIndex(prevIndex)

#-------------------------------------------------------------------------------
    def keyPressEvent(self, event):
        """Keyboard event handler"""
        
        if event.key() == QtCore.Qt.Key_Space:
            self._mainFrameParent.transferCardItems(self.selectedItems(), self)
            
            if not self.selectedItems():
                self.__cursorToNextIndex()
                
        elif event.key() == QtCore.Qt.Key_Down:
            self.__cursorToNextIndex()
            
        elif event.key() == QtCore.Qt.Key_Up:
            self.__cursorToPrevIndex()
            
        elif event.key() == QtCore.Qt.Key_Right:
            self._mainFrameParent.transferCardItems(self.selectedItems(), self)
            
            if not self.selectedItems():
                self.__cursorToNextIndex()

        elif event.key() == QtCore.Qt.Key_Left:
            self._mainFrameParent.transferCardItems(self.selectedItems(), self)
        
        elif event.key() == QtCore.Qt.Key_Shift:
            self._mainFrameParent.SwitchFocusedCardList()
            
            if not self.selectedItems():
                self.__cursorToNextIndex()
        
#-------------------------------------------------------------------------------
    def wheelEvent(self, wheelEvent):
        """
        Overwritten wheelEvent handler. With this, mousewheel traverses over
        items instead of moving the sidebar.
        """
        
        if wheelEvent.delta() < 0:
            self.__cursorToNextIndex()
        else:
            self.__cursorToPrevIndex()
            
#-------------------------------------------------------------------------------
    def _switchCard(self, action):
        """
        Switches a chosen card for some other same card from another mtg set.
        """
        
        newCard = action.card
        oldCardItem = self.currentItem()
        
        self._mainFrameParent.switchCardItem(newCard, oldCardItem, self)
        
        self.__cursorToNextIndex()
            
#==========================================================================#
#                              Public methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def addFilterWord(self, filterWord):
        """
        Hides certain types or colours of cards.
        """
        
        self._filters.append(filterWord)

#-------------------------------------------------------------------------------
    def removeFilterWord(self, filterWord):
        """
        Hides certain types or colours of cards.
        """
        if filterWord in self._filters:
            self._filters.pop(self._filters.index(filterWord))
        
        if 'M' in filterWord:
            for filterW in self._filters:
                if 'M' in filterW:
                    self._filters.pop(self._filters.index(filterW))

#-------------------------------------------------------------------------------
    def applyFilters(self):
        """
        Applies the filterswords and hides/unhides cards according to them.
        """
        
        self.showAll()
        filters = self._filters
        
        for card in self._cards.values():
            for filterWord in self._filters:
                if 'M' in filterWord:
                    for color in card.color:
                        if color in filterWord:
                            card.setHidden(True)
            
            if  card.color in filters or card.simpleType in filters:
                card.setHidden(True)
                
#-------------------------------------------------------------------------------
    def addCard(self, card):
        """
        Adds a Card instance to the listwidget.
        """
        
        if card.id in self._cards.keys():
            self._cards[card.id].add()
        else:
            if card.cost and card.cost != 'None':
                manaSymbols = self.__mergeImages(card.getManaSymbolPaths())
            else:
                manaSymbols = ''
                  
            cardItem = TreeCardItem(card, manaSymbols)
            self._cards[card.id] = cardItem
            
            if self._layout == 'simpleList':
                self.addTopLevelItem(cardItem)
            else:
                if card.simpleType == 'Land':
                    self._seperatorContainer['Land'].addChild(cardItem)
                else:
                    if self._layout == 'seperateByCC':
                        self._seperatorContainer['CC'][card.simpleCC].addChild(cardItem)
                    if self._layout == 'seperateByType':
                        self._seperatorContainer['Type'][card.simpleType].addChild(cardItem)
                    if self._layout == 'seperateByColor':
                        self._seperatorContainer['Color'][card.simpleColor].addChild(cardItem)
                    
        self.resizeColumns()
        #self.refreshNumbers()
        
#-------------------------------------------------------------------------------
    def addCards(self, cards):
        """
        Adds multiple Card instances to the listwidget.
        """
        
        self.setSortingEnabled(False)
        
        for card in cards:
            self.addCard(card)
        
        self.setSortingEnabled(True)
        self.resizeColumns()
        #self.refreshNumbers()
        
#-------------------------------------------------------------------------------
    def resizeColumns(self):
        """Resizes columns in a smart way."""
        
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)
        self.resizeColumnToContents(3)
        self.resizeColumnToContents(4)

#-------------------------------------------------------------------------------
    def cardCount(self):
        """
        Returns the number of cards in the list.
        """
        
        num = 0
        
        for card in self._cards.values():
            num += card.getQty()
        
        return num
    
#-------------------------------------------------------------------------------
    def clearList(self, delete=False):
        """
        Cleares the list. Has option to delete the contents completely or just 
        on the surface.
        """

        while self.topLevelItemCount() > 0:
            self.takeTopLevelItem(0).takeChildren()
        
        if delete:
            self._cards.clear()

#-------------------------------------------------------------------------------
    def refreshLayout(self):
        """
        Redoes the layout.
        """
        
        if self._layout == 'simpleList':
            self.simpleList()
        elif self._layout == 'seperateByCC':
            self.seperateByCC()
        elif self._layout == 'seperateByColor':
            self.seperateByColor()
        elif self._layout == 'seperateByType':
            self.seperateByType()
            
#-------------------------------------------------------------------------------
    def refreshNumbers(self):
        """
        Refreshes the numbers of cards showing on seperator texts.
        
        For example if the cards are seperated by card types, and a creature
        card is added to the list, then instead of "Creatures(0)" it will 
        read "Creatures(1)".
        """
        if self._layout == 'simpleList':
            return
        
        for index in range(self.topLevelItemCount()):
            topLevelItem = self.topLevelItem(index)
            
            numTxt = '({num})'.format(num=topLevelItem.childCount())
            title = str(topLevelItem.text(0)).rsplit('(')[0].join(numTxt)
            topLevelItem.setText(0, title)
        
#-------------------------------------------------------------------------------
    def hideSelected(self):
        """
        Hides the selected items.
        """
        
        for item in self.selectedItems():
            item.setHidden(True)

#-------------------------------------------------------------------------------
    def getCards(self):
        """
        Returns the Card instances of the list.
        """
        
        return [card.getCompositeClass() for card  in self._cards.values()]

#-------------------------------------------------------------------------------
    def showAll(self):
        """
        Shows all hidden items.
        """
        
        for item in self._cards.values():
            item.setHidden(False)
            
        for index in range(0, self.topLevelItemCount()):
            self.topLevelItem(index).setHidden(False)

#-------------------------------------------------------------------------------
    def simpleList(self):
        """
        Shows the cards as a simple list without orderings.
        """
        
        self.clearList()
        self._layout = 'simpleList'
        
        self.addTopLevelItems(self._cards.values())
        
        self.applyFilters()
        self.resizeColumns()
        
#-------------------------------------------------------------------------------
    def seperateByColor(self):
        """
        Seperates items by color.
        """
        
        self.clearList()
        self._layout = 'seperateByColor'
        
        self.__cardsToColorSeparators()
        self.__colorToTopLevel()
        
        self.applyFilters()
        self.resizeColumns()
        
#-------------------------------------------------------------------------------
    def seperateByType(self):
        """
        Seperates items by type.
        """
        
        self.clearList()
        self._layout = 'seperateByType'
        
        self.__cardsToTypeSeparators()
        self.__typeToTopLevel()
        
        self.applyFilters()
        self.resizeColumns()
        
#-------------------------------------------------------------------------------
    def seperateByCC(self):
        """
        Seperates items by casting cost.
        """
        
        self.clearList()
        self._layout = 'seperateByCC'
        
        self.__cardsToCCSeparators()
        self.__CCToTopLevel()
        
        self.applyFilters()
        self.resizeColumns()
