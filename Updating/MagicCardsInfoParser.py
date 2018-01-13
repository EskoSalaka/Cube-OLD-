import urllib2
import urllib
import os
import threading 
import time
from bs4 import BeautifulSoup

from Base.Card import Card
from Base.Set import Set
from PyQt4 import QtCore

################################################################################
class MagicCardsInfoParser:
    """
    Collects mtg set names, links, cards and other info from magiccards.info
    website specifically.
    
    Tags in the page:
    
    <h1>: Header 1, 'Sitemap', the largest heading.
    
    <h2>: Header 2, Second largest headings, these are surrounding the language
          selections, we only need the English and we stop when the h2 attribute 
          is something else.
    
    <h3>: Header 3, third largest headers, these are surrounding set types, 
          like 'Expansions' and 'Core Sets'. This is the smallest header.
          
    <a>: Hyperlink tag, has the href attribute which we need to get links for
         each mtg set
    """

#-------------------------------------------------------------------------------
    def __init__(self):
        
        #------------------------------------
        self._mainUrl = 'http://magiccards.info'

    
#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _checkFolder(self, folderPath):
        """
        Checks is a given folder exists, and creates a new on if it 
        doesnt.
        """
        
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)



#-------------------------------------------------------------------------------
    def _getSoup(self, url):
        """Returns a soup object from a given url"""

        response = urllib2.urlopen(url.lower())
        
        return BeautifulSoup(response.read())

#-------------------------------------------------------------------------------
    def _setCodeFromSetName(self, mtgSetName):
        """Returns a set code of the given mtg set name."""
        
        setNames = self.getMtgSetNames()
        
        if mtgSetName in setNames['Expansion']:
            return setNames['Expansion'][mtgSetName]
        
        if mtgSetName in setNames['Core Set']:
            return setNames['Core Set'][mtgSetName]
        
        if mtgSetName in setNames['Special']:
            return setNames['Special'][mtgSetName]
        
#-------------------------------------------------------------------------------
    def _downloadImage(self, imageUrl, imageName, destFolder, 
                       currentProgressBar=None):
        """Downloads an image from a given url."""
        
        urllib.urlretrieve(imageUrl.lower(), destFolder + imageName)
    
#==========================================================================#
#                              Public Methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def checkConnection(self):
        """
        Checks if magiccards.info is online.
        """
        
        try:
            urllib2.urlopen('http://magiccards.info/')
        except:
            return False
        
        return True

#-------------------------------------------------------------------------------
    def getOfficialMtgSetNames(self):
        """
        Returns a dictionary of all the mtg set names and codes. these ones
        are the official ones from gatherer.
        """

#-------------------------------------------------------------------------------
    def getMtgSetNames(self):
        """
        Returns a dictionary of all the mtg set names and codes. It extracts 
        all the hyperlink tags from the sitemap(with all the links to sets)
        which contain both the set name and code. 
        
        The dictionary actually contains three dictionaries, which contain
        the actual set names. One contains the expansions, one core sets
        and the third all the other sets, the specials.
        """
        
        setNames = {}
        
        expansions = {}
        coreSets = {}
        specials = {}
        all = {}
        
        setNames['Expansion'] = expansions
        setNames['Core Set'] = coreSets
        setNames['Special'] = specials
        setNames['All'] = all
        
        
        #------------------------------------
        #On the current(july 2, 2013) sitemap the Expansions are all on the
        #left column under 'Expansions', Core Sets are on the middle column 
        #under the first large heading 'Core Sets' and the rest are special 
        #sets, which go on from the rest of the middle colmun and the whole
        #third column. In fact, only the places for the expansions and
        #core sets are needed, since the special sets are everything
        #other than these.
        soup = self._getSoup(self._mainUrl + '/sitemap.html')
        
        expansionsSoup = soup.find_all('table')[1].find_all('td')[0]
        coreSetsSoup = soup.find_all('table')[1].find_all('td')[1]
        
        expansionATags = expansionsSoup.find_all('a')
        coreSetsSoupATags = coreSetsSoup.ul.find_all('a')
        
        for tag in expansionATags:
            if 'href' in tag.attrs:
                if '/en.'  in tag.attrs['href']:
                    setName = tag.string
                    setCode = tag.attrs['href'].split('/')[1].upper()
                    
                    expansions[setName] = setCode
                    all[setName] = setCode
        
        for tag in coreSetsSoupATags:
            if 'href' in tag.attrs:
                if '/en.'  in tag.attrs['href']:
                    setName = tag.string
                    setCode = tag.attrs['href'].split('/')[1].upper()
                    
                    coreSets[setName] = setCode
                    all[setName] = setCode
                    
        allATags = soup.find_all('a')
        
        for tag in allATags:
            if 'href' in tag.attrs:
                if '/en.'  in tag.attrs['href']:
                    setName = tag.string
                    setCode = tag.attrs['href'].split('/')[1].upper()
                    
                    if setName not in expansions and setName not in coreSets:
                        specials[setName] = setCode
                        all[setName] = setCode

        return setNames
            
