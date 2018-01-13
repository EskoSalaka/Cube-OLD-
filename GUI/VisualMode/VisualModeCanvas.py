"""VisualModeCanvas-class module."""
import cPickle as pickle
from PyQt4 import QtCore, QtGui 

from CardLabel import CardLabel
from CardPile import CardPile
from Database import Database
import copy

################################################################################
class VisualModeCanvas(QtGui.QFrame):
    """
    A QFrame which incorporates dragging and dropping QLabels represented as 
    cards. It's used for a more visual deckbuilding tool where you can work
    with actual card images on a desktop.
    
    Dragging and dropping is implemented by overwriting dragEnter, dragMove,
    drop and mousePress Events.
    """

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent):
        super(VisualModeCanvas, self).__init__(parent=parent)
        
        #------------------------------------
        self._cardPiles = []
        self._cardLabelContainer = []
        self._rubberBand = None
        self._rubberBandOrigin = QtCore.QPoint(0,0)
        self.l = None
        
        db = pickle.load(open('MasterBase.pick', 'rb'))
        
        self.impath = 'D:\Misc\MTG card images\Fulls'
        self.sets = db.getMtgSetNames()

        #------------------------------------
        self.setFrameStyle(QtGui.QFrame.Sunken | QtGui.QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setMinimumSize(600, 600)
        
        self.l = CardLabel(db.getCards('Counterspell')[0].getStringCardData(), self, self.sets, self.impath)

        
        self.l3 = CardLabel(db.getCards('Wild Mongrel')[0].getStringCardData(), self, self.sets, self.impath)

        
        #------------------------------------
        pile1 = CardPile(self)
        pile2 = CardPile(self)
        
        pile1.movePile(50, 50)
        pile1.movePile(100, 100)
        pile1.addCardLabel(self.l, 0)
        
        pile2.addCardLabel(self.l3, 0)
        self._cardPiles.append(pile1)
        self._cardPiles.append(pile2)


#==========================================================================#
#                              Public methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def getCanvasStats(self, event):
        """
        Returns the stats of the cards in the canvas.
        """

#-------------------------------------------------------------------------------
    def sortByColor(self, event):
        """
        Sorts the cards in the canvas to piles on designated places
        by color.
        """

#-------------------------------------------------------------------------------
    def sortByType(self, event):
        """
        Sorts the cards in the canvas to piles on designated places
        by type.
        """

#-------------------------------------------------------------------------------
    def sortByCC(self, event):
        """
        Sorts the cards in the canvas to piles on designated places
        by casting cost.
        """
        
#==========================================================================#
#                              Events                                      #
#==========================================================================#

#-------------------------------------------------------------------------------
    def mousePressEvent(self, event):
        """
        Overwritten mousePressEvent. With this the dragging and dropping
        of Card labels is enabled.
        """
        
        eventPos = event.pos()
        child = self.childAt(eventPos)
        
        if type(child) == CardLabel:
            #Left mouse button
            if event.button() == 1:
                pile = child.getPile()
                cardCopy = child.getCopy()
                offset = eventPos - child.pos()
                pile.removeCardLabel(child)
                
                self._cardLabelContainer.append((cardCopy, offset))
                self._startDrag(self.__getTransparentPixMap(child.pixmap()),
                                offset)
                
            #Right mouse button
            elif event.button() == 2:
                self.__showContextMenu(event.pos())

            #Middle mouse button
            elif event.button() == 4:
                pile = child.getPile()
                offset = eventPos - child.pos()
                childIndex = child.positionInPile()
                sectionCut = pile.getSectionCut(childIndex)
                
                cardCopies = [(cardLabel.getCopy(), offset) for cardLabel in
                              sectionCut]
                self._cardLabelContainer.extend(cardCopies)

                sectionPixMaps = [cardLabel.pixmap() for cardLabel in 
                                  sectionCut]
                mergedPixMap = self.__mergePixMaps(sectionPixMaps)
                self._startDrag(mergedPixMap, offset)
        
        elif not child:
            self._rubberBandOrigin = eventPos
            self._rubberBand = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,
                                                 self)
            self._rubberBand.setGeometry(QtCore.QRect(eventPos, QtCore.QSize()))
            self._rubberBand.show()
            
            
#-------------------------------------------------------------------------------
    def dragEnterEvent(self, event):
        """
        Overwritten dragEnterEvent. With this the dragging and dropping
        of Card labels is enabled.
        """

        event.accept()

                              
#-------------------------------------------------------------------------------
    def dragMoveEvent(self, event):
        """
        Overwritten dragMoveEvent. With this the dragging and dropping
        of Card labels is enabled.
        """
        
        event.accept()

#-------------------------------------------------------------------------------
    def dragLeaveEvent(self, event):
        """
        Overwritten dragEnterEvent. With this the dragging and dropping
        of Card labels is enabled.
        """


#-------------------------------------------------------------------------------
    def dropEvent(self, event):
        """
        Overwritten dropEvent. With this the dragging and dropping
        of Card labels is enabled.
        """
        print 1
        eventPos = event.pos()

        child = self.childAt(eventPos)
        source = event.source()
        if len(source._cardLabelContainer) < 2:
            (cardLabel, offset) = source._cardLabelContainer.pop()
            
            if type(child) == CardLabel:
                self._dropCardLabelOnPile(cardLabel, child)
                
            
            else:
                self._dropCardLabelOnCanvas(cardLabel, event.pos() - offset)
                
        else:
            if type(child) == CardLabel:
                
                (firstCardLabel, offset) = source._cardLabelContainer.pop(0)
                self._dropCardLabelOnPile(firstCardLabel, child)
                
                prevCardLabel = firstCardLabel
                for (cardLabel, offset) in source._cardLabelContainer:
                    self._dropCardLabelOnPile(cardLabel, prevCardLabel)
                    prevCardLabel = cardLabel
                
                source._cardLabelContainer = []
            
            else:
                (firstCardLabel, offset) = source._cardLabelContainer.pop(0)
                self._dropCardLabelOnCanvas(firstCardLabel, event.pos() - offset)
                
                prevCardLabel = firstCardLabel
                for (cardLabel, offset) in source._cardLabelContainer:
                    self._dropCardLabelOnPile(cardLabel, prevCardLabel)
                    prevCardLabel = cardLabel
                
                source._cardLabelContainer = []
        
        event.accept()

