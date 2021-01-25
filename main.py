import sys

from PyQt5 import QtWidgets

import config
from legacy.initialization.initialization import initialize
from tools import database, fsys
from ui.window import Window


def main():
    database.connect(config.database)

    if not fsys.is_locked(config.resources + "/.initialization.lock"):
        initialize()
        fsys.lock(config.resources + "/.initialization.lock")

    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    sys.exit(app_exit(app))


def app_exit(app):
    app.exec()
    database.disconnect()


if __name__ == '__main__':
    main()