#-------------------------------------------------------------------------------
    def getMtgSet(self, mtgSetName):
        """
        Returns a Set instance from a given urls which contains a specific
        mtg set.
        """
        
        url = 'http://magiccards.info/' + \
               self._setCodeFromSetName(mtgSetName).lower() + \
               '/en.html'

        soup = self._getSoup(url)
        
        #------------------------------------
        #First we get the set name and code, which is located in the first
        #title tag of the first head tag
        setName = unicode(soup.find('head').find('title').string)
        setCode = unicode(self._setCodeFromSetName(setName))
        
        setNames = self.getMtgSetNames()
        
        if setName in setNames['Special']:
            isSpecial = True
        else:
            isSpecial = False
        
        print setName, isSpecial
        
        mtgSet = Set(setName, setCode, isSpecial) 
        
        #------------------------------------
        #Next we go through all the cards on the same site and 
        #create card instances. All the relevant card info can be
        #exctracted without going through the sites of single cards.
        #The cards are located inside the fourth table tags td tags
        #starting from the second one.
        cards = {}
        
        try:
            cardTags = soup.find_all('table')[3].find_all('tr')[1:]
        except IndexError:
            cardTags = soup.find_all('table')[2].find_all('tr')[1:]
        
        for cardTag in cardTags:
            tdTags = cardTag.find_all('td')
            
            collectorNum = unicode(tdTags[0].string)
            cardName = unicode(tdTags[1].find('a').string)
            cardId = unicode(setCode + collectorNum)
            cardType = unicode(tdTags[2].string)
            cardCost = unicode(tdTags[3].string)
            cardRarity = unicode(tdTags[4].string)
            
            if not cardCost or cardCost == 'None':
                cardCost = ''
                
            #------------------------------------
            #Now, there are some special types of cards needed to be 
            #considered: double faced, split and flip cards. These are
            #found by their collector number, the first always contains
            #the letter 'a' and the other the letter 'b'. Also, split cards
            #have the '(' and ')' signs in their names.
            if 'a' in collectorNum and '(' in cardName and ')' in cardName:
                cardName = cardName.split('(')[1].split(')')[0]
            
            elif 'b' in collectorNum and '(' in cardName and ')' in cardName:
                firstHalf = cards[cardId.replace('b', 'a')]
                totalCost = firstHalf.cost + ' ' + cardCost
                firstHalf.cost = totalCost
                continue
            
            elif 'b' in collectorNum:
                continue
            
            newCard = Card(cardId, cardName, setName, 
                           cardRarity, cardCost, cardType)

            cards[cardId] = newCard
        
        for card in cards.values():
            mtgSet.addCard(card)
        
        return mtgSet

#-------------------------------------------------------------------------------
    def downloadMtgSetImages(self, mtgSetCode, destFolder, 
                             currentProgressBar=None, currentProgressText=None):
        """
        Downloads all the images of a mtg set with a given url and destination
        folder. The image names will be mws style (eg. Counterspell.full.jpg),
        and the images will be FULL card images without borders, as these types
        are all that are really needed. In the dest folder there should be
        another folder with the same name as the set code, if not then 
        a new will be created.
        
        Also, a progress bar can be given. If so, then the progress bar will be
        updated after each image is downloaded.
        
        Note, that the letters in url's always have to be lowered.
        """
        
        soup = self._getSoup('http://magiccards.info/' + mtgSetCode + '/en.html')
        
        downloadFolder = destFolder + "\\" + mtgSetCode + '\\'
        self._checkFolder(downloadFolder)
        
        atags = soup.find_all('a')
        atags = [tag for tag in atags if '/en/' in tag.get('href')]
        cardNames = [tag.string for tag in atags]
        
        if currentProgressBar:
            totalNum = len(cardNames)
            currentProgressBar.setMaximum(totalNum)
        
        #------------------------------------
        seen = []
        imageNames = {}
        
        try:
            cardTags = soup.find_all('table')[3].find_all('tr')[1:]
        except IndexError:
            cardTags = soup.find_all('table')[2].find_all('tr')[1:]
        
        for cardTag in cardTags:
            tdTags = cardTag.find_all('td')
            
            collectorNum = unicode(tdTags[0].string)
            cardName = unicode(tdTags[1].find('a').string)
            
            if '(' in cardName and ')' in cardName:
                cardName = cardName.split('(')[1].split(')')[0].replace('/','')
                
                if 'b' in collectorNum:
                    continue
                
            seen.append(unicode(tdTags[1].find('a').string))
            
            cardCount = cardNames.count(tdTags[1].find('a').string)
            cardCountSoFar = seen.count(tdTags[1].find('a').string)
            
            if cardCount > 1:
                cardCount = cardCountSoFar
            else:
                cardCount = ''
            
            imageName = cardName + str(cardCount) + '.full.jpg'
            imageUrl = 'http://magiccards.info/scans/en/' + \
                        mtgSetCode + '/' + \
                        str(collectorNum) + '.jpg'
            
            imageNames[imageName] = imageUrl
            
        count = 1
        for (imageName, imageUrl) in imageNames.iteritems():
            if currentProgressBar:
                QtCore.QCoreApplication.processEvents()
                text = 'Downloading image {cardName} ({current} out of {total})'
                text = text.format(cardName=imageName, 
                                   current=count, 
                                   total=totalNum)
                currentProgressText.setText(text)
                currentProgressBar.setValue(count)
                QtCore.QCoreApplication.processEvents()
                
            target = self._downloadImage
            args=(imageUrl, imageName, downloadFolder)
            
            t = threading.Thread(target=target, args=args)
            t.daemon = True
            time.sleep(0.02)
            t.start()
            count += 1
            

#-------------------------------------------------------------------------------
    def test(self):
        self.downloadMtgSetImages('m13', 'C:\\Users\\esko\\Desktop\\')
        

        
        