"""StatisticsAnalyzer class module."""

import random
import numpy

from numpy.random import hypergeometric
from collections import  defaultdict

################################################################################
class StatisticsAnalyzer:
    """
    A class for analyzing mtg decks or cubes. It can also be used to configure
    certain matplotlib figures like color and type distribution pies.
    """

#-------------------------------------------------------------------------------
    def __init__(self):
        
        self._cards = []
        
        #------------------------------------
        #The types, colours and the rest are held in various dicts. From these 
        #it's simple to calculate whatever stats you want. The dicts are mostly
        #self-explanatory.
        self._colors = {'B':0, 'R':0, 'G':0, 'U':0, 'W':0, 'C':0, 'M':0}
        self._castingCosts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        self._creatureManaCosts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        self._nonCreatureManaCosts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        self._manaSymbols = {'B':0, 'R':0, 'G':0, 'U':0, 'W':0, 'C':0}
        self._types =  {'Artifact':0, 'Creature':0, 'Enchantment':0, 
                        'Instant':0, 'Land':0, 'Planeswalker':0, 'Sorcery':0}
        
        self._simpleTypes = {'Creature':0, 'Non-Creature':0, 'Land':0}
        
        
        #------------------------------------
        #Some matplotlib customization stuff
        self._matplotlibColors = {'G':'#00A550','R':'#C45655', 'B':'#2F4F4F', 
                                  'U':'#0892D0','W':'#FFFFE0', 'C':'0.7', 
                                  'M': '#FFB300'}


#==========================================================================#
#                              Public methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def addCard(self, card):
        """Adds a new Card instance to the analyzer."""
        
        self._cards.append(card)
        self._simpleTypes[card.simpleType] += 1
        
        #Case 1: Land. In this case the card has no manacost, color, or type
        #other than land
        if 'Land' in card.type:
            self._types['Land'] += 1
        
        #Every card other than land:
        else:
            #Color
            if len(card.color) > 1:
                self._colors['M'] += 1
            
            elif len(card.color) == 1:
                self._colors[card.color] += 1
            
            else:
                self._colors['C'] += 1
            
            #Manasymbols
            for symbol in card.cost:
                if symbol == 'R':
                    self._manaSymbols['R'] += 1
                if symbol == 'U':
                    self._manaSymbols['U'] += 1
                if symbol == 'G':
                    self._manaSymbols['G'] += 1
                if symbol == 'W':
                    self._manaSymbols['W'] += 1
                if symbol == 'B':
                    self._manaSymbols['B'] += 1
                else:
                    try:
                        int(symbol)
                        self._manaSymbols['C'] += int(symbol)
                    except ValueError:
                        pass
            
            #Manacosts
            if card.totalCost < 6:
                if 'Creature' in card.type:
                    self._creatureManaCosts[card.totalCost] += 1
                else:
                    self._nonCreatureManaCosts[card.totalCost] += 1
                
                self._castingCosts[card.totalCost] += 1
                
            else:
                if 'Creature' in card.type:
                    self._creatureManaCosts[6] += 1
                else:
                    self._nonCreatureManaCosts[6] += 1
                
                self._castingCosts[6] += 1
            
            #Types
            if 'Creature' in card.type:
                self._types['Creature'] += 1
            
            if 'Enchantment' in card.type:
                self._types['Enchantment'] += 1
            
            if 'Artifact' in card.type:
                self._types['Artifact'] += 1
            
            if 'Instant' in card.type:
                self._types['Instant'] += 1
            
            if 'Planeswalker' in card.type:
                self._types['Planeswalker'] += 1
            
            if 'Sorcery' in card.type:
                self._types['Sorcery'] += 1

