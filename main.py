import sys

from PyQt5 import QtWidgets

import config
from initialization.initialization import initialize
from preprocessing.preprocessing import preprocessing
from tools import database, fsys
from ui.window import Window


def main():
    database.connect(config.database)

    if not fsys.is_locked(config.resources + "/.initialization.lock"):
        initialize()
        fsys.lock(config.resources + "/.initialization.lock")

    if not fsys.is_locked(config.resources + "/.preprocessing.lock"):
        preprocessing()
        fsys.lock(config.resources + "/.preprocessing.lock")

    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    sys.exit(app_exit(app))


def app_exit(app):
    app.exec()
    database.disconnect()


if __name__ == '__main__':
    main()
