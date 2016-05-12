import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTranslator
import main_window

def main():
    app = QtGui.QApplication(sys.argv)
    # trans = QTranslator()
    # trans.load("translate.qm")
    # app.installTranslator(trans)
    form = main_window.MainWindow()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()