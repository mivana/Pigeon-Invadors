from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QImage, QPalette, QIcon, QPixmap, QTransform
import sys, random
from game import Game
from board import Board

if __name__ == '__main__':
    app = QApplication([])
    game = Game()
    sys.exit(app.exec_())