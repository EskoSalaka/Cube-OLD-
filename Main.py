import sys

from PyQt4 import QtGui

from MainWindow import Ui_MainWindow

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle(app.setStyle("plastique"))
    ui = Ui_MainWindow()
    ui.setWindowTitle('Cube')
    ui.show()
    sys.exit(app.exec_())