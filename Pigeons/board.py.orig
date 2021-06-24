from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QImage, QPalette, QIcon, QPixmap, QTransform
from player import Player
from bird import Bird
from bullet import Bullet
from endGame import EndGame
from multiprocessing import Queue, Process, Lock, JoinableQueue
import random, time


NUM_BIRDS = 30
BIRD_SPEED = 800
BIRD_BULLET_SPEED = 1500
BULLET_SPEED = 25
BIGBIRD_SPEED = 50

#Process that calucates the coordinates for Big Bird
def calculateBigBird(q):
    while(True):
        pos = q.get()
        if(pos == "CLOSE"):
            break
        move = pos + BIGBIRD_SPEED
        q.put(move)


class Board(QFrame):

    BoardWidth = 1200
    BoardHeight = 850

    def __init__(self, parent):
        super().__init__(parent)

        self.initBoard()

    def initBoard(self):
        '''initiates board'''

        #Queue for communication with the Process
        self.q = Queue()

        # setting timer for players
        self.timer = QBasicTimer()
        self.timer.start(20, self)

        # setting timer for birds
        self.timerBirds = QBasicTimer()
        self.timerBirds.start(BIRD_SPEED, self)
        self.timerBirdsID = self.timerBirds.timerId()

        # setting timer for birds bullets
        self.timerBird_bullet = QBasicTimer()
        self.timerBird_bullet.start(BIRD_BULLET_SPEED, self)
        self.timerBird_bulletID = self.timerBird_bullet.timerId()

        self.timerCounter = 0
        self.timerCounterBullets = 0

        # counter for levels
        self.lvl = 1
        self.nextLvl = False

        # setting label for showing number of levels
        self.lvlLabel = QLabel(self)
        pic = QPixmap('level.png')
        pic = pic.scaled(125,65)
        self.lvlLabel.setPixmap(pic)
        self.lvlLabel.move(450, 20)

        self.lvlNumberLabel = QLabel(self)
        self.changeLvlNumber()
        self.lvlNumberLabel.move(600, 22)

        self.lvlNumberLabel2 = QLabel(self)
        pic = QPixmap('blue-watercolor-number-1B.png')
        pic = pic.scaled(25, 60)
        self.lvlNumberLabel2.setPixmap(pic)
        self.lvlNumberLabel2.move(630, 22)
        self.lvlNumberLabel2.hide()

        # setting label for showing who's winner
        self.winnerLabel = QLabel(self)
        pic = QPixmap('winner.png')
        pic = pic.scaled(700, 60)
        self.winnerLabel.setPixmap(pic)
        self.winnerLabel.move(190,530)
        self.winnerLabel.hide()

        self.winnerNumLabel = QLabel(self)
        pic = QPixmap('blue-watercolor-number-0B.png')
        pic = pic.scaled(25, 60)
        self.winnerNumLabel.setPixmap(pic)
        self.winnerNumLabel.move(925, 530)
        self.winnerNumLabel.hide()

        self.noWinnerLabel = QLabel(self)
        pic = QPixmap('nowinner.png')
        pic = pic.scaled(500, 60)
        self.noWinnerLabel.setPixmap(pic)
        self.noWinnerLabel.move(340, 530)
        self.noWinnerLabel.hide()

        # setting curent value for birds speed and bullets speed
        self.curBirdSpeed = 30
        self.curBirdBulletSpeed = 10

        # firing speed for bird's bullets
        self.speedBirdBullets = 75

        self.bigBird = Bird(self,-55,80,70,70)
        self.bigBirdUp = True
        self.bigBirdHit = False
        #self.bigBirdStarted = False
        self.bigBirdFlying = False

        self.bigBird.setGeometry(10,100,70,70)
        self.bigBird.hide()

        # initializing 3x10 birds, their directions, counter for number of hitted ones, bullets they have and number of ones they fired
        self.birds = [Bird(self, 0, 0,50,50) for i in range(NUM_BIRDS)]
        self.BirdsGoingLeft = True
        self.BirdsGoingRight = False
        self.wingsUp = [True for i in range(NUM_BIRDS)]
        self.bird_hit = [False for i in range(NUM_BIRDS)]
        self.dead_count = 0

        self.bird_bullets = [Bullet(self, 0, 0, 'Poop-512.png') for i in range(NUM_BIRDS)]
        self.bird_bullets_fired = [False for i in range(NUM_BIRDS)]

        self.leftBirdsWall = 9
        self.rightBirdsWall = 0
        self.rowNum =  20

        self.setUpGame()

        # initializing 2 players, their bullets, flags for firing bullets, hitting birds, touching another label, being dead and checking which key is pressed
        self.player1 = Player(self, 1100, 750, 1110,'planeW.gif')
        self.player2 = Player(self, 50, 750, 0, 'planeG.gif')
        self.bullet1 = Bullet(self, 1120, 740, 'bullet.png')
        self.bullet1.hide()
        self.bullet2 = Bullet(self, 70, 740, 'bullet.png')
        self.bullet2.hide()

        self.isFired1 = False
        self.isFired2 = False
        self.labelsTouching1 = False
        self.labelsTouching2 = False
        self.hitBird1 = False
        self.hitBird2 = False

        self.noWinner = False

        self.isDead = 0
        self.isDead1=False
        self.isDead2=False

        self.gameOver=False

        self.keys_pressed = set()

        self.startProcess()

        self.setFocusPolicy(Qt.StrongFocus)

    #closes the process when app closes
    def closeProcess(self):
        self.q.put("CLOSE")

    #starts the process
    def startProcess(self):
        self.p = Process(target=calculateBigBird, args=[self.q])
        self.p.start()

    # method for setting up game -> place birds on board in formation
    def setUpGame(self):
        j = 0
        i = 0
        for z in range(NUM_BIRDS):
            self.birds[z].setX(1100 - i * 65)
            self.birds[z].setY(150 + j * 55)
            self.birds[z].setGeo()

            self.FlightPicture(self.birds[z],False,True)

            self.bird_bullets[z].set_bullets(1125 - i * 80, 205 + j * 80)
            self.bird_bullets[z].hide()

            i += 1
            if (i != 0 and i % 10 == 0):
                j += 1
                i = 0

    # method for updating game
    def game_update(self):
        #checks if neighbor birds are alive
        self.checkNeighbors()

        #counter for the Big Bird and Bird's Bullets
        self.timerCounter += 1
        self.timerCounterBullets += 1

        #Big Birds movement
        if (self.timerCounter % 14 == 0) and self.bigBirdFlying and self.bigBirdHit is False:
            self.timerCounter = 0
            self.flyBigBird()

        #Bird's Bullets movement
        if(self.timerCounterBullets % self.speedBirdBullets == 0):
            self.update_bullets()
            self.timerCounterBullets = 0


        # -> checks which player has fired bullet and calls responding method
        if self.isFired1:
            self.isFired1 = self.fireBullet(self.bullet1, self.bullet1.y - BULLET_SPEED,True)
        else:
            self.bullet1.hide()
            self.hitBird1 = False

        if self.isFired2:
            self.isFired2 = self.fireBullet(self.bullet2, self.bullet2.y - BULLET_SPEED, True)
        else:
            self.bullet2.hide()
            self.hitBird2 = False

        # -> checks if bird has been hit and sets her at responding position
        if self.hitBird1:
            self.bullet1.y = 0
            self.bullet1.x = 0
            self.bullet1.hide()

        if self.hitBird2:
            self.bullet2.y = 0
            self.bullet2.x = 0
            self.bullet2.hide()

        # -> checks flags to know if it needs to stop game and display winner
        if self.isDead1 is True and self.isDead2 is True:
            self.gameOver= True

            if (self.player1.num_lifes > 0 and self.player2.num_lifes > 0):
                self.noWinner = True
            self.endGame()

        # -> checks which key is being pressed and calls responding method to move player in wanted direction
        if Qt.Key_Left in self.keys_pressed:
            self.MovePlayer(self.player1, self.player1.x - 20, 'planeWLeft.gif')
        if Qt.Key_Right in self.keys_pressed:
            self.MovePlayer(self.player1, self.player1.x + 20, 'planeWRight.gif')
        if Qt.Key_A in self.keys_pressed:
            self.MovePlayer(self.player2, self.player2.x - 20, 'planeGLeft.gif')
        if Qt.Key_D in self.keys_pressed:
            self.MovePlayer(self.player2, self.player2.x + 20, 'planeGRight.gif')

        # -> checks if player is alive and sets position for bullet to be fired
        if Qt.Key_Up in self.keys_pressed and self.isFired1 is False and self.isDead1 is False:
            self.bullet1.y = self.player1.y - 15
            self.bullet1.x = self.player1.x + 20
            self.bullet1.move(self.bullet1.x, self.bullet1.y)
            self.bullet1.show()
            self.isFired1 = True
        if Qt.Key_W in self.keys_pressed and self.isFired2 is False and self.isDead2 is False:
            self.bullet2.y = self.player2.y - 15
            self.bullet2.x = self.player2.x + 20
            self.bullet2.move(self.bullet2.x, self.bullet2.y)
            self.bullet2.show()
            self.isFired2 = True

        # -> checks if there's need to update game to new level, if bird's bullet has hit the player, which player has hit the bird
        for i in range(NUM_BIRDS):
            if(self.dead_count == 30 and (self.isDead1 is False or self.isDead2 is False)):
                self.nextLvl = True
                self.lvl += 1
                self.curBirdSpeed += 2
                if(self.lvl % 4 == 0):
                    self.curBirdBulletSpeed += 2

                if(self.lvl % 4 == 0):
                    self.speedBirdBullets = round(self.speedBirdBullets - 5, 0)

                self.bigBird.move(-55,80)
                self.bigBird.hide()

                self.bigBirdFlying = False

                self.changeLvlNumber()

                if self.isDead1 is False:
                    self.player1.num_lifes = 3
                    for i in range(self.player1.num_lifes):
                        self.player1.lifes[i].show()

                if self.isDead2 is False:
                    self.player2.num_lifes = 3
                    for i in range(self.player2.num_lifes):
                        self.player2.lifes[i].show()

                self.setUpGame()

                self.BirdsGoingLeft = True
                self.BirdsGoingRight = False
                self.wingsUp = [True for i in range(NUM_BIRDS)]
                self.bird_hit = [False for i in range(NUM_BIRDS)]
                self.dead_count = 0

                self.bird_bullets_fired = [False for i in range(NUM_BIRDS)]

                self.leftBirdsWall = 9
                self.rightBirdsWall = 0

                self.hitBird1 = True
                self.hitBird2 = True

                if self.isDead1 is False:
                    self.player1.x = 1100
                    self.player1.y = 750
                    self.player1.move(self.player1.x, self.player1.y)

                if self.isDead2 is False:
                    self.player2.x = 50
                    self.player2.y = 750
                    self.player2.move(self.player2.x, self.player2.y)

            if self.bird_bullets_fired[i] and self.bird_hit[i] is False:
                if self.areLabelsTouching(self.bird_bullets[i], self.player1) is False and self.areLabelsTouching(self.bird_bullets[i], self.player2) is False:
                    self.bird_bullets_fired[i] = self.fireBullet(self.bird_bullets[i], self.bird_bullets[i].y + self.curBirdBulletSpeed, False)
                elif self.areLabelsTouching(self.bird_bullets[i], self.player2):
                    self.player2.move(50, 750)
                    self.player2.x = 50
                    self.player2.num_lifes -= 1
                    self.player2.lifes[self.player2.num_lifes].hide()
                    self.bird_bullets_fired[i] = False
                    self.bird_bullets[i].hide()
                    if self.player2.num_lifes == 0:
                        self.isDead2 = True
                        self.isDead = 2
                        self.player2.setParent(None)
                elif self.areLabelsTouching(self.bird_bullets[i], self.player1):
                    self.player1.move(1100, 750)
                    self.player1.x = 1100
                    self.player1.num_lifes -= 1
                    self.player1.lifes[self.player1.num_lifes].hide()
                    self.bird_bullets_fired[i] = False
                    self.bird_bullets[i].hide()
                    if self.player1.num_lifes == 0:
                        self.isDead1 = True
                        self.isDead = 1
                        self.player1.setParent(None)

            if self.gameOver:
                self.birds[i].hide()
                self.bird_bullets[i].hide()

            if (self.bird_hit[i]):
                self.birds[i].hide()
                self.bird_bullets[i].hide()

            else:
                value = self.detectCollision(self.birds[i], self.bullet1, self.bullet2)
                if (value == 1):
                    self.dead_count += 1
                    print(self.dead_count)
                    self.hitBird1 = True
                    self.bird_hit[i] = True
                if (value == 2):
                    self.dead_count += 1
                    print(self.dead_count)
                    self.hitBird2 = True
                    self.bird_hit[i] = True

                if self.bigBirdFlying:
                    value = self.detectCollision(self.bigBird, self.bullet1, self.bullet2)
                    if (value == 1 and self.player1.num_lifes < 3):
                        self.bigBirdHit = True
                        self.bigBird.hide()
                        if self.player1.num_lifes < 3:
                            self.player1.num_lifes += 1
                            self.player1.lifes[self.player1.num_lifes-1].show()
                    if (value == 2 and self.player2.num_lifes < 3):
                        self.bigBirdHit = True
                        self.bigBird.hide()
                        if self.player2.num_lifes < 3:
                            self.player2.num_lifes += 1
                            self.player2.lifes[self.player2.num_lifes].show()

    # method for checking if there's been collision between two labels
    def areLabelsTouching(self, label1, label2):
        self.label1 = label1
        self.label2 = label2
        if self.label2.x <= self.label1.x <= self.label2.x + self.label2.dimX and self.label1.y + self.label1.dimY >= \
                self.label2.y:
            return True
        elif self.label2.x <= self.label1.x + self.label1.dimX <= self.label2.x + self.label2.dimX and self.label1.y + \
                self.label1.dimY >= self.label2.y:
            return True
        else:
            return False

    #Determinates if the Big Bird will fly or not
    def startBigBird(self):
        chance = random.randint(1,100)
        if(chance < 10):
            self.bigBird.move(-55, 80)
            self.bigBirdFlying = True

    #Movement of the Big Bird
    def flyBigBird(self):
        if self.bigBird.x < 1200:
            self.q.put(self.bigBird.x)
            pos = self.q.get()
            self.bigBird.move(pos, self.bigBird.y)
            if self.bigBirdHit is False:
                self.FlightPicture(self.bigBird, self.bigBirdUp, False)
            else:
                self.bigBird.hide()

            if self.bigBirdUp:
                self.bigBirdUp = False
            else:
                self.bigBirdUp = True
        else:
            self.bigBirdFlying = False
            self.bigBird.hide()

    #Checks if the birds 'neighbors' are alive or not, used for the movement of the alive birds to the end of the screen
    def checkNeighbors(self):
        for i in range(self.rightBirdsWall, self.leftBirdsWall):
            if (self.bird_hit[i] is False or self.bird_hit[i + 10] is False or self.bird_hit[i + 20] is False):
                break
            else:
                self.rightBirdsWall = i + 1

        for j in range(self.leftBirdsWall, self.rightBirdsWall, -1):
            if (self.bird_hit[j] is False or self.bird_hit[j + 10] is False or self.bird_hit[j+ 20] is False):
                break
            else:
                self.leftBirdsWall = j - 1

    # method for birds movement formation
    def update_birds(self):
        if(self.bigBirdFlying is False):
            self.startBigBird()

        if (self.BirdsGoingLeft):

            newX1 = self.birds[self.leftBirdsWall].x - self.curBirdSpeed - 10
            newX2 = self.birds[self.leftBirdsWall + 10].x - self.curBirdSpeed - 10
            newX3 = self.birds[self.leftBirdsWall + 20].x - self.curBirdSpeed - 10
            if self.bird_hit[self.rightBirdsWall + 20] is False:
                newY = self.birds[self.rightBirdsWall + 20].y + self.curBirdSpeed
            elif self.bird_hit[self.rightBirdsWall + 10] is False:
                newY = self.birds[self.rightBirdsWall + 10].y + self.curBirdSpeed
            else:
                newY = self.birds[self.rightBirdsWall].y + self.curBirdSpeed


            if(newY > 720):
                self.isDead1 = True
                self.isDead2 = True

            if self.gameOver is False:
                if (newX1 > 10 and newX2 > 10 and newX3 > 10):
                    for i in range(NUM_BIRDS):
                        if self.bird_hit[i] is False:
                            #self.qB.put(self.birds[i].x)
                            #self.qB.put("SPEED")
                            #self.qB.put(self.curBirdSpeed)
                            #move = self.qB.get()
                            #self.birds[i].move(move, self.birds[i].y)
                            self.birds[i].move(self.birds[i].x - self.curBirdSpeed, self.birds[i].y)
                            self.FlightPicture(self.birds[i], self.wingsUp[i],True)

                            if (self.wingsUp[i]):
                              self.wingsUp[i] = False
                            else:
                                self.wingsUp[i] = True
                        else:
                            self.birds[i].hide()

                else:
                    for i in range(NUM_BIRDS):
                        if self.bird_hit[i] is False:
                            self.birds[i].move(self.birds[i].x, self.birds[i].y + self.curBirdSpeed - 5)
                            self.FlightPicture(self.birds[i], self.wingsUp[i], False)
                            if (self.wingsUp[i]):
                                self.wingsUp[i] = False
                            else:
                                self.wingsUp[i] = True
                            self.BirdsGoingLeft = False
                            self.BirdsGoingRight = True
                        else:
                            self.birds[i].hide()

            else:
                for i in range(NUM_BIRDS):
                    self.birds[i].hide()

        elif(self.BirdsGoingRight):

            newX1 = self.birds[self.rightBirdsWall].x + self.curBirdSpeed + 10
            newX2 = self.birds[self.rightBirdsWall+10].x + self.curBirdSpeed + 10
            newX3 = self.birds[self.rightBirdsWall+20].x + self.curBirdSpeed + 10

            if self.bird_hit[self.leftBirdsWall + 20]:
                newY = self.birds[self.leftBirdsWall + 20].y + self.curBirdSpeed
            elif(self.bird_hit[self.leftBirdsWall + 10]):
                newY = self.birds[self.leftBirdsWall + 10].y + self.curBirdSpeed
            else:
                newY = self.birds[self.leftBirdsWall].y + self.curBirdSpeed


            if(newY > 720):
                self.isDead1 = True
                self.isDead2 = True

            if self.gameOver is False:

                if (newX1 < 1150 and newX2 < 1150 and newX3 < 1150):
                    for i in range(NUM_BIRDS):
                        if self.bird_hit[i] is False:
                            self.birds[i].move(self.birds[i].x + self.curBirdSpeed, self.birds[i].y)
                            self.FlightPicture(self.birds[i], self.wingsUp[i], False)
                            if (self.wingsUp[i]):
                                self.wingsUp[i] = False
                            else:
                                self.wingsUp[i] = True
                        else:
                            self.birds[i].hide()

                else:
                    for i in range(NUM_BIRDS):
                        if self.bird_hit[i] is False:
                            self.birds[i].move(self.birds[i].x, self.birds[i].y + self.curBirdSpeed - 5)
                            self.FlightPicture(self.birds[i], self.wingsUp[i],True)
                            if (self.wingsUp[i]):
                                self.wingsUp[i] = False
                            else:
                                self.wingsUp[i] = True
                            self.BirdsGoingLeft = True
                            self.BirdsGoingRight = False
                        else:
                            self.birds[i].hide()

            else:
                for i in range(NUM_BIRDS):
                    self.birds[i].hide()

    # method for changing picture of a bird to mimic winds movement
    def FlightPicture(self,bird, wUp , left):
        if(wUp):
            picture = QPixmap("13g.gif")
        else:
            picture = QPixmap("18g.gif")

        if (left):
            picture = picture.transformed(QTransform().scale(-1, 1))

        picture = picture.scaled(50, 50)
        bird.setPixmap(picture)

    # method for birds randomly firing bullets
    def update_bullets(self):
        for i in range(NUM_BIRDS):
            choice = False
            if(self.nextLvl):
                chance = 200
            chance = round(200-self.dead_count,0)
            number = random.randint(1,chance)
            if(number < 20):
                choice = True
            if(choice and self.bird_bullets_fired[i] is False):
                self.bird_bullets[i].x = self.birds[i].x + 50
                self.bird_bullets[i].y = self.birds[i].y + 55

                self.bird_bullets[i].move(self.bird_bullets[i].x,self.bird_bullets[i].y)
                self.bird_bullets[i].show()
                self.bird_bullets_fired[i] = True

    # method for detecting key being pressed and adding that event to array of pressed keys
    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

    # method for detecting released pressed key and removing that event from array of pressed keys
    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.key())

        key = event.key()

        if key == Qt.Key_Left:
            self.changePicture(self.player1, 'planeW.gif')
        if key == Qt.Key_Right:
            self.changePicture(self.player1, 'planeW.gif')
        if key == Qt.Key_A:
            self.changePicture(self.player2, 'planeG.gif')
        if key == Qt.Key_D:
            self.changePicture(self.player2, 'planeG.gif')

    # method for moving players within the range of board when keys are pressed
    def MovePlayer(self, player, newX, newPicture):

        if newX < Board.BoardWidth - 60 and newX > 10:
            self.player = player
            self.changePicture(self.player, newPicture)
            self.player.x = newX
            self.player.move(newX, self.player.y)
            self.show()

    # method for changing picture of a player to mimic movement in requested direction
    def changePicture(self, label, newPicture):
        picture = QPixmap(newPicture)
        picture = picture.scaled(40, 60)
        label.setPixmap(picture)

    # method for ending game and showing result
    def endGame(self):
        self.end = EndGame(self)

        if(self.noWinner is False):
            if self.isDead == 2 :
                pic = QPixmap('blue-watercolor-number-2B.png')
            else:
                pic = QPixmap('blue-watercolor-number-1B.png')
            pic = pic.scaled(25, 60)
            self.winnerNumLabel.setPixmap(pic)

            self.winnerLabel.show()
            self.winnerNumLabel.show()
        else:
            self.noWinnerLabel.show()

        self.end.show()
        self.lvlLabel.hide()
        self.lvlNumberLabel.hide()
        self.lvlNumberLabel2.hide()
        self.player1.hide()
        self.player2.hide()
        self.bigBird.hide()

        for i in range(self.player1.num_lifes):
            self.player1.lifes[i].hide()

        for i in range(self.player2.num_lifes):
            self.player2.lifes[i].hide()

    # method for changing number of level
    def changeLvlNumber(self):
        if(self.lvl > 9 and self.lvl < 100):
            strLvl = str(self.lvl)
            pic1 = QPixmap('blue-watercolor-number-' + strLvl[0] + 'B.png')
            pic2 = QPixmap('blue-watercolor-number-' + strLvl[1] + 'B.png')

            pic1 = pic1.scaled(25, 60)
            pic2 = pic2.scaled(25, 60)

            self.lvlNumberLabel.setPixmap(pic1)
            self.lvlNumberLabel2.setPixmap(pic2)
            self.lvlNumberLabel.show()
            self.lvlNumberLabel2.show()
        else:
            pic = QPixmap('blue-watercolor-number-' + str(self.lvl) + 'B.png')
            pic = pic.scaled(25, 60)
            self.lvlNumberLabel.setPixmap(pic)
            self.lvlNumberLabel.show()

    # method for player firing bullets
    def fireBullet(self, bullet, newY, player):
        self.bullet = bullet

        if(player):
            if newY < 10:
                self.bullet.hide()
                return False
            else:
                self.bullet.move(self.bullet.x, newY)
                self.bullet.y = newY
                self.bullet.show()
                return True
        elif(newY > 840):
            self.bullet.hide()
            return False
        else:
            self.bullet.move(self.bullet.x, newY)
            self.bullet.y = newY
            self.bullet.show()
            return True

    # method for detecting which player has hit the bird
    def detectCollision(self, label1, label2, label3):
        self.label1 = label1
        self.label2 = label2

        detX1_start = self.label1.x
        detX1_stop = self.label1.x + self.label1.dimX

        detY1_start = self.label1.y
        detY1_stop = self.label1.y + self.label1.dimY

        detX2_start = self.label2.x
        detX2_stop = self.label2.x + self.label2.dimX

        detY2_start = self.label2.y
        detY2_stop = self.label2.y + self.label2.dimY

        if (detX2_start > detX1_start and detX2_start < detX1_stop):
            if (detY2_start > detY1_start and detY2_start < detY1_stop):
                return 1
            elif (detY2_stop > detY1_start and detY2_stop < detY1_stop):
                return 1
        elif (detX2_stop > detX1_start and detX2_stop < detX1_stop):
            if (detY2_start > detY1_start and detY2_start < detY1_stop):
                return 1
            elif (detY2_stop > detY1_start and detY2_stop < detY1_stop):
                return 1

        self.label2 = label3

        detX1_start = self.label1.x
        detX1_stop = self.label1.x + self.label1.dimX

        detY1_start = self.label1.y
        detY1_stop = self.label1.y + self.label1.dimY

        detX2_start = self.label2.x
        detX2_stop = self.label2.x + self.label2.dimX

        detY2_start = self.label2.y
        detY2_stop = self.label2.y + self.label2.dimY

        if (detX2_start > detX1_start and detX2_start < detX1_stop):
            if (detY2_start > detY1_start and detY2_start < detY1_stop):
                return 2
            elif (detY2_stop > detY1_start and detY2_stop < detY1_stop):
                return 2
        elif (detX2_stop > detX1_start and detX2_stop < detX1_stop):
            if (detY2_start > detY1_start and detY2_start < detY1_stop):
                return 2
            elif (detY2_stop > detY1_start and detY2_stop < detY1_stop):
                return 2

        return -1

    # method for initiazing game update according to timer event
    def timerEvent(self, event):
        if self.gameOver is False:
            self.game_update()

            if (self.timerBirdsID == event.timerId()):
                self.update_birds()

            self.update()
