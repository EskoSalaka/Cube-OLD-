"""QuickStatsCanvas class module."""
from __future__ import unicode_literals
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy
import matplotlib as mpl

from Base.StatisticsAnalyzer import StatisticsAnalyzer

################################################################################
class QuickStatsCanvas(FigureCanvas):
    """
    An implementation of the Matplotlib figure canvas, which is also
    a PyQt4 widget. It displays quick statistics of the deck.
    """

#-------------------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        
        self._figure = Figure(facecolor='0.94')
        FigureCanvas.__init__(self, self._figure)
        
        self._colorDistPie = self._figure.add_subplot(142)
        self._manaCostBar = self._figure.add_subplot(141)
        self._manaSymbolsBar = self._figure.add_subplot(143)
        self._typesPie = self._figure.add_subplot(144)
        
        mpl.rcParams['legend.fontsize'] = 9
        mpl.rcParams['font.size'] =  10
        
        self._figure.tight_layout(rect=[0.0, 0.21, 1, 0.93])
        
        self._statsAnalyzer = StatisticsAnalyzer()
        
        self.Update()

#==========================================================================#
#                              Configuration                               #
#==========================================================================#

#-------------------------------------------------------------------------------
    def removeCardData(self, card):
        """Removes the given cards data from the dictionaries. Not fail safe."""
        
        self._statsAnalyzer.removeCard(card)
        

#-------------------------------------------------------------------------------
    def addCardData(self, card):
        """Adds the given cards data to the stats dictionaries."""
        
        self._statsAnalyzer.addCard(card)

#-------------------------------------------------------------------------------
    def Update(self):
        """Updates and repaints the graphs. """
        
        self._statsAnalyzer.colorDistPie(self._colorDistPie)
        self._statsAnalyzer.manaCostsBar(self._manaCostBar)
        self._statsAnalyzer.manaSymbolsBar(self._manaSymbolsBar)
        self._statsAnalyzer.simpleTypesDistributionPie(self._typesPie)
        self._figure.canvas.draw()
        
#-------------------------------------------------------------------------------
    def clear(self):
        """Clears the list of all data."""
        
        self._statsAnalyzer.clear()
        self.Update()
        