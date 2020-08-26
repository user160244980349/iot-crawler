from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.title = "VAST2014MC1"
        self.left = 0
        self.top = 0
        self.right = 1450
        self.bot = 850

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.right, self.bot)
        self.center()

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())
