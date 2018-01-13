#!/usr/bin/python
# -*- coding: latin-1 -*-


################################################################################
class FileHandler:
    """
    A class for reading and writing various files.
    """

#-------------------------------------------------------------------------------
    def __init__(self, database):
        
        self._db = database
        self._setNames = self._db.getMtgSetNames()

#==========================================================================#
#                              Public methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def makeCard(self, textLine):
        """
        Checks if a given line of text is a card name and returns a card instance
        if it is. Otherwise returns False.
        
        It first tries to return a card instance which is from a regular mtg set.
        """
        
        if '//' in textLine:
            textLine = textLine.replace('//', '/')
            textLine = textLine.replace(' ', '')

        if self._db.hasCard(textLine):
            regularCards = self._db.getRegularCards(textLine)
            
            if regularCards:
                return regularCards[-1]
            else:
                return self._db.getCards(textLine)[-1]
        
        else:
            return False


#-------------------------------------------------------------------------------
    def readMWSDeck(self, deckFile):
        """
        Returns cards from an MWSdeck format file. Reads the file 
        line-by-line.
        
        
        """
        
        lands = {'Forest' : 0, 'Island' : 0, 'Plains' : 0, 
                 'Swamp' : 0, 'Mountain' : 0}
        
        sideBoard = []
        deck = []
        rejected = []
        
        for line in deckFile:
            
            #1. Check if the line has card information by checking if the line
            #contains the '[' and ']' characters. Every mwsdeck file has these.
            #Also check if the line is not a comment
            if '[' and ']' in line and not '/' in line:
                
                #2. Then extract the set, name, count and the altArt 
                #number(if any) of the card
                cardName = line.split('] ')[-1].split('(')[0].rstrip()
                num = int(''.join(filter(lambda x: x.isdigit(), line.split('[', 1)[0])))
                setCode = line.split('[', 1)[-1].split(']', 1)[0]
                
                if cardName in lands:
                    lands[cardName] += num
                    continue
                
                if not self._db.hasCard(cardName):
                    rejected.append(cardName)
                    continue
                
                if self._db.hasMtgSet(mtgSetCode=setCode):
                    setInstance = self._db.getMtgSet(mtgSetCode=setCode)
                    cardInstance = setInstance.getCard(cardName=cardName)
                    print setInstance.name, cardInstance.name
                    
                    if not cardInstance:
                        print 1
                        cardInstance = self._db.getCards(cardName)[-1]
                
                else:
                    cardInstance = self._db.getCards(cardName)[-1]
                
                if 'SB:' in line:
                    for _ in range(num):
                        sideBoard.append(cardInstance)
                else:
                    for _ in range(num):
                        deck.append(cardInstance)
                
                    
        return deck, sideBoard, lands, rejected
    
#-------------------------------------------------------------------------------
    def writeMwsDeck(self, deckFile, deckCards, sbCards):
        """
        Creates an mwsdeck file from given cards. It's not formatted
        in any way, only cardnames on each line are written.
        """

        #-----------------------------
        #First we write the cards in the deck to the file
        for card in deckCards:
            qty = card.getQty()
            setCode = self._setNames[card.mtgSetName]
            altArt = card.altArt
            
            if card.isDual:
                cardName = unicode(card.name) + '/' + card.dualCardName
            else:
                cardName = unicode(card.name)
                
            if altArt:
                line = u'{qty} [{setCode}] {cardName} ({altArt})\n'.format(qty=qty, 
                                                               setCode=setCode, 
                                                               cardName=cardName,
                                                               altArt=altArt)
            else:
                line = u'{qty} [{setCode}] {cardName}\n'.format(qty=qty, 
                                                           setCode=setCode, 
                                                           cardName=cardName)
            deckFile.write(line.encode('latin-1'))
            
       
        #-----------------------------
        #Then sideboard
        for card in sbCards:
            qty = card.getQty()
            setCode = setCode = self._setNames[card.mtgSetName]
            altArt = card.altArt
            
            if card.isDual:
                cardName = unicode(card.name) + '/' + card.dualCardName
            else:
                cardName = unicode(card.name)
                
            if altArt:
                line = u'SB: {qty} [{setCode}] {cardName} ({altArt})\n'.format(qty=qty, 
                                                                   setCode=setCode, 
                                                                   cardName=cardName,
                                                                   altArt=altArt)
            else:
                line = u'SB: {qty} [{setCode}] {cardName}\n'.format(qty=qty, 
                                                               setCode=setCode, 
                                                               cardName=cardName)
            deckFile.write(line.encode('latin-1'))
                
