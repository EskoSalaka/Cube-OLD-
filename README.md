# Cube

Cube is a handy MTG tool designed for quick and easy deckbuilding
specifically for limited formats. It is built with PyQt4 and supports

* Creating, editing and saving decks in various formats
* Creating, editing and saving cubes
* Generating desired types of sealed decks from standard expansion
* Generating sealed decks from cubes
* Filtering cards in various ways
* Easily updating the card database and downloading card images from
magiccards.info

Cube only works with full card images and is not very useful in other
things such as simply browsing cards or maintaining collections.

<img src="git_images\Capture1.JPG">

# Current status

While it still is fully functional and totally usable, Cube is becoming
more or less decrepit. The Cube only works with Python2.7 and PyQt4 and is currently being updated
to Python3 and PyQt5. Another problem with Cube is that the card database has very little data and it is updated
by scraping the info from https://magiccards.info/. The database itself is just a pickled Python dictionary.

In the future, maintaining and updating the card database will be done with MtgApi (https://docs.magicthegathering.io/#cards)
and the database itself will be implemented with ZODB (http://www.zodb.org/en/latest/).

The progress of the new version can be found here https://github.com/EskoSalaka/Cube

# Requirements and installation

* Python 2.7
* PyQt4
* Matplotlib
* BeautifulSoup4

Note, that using neither PyQt5 or Python3 will not work!

BeautifulSoup and Matplotlib can be simply installed with

```
pip install matplotlib
```
and
```
pip install beautifulsoup4
```

PyQt4 has to be installed with a wheel which can be found here
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4

Installing a wheel with pip can be done in the following way
```
pip install PyQt4-4.11.4-cp35-none-win_amd64.whl
```

Be sure to choose the correct windows and Python versions for PyQt

The Cube itself can be cloned with

```
git clone https://github.com/EskoSalaka/Cube-OLD-.git
```

Running Main.py will run the app.


# Usage

### Editing decks

Deck creation itself is rather intuitive. Double-clicking the cards will move them from the sideboard
to the deck and right-clicking will bring out a menu where you can choose to seperate cards by color, type or
casting cost. After the deck is finished, it can be saved from "File" --> "Save deck as". Statistics of the deck
are shown automatically on the top of the card lists.

Basic lands can be added by using the spinner on the lower right corner.

### Generating sealed decks

Sealed decks can be generated from "Sealed Deck Generation" --> "Standard Sealed deck"

by choosing sets from the dropdown menu and adding booster packs with desired amount of cards.

<img src="git_images\Capture2.JPG">


Sealed decks from cubes can be generated from "Sealed Deck Generation" --> "Sealed Deck from cube".
The cubes can be provided as simple text files, Magic Workstation deck files or .CUBE files, which can be created with the app.

### Updating

Updating the database and downloading card images can be done from "Database" --> "Update the database".
Clicking on the "Connect" button will establish the connection to magiccards.info and automatically look for new sets.
New sets will be marked red. Choosing whatever sets to be added (or updated) to the database and clicking on "Update sets"
will update the database with the chosen data

<img src="git_images\Capture5.JPG">

Choosing sets and clicking on "Download images" will automatically download all the card images of the set
to the chosen folder.

<img src="git_images\Capture4.JPG">

### Editing cubes

Cube editor can be opened with the "Open cube editor" - button. In the cube editor, the whole card database is loaded into a list separated by colours, types and
total castings costs. Older cubes can be loaded via "File" --> "Open a acube" and saving the current cube can be done via  "File" --> "Save cube as".

Similarly, statistics for the cube are shown in the statistics window. Handily, the cards already in the cube can be colored by
clicking the appropriate button in the toolbar. Cards in the cube or in the database can be filtered as normal, but currently there is no
search feature for a single cards or filtering by sets.

<img src="git_images\Capture6.JPG">