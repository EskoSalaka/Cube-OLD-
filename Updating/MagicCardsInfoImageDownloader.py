import urllib, urllib2
import os

from bs4 import BeautifulSoup

################################################################################
class MagicCardsInfoImageDownloader:
    """
    This class handles downloading images from magiccards.info site.
    """

#-------------------------------------------------------------------------------
    def __init__(self):
        pass
    
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
    def _downloadImage(self, imageUrl, imageName, destFolder):
        """Downloads an image from a given url."""
        
        urllib.urlretrieve(imageUrl, destFolder + imageName)

#-------------------------------------------------------------------------------
    def _getSoup(self, url):
        """Returns a soup object from a given url"""
        
        response = urllib2.urlopen(url)
        
        return BeautifulSoup(response.read())
    
#==========================================================================#
#                              Public Methods                              #
#==========================================================================#

#-------------------------------------------------------------------------------
    def downloadMtgSetImages(self, mtgSetCode, destFolder):
        """
        Downloads all the images of a mtg set with a given url and destination
        folder. The image names will be mws style (eg. Counterspell.full.jpg),
        and the images will be FULL card images without borders, as these types
        are all that are really needed. In the dest folder there should be
        another folder with the same name as the set code, if not then 
        a new will be created.
        """
        
        
        
        soup = self._getSoup('http://magiccards.info/' + mtgSetCode + '/en.html')
        
        #------------------------------------
        #First we extract the cards' hyperlink tags(a-tags)
        
        atags = soup.find_all('a')
        atags = [tag for tag in atags if '/en/' in tag.get('href')]
        
        #------------------------------------
        #Next we go through the hrefs of the hypelink tags and extract the card 
        #name. On the site of the set the cards are always in order so that
        #first cards collectors number is 1 and seconds 2 and so on. Knowing 
        #this we can download each card image one by one since the links to the
        #images of the cards contain the collectors numbers.
        
        downloadFolder = destFolder + mtgSetCode + '//'
        
        self._checkFolder(downloadFolder)
        
        cardNames = [tag.string for tag in atags]
        seen = []
        cardNum = 1
        
        for tag in atags:
            cardName = tag.string
            
            if cardNames.count(cardName) > 1:
                seen.append(cardName)
                count = seen.count(cardName)
                
                imageName = cardName + str(count) + '.full.jpg'
                imageUrl = 'http://magiccards.info/scans/en/' + \
                            mtgSetCode + '/' + \
                            str(cardNum) + '.jpg'
                
            else:
                imageName = cardName + '.full.jpg'
                imageUrl = 'http://magiccards.info/scans/en/' + mtgSetCode + '/' + \
                            str(cardNum) + '.jpg'
            
            self._downloadImage(imageUrl, imageName, downloadFolder)
            cardNum += 1
            