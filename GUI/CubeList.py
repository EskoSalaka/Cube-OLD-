#!/usr/bin/python
# -*- coding: latin-1 -*-

"""CubeList class module."""
from collections import defaultdict

from PyQt4 import QtGui, QtCore
from TreeCardItem import TreeCardItem

################################################################################
class CubeList(QtGui.QTreeWidget):
    """A listview of cards. """

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent):
        super(CubeList, self).__init__(parent)
        
        #-----------------------------------------------
        self._font = QtGui.QFont('Matrix Bold', 13, QtGui.QFont.Bold)
        self._cards = {}
        self._sortedCards = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        self._seperators = defaultdict(lambda: defaultdict(lambda: defaultdict(defaultdict)))
        
        #-----------------------------------------------
        self.__setup()
        self.__connectSignals()
        self.__setupTopLevelSeperators()
        
        
        #-----------------------------------------------
        self._mainFrameParent = mainFrameParent
        self._layout = ''
        self._filters = []
        
        

#==========================================================================#
#                              Private Methods                             #
#==========================================================================#

#-------------------------------------------------------------------------------
    def __setup(self):
        """Sets up the treewiev with wanted properties."""
        
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(self.ExtendedSelection)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setMouseTracking(True)
        #self.setColumnCount(6)
        self.setSortingEnabled(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setIndentation(7)
        #self.setAcceptDrops(True)
        #self.setDragEnabled(True)
        #self.setDragDropOverwriteMode(False)

        labels = ['Name', 'Cost', 'Set', 'Color', 'Type', 'Qty']
        header = self.headerItem()
        self.setHeaderLabels(QtCore.QStringList(labels))
        header.setText(0, "Card")
        
#-------------------------------------------------------------------------------
    def __showContextMenu(self, pos):
        """Shows the context menu of the card list."""
        
        contextMenu = QtGui.QMenu(self)
        
        contextMenu.addAction('Move/Remove cards', self.__transferSelected)
        contextMenu.addAction('Hide selected cards', self.hideSelected)
        
        contextMenu.addSeparator()
        
        contextMenu.addAction('Collapse all seperators', self.__collapseAll)
        contextMenu.addAction('Expand all seperators', self.__expandAll)
        
        contextMenu.exec_(self.mapToGlobal(pos))
        
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
    def __getColorSeperators(self):
        """
        Creates and returns seperators for colors(lands and artifacts also 
        included in these.
        """
        
        B = QtGui.QTreeWidgetItem('')
        B.setText(0, 'Black')
        B.setFont(0, self._font)
        B.setData(0,1,QtGui.QPixmap('Manasymbols\small\B.gif'))
        
        G = QtGui.QTreeWidgetItem('')
        G.setText(0, 'Green')
        G.setFont(0, self._font)
        G.setData(0,1,QtGui.QPixmap('Manasymbols\small\G.gif'))
        
        R = QtGui.QTreeWidgetItem('')
        R.setText(0, 'Red')
        R.setFont(0, self._font)
        R.setData(0,1,QtGui.QPixmap('Manasymbols\small\R.gif'))
        
        U = QtGui.QTreeWidgetItem('')
        U.setText(0, 'Blue')
        U.setFont(0, self._font)
        U.setData(0,1,QtGui.QPixmap('Manasymbols\small\U.gif'))
        
        W = QtGui.QTreeWidgetItem('')
        W.setText(0, 'White')
        W.setFont(0, self._font)
        W.setData(0,1,QtGui.QPixmap('Manasymbols\small\W.gif'))
        
        M = QtGui.QTreeWidgetItem('')
        M.setText(0, 'Multicolor')
        M.setFont(0, self._font)
        
        paths = ['Manasymbols\small\B.gif', 
                 'Manasymbols\small\U.gif',
                 'Manasymbols\small\W.gif', 
                 'Manasymbols\small\R.gif',
                 'Manasymbols\small\G.gif']
        
        M.setData(0,1,QtGui.QPixmap(self.__mergeImages(paths)))
        
        C = QtGui.QTreeWidgetItem('')
        C.setText(0, 'Colorless/Artifact')
        C.setFont(0, self._font)
        C.setData(0,1,QtGui.QPixmap('Manasymbols\small\Artifact.jpg'))
        
        lands = QtGui.QTreeWidgetItem('')
        lands.setText(0, 'Land')
        lands.setFont(0, self._font)
        lands.setData(0,1,QtGui.QPixmap('Manasymbols\small\Land.jpg'))
        
        
        
        return [W, U, B, R, G, M, C, lands]

#-------------------------------------------------------------------------------
    def __getTypeSeperators(self):
        """
        Creates and returns seperators for types. In the future there 
        could be more than just creatures and non-creature spells.
        """
        
        nonCreaturePaths = ['Manasymbols\small\Instant.jpg',
                            'Manasymbols\small\Sorcery.jpg',
                            'Manasymbols\small\Enchantment.jpg']
        
        creatures = QtGui.QTreeWidgetItem('')
        creatures.setText(0, 'Creatures')
        creatures.setFont(0, self._font)
        creatures.setData(0,1,QtGui.QPixmap('Manasymbols\small\Creature.jpg'))
        
        nonCreatureSpells = QtGui.QTreeWidgetItem('')
        nonCreatureSpells.setText(0, 'Non-creature spells')
        nonCreatureSpells.setFont(0, self._font)
        nonCreatureSpells.setData(0,1,QtGui.QPixmap(self.__mergeImages(nonCreaturePaths)))
        
        return [creatures, nonCreatureSpells]

#-------------------------------------------------------------------------------
    def __getCCSeperators(self):
        """
        Creates and returns seperators for casting cost. 
        """
        
        CC0 = QtGui.QTreeWidgetItem('')
        CC0.setText(0, '')
        CC0.setFont(0, self._font)
        CC0.setData(0,1,QtGui.QPixmap('Manasymbols\small\\0.gif'))
        
        CC1 = QtGui.QTreeWidgetItem('')
        CC1.setText(0, '')
        CC1.setFont(0, self._font)
        CC1.setData(0,1,QtGui.QPixmap('Manasymbols\small\\1.gif'))
        
        CC2 = QtGui.QTreeWidgetItem('')
        CC2.setText(0, '')
        CC2.setFont(0, self._font)
        CC2.setData(0,1,QtGui.QPixmap('Manasymbols\small\\2.gif'))
        
        CC3 = QtGui.QTreeWidgetItem('')
        CC3.setText(0, '')
        CC3.setFont(0, self._font)
        CC3.setData(0,1,QtGui.QPixmap('Manasymbols\small\\3.gif'))
        
        CC4 = QtGui.QTreeWidgetItem('')
        CC4.setText(0, '')
        CC4.setFont(0, self._font)
        CC4.setData(0,1,QtGui.QPixmap('Manasymbols\small\\4.gif'))
        
        CC5 = QtGui.QTreeWidgetItem('')
        CC5.setText(0, '')
        CC5.setFont(0, self._font)
        CC5.setData(0,1,QtGui.QPixmap('Manasymbols\small\\5.gif'))
        
        CC6 = QtGui.QTreeWidgetItem('')
        CC6.setText(0, '')
        CC6.setFont(0, self._font)
        CC6.setData(0,1,QtGui.QPixmap(self.__mergeImages(['Manasymbols\small\\6.gif', 'Manasymbols\small\\Plus.png'])))
        
        return [CC0, CC1, CC2, CC3, CC4, CC5, CC6]
        
                
#-------------------------------------------------------------------------------
    def __setupTopLevelSeperators(self):
        """
        Sets up top-level items. 
        """
        
        colors = ['W', 'U', 'B', 'R', 'G', 'M', 'C']
        colorSeperators = self.__getColorSeperators()
        lands = colorSeperators.pop()
        
        for color, seperator in zip(colors, colorSeperators):
            typeSeperators = self.__getTypeSeperators()
            CCSeperators1 = self.__getCCSeperators()
            CCSeperators2 = self.__getCCSeperators()
            
            self.addTopLevelItem(seperator)
            seperator.addChildren((typeSeperators[0], 
                                  typeSeperators[1]))
            typeSeperators[0].addChildren(CCSeperators1)
            typeSeperators[1].addChildren(CCSeperators2)

            for x in range(0,7):
                self._seperators[color]['Creature'][x] = CCSeperators1[x]
                self._seperators[color]['Non-Creature'][x] = CCSeperators2[x]
        
        
        self._seperators['C']['Land'][0] = lands
        self.addTopLevelItem(lands)
        

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
        Called when an item is doubleclicked. Transfers the doubleclicked
        item to the other list if the item is a CardItem.
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
    def __transferSelected(self):
        """
        Transfers cards between the cube and masterbase.
        """
        
        cardItems = []
        for item in self.selectedItems():
            if item.__class__.__name__ == 'TreeCardItem':
                cardItems.append(item)
        
        self._mainFrameParent.transferCardItems(cardItems, self)

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
        Adds a Card instance to the CubeList.
        """
        
        if card.id in self._cards.keys():
            self._cards[card.id].add()
        else:
            if card.cost:
                manaSymbols = self.__mergeImages(card.getManaSymbolPaths())
            else:
                manaSymbols = ''
                  
            cardItem = TreeCardItem(card, manaSymbols)
            self._cards[card.id] = cardItem
            
            self._seperators[cardItem.simpleColor][cardItem.simpleType][cardItem.simpleCC].addChild(cardItem)
        
        self.resizeColumns()
            
#-------------------------------------------------------------------------------
    def addCards(self, cards, progressDialog=None):
        """
        Adds multiple Card instances to the listwidget. Has an optional
        progressdialog argument if dealing with adding long lists of cards.
        If a progresdialog is given it is udated along the way.
        """
        
        self.setSortingEnabled(False)
        cardItems = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        
        for card in cards:
            if card.id in self._cards.keys():
                self._cards[card.id].add()
            else:
                if card.cost:
                    manaSymbols = self.__mergeImages(card.getManaSymbolPaths())
                else:
                    manaSymbols = ''
                  
                cardItem = TreeCardItem(card, manaSymbols)
                self._cards[card.id] = cardItem
                cardItems[card.simpleColor][card.simpleType][card.simpleCC].append(cardItem)
        
        if progressDialog:
            progressDialog.setRange(0, 7)
        
        steps = 0
        for color in ['W', 'U', 'B', 'R', 'G', 'M', 'C']:
            for CC in range(0,7):
                steps += 1
                seperator = self._seperators[color]['Creature'][CC]
                cards = cardItems[color]['Creature'][CC]
                if cards:
                    seperator.addChildren(cards)
                
                seperator = self._seperators[color]['Non-Creature'][CC]
                cards = cardItems[color]['Non-Creature'][CC]
                if cards:
                    seperator.addChildren(cards)
                
                if progressDialog:
                    progressDialog.setValue(steps)
                    QtGui.QApplication.processEvents()
        
        seperator = self._seperators['C']['Land'][0]
        cards = cardItems['C']['Land'][0]
        if cards:
            seperator.addChildren(cards)
        
        steps += 1
        if progressDialog:
            progressDialog.setValue(steps)
            QtGui.QApplication.processEvents()
        
        self.setSortingEnabled(True)
        self.resizeColumns()
        
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
        
        self.__setupTopLevelSeperators()

#-------------------------------------------------------------------------------
    def colorCards(self, cards, color=(221,221,221)):
        """
        Colors the chosen cards with chosen color. Used in coloring the
        cards in masterbase which are already in the cube. 
        """

        brush = QtGui.QBrush(QtGui.QColor(color[0], color[1], color[2]))
        
        cards = set(cards)
        cardNames = [card.name for card in cards]
        matchingCards = [card for card in self._cards.values() if card.name in cardNames]
        
        for cardItem in matchingCards:
            cardItem.setBackground(0, brush)
            
#-------------------------------------------------------------------------------
    def deColorCards(self, cards, color=(221,221,221)):
        """
        Repaints all the cards background back to white.
        """
        
        brush = QtGui.QBrush(QtGui.QColor(0,0,0))
        
        for cardItem in self._cards.values():
            cardItem.setBackground(brush)
        
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
