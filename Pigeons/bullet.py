from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Bullet(QLabel):
    def __init__(self, parent, x, y, pic):
        super(Bullet, self).__init__(parent)

        if(pic == 'Poop-512.png'):
            self.dimX = 20
            self.dimY = 20
        else:
            self.dimX = 10
            self.dimY = 15

        # bullet look, size and position on board
        bullet = QPixmap(pic)
        bullet = bullet.scaled(self.dimX, self.dimY)
        self.setPixmap(bullet)
        self.x = x
        self.y = y
        self.setGeometry(x, y, self.dimX, self.dimY)

    # setter for x and y position
    def set_bullets(self,x,y):
        self.x = x
        self.y = y
        self.setGeometry(x,y,self.dimX,self.dimY)