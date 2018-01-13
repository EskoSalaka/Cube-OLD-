#!/usr/bin/python
# -*- coding: latin-1 -*-

"""SetsTreeWidget class module."""


from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


################################################################################
class SetsTreeWidget(QtGui.QTreeWidget):
    """
    A tree view of mtg sets. This view is used in updating/editing the database.
    It displays list of mtg expansions, core sets and other sets.
    """

#-------------------------------------------------------------------------------
    def __init__(self, parent, db):
        
        #-----------------------------------------------
        super(SetsTreeWidget, self).__init__(parent)
        
        
        #-----------------------------------------------
        self._topLevelItems = {}
        self._mtgSetNameItems = {}
        self._db = db
        
        self.__setup()


#==========================================================================#
#                              Private Methods                             #
#==========================================================================#
#-------------------------------------------------------------------------------
    def _setupTopLevelItems(self):
        """Sets up the top level seperator items."""
        
        seperatorFont = QtGui.QFont('Matrix Bold', 10, QtGui.QFont.Bold)
        
        expansionsItem = QtGui.QTreeWidgetItem(self)
        expansionsItem.setText(0, 'Expansions')
        expansionsItem.setFont(0, seperatorFont)
        
        coresetsItem = QtGui.QTreeWidgetItem(self)
        coresetsItem.setText(0, 'Core Sets')
        coresetsItem.setFont(0, seperatorFont)
        
        specialsItem = QtGui.QTreeWidgetItem(self)
        specialsItem.setText(0, 'Specials&Other')
        specialsItem.setFont(0, seperatorFont)
        
        self._topLevelItems['Expansions'] = expansionsItem
        self._topLevelItems['Core Sets'] = coresetsItem
        self._topLevelItems['Specials&Other'] = specialsItem
        
        self.addTopLevelItems(self._topLevelItems.values())

#-------------------------------------------------------------------------------
    def __setup(self):
        """Sets up the general layout."""
        
        self.setAlternatingRowColors(True)
        self.setColumnCount(2)
        #labels = QtCore.QStringList(['Name', 'Code'])
        self.setIndentation(5)
        #self.setHeaderHidden(True)
        self._setupTopLevelItems()
        
        self.headerItem().setText(0, _translate("SetNameEditorDialog", "Name", None))
        self.headerItem().setText(1, _translate("SetNameEditorDialog", "Code", None))


#==========================================================================#
#                              Public methods                              #
#==========================================================================#
#-------------------------------------------------------------------------------
    def addMtgSets(self, mtgSets):
        """Adds a structured list of mtg sets to the tree."""
        
        for (mtgSetName, mtgSetCode) in mtgSets['Expansion'].iteritems():
            newItem = QtGui.QTreeWidgetItem(self._topLevelItems['Expansions'])
            newItem.setText(0, mtgSetName)
            newItem.setText(1, mtgSetCode)
            newItem.setFlags(QtCore.Qt.ItemIsUserCheckable | 
                             QtCore.Qt.ItemIsEnabled | 
                             QtCore.Qt.ItemIsEditable)
            newItem.setCheckState(0, QtCore.Qt.Unchecked)
            newItem.isNew = False
            self._mtgSetNameItems[mtgSetName] = newItem
            
            
        for (mtgSetName, mtgSetCode) in mtgSets['Core Set'].iteritems():
            newItem = QtGui.QTreeWidgetItem(self._topLevelItems['Core Sets'])
            newItem.setText(0, mtgSetName)
            newItem.setText(1, mtgSetCode)
            newItem.setFlags(QtCore.Qt.ItemIsUserCheckable | 
                             QtCore.Qt.ItemIsEnabled | 
                             QtCore.Qt.ItemIsEditable)
            newItem.setCheckState(0, QtCore.Qt.Unchecked)
            newItem.isNew = False
            self._mtgSetNameItems[mtgSetName] = newItem
        
        for (mtgSetName, mtgSetCode) in mtgSets['Special'].iteritems():
            newItem = QtGui.QTreeWidgetItem(self._topLevelItems['Specials&Other'])
            newItem.setText(0, mtgSetName)
            newItem.setText(1, mtgSetCode)
            newItem.setFlags(QtCore.Qt.ItemIsUserCheckable | 
                             QtCore.Qt.ItemIsEnabled | 
                             QtCore.Qt.ItemIsEditable)
            newItem.setCheckState(0, QtCore.Qt.Unchecked)
            newItem.isNew = False
            self._mtgSetNameItems[mtgSetName] = newItem
            
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        
#-------------------------------------------------------------------------------
    def getCheckedItems(self):
        """Returns the items which have been checked."""
        
        checkedItems = []
        
        for item in self._mtgSetNameItems.values():
            if item.checkState(0):
                checkedItems.append(item)
        
        return checkedItems

#-------------------------------------------------------------------------------
    def markNewMtgSets(self, newMtgSets):
        """
        Colours the sets which are not found in the database according
        to set names.
        """
        
        for mtgSetName in self._mtgSetNameItems.keys():
            if mtgSetName in newMtgSets:
                listItem = self._mtgSetNameItems[mtgSetName]
                listItem.setBackground(0, QtGui.QBrush(QtGui.QColor(200,0,0,50)))
                listItem.setBackground(1, QtGui.QBrush(QtGui.QColor(200,0,0,50)))
                listItem.isNew = True

#-------------------------------------------------------------------------------
    def checkAll(self):
        """
        Checks all the mtg sets.
        """
        
        for item in self._mtgSetNameItems.values():
            item.setCheckState(0, 2)

#-------------------------------------------------------------------------------
    def checkNewMtgSets(self):
        """
        Checks all the new mtg sets.
        """
        
        for item in self._mtgSetNameItems.values():
            if item.isNew:
                item.setCheckState(0, 2)
        
#-------------------------------------------------------------------------------
    def checkExpansions(self):
        """
        Checks all the mtg sets belonging to the 'Expansions'.
        """
        
        expansions = self._topLevelItems['Expansions']
        
        for childIndex in range(expansions.childCount()):
            expansions.child(childIndex).setCheckState(0, 2)

#-------------------------------------------------------------------------------
    def checkCoreSets(self):
        """
        Checks all the mtg sets belonging to the 'Core Sets'.
        """
        
        coreSets = self._topLevelItems['Core Sets']
        
        for childIndex in range(coreSets.childCount()):
            coreSets.child(childIndex).setCheckState(0, 2)

#-------------------------------------------------------------------------------
    def checkSpecials(self):
        """
        Checks all the mtg sets belonging to the 'Specials&Other'.
        """
        
        specials = self._topLevelItems['Special&Other']
        
        for childIndex in range(specials.childCount()):
            specials.child(childIndex).setCheckState(0, 2)

#-------------------------------------------------------------------------------
    def unCheckAll(self):
        """
        Unhecks all the mtg sets.
        """
        
        for item in self._mtgSetNameItems.values():
            item.setCheckState(0, 0)
