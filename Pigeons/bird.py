from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Bird(QLabel):

    def __init__(self,parent, x,y,dimX,dimY):
        super(Bird,self).__init__(parent)

        # birds look, size and position on board
        bird = QPixmap('13g.gif')
        bird = bird.scaled(dimX,dimY)
        self.setPixmap(bird)
        self.dimX = dimX
        self.dimY = dimY
        self.x = x
        self.y = y

    # setter for x and y position
    def setX(self,x):
        self.x = x

    def setY(self,y):
        self.y = y

    # method for moving bird
    def move(self, x, y):
        self.setX(x)
        self.setY(y)
        self.setGeo()

    # method for setting bird on x and y position
    def setBird(self,x,y):
        self.x = x
        self.y = y
        self.setGeometry(x,y,self.dimX,self.dimY)

    # method for fixing bird on board
    def setGeo(self):
        self.setGeometry(self.x,self.y,self.dimX,self.dimY)
        self.show()