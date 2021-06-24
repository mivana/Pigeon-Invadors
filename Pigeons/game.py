from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtGui import QBrush, QImage, QPalette, QIcon
from board import Board


class Game(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        '''initiates application UI'''

        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.resize(1200, 850)
        self.center()
        self.setWindowTitle('Pigeon Invaders')
        self.setWindowIcon(QIcon('13g.gif'))

        # setting background picture
        oImage = QImage("sky.png")
        sImage = oImage.scaled(1200, 850)
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.show()

    def closeEvent(self, *args, **kwargs):
        self.tboard.closeProcess()

    # method for centering main window
    def center(self):
        '''centers the window on the screen'''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)