#-------------------------------------------------------------------------------
    def readTextFile(self, textFile):
        """
        Returns cards from a text file. Reads the file 
        line-by-line and attempts to recognize card names on each.
        
        This algorithm is not particularly sophisticated; it only strips
        leading and trailing spaces, newline characters and numbers, and 
        assumes that the leftover characters make up a cardname. Therefore, it
        can be used to read simple lists like apperentice .dec files. Also, 
        the string on each line has to be converted to unicode with the latin-1
        character set because of the latin AE character and few other special
        characters that appear in some of the cards.
        """
        
        sideBoard = []
        rejected = ''
        duplicates = []

        for line in textFile:
            line = ''.join(filter(lambda x: not x.isdigit(), line))
            line = line.lstrip()
            card = self.makeCard(line.rstrip())
            
            if card:
                if card not in sideBoard:
                    sideBoard.append(card)
                else:
                    duplicates.append(line)
            else:
                rejected = rejected + line
        
        for duplicate in set(duplicates):
            dupTxt = '(Duplicate{num})'.format(num=duplicates.count(duplicate))
            rejected = rejected + dupTxt + duplicate

        return sideBoard, rejected

#-------------------------------------------------------------------------------
    def cubeToTxtFile(self, cube, textFile, 
                            frontHook='', backHook='',
                            spoilerFrontHook='', spoilerBackHook=''):
        """
        Writes a Cube instance  as a textfile. It uses the general magic deck
        format with simple cardnames and number 1 before each cardname. It is
        also organized by color, type and casting cost.
        
        Alternatively autocard and spoiler hooks can be inserted for various 
        forums. The hooks will be written before and after the card name
        respectively, and spoiler hooks before and after every section.
        """
        
        sortedCards = cube.getSortedCards()
        if spoilerBackHook and spoilerFrontHook:
            spoilerFrontHook = spoilerFrontHook + '\n'
            spoilerBackHook = spoilerBackHook + '\n'
        #-----------------------------
        #Lands
        num = len(sortedCards['C']['Land'][0])
        textFile.write('Lands({num})\n'.format(num=num).encode('latin-1'))
        textFile.write(spoilerFrontHook.encode('latin-1'))
        for card in sortedCards['C']['Land'][0]:
            line = '   1 ' + frontHook + card.name  + backHook + '\n'
            textFile.write(line.encode('latin-1'))
        
        textFile.write(spoilerBackHook.encode('latin-1'))
        
        #-----------------------------
        #Black Creatures
        textFile.write('\n'.encode('latin-1'))
        textFile.write('Black\n'.encode('latin-1'))
        textFile.write(spoilerFrontHook.encode('latin-1'))
        textFile.write('---Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['B']['Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['B']['Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
        
        #-----------------------------
        #Black non-creatures
        textFile.write('---Non-Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['B']['Non-Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['B']['Non-Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
        
        textFile.write(spoilerBackHook.encode('latin-1'))
        
        #-----------------------------
        #Red Creatures
        textFile.write('\n'.encode('latin-1'))
        textFile.write('Red\n'.encode('latin-1'))
        textFile.write(spoilerFrontHook.encode('latin-1'))
        textFile.write('---Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['R']['Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['R']['Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
        
        #-----------------------------
        #Red non-creatures
        textFile.write('---Non-Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['R']['Non-Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['R']['Non-Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
            
        textFile.write(spoilerBackHook.encode('latin-1'))
        
        #-----------------------------
        #Green Creatures
        textFile.write('\n'.encode('latin-1'))
        textFile.write('Green\n'.encode('latin-1'))
        textFile.write(spoilerFrontHook.encode('latin-1'))
        textFile.write('---Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['G']['Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['G']['Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
        
        #-----------------------------
        #Green non-creatures
        textFile.write('---Non-Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['G']['Non-Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['G']['Non-Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))

        #-----------------------------
        #Blue Creatures
        textFile.write('\n'.encode('latin-1'))
        textFile.write('Blue\n'.encode('latin-1'))
        textFile.write(spoilerFrontHook.encode('latin-1'))
        textFile.write('---Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['U']['Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['U']['Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
            
        textFile.write(spoilerBackHook.encode('latin-1'))
        
        #-----------------------------
        #Blue non-creatures
        textFile.write('---Non-Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['U']['Non-Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['U']['Non-Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
        
        #-----------------------------
        #White Creatures
        textFile.write('\n'.encode('latin-1'))
        textFile.write('White\n'.encode('latin-1'))
        textFile.write(spoilerFrontHook.encode('latin-1'))
        textFile.write('---Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['W']['Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['W']['Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
            
        textFile.write(spoilerBackHook.encode('latin-1'))
        
        #-----------------------------
        #White non-creatures
        textFile.write('---Non-Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['W']['Non-Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['W']['Non-Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))

        #-----------------------------
        #Colorless Creatures
        textFile.write('\n'.encode('latin-1'))
        textFile.write('Colorless/Artifacts\n'.encode('latin-1'))
        textFile.write(spoilerFrontHook.encode('latin-1'))
        textFile.write('---Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['C']['Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['C']['Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
        
        #-----------------------------
        #Colorless non-creatures
        textFile.write('---Non-Creatures\n'.encode('latin-1'))
        
        for CC in range(0,7):
            num = len(sortedCards['C']['Non-Creature'][CC])
            line = '------{CC}CC({num})\n'.format(CC=CC, num=num)
            textFile.write(line.encode('latin-1'))
            
            for card in sortedCards['C']['Non-Creature'][CC]:
                line = '   1 ' + frontHook + card.name  + backHook + '\n'
                textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
            
        textFile.write(spoilerBackHook.encode('latin-1'))

        #-----------------------------
        #Multicolor cards
        combinations = ['WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG']
        textFile.write('Multicolor\n'.encode('latin-1'))
        textFile.write(spoilerFrontHook.encode('latin-1'))
        textFile.write('\n'.encode('latin-1'))
        
        for combo in combinations:
            textFile.write('{combo}\n'.format(combo=combo).encode('latin-1'))
            
            textFile.write('---Creatures\n'.encode('latin-1'))
            for CC in range(0,7): 
                for card in sortedCards['M']['Creature'][CC]:
                    if combo == card.color or combo[::-1] == card.color:
                        line = '   1 ' + frontHook + card.name  + backHook + '\n'
                        textFile.write(line.encode('latin-1'))
            
            textFile.write('\n'.encode('latin-1'))
            textFile.write('---Non-Creatures\n'.encode('latin-1'))
            for CC in range(0,7): 
                for card in sortedCards['M']['Non-Creature'][CC]:
                    if combo == card.color or combo[::-1] == card.color:
                        line = '   1 ' + frontHook + card.name  + backHook + '\n'
                        textFile.write(line.encode('latin-1'))
        
        textFile.write('\n'.encode('latin-1'))
        textFile.write('The Rest\n'.format(combo=combo).encode('latin-1'))
        textFile.write('\n'.encode('latin-1'))
        
        textFile.write('---Creatures\n'.encode('latin-1'))
        for CC in range(0,7): 
            for card in sortedCards['M']['Creature'][CC]:
                if len(card.color) > 2:
                    line = '   1 ' + frontHook + card.name  + backHook + '\n'
                    textFile.write(line.encode('latin-1'))
                    
        textFile.write('\n'.encode('latin-1'))
        textFile.write('---Non-Creatures\n'.encode('latin-1'))
        for CC in range(0,7): 
            for card in sortedCards['M']['Non-Creature'][CC]:
                if len(card.color) > 2:
                    line = '   1 ' + frontHook + card.name  + backHook + '\n'
                    textFile.write(line.encode('latin-1'))
                    
        textFile.write(spoilerBackHook.encode('latin-1'))
        
        