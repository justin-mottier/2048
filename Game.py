#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from time import *
import copy
import os
from Direction import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

class Game():
    def __init__(self, window, mode):
        """
            Constructeur de la classe (initialisation des variables)

            :param window: pointeur vers la classe Window
            :param mode: mode de jeu
            :type window: Window
            :type mode: String
        """
        self.window = window
        self.score = 0;
        self.coup = 0;
        self.mode = mode

        #On desactive le bot pour être sûr
        self.iaRunning = False
        self.window.iaRunning = False
        self.window.keyPressEvent = self.keyPressEvent

        #Direction
        self.dir = [Direction.RIGHT,Direction.UP,Direction.LEFT,Direction.DOWN]
        self.dirMiroir = [Direction.LEFT,Direction.DOWN,Direction.RIGHT,Direction.UP]

        #Combo
        self.combo = 0;
        self.comboSteps = 0;
        self.comboLastFailed = False;

        #Initialisation des listes de jeu
        self.liste = self.initList()
        self.listeBackup = copy.deepcopy(self.liste)

    def initList(self):
        """
            Initialise la grille de jeu (4x4) remplie de 0 et place deux case 2 (90% de chance) ou 4 (10% de chance) aléatoirement dans la grille.
            Initialise la partie avec les données de la partie sauvegardée si le joueur choisie de la charger.

            :return: grille de jeu
            :rtype: liste d'entier
        """
        #si le fichier save.txt ne contient pas de sauvegarde on crée une liste vide sinon on charge la sauvegarde
        if (os.path.getsize("save.txt") == 0):
            liste = []
            for i in range(4):
                tmp= []
                for j in range(4):
                    tmp.append(0)
                liste.append(tmp)
            ret = random.random()
            #Place un 2 si ret <= 0.90 sinon place un 4
            if (ret <= 0.90):
                liste[random.randint(0,3)][random.randint(0,3)] = 2
            else:
                liste[random.randint(0,3)][random.randint(0,3)] = 4
            ret = random.random()
            randx = random.randint(0,3)
            randy = random.randint(0,3)
            #Verifie si les coordonnées de la deuxieme case n'est pas égale à la première
            while (liste[randx][randy] != 0):
                randx = random.randint(0,3)
                randy = random.randint(0,3)
            if (ret <= 0.90):
                liste[randx][randy] = 2
            else:
                liste[randx][randy] = 4
        else :
            save = open("save.txt",'r')
            liste = []
            cpt = 0
            #Initialise toutes les variables de la partie.
            for i in save:
                if (cpt == 4):
                    self.score += int(i)
                elif (cpt == 5):
                    self.combo += int(i)
                elif (cpt == 6):
                    self.comboSteps += int(i)
                elif (cpt == 7):
                    self.coup += int(i)
                elif (cpt == 8):
                    self.mode = str(i)
                else:
                    liste.append(eval(i))
                cpt += 1
            save.close()
            #Supprime la sauvegarde du fichier.
            reset = open("save.txt",'w')
            reset.write("")
            reset.close()
            self.window.repaint()
        return liste

    def keyPressEvent(self,event):
        """
            Récupère la touche pressée du clavier et fait l'action correspondant à la touche pressée

            :param event: événement touche du clavier appuyée
            :type event: QKeyEvent
        """
        if (self.window.canPlay): #Verifie si l'utilisateur peut jouer
            input = False
            #Les differentes action par rapport à la touche pressée
            if(event.key() == Qt.Key_Up):
                self.window.statusBar().showMessage("Up")
                if (self.move(Direction.UP)): #La fonction bouge toute la matrice vers le haut et si il y a des modifications alors on fait apparaitre un 2 ou 4 aléatoirement
                    self.spawnRandom()
                    input = True
                    self.coup += 1
            elif(event.key() == Qt.Key_Right):
                self.window.statusBar().showMessage("Right")
                if (self.move(Direction.RIGHT)):
                    self.spawnRandom()
                    input = True
                    self.coup += 1
            elif(event.key() == Qt.Key_Left):
                self.window.statusBar().showMessage("Left")
                if (self.move(Direction.LEFT)):
                    self.spawnRandom()
                    input = True
                    self.coup += 1
            elif(event.key() == Qt.Key_Down):
                self.window.statusBar().showMessage("Down")
                if (self.move(Direction.DOWN)):
                    self.spawnRandom()
                    input = True
                    self.coup += 1

            #Si le mode de jeu est "Contre pop" et l'utilisateur à jouer un coup
            if (self.mode == "vsIa" and input):
                #On donne la grille actuelle au bot
                self.window.vsIa.liste = self.liste
                #Le bot joue son coup
                move = self.window.vsIa.playAgainst()
                if(self.move(move)):
                    self.spawnRandom()

            #Teste si la partie est gagnée si oui on fait apparaitre la fenêtre sinon on teste si la grille est pleine si oui on fait apparaitre la fenêtre
            self.isWin()
            self.isLose()

            #Sauvegarde la partie tout les 10 coups
            if (self.coup % 10 == 0): self.sauvegarder()

    def spawnRandom(self):
        """
            Place une case 2 (90% de chance) ou 4 (10% de chance) aléatoirement dans la grille
        """
        sleep(0.03)
        ret = random.random()
        randx = random.randint(0,3)
        randy = random.randint(0,3)
        #Verifie si les coordonnées de la case n'est pas égale à une case de la grille
        while (self.liste[randx][randy] != 0):
            randx = random.randint(0,3)
            randy = random.randint(0,3)
        #Place un 2 si ret <= 0.90 sinon place un 4
        if (ret <= 0.90):
            self.liste[randx][randy] = 2
        else:
            self.liste[randx][randy] = 4
        #Met à jour l'affichage avec les nouvelles données du jeu
        self.window.renderAreaGame.score = self.score
        self.window.renderAreaGame.liste = self.liste
        self.window.renderAreaGame.combo = self.combo
        self.window.renderAreaGame.comboSteps = self.comboSteps
        self.window.repaint()

    def isLose(self):
        """
            Vérifie l'état de la partie si l'utilisateur à perdu
        """
        #Si il y a un 0 dans la grille l'utilisateur n'a pas perdu donc on sort de la fonction
        for i in self.liste:
            if (0 in i):
                return
        #Si un mouvement est possible l'utilisateur n'a pas perdu donc on sort de la fonction
        if(self.isPossible()):
            return

        effect=QSoundEffect() #Joue le son de la defaite
        effect.setSource(QUrl.fromLocalFile("sound/lose.wav"))
        effect.setVolume(0.25)
        effect.play()

        #Initialisation de la boite de dialogue
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Information)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.setWindowTitle("Perdu !")
        #Si le bot est en train de jouer on affiche pas la même phrase dans la fenêtre
        if (not self.iaRunning):
            #Affiche la fenêtre perdu version utilisateur
            dialog.setText("Vous avez perdu et votre score est de : "+str(self.score))
            dialog.exec_()

            #Teste si le score est assez grand pour rentrer dans les scores
            if (self.window.highscoreF.testScoreSuffisant(self.score, self.mode)) :
                nom = ""
                while nom == "" or len(nom) > 10 or "#" in nom or "/" in nom or nom == "Pseudo":
                    nom, okPressed = QInputDialog.getText(self.window, "Entrée dans les records !","Entrez votre nom :",QLineEdit.Normal, 'Pseudo')
                    if okPressed and nom != "" and len(nom) <= 10 and "#" not in nom and "/" not in nom and nom != "Pseudo": #Si le joueur appuie sur ok et que son pseudo est dans les regles on l'ajoute dans le highscore
                        #On ajoute le score par rapport au mode joué
                        if (self.mode == ""): self.window.highscoreF.ajouterScoreClassique(nom, self.score)
                        if (self.mode == "vsIa"): self.window.highscoreF.ajouterScoreVPop(nom, self.score)
                        if (self.mode == "miroir"):self.window.highscoreF.ajouterScoreMiroir(nom, self.score)
        else:
            #Affiche la fenêtre perdu version bot
            dialog.setText("Pop a perdu et son score est de : "+str(self.score))
            dialog.exec_()

            #Si le bot a perdu et que son score rentre dans le highscore on l'ajoute
            if (self.window.highscoreF.testScoreSuffisant(self.score, self.mode)) :
                if (self.mode == ""): self.window.highscoreF.ajouterScoreClassique("Pop", self.score)
                if (self.mode == "vsIa"): self.window.highscoreF.ajouterScoreVPop("Pop", self.score)

        #Relance une partie
        self.window.newGame(None)

    def isWin(self):
        """
            Vérifie l'état de la partie si l'utilisateur à gagné
        """
        #si il y a un 2048 dans la grille l'utilisateur gagne la partie
        for i in self.liste:
            if (2048 in i):
                effect=QSoundEffect() #Joue le son de la victoire
                effect.setSource(QUrl.fromLocalFile("sound/win.wav"))
                effect.setVolume(0.25)
                effect.play()

                dialog = QMessageBox()
                dialog.setIcon(QMessageBox.Information)
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setWindowTitle("Gagné !")
                #Si le bot est en train de jouer on affiche pas la même phrase dans la fenêtre
                if (not self.iaRunning):
                    #Affiche la fenêtre gagné version utilisateur
                    dialog.setText("Vous avez gagné avec un score de "+str(self.score))
                    dialog.exec_()

                    #Teste si le score est assez grand pour rentrer dans les scores
                    if (self.window.highscoreF.testScoreSuffisant(self.score, self.mode)) :
                        nom = ""
                        while nom == "" or len(nom) > 10 or "#" in nom or "/" in nom or nom == "Pseudo":
                            nom, okPressed = QInputDialog.getText(self.window, "Entrée dans les records !","Entrez votre nom :",QLineEdit.Normal, 'Pseudo')
                            if okPressed and nom != "" and len(nom) <= 10 and "#" not in nom and "/" not in nom and nom != "Pseudo": #Si le joueur appuie sur ok et que son pseudo est dans les regles on l'ajoute dans le highscore
                                #On ajoute le score par rapport au mode joué
                                if (self.mode == ""): self.window.highscoreF.ajouterScoreClassique(nom, self.score)
                                if (self.mode == "vsIa"): self.window.highscoreF.ajouterScoreVPop(nom, self.score)
                                if (self.mode == "miroir"):self.window.highscoreF.ajouterScoreMiroir(nom, self.score)
                else:
                    #Affiche la fenêtre gagné version bot
                    dialog.setText("Pop a gagné et son score est de : "+str(self.score))
                    dialog.exec_()

                    #Si le bot a perdu et que son score rentre dans le highscore on l'ajoute
                    if (self.window.highscoreF.testScoreSuffisant(self.score, self.mode)) :
                        if (self.mode == ""): self.window.highscoreF.ajouterScoreClassique("Pop", self.score)
                        if (self.mode == "vsIa"): self.window.highscoreF.ajouterScoreVPop("Pop", self.score)

                #Relance une partie
                self.window.newGame(None)
                return

    def backupMove(self):
        """
            Retour en arrière d'un mouvement grâce à la grille backup
        """
        #si l'utilisateur a fait plus de 50 coups et que la grille backup n'est pas égale à la grille de jeu
        if (self.coup-50 > 0 and self.liste != self.listeBackup):
            for i in range(len(self.listeBackup)):
                for j in range(len(self.listeBackup[i])):
                    self.liste[i][j] = self.listeBackup[i][j]
            self.coup -= 50
            self.window.repaint()

    def isPossible(self):
        """
            Vérifie si l'utilisateur peut encore jouer en vérifiant si deux nombres sont à côté

            :return: un mouvement est possible
            :rtype: boolean
        """
        for i in range(len(self.liste)):
            for j in range(len(self.liste[i])):
                if (i == 0 and j == 0): #Coin Haut Gauche
                    if (self.liste[i][j] == self.liste[i][j+1] or self.liste[i][j] == self.liste[i+1][j]):
                        return True
                elif (i == 0 and j == len(self.liste)-1): #Coin Haut Droite
                    if (self.liste[i][j] == self.liste[i][j-1] or self.liste[i][j] == self.liste[i+1][j]):
                        return True
                elif (i == len(self.liste)-1 and j == 0): #Coin Bas Gauche
                    if (self.liste[i][j] == self.liste[i][j+1] or self.liste[i][j] == self.liste[i-1][j]):
                        return True
                elif (i == len(self.liste)-1 and j == len(self.liste)-1): #Coin Bas Droite
                    if (self.liste[i][j] == self.liste[i][j-1] or self.liste[i][j] == self.liste[i-1][j]):
                        return True
                elif (i==0): #Ligne de Gauche
                    if (self.liste[i][j] == self.liste[i+1][j] or self.liste[i][j] == self.liste[i][j-1] or self.liste[i][j] == self.liste[i][j+1]):
                        return True
                elif (i==len(self.liste)-1): #Ligne de Droite
                    if (self.liste[i][j] == self.liste[i-1][j] or self.liste[i][j] == self.liste[i][j-1] or self.liste[i][j] == self.liste[i][j+1]):
                        return True
                elif (j == 0): #Ligne du Haut
                    if (self.liste[i][j] == self.liste[i-1][j] or self.liste[i][j] == self.liste[i+1][j] or self.liste[i][j] == self.liste[i][j+1]):
                        return True
                elif (j == len(self.liste)-1): #Ligne du Bas
                    if (self.liste[i][j] == self.liste[i-1][j] or self.liste[i][j] == self.liste[i+1][j] or self.liste[i][j] == self.liste[i][j-1]):
                        return True
                else: #Milieu de la grille
                    if (self.liste[i][j] == self.liste[i+1][j] or self.liste[i][j] == self.liste[i-1][j] or self.liste[i][j] == self.liste[i][j+1] or self.liste[i][j] == self.liste[i][j-1]):
                        return True
        return False

    def move(self,direction):
        """
            Déplace la grille vers la direction donnée

            :param direction: direction du déplacement
            :type direction: Direction
            :return: si il y a eu une modification dans la grille
            :rtype: boolean
        """
        #Récupère la grille avant le déplacement pour la mettre dans la grille backup
        self.listeBackup = copy.deepcopy(self.liste)

        #Initialise variable
        ret = False
        modif = True
        self.comboMoveOK = False

        #Si le mode de jeu est miroir on inverse la direction
        if (self.mode == "miroir"): direction = self.dirMiroir[self.dir.index(direction)]

        if (direction == Direction.UP):
            while modif == True: #Tant qu'il y a une modification dans la grille on relance
                modif = False
                for i in range(1,len(self.liste)):
                    for j in range(len(self.liste[i])):
                        #Si le nombre de la case actuelle est plus grand que 0 et que la case du dessus soit égale à la case acutelle ou qu'elle soit égale à 0
                        if (self.liste[i][j] != 0 and (self.liste[i][j] == self.liste[i-1][j] or self.liste[i-1][j] == 0) and self.liste[i][j] >= 0):
                            #Si le nombre de la case actuelle est égale à la case du dessus on les fusionne sinon on bouge la case actuelle vers le haut
                            if (self.liste[i][j] == self.liste[i-1][j] and self.liste[i][j]>0):
                                #Ajoute le score de la fusion des 2 cases
                                self.score += self.liste[i-1][j]*2*(1+self.combo)
                                self.augmenterCombo()
                                #Fusion des 2 cases et met le nombre fusionné en négatif pour qu'il ne soit pas fusionné une nouvelle fois
                                self.liste[i-1][j] = self.liste[i-1][j]*(-2)
                                self.liste[i][j] = 0
                            else:
                                self.liste[i-1][j] = self.liste[i][j]
                                self.liste[i][j] = 0
                            #Il y a une modification dans la grille
                            ret = True
                            modif = True
                #Met à jour l'affichage pour créer un effet de déplacement
                self.window.repaint()
                sleep(0.03)
        elif (direction == Direction.RIGHT):
            while modif == True:
                modif = False
                for i in range(len(self.liste)):
                    for j in range(len(self.liste[i])-2,-1,-1):
                        if (self.liste[i][j] != 0 and (self.liste[i][j] == self.liste[i][j+1] or self.liste[i][j+1] == 0) and self.liste[i][j] >= 0):
                            if (self.liste[i][j] == self.liste[i][j+1] and self.liste[i][j]>0):
                                self.score += self.liste[i][j+1]*2*(1+self.combo)
                                self.augmenterCombo()
                                self.liste[i][j+1] = self.liste[i][j+1]*(-2)
                                self.liste[i][j] = 0
                            else:
                                self.liste[i][j+1] = self.liste[i][j]
                                self.liste[i][j] = 0
                            ret = True
                            modif = True
                self.window.repaint()
                sleep(0.03)
        elif (direction == Direction.LEFT):
            while modif == True:
                modif = False
                for i in range(len(self.liste)):
                    for j in range(1,len(self.liste[i])):
                        if (self.liste[i][j] != 0 and (self.liste[i][j] == self.liste[i][j-1] or self.liste[i][j-1] == 0) and self.liste[i][j] >= 0):
                            if (self.liste[i][j] == self.liste[i][j-1] and self.liste[i][j] > 0):
                                self.score += self.liste[i][j-1]*2*(1+self.combo)
                                self.augmenterCombo()
                                self.liste[i][j-1] = self.liste[i][j-1]*(-2)
                                self.liste[i][j] = 0
                            elif (self.liste[i][j] != self.liste[i][j-1]):
                                self.liste[i][j-1] = self.liste[i][j]
                                self.liste[i][j] = 0
                            ret = True
                            modif = True
                self.window.repaint()
                sleep(0.03)
        elif (direction == Direction.DOWN):
            while modif == True:
                modif = False
                for i in range(len(self.liste)-2,-1,-1):
                    for j in range(len(self.liste[i])):
                        if (self.liste[i][j] != 0 and (self.liste[i][j] == self.liste[i+1][j] or self.liste[i+1][j] == 0) and self.liste[i][j] >= 0):
                            if (self.liste[i][j] == self.liste[i+1][j] and self.liste[i][j] > 0):
                                self.score += self.liste[i+1][j]*2*(1+self.combo)
                                self.augmenterCombo()
                                self.liste[i+1][j] = self.liste[i+1][j]*(-2)
                                self.liste[i][j] = 0
                            else:
                                self.liste[i+1][j] = self.liste[i][j]
                                self.liste[i][j] = 0
                            ret = True
                            modif = True
                self.window.repaint()
                sleep(0.03)

        #Remet tous les nombres en positifs
        for i in range(len(self.liste)):
            for j in range(len(self.liste[i])):
                if (self.liste[i][j]<0):
                    self.liste[i][j]=self.liste[i][j]*(-1)

        #Si il n'y a pas eu de fusion on remet le combo à 0
        if (self.comboMoveOK == False):
            if (self.comboLastFailed):
                self.combo = 0
                self.comboSteps = 0
            else: self.comboLastFailed = True

        return ret

    def augmenterCombo(self) :
        """
            Augmente le combo
        """
        self.comboLastFailed = False
        self.comboMoveOK = True
        if (self.combo < 3):
            if (self.comboSteps < 4):
                self.comboSteps += 1
            else:
                self.comboSteps = 0
                self.combo += 1

    def sauvegarder(self):
        """
            Sauvegarde la partie en cours dans le fichier save.
        """
        sauvegarde = open("save.txt",'w')
        #On copie toute la grille de jeu
        for i in range(len(self.liste)):
            tab = []
            for j in range(len(self.liste[i])):
                tab.append(self.liste[i][j])
            sauvegarde.write(str(tab)+'\n')
        #On copie le score
        sauvegarde.write(str(self.score)+'\n')
        #On copie le combo
        sauvegarde.write(str(self.combo)+'\n')
        #On copie le comboSteps
        sauvegarde.write(str(self.comboSteps)+'\n')
        #On copie le nombre de coup
        sauvegarde.write(str(self.coup)+'\n')
        #On copie le mode en cours
        sauvegarde.write(self.mode)
        #On ferme le fichier
        sauvegarde.close()
