import sys
import os

from PyQt4 import QtGui
from PyQt4.QtCore import QTranslator

import main_window

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

translate_file_path = os.path.join(application_path, 'resources', 'languages.qm')

def main():
    app = QtGui.QApplication(sys.argv)
    trans = QTranslator()
    trans.load(translate_file_path)
    app.installTranslator(trans)
    form = main_window.MainWindow()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()