#-------------------------------------------------------------------------------
    def removeCard(self, card):
        """Removes the given Card instance from the analyzer."""
        
        self._cards.pop(self._cards.index(card))
        self._simpleTypes[card.simpleType] -= 1
        
        
        #Case 1: Land. In this case the card has no manacost, color, or type
        #other than land
        if 'Land' in card.type:
            self._types['Land'] -= 1
        
        #Every card other than land:
        else:
            #Color
            if len(card.color) > 1:
                self._colors['M'] -= 1
            
            elif len(card.color) == 1:
                self._colors[card.color] -= 1
            
            else:
                self._colors['C'] -= 1
            
            #Manasymbols
            for symbol in card.cost:
                if symbol == 'R':
                    self._manaSymbols['R'] -= 1
                if symbol == 'U':
                    self._manaSymbols['U'] -= 1
                if symbol == 'G':
                    self._manaSymbols['G'] -= 1
                if symbol == 'W':
                    self._manaSymbols['W'] -= 1
                if symbol == 'B':
                    self._manaSymbols['B'] -= 1
                else:
                    try:
                        int(symbol)
                        self._manaSymbols['C'] -= int(symbol)
                    except ValueError:
                        pass
            
            #Manacosts
            if card.totalCost < 6:
                if 'Creature' in card.type:
                    self._creatureManaCosts[card.totalCost] -= 1
                else:
                    self._nonCreatureManaCosts[card.totalCost] -= 1
                
                self._castingCosts[card.totalCost] -= 1
                
            else:
                if 'Creature' in card.type:
                    self._creatureManaCosts[6] -= 1
                else:
                    self._nonCreatureManaCosts[6] -= 1
                
                self._castingCosts[6] -= 1
            
            #Types
            if 'Creature' in card.type:
                self._types['Creature'] -= 1
            
            if 'Enchantment' in card.type:
                self._types['Enchantment'] -= 1
            
            if 'Artifact' in card.type:
                self._types['Artifact'] -= 1
            
            if 'Instant' in card.type:
                self._types['Instant'] -= 1
            
            if 'Planeswalker' in card.type:
                self._types['Planeswalker'] -= 1
            
            if 'Sorcery' in card.type:
                self._types['Sorcery'] -= 1
        
#-------------------------------------------------------------------------------
    def clear(self):
        """Cleares the whole analyzer."""
        
        self._cards = []
        self._colors = {'B':0, 'R':0, 'G':0, 'U':0, 'W':0, 'C':0, 'M':0}
        self._castingCosts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        self._creatureManaCosts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        self._nonCreatureManaCosts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        self._manaSymbols = {'B':0, 'R':0, 'G':0, 'U':0, 'W':0, 'C':0}
        self._types =  {'Artifact':0, 'Creature':0, 'Enchantment':0, 
                        'Instant':0, 'Land':0, 'Planeswalker':0, 'Sorcery':0}
        
        self._simpleTypes = {'Creature':0, 'Non-Creature':0, 'Land':0}
        
#-------------------------------------------------------------------------------
    def getSampleHand(self, card):
        """Returns 7 random cards from the card list."""
        
        return random.sample(self._cards, 7)

#-------------------------------------------------------------------------------
    def getCardDrawnProbabilities(self, tries=100000):
        """
        Calculates, for each card, the probabilities for drawing that card at 
        least once by each turn up to 10.
        
        The probabilities will be returned as a dict card names and lists
        in which each of the indexes of the list tells the probability for
        the index-turn.
        """
        
        cardDrawnProbabilities = {}
        cardCounts = defaultdict(int)
        
        for card in self._cards:
            cardCounts[card.name] += 1
        
        for card in self._cards:
            cardDrawnProbabilities[card.name] = []
            
            nGood = cardCounts[card.name]
            samples = len(self._cards)
            nBad = samples - nGood
            
            for turnNumber in range(0,11):
                #------------------------------------
                #The probability for getting AT LEAST one pointed card from
                #a sample of total number of cards with a certain number
                #of cards drawn can be extracted from the hypergeometric
                #distribution.
                cardsDrawn = turnNumber + 7
                
                draws = hypergeometric(nGood, nBad, cardsDrawn, tries)
                probability = sum(draws>=1) / float(tries)
                
                cardDrawnProbabilities[card.name].append(probability)
            
#-------------------------------------------------------------------------------
    def getAverageCastingCost(self):
        """Returns the average casting cost of the cards. Ignores lands."""
        
        costs = [card.totalCost for card in self._cards if 
                 'Land' not in card.type]
        
        try:
            return round(float(sum(costs)) / float(len(costs)), 1)
        except ZeroDivisionError:
            return 0

#==========================================================================#
#                              Matplotlib figure configs                   #
#==========================================================================#

#-------------------------------------------------------------------------------
    def typesDistributionPie(self, typesDistPie):
        """
        Configures a given matplotlib pie with the card info 
        contained in the class.
        """
        
#-------------------------------------------------------------------------------
    def simpleTypesDistributionPie(self, typesDistPie):
        """
        Configures a given matplotlib pie with the card info 
        contained in the class. In this variation only creatures, lands and
        other non-creature cards are plotted.
        """
        
        typesDistPie.clear()
        typesDistPie.set_title('Type Distribution')
        
        colors = []
        fracs = []
        labels = []
        
        if self._simpleTypes['Land']:
            fracs.append(self._simpleTypes['Land'])
            colors.append('y')
            labels.append('Lands')
            
        if self._simpleTypes['Non-Creature']:
            fracs.append(self._simpleTypes['Non-Creature'])
            colors.append('#F0E68C')
            labels.append('Other')
            
        if self._simpleTypes['Creature']:
            fracs.append(self._simpleTypes['Creature'])
            colors.append('#FF8C00')
            labels.append('Creatures')
        
        def autoPct(pct):
            val = int(round(pct * sum(fracs) / 100.0))
            return '{p:.0f}%  ({v:d})'.format(p=pct,v=val)
        
        typesDistPie.pie(fracs, autopct=autoPct,
                           colors=colors, shadow=True)
        if labels:
            typesDistPie.legend(labels, loc=(-0.25, -0.22), columnspacing=0.5, frameon=False)

