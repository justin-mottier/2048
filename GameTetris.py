#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from time import *
from Direction import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

class GameTetris():
    def __init__(self,window):
        """
            Constructeur de la classe (initialisation des variables)

            :param window: pointeur vers la classe Window
            :type window: Window
        """
        self.window = window
        self.score = 0
        self.window.keyPressEvent = self.keyPressEvent
        self.valueTile = 0
        self.xTile = 0
        self.yTile = 0

        self.initGame()

    def initGame(self):
        """
            Initialise la grille de jeu (4x5) remplie de 0
        """
        self.liste = []
        for i in range(5):
            tmp= []
            for j in range(4):
                tmp.append(0)
            self.liste.append(tmp)
        #Lance le jeu
        self.play()

    def resetGame(self):
        """
            Réinitialisation de la partie en mettant toute la grille à 0
        """
        for i in range(5):
            for j in range(4):
                self.liste[i][j] = 0
        #On remet le score à 0 et stop tous les timers
        self.score = 0
        self.timer.stop()
        self.timerCheckEndTile.stop()
        #Met à jour l'affichage
        self.window.renderAreaGame.score = self.score
        self.window.repaint()
        #Lance le jeu
        self.play()

    def spawnRandom(self):
        """
            Place une case 2 (70% de chance) ou 4 (20% de chance) ou 8 (10% de chance) aléatoirement dans la première ligne de la grille
        """
        ret = random.random()
        randx = random.randint(0,3)
        self.liste[0][randx] = self.valueTile
        #Place un 2 si ret <= 0.70 sinon si ret <= 0.90 place un 4 sinon place un 8
        if (ret <= 0.70):
            self.valueTile = 2
        elif (ret <= 0.90):
            self.valueTile = 4
        else:
            self.valueTile = 8
        #Initialisation des variables contenant les coordonnées de la case en mouvement
        self.xTile = randx;
        self.yTile = 0;
        #Si la variable renderAreaGame existe dans la classe Window on met à jour l'affichage
        if (hasattr(self.window, 'renderAreaGame')): self.window.renderAreaGame.valueTile = self.valueTile
        self.window.repaint()

    def isLose(self):
        """
            Vérifie l'état de la partie

            :return: si l'utilisateur à perdu
            :rtype: boolean
        """
        #Si il y a au moins 1 case plus grande que 0 dans la première ligne de la grille alors l'utilisateur à perdu
        if self.liste[0].count(0) != 4:
            effect=QSoundEffect() #Joue le son de la defaite
            effect.setSource(QUrl.fromLocalFile("sound/lose.wav"))
            effect.setVolume(0.25)
            effect.play()

            #Affiche une fenêtre
            dialog = QMessageBox()
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setWindowTitle("Perdu !")
            dialog.setText("Vous avez perdu et votre score est de : "+str(self.score))
            dialog.exec_()

            #Teste si le score est assez grand pour rentrer dans les scores
            if (self.window.highscoreF.testScoreSuffisant(self.score, "tetris")) :
                nom = ""
                while nom == "" or len(nom) > 10 or "#" in nom or "/" in nom or nom == "Pseudo":
                    nom, okPressed = QInputDialog.getText(self.window, "Entrée dans les records !","Entrez votre nom :",QLineEdit.Normal, 'Pseudo')
                    if okPressed and nom != "" and len(nom) <= 10 and "#" not in nom and "/" not in nom and nom != "Pseudo": #Si le joueur appuie sur ok et que son pseudo est dans les regles on l'ajoute dans le highscore
                        self.window.highscoreF.ajouterScoreTetris(nom, self.score)
            return True
        return False

    def isWin(self):
        """
            Vérifie l'état de la partie

            :return: si l'utilisateur à gagné
            :rtype: boolean
        """
        #si il y a un 2048 dans la grille l'utilisateur gagne la partie
        for i in self.liste:
            if (2048 in i):
                effect=QSoundEffect() #Joue le son de la victoire
                effect.setSource(QUrl.fromLocalFile("sound/win.wav"))
                effect.setVolume(0.25)
                effect.play()

                #Affiche une fenêtre
                dialog = QMessageBox()
                dialog.setIcon(QMessageBox.Information)
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setWindowTitle("Gagné !")
                dialog.setText("Vous avez gagné !")
                dialog.exec_()

                #Teste si le score est assez grand pour rentrer dans les scores
                if (self.window.highscoreF.testScoreSuffisant(self.score, "tetris")) :
                    nom = ""
                    while nom == "" or len(nom) > 10 or "#" in nom or "/" in nom or nom == "Pseudo":
                        nom, okPressed = QInputDialog.getText(self.window, "Entrée dans les records !","Entrez votre nom :",QLineEdit.Normal, 'Pseudo')
                        if okPressed and nom != "" and len(nom) <= 10 and "#" not in nom and "/" not in nom and nom != "Pseudo": #Si le joueur appuie sur ok et que son pseudo est dans les regles on l'ajoute dans le highscore
                            self.window.highscoreF.ajouterScoreTetris(nom, self.score)
                return True
        return False

    def keyPressEvent(self, event):
        """
            Récupère la touche pressée du clavier et fait l'action correspondant à la touche pressée

            :param event: touche du clavier pressée
            :type event: QKeyEvent
        """
        #Les differentes action par rapport à la touche pressée
        if(event.key() == Qt.Key_Left):
            #Bouge la case en mouvement vers la gauche
            self.window.statusBar().showMessage("Left")
            self.move(Direction.LEFT)
        elif(event.key() == Qt.Key_Right):
            self.window.statusBar().showMessage("Right")
            self.move(Direction.RIGHT)
        elif(event.key() == Qt.Key_Down):
            self.window.statusBar().showMessage("Down")
            self.move(Direction.DOWN)
        elif(event.key() == Qt.Key_Space):
            self.window.statusBar().showMessage("Space")
            #Si le timer est activé on met en pause le jeu sinon on relance le timer et on enlève la pause
            if (self.timer.isActive()):
                #Met à jour l'affichage du bouton pause
                self.window.renderAreaGame.pauseState = True
                #Stop tous les timers
                self.timer.stop()
                self.timerCheckEndTile.stop()
            else:
                self.window.renderAreaGame.pauseState = False
                self.timer.start(750)
            self.window.update()

    def downTile(self):
        """
            Fait descendre les cases de la grille
        """
        self.timerCheckEndTile.stop()
        for i in range(len(self.liste)-2,-1,-1):
            for j in range(len(self.liste[i])):
                #Si le nombre de la case actuelle est plus grand que 0 et que la case du dessus soit égale à la case acutelle ou qu'elle soit égale à 0
                if (self.liste[i][j] != 0 and (self.liste[i][j] == self.liste[i+1][j] or self.liste[i+1][j] == 0)):
                    #Si le nombre de la case actuelle est égale à la case du dessus on les fusionne sinon on bouge la case actuelle vers le haut
                    if (self.liste[i][j] == self.liste[i+1][j]):
                        #Ajoute le score de la fusion des 2 cases
                        self.score += self.liste[i+1][j]*2
                        #Met à jour les coordonnées de la case en mouvement
                        if (self.yTile < 4 and self.liste[self.yTile+1][self.xTile] == self.liste[self.yTile][self.xTile]): self.yTile += 1
                        self.liste[i+1][j] = self.liste[i+1][j]*2
                        self.liste[i][j] = 0
                    else:
                        if (self.yTile < 4 and self.liste[self.yTile+1][self.xTile] == 0): self.yTile += 1
                        self.liste[i+1][j] = self.liste[i][j]
                        self.liste[i][j] = 0
        #Met en route le timer pour verifier la case en mouvement
        self.timerCheckEndTile.start(500)
        #Met à jour l'affichage de la partie
        self.window.repaint()

    def endMoveTile(self):
        """
            Vérifie si la case en mouvement ne peut plus descendre
        """
        #Si la case en mouvement a atteint la fin de la grille ou qu'elle soit juste au-dessus d'une autre case
        if ((self.yTile == 4) or (self.yTile <= 3 and self.liste[self.yTile+1][self.xTile] > 0 and self.liste[self.yTile+1][self.xTile] != self.liste[self.yTile][self.xTile])):
            self.timer.stop()
            #Fusionne toutes les cases de la grille
            self.allCombi()
            #Si l'utilisateur à perdu ou gagné on relance la partie sinon on fait apparaître une nouvelle case et on relance le timer
            if (self.isLose() or self.isWin()):
                #relance une partie
                self.resetGame()
            else:
                self.spawnRandom()
                self.timer.start(750)

    def downTilePress(self):
        """
            Descend la case en mouvement jusqu'a la première position disponible dans la colonne où elle se trouve
        """
        y = self.yTile
        #Tant que la case du-dessous est vide et qu'on a pas atteint la fin de la grille on descend
        while (y <=3 and self.liste[y+1][self.xTile] == 0):
            y += 1

        for i in range(y-self.yTile):
            self.liste[self.yTile+1][self.xTile] = self.liste[self.yTile][self.xTile]
            self.liste[self.yTile][self.xTile] = 0
            self.yTile+=1
            self.window.repaint()
            sleep(0.1)

    def allCombi(self):
        """
            Fusionne toutes les cases de la grille
        """
        modif = True
        while modif == True: #Tant qu'il y a une modification dans la grille on relance
            modif = False
            for i in range(len(self.liste)-2,-1,-1):
                for j in range(len(self.liste[i])):
                    #Si le nombre de la case actuelle est plus grand que 0 et que la case du dessus soit égale à la case acutelle ou qu'elle soit égale à 0
                    if (self.liste[i][j] != 0 and (self.liste[i][j] == self.liste[i+1][j] or self.liste[i+1][j] == 0)):
                        #Si le nombre de la case actuelle est égale à la case du dessus on les fusionne sinon on bouge la case actuelle vers le haut
                        if (self.liste[i][j] == self.liste[i+1][j]):
                            #Ajoute le score de la fusion des 2 cases
                            self.score += self.liste[i+1][j]*2
                            self.liste[i+1][j] = self.liste[i+1][j]*2
                            self.liste[i][j] = 0
                        else:
                            self.liste[i+1][j] = self.liste[i][j]
                            self.liste[i][j] = 0
                        #Il y a une modification dans la grille
                        modif = True
            #Met à jour l'affichage pour créer un effet de déplacement
            self.window.renderAreaGame.score = self.score
            self.window.repaint()
            sleep(0.3)

    def move(self, direction):
        """
            Bouge la case vers la direction donnée en paramètre

            :param direction: direction de déplacement de la case en mouvement
            :type direction: Direction
        """
        self.timerCheckEndTile.stop()
        #Si le timer est désactivé on l'active et on met à jour l'affichage du bouton stop
        if (not self.timer.isActive()):
            self.window.renderAreaGame.pauseState = False
            #On relance le timer
            self.timer.start(750)
        #On vérifie pour chaque direction si la case en mouvement ne sort pas de la grille et qu'elle ne prenne pas la place d'une autre case
        if (direction == Direction.LEFT) and self.xTile > 0 and self.xTile <= 3 and self.liste[self.yTile][self.xTile-1] == 0:
            self.liste[self.yTile][self.xTile-1] = self.liste[self.yTile][self.xTile]
            self.liste[self.yTile][self.xTile] = 0
            #On met à jour les coordonnées de la case en mouvement
            self.xTile -= 1
        elif (direction == Direction.RIGHT) and self.xTile >= 0 and self.xTile < 3 and self.liste[self.yTile][self.xTile+1] == 0:
            self.liste[self.yTile][self.xTile+1] = self.liste[self.yTile][self.xTile]
            self.liste[self.yTile][self.xTile] = 0
            self.xTile += 1
        elif (direction == Direction.DOWN) and self.yTile <= 3 and self.liste[self.yTile+1][self.xTile] == 0:
            self.downTilePress()
        #On vérifie pour chaque direction si la case en mouvement ne sort pas de la grille et fusionne avec la case de gauche ou droite
        elif (direction == Direction.LEFT) and self.xTile > 0 and self.xTile <= 3 and self.liste[self.yTile][self.xTile-1] == self.liste[self.yTile][self.xTile]:
            #Ajoute le score de la fusion des 2 cases
            self.score += self.liste[self.yTile][self.xTile-1]*2
            self.liste[self.yTile][self.xTile-1] = self.liste[self.yTile][self.xTile]*2
            self.liste[self.yTile][self.xTile] = 0
            self.xTile -= 1
        elif (direction == Direction.RIGHT) and self.xTile >= 0 and self.xTile < 3 and self.liste[self.yTile][self.xTile+1] == self.liste[self.yTile][self.xTile]:
            #Ajoute le score de la fusion des 2 cases
            self.score += self.liste[self.yTile][self.xTile+1]*2
            self.liste[self.yTile][self.xTile+1] = self.liste[self.yTile][self.xTile]*2
            self.liste[self.yTile][self.xTile] = 0
            self.xTile += 1
        self.window.repaint()
        self.timerCheckEndTile.start(550)

    def play(self):
        """
            Lance la partie
        """
        ret = random.random()
        #Place un 2 si ret <= 0.70 sinon si ret <= 0.90 place un 4 sinon place un 8
        if (ret <= 0.70):
            self.valueTile = 2
        elif (ret <= 0.90):
            self.valueTile = 4
        else:
            self.valueTile = 8

        #Initialise les timers
        self.timerCheckEndTile = QTimer()
        self.timerCheckEndTile.setSingleShot(True)
        self.timer = QTimer()

        #Chaque fois que le timer est à 0 on descend de 1 la case en mouvement
        self.timer.timeout.connect(self.downTile)
        #Chaque fois que le timerCheckEndTile est à 0 on vérifie si la case en mouvement a atteint la fin de la grille ou qu'elle soit juste au-dessus d'une autre case
        self.timerCheckEndTile.timeout.connect(self.endMoveTile)
        #On lance le timer
        self.timer.start(750)
        #Fait apparaître une case
        self.spawnRandom()
