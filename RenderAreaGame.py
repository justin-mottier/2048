#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
from time import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class RenderAreaGame(QWidget):
    def __init__(self, window, parent=None):
        """
            Constructeur de la classe

            :param window: pointeur vers la classe Window
            :type window: Window
        """
        super(RenderAreaGame,self).__init__(parent)
        self.window = window
        self.initUI()

    def initUI(self):
        """
            initialisation des variables
        """
        #On récupère la grille de jeu et le mode de jeu
        self.liste = self.window.game.liste
        self.mode = self.window.mode

        #initialisation de variables
        self.score = 0
        self.combo = 0
        self.comboSteps = 0
        self.botState = False

        #Si le mode est tetris on crée d'autres variables
        if (self.mode == "tetris"):
            #On récupère la valeur de la prochaine case
            self.valueTile = self.window.game.valueTile
            self.pauseState = False
            self.rectPause = QRect(420,6,35,35)

        self.pen = QPen(QColor(255,255,255))
        self.pen.setWidth(2)
        font = QFont("Arial", 14, QFont.Bold)
        self.setFont(font)
        self.brush = Qt.NoBrush

        self.rectReset = QRect(400,6,35,35)
        self.rectBot = QRect(450,7,35,35)

        #On change la position de l'interface graphique de la grille par rapport au mode
        if (self.mode != "tetris"): self.position = [125,52,30,100]
        else : self.position = [100,102,25,75]

    def drawFigure(self,painter):
        """
            Affichage la grille de jeu, le score puis par rapport au mode le combot , le bot, le bouton retour (mode classique/vsPop/miroir) et prochaine case et bouton pause (mode tetris)
            :param painter: painter
            :type painter: QPainter
        """
        #Dictionnaire avec les images des planètes avec leur valeur
        dicoPicture = {2:"planets/pluto.png",4:"planets/lune.png",8:"planets/mercure.png",16:"planets/mars.png",32:"planets/venus.png",64:"planets/neptune.png",128:"planets/terre.png",256:"planets/uranus.png",512:"planets/saturne.png",1024:"planets/jupiter.png",2048:"planets/sun.png"}
        if (self.mode == "tetris"): painter.drawPixmap(102,self.geometry().y()+25,375,75,QPixmap("draw/rect_background_2.png"))

        #On parcours l'ensemble de la grille de jeu pour l'afficher
        for i in range(len(self.liste)):
            for j in range(4):
                #Si le mode de jeu est différent de tetris on affiche le rectangle de fond sinon on l'affiche cas partir de la 2eme ligne de la grille de jeu
                if (self.mode != "tetris"): painter.drawPixmap((self.position[0]*j)+ self.position[1],(self.position[0]*i)+self.geometry().y()+self.position[2],self.position[3],self.position[3],QPixmap("draw/rect_background.png"))
                elif (i > 0): painter.drawPixmap((self.position[0]*j)+ self.position[1],(self.position[0]*i)+self.geometry().y()+self.position[2],self.position[3],self.position[3],QPixmap("draw/rect_background.png"))
                k = 2
                while (k <= 2048):
                    #Si la position de la grille est égale à k ou -k on affiche la planète correspondante répertoriée dans le dictionnaire
                    if (self.liste[i][j] == k):
                        #Si le mode de jeu est miroir on affiche l'inverse de la planète k
                        if (self.mode != "miroir"): painter.drawPixmap((self.position[0]*j)+ self.position[1],(self.position[0]*i)+self.geometry().y()+self.position[2],self.position[3],self.position[3],QPixmap(dicoPicture.get(k)))
                        else: painter.drawPixmap((self.position[0]*j)+ self.position[1],(self.position[0]*i)+self.geometry().y()+self.position[2],self.position[3],self.position[3],QPixmap(dicoPicture.get(4096/k)))
                        break
                    elif (self.liste[i][j] == -k):
                        if (self.mode != "miroir"): painter.drawPixmap((self.position[0]*j)+ self.position[1],(self.position[0]*i)+self.geometry().y()+self.position[2],self.position[3],self.position[3],QPixmap(dicoPicture.get(k)))
                        else: painter.drawPixmap((self.position[0]*j)+ self.position[1],(self.position[0]*i)+self.geometry().y()+self.position[2],self.position[3],self.position[3],QPixmap(dicoPicture.get(4096/k)))
                        break
                    k *= 2
        painter.drawText(QPoint(130, self.geometry().y()+8),"score : "+str(self.score))
        if (self.mode != "tetris"):
            #Par rapport au niveau de combo on change l'image
            if (self.comboSteps == 0 and self.combo != 3): painter.drawPixmap(260, self.geometry().y()-16,35,35,QPixmap("draw/combo_0.png"))
            elif (self.comboSteps == 1 and self.combo != 3): painter.drawPixmap(260, self.geometry().y()-16,35,35,QPixmap("draw/combo_1.png"))
            elif (self.comboSteps == 2 and self.combo != 3): painter.drawPixmap(260, self.geometry().y()-16,35,35,QPixmap("draw/combo_2.png"))
            elif (self.comboSteps == 3 and self.combo != 3): painter.drawPixmap(260, self.geometry().y()-16,35,35,QPixmap("draw/combo_3.png"))
            elif (self.comboSteps == 4 and self.combo != 3): painter.drawPixmap(260, self.geometry().y()-16,35,35,QPixmap("draw/combo_4.png"))
            elif (self.combo == 3 and self.comboSteps == 0): painter.drawPixmap(260, self.geometry().y()-16,35,35,QPixmap("draw/combo_5.png"))
            painter.drawText(266, self.geometry().y()+8,str(self.combo+1)+"x")
            #Si le nombre de coup est plus petit que 50 on affiche le bouton reset en off sinon en on
            if (self.window.game.coup < 50): painter.drawPixmap(400,6,35,35,QPixmap("draw/reset_off.png"))
            else: painter.drawPixmap(400,6,35,35,QPixmap("draw/reset_on.png"))
            #Si le bot est desactivé et le mode est différent de miroir on affiche le bouton bot en off sinon en on
            if (not self.botState and self.mode != "miroir"): painter.drawPixmap(450,7,35,35,QPixmap("draw/robotOff.png"))
            elif (self.botState and self.mode != "miroir"): painter.drawPixmap(450,7,35,35,QPixmap("draw/robotOn.png"))
        else:
            painter.drawText(QPoint(250, self.geometry().y()+8),"Prochaine :")
            #Par rapport à la valeur de la prochaine case on change la planète à afficher
            if (self.valueTile == 2): painter.drawPixmap(365, 6,35,35,QPixmap("planets/pluto.png"))
            elif (self.valueTile == 4): painter.drawPixmap(365, 6,35,35,QPixmap("planets/lune.png"))
            elif (self.valueTile == 8): painter.drawPixmap(365, 6,35,35,QPixmap("planets/mercure.png"))
            #Si la pause est désactivé on affiche le bouton pause en off sinon en on
            if (not self.pauseState): painter.drawPixmap(420,6,35,35,QPixmap("draw/pause_off.png"))
            else: painter.drawPixmap(420,6,35,35,QPixmap("draw/pause_on.png"))

    def mousePressEvent(self, event):
        """
            Execute la fonction quand l'utilisateur utilise sa souris

            :param event: événement de la souris
            :type event: QMouseEvent
        """
        if (self.mode != "tetris"):
            #Si l'utilisateur appuie sur le rectangle du bouton reset et le nombre de coup est plus grand que 50 on fait le backupMove
            if (self.rectReset.contains(event.pos())):
                if (self.window.game.coup >= 50):
                    self.window.game.backupMove()
            #Si l'utilisateur appuie sur le rectangle du bouton bot
            elif (self.rectBot.contains(event.pos()) and self.mode != "miroir"):
                if (not self.botState):
                    #On lance le bot
                    self.window.iaRunning = True
                    self.window.game.iaRunning = True
                    self.botState = True
                    self.window.setIA(event)
                else:
                    #On éteint le bot
                    self.window.iaRunning = False
                    self.window.game.iaRunning = False
                    self.botState = False
        else:
            #Si l'utilisateur appuie sur le rectangle du bouton pause
            if (self.rectPause.contains(event.pos())):
                if (not self.pauseState):
                    #On met en pause le jeu
                    self.pauseState = True
                    self.window.game.timer.stop()
                    self.window.game.timerCheckEndTile.stop()
                else:
                    #On relance le jeu
                    self.pauseState = False
                    self.window.game.timer.start(750)
        self.update()

    def paintEvent(self, event):
        """
            Crée le QPainter et affiche l'interface graphique
            :param event: événement
            :type event: event
        """
        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        self.drawFigure(painter)