#-------------------------------------------------------------------------------
    def manaSymbolsBar(self, manaSymbolsBar):
        """
        Configures a given matplotlib barplot with the card info 
        contained in the class.
        """
        
        title = 'Manasymbols'
        
        yTickLabels = []
        xTickLabels = []
        manaSymbols = []
        sortedColors = []
        
        manaSymbolsBar.clear()
        
        for (color, num) in self._manaSymbols.iteritems():
            if color == 'C':
                continue
            
            yTickLabels.append(color)
            manaSymbols.append(num)
            sortedColors.append(self._matplotlibColors[color])
        
        indices = numpy.arange(0,5)
        width = 0.7
        
        rects = manaSymbolsBar.barh(indices+width/2, manaSymbols, width, color=sortedColors)
        
        manaSymbolsBar.set_yticks(indices+width)
        manaSymbolsBar.set_xticklabels(xTickLabels)
        manaSymbolsBar.set_yticklabels(yTickLabels)
        manaSymbolsBar.set_title(title)
        manaSymbolsBar.set_ylim([0, 5.5])
        manaSymbolsBar.set_xlim([0, max(manaSymbols)+2])
        
        def autolabel(rects):
            for rect in rects:
                manaSymbolsBar.text(0.9 + rect.get_width(),
                                          rect.get_y() + width / 2, 
                                          '%d'%int(rect.get_width()),
                                          horizontalalignment='center',
                                          verticalalignment='center',
                                          )
        
        autolabel(rects)
        
#-------------------------------------------------------------------------------
    def manaCostsBar(self, manaCostBar):
        """
        Configures a given matplotlib barplot with the card info 
        contained in the class.
        """
        
        manaCostBar.clear()
        
        title = 'Manacosts'
        xlabel = 'Avg casting cost: ({avgCC})'.format(avgCC=self.getAverageCastingCost())
        
        xTickLabels = ('0', '1', '2', '3', '4', '5', '6+')
        yTickLabels = ()
        
        creatureManaCosts = [self._creatureManaCosts[index] for index in range(7)]
        otherManaCosts = [self._nonCreatureManaCosts[index] for index in range(7)]
        totals = [sum(total) for total in zip(creatureManaCosts, otherManaCosts)]
        
        indices = numpy.arange(0,7)
        width = 0.7
        
        rects1 = manaCostBar.bar(indices+width/2, creatureManaCosts,
                                       width, color='#FF8C00')
        
        rects2 = manaCostBar.bar(indices+width/2, otherManaCosts, 
                                      width, color='#F0E68C', 
                                      bottom=creatureManaCosts)
        
        manaCostBar.set_xticks(indices+width)
        manaCostBar.set_xticklabels(xTickLabels)
        manaCostBar.set_yticklabels(yTickLabels)
        manaCostBar.set_title(title)
        manaCostBar.set_xlabel(xlabel)
        manaCostBar.set_xlim([0, 7.5])
        manaCostBar.set_ylim([0, max(totals)+2])
        
        for rect, rect2 in zip(rects1, rects2):
            height = rect.get_height() + rect2.get_height() + 0.2
            
            manaCostBar.text(rect.get_x() + rect.get_width() / 2.0,
                             0.4 + height, 
                             '%d'%int(height),
                             horizontalalignment='center',
                             verticalalignment='center',
                             )
        
        
        manaCostBar.legend(['Creatures', 'Other'], loc=(1.0, -0.2), columnspacing=0.5, frameon=False)
        



#-------------------------------------------------------------------------------
    def colorDistPie(self, colorDistPie):
        """
        Configures a given matplotlib piechart with the card info 
        contained in the class.
        """
        
        colorDistPie.clear()
        colorDistPie.set_title('Color Distribution')
        
        arrangedColors = []
        fracs = []
        
        for (color, num) in self._colors.iteritems():
            if num:
                fracs.append(self._colors[color])
                arrangedColors.append(self._matplotlibColors[color])
        
        colorDistPie.pie(fracs, labels=fracs, 
                         colors=arrangedColors, shadow=True,
                         startangle=90)
        
    
#==========================================================================#
#                              Private methods                             #
#==========================================================================#
        
#==========================================================================#
#                              Properties                                  #
#==========================================================================#