#-------------------------------------------------------------------------------
    def mouseDoubleClickEvent(self, event):
        """
        Overwritten mouseDoubleClickEvent. 
        """
        
        print 1

#-------------------------------------------------------------------------------
    def mouseMoveEvent(self, event):
        """
        Overwritten mouseMoveEvent. 
        """
        
        eventPos = event.pos()
        
        if self._rubberBand:
            rubberBandRect = QtCore.QRect(self._rubberBandOrigin, 
                                          eventPos)
            self._rubberBand.setGeometry(rubberBandRect.normalized())


#-------------------------------------------------------------------------------
    def mouseReleaseEvent(self, event):
        """
        Overwritten mouseMoveEvent. 
        """
        inter = []
        
        print 2
        for cardPile in self._cardPiles:
            inter.extend(cardPile.intersects(self._rubberBand.rect()))
        
        self._rubberBand.close()
        self._rubberBandOrigin = QtCore.QPoint(0,0)

#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _dragIntersectsPiles(self):
        """
        Checks if the dragged cardlabel is intersecting with any CardPiles.
        """
        
#-------------------------------------------------------------------------------
    def _dropCardLabelOnPile(self, cardLabel, childCardLabel):
        """
        Drops a cardlabel in a card pile on a ChildCardLabel.
        """
        cardLabel.setParent(self)
        pile = childCardLabel.getPile()
        pile.addCardLabel(cardLabel, pile.cardLabelIndex(childCardLabel) + 1)
        cardLabel.show()

#-------------------------------------------------------------------------------
    def _dropCardLabelOnCanvas(self, cardLabel, dropSpot):
        """
        Drops a cardlabel in a card pile on this canvas.
        """
        
        cardLabel.setParent(self)
        newPile = CardPile(self)
        newPile.addCardLabel(cardLabel, 0)
        self._cardPiles.append(newPile)
        newPile.movePile(dropSpot.x(), dropSpot.y())
        cardLabel.show()
        
#-------------------------------------------------------------------------------
    def _makeCardLabelFromEvent(self):
        """
        Checks if the dragged cardlabel is intersecting with any CardPiles.
        """

#-------------------------------------------------------------------------------
    def _startDrag(self, pixMap, hotSpot):
        """
        Creatues a QDrag object and fires up the dragging process.
        """
        
        drag = QtGui.QDrag(self)
        drag.setMimeData(QtCore.QMimeData())
        drag.setPixmap(pixMap)
        drag.setHotSpot(hotSpot)
        
        drag.exec_(QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)

        
#-------------------------------------------------------------------------------
    def __showContextMenu(self, pos):
        """Shows the context menu of the canvas."""
        
        contextMenu = QtGui.QMenu(self)
        contextMenu.addAction('Move selected cards to deck/sideboard', 
                              self._makeCardLabelFromEvent)
        contextMenu.addSeparator()
        contextMenu.exec_(self.mapToGlobal(pos))

#-------------------------------------------------------------------------------
    def __mergePixMaps(self, pixMaps):
        """
        Combines a list of pixmaps into one.
        """
        
        width = pixMaps[0].width()
        height = pixMaps[0].height() 
        
        mergedPixMap = QtGui.QPixmap(width, height+ 20 * len(pixMaps))
        bitMap = QtGui.QBitmap(mergedPixMap)
        bitMap.clear()
        mergedPixMap.setMask(bitMap)
        painter = QtGui.QPainter(mergedPixMap)
        
        counter = 0
        for pixMap in pixMaps:
            tempPixMap = QtGui.QPixmap(pixMap)
            painter.drawPixmap(0, 20 * counter, 
                               width, height,
                               tempPixMap)
            
            counter += 1
            
        
        return mergedPixMap

#-------------------------------------------------------------------------------
    def __getTransparentPixMap(self, pixMap):
        """
        Makes a transparent pixmap out of given pixmap. Adds some alpha channel.
        """
        
        transpPixMap = QtGui.QPixmap(pixMap.size())
        transpPixMap.fill(QtCore.Qt.transparent)
        
        painter = QtGui.QPainter()
        painter.begin(transpPixMap)
        painter.setCompositionMode(painter.CompositionMode_Source)
        painter.drawPixmap(transpPixMap.rect(), pixMap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        
        color = QtGui.QColor(0,0,0,70)
        painter.fillRect(0,0, pixMap.width(),pixMap.height(), 
                         QtGui.QBrush(color))
        return transpPixMap


import sys

app = QtGui.QApplication(sys.argv)
ui = VisualModeCanvas(None, None)

ui2 = VisualModeCanvas(None, None)

mainw = QtGui.QMainWindow()
frame = QtGui.QFrame()

lay = QtGui.QHBoxLayout(frame)
lay.addWidget(ui)
lay.addWidget(ui2)
mainw.setCentralWidget(frame)
mainw.show()
sys.exit(app.exec_())