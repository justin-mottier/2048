#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

from Game import *
from GameTetris import *
from RenderAreaGame import *
from ButtonHome import *
from IA import *
from Highscores import *
from RenderAreaHome import *
from Direction import *
from Son import *

class Window(QMainWindow):
    def __init__(self):
        """
            Constructeur de la class
        """
        super().__init__()
        self.highscoreF = Highscores(self) #Initialise le Hightscore
        self.mode = ""
        self.initUI()

    def initUI(self):
        """
            Initialise la fenêtre de jeu avec la taille initial, le titre et les differentes implémentation dans la fenêtre
        """

        #Met en place la musique de fond
        self.playerMusic = QMediaPlayer(self)
        content = QMediaContent(QUrl.fromLocalFile("sound/ambiantSoundKevinMacLeod.wav"))
        #On met la musique de fond en boucle
        playlist = QMediaPlaylist(self)
        playlist.setPlaybackMode(QMediaPlaylist.Loop)
        playlist.addMedia(content)

        self.playerMusic.setPlaylist(playlist)
        self.playerMusic.setVolume(100)
        self.playerMusic.play()


        self.setGeometry(10, 10, 580, 580)
        self.setFixedSize(580,580)
        p = self.palette()
        p.setBrush(QPalette.Window,QBrush(QImage("draw/background.png")))
        self.setPalette(p)
        self.setWindowTitle('2048')
        self.statusBar().showMessage("")
        self.setMenuBar()
        self.setCenter()
        self.home(None)
        self.show()

    def keyPressEvent(self,event):
        """
            Initialise la fonction
            :param event: événement touche du clavier appuyée
            :type event: QKeyEvent
        """
        pass

    def home(self,event):
        """
            Mise en place du menu avec les differents boutons
            :param event: événement
            :type event: event
        """
        #Initialise l'écran du menu principal avec le logo
        ecran = RenderAreaHome()
        self.canPlay = False #Interdit l'utilisateur de jouer tant qu'il est dans le menu
        #On reset tout si l'utilisateur était en train de jouer
        if self.mode == "tetris":
            self.game.timer.stop()
            self.mode = ""
        else: self.mode = ""
        self.iaRunning = False
        self.statusBar().showMessage("")

        #Si la variable game existe et le type de la varible est Game alors on sauvegarde la partie en cours
        if(hasattr(self, 'game') and type(self.game) is Game): self.game.sauvegarder()

        playGif = ButtonHome("home/jouer.gif",self.width()/2, self.width()/3,ecran) #Creation du bouton "Jouer"
        playGif.mouseReleaseEvent = self.subHomePlay  #On ajoute une action au bouton "Jouer"

        loadGif = ButtonHome("home/charger.gif",self.width()/2, self.width()/3+(80*1),ecran)
        loadGif.mouseReleaseEvent = self.loadGame

        highscoreGif = ButtonHome("home/highscore.gif",self.width()/2, self.width()/3+(80*2),ecran)
        highscoreGif.mouseReleaseEvent = self.highscores

        quitGif = ButtonHome("home/quitter.gif",self.width()/2, self.width()/3+(80*3),ecran)
        quitGif.mouseReleaseEvent = self.quit

        self.setCentralWidget(ecran)

    def subHomePlay(self,event):
        """
            Mise en place du menu avec les differents boutons
            :param event: événement
            :type event: event
        """
        ecran = RenderAreaHome()

        classiqueGif = ButtonHome("home/classique.gif",self.width()/2, self.width()/3,ecran) #Creation du bouton "Jouer"
        classiqueGif.mouseReleaseEvent = self.newGame #On ajoute une action au bouton "Jouer"

        miroirGif = ButtonHome("home/miroir.gif",self.width()/2, self.width()/3+(70*1),ecran)
        miroirGif.mouseReleaseEvent = self.miroir

        popGif = ButtonHome("home/vsPop.gif",self.width()/2, self.width()/3+(70*2),ecran)
        popGif.mouseReleaseEvent = self.setVsIa

        tetrisGif = ButtonHome("home/tetris.gif",self.width()/2, self.width()/3+(70*3),ecran)
        tetrisGif.mouseReleaseEvent = self.tetris

        backGif = ButtonHome("home/retour.gif",self.width()/2, self.width()/3+(70*4),ecran)
        backGif.mouseReleaseEvent = self.home

        self.setCentralWidget(ecran)

    def setMenuBar(self):
        """
            Crée la bar de menu avec les differents onglets et les actions de chaque
        """
        mainMenu = self.menuBar()
        systemeMenu = mainMenu.addMenu('Système')
        jeuMenu = mainMenu.addMenu('Jeu')
        helpMenu = mainMenu.addMenu('Aide')

        newAction = QAction("&Nouvelle partie", self, icon=QIcon("icon/new_game.png"), shortcut = "Ctrl+N", statusTip = "Commencer une nouvelle partie", triggered=self.newGame)
        systemeMenu.addAction(newAction)

        highscoreAction = QAction("&Highscores", self, icon=QIcon("icon/leaderboard.png"), shortcut = "Ctrl+H", statusTip = "Voir les meilleurs scores !", triggered = self.highscores)
        systemeMenu.addAction(highscoreAction)

        backHome = QAction("&Menu principal", self, icon=QIcon("icon/home.png"), shortcut="Ctrl+M", statusTip="Retour au menu principal", triggered=self.home)
        systemeMenu.addAction(backHome)

        exitAction = QAction("&Quitter", self, icon=QIcon('icon/exit.svg'), shortcut="Ctrl+Q",statusTip="Quitter l'application", triggered=self.quit)
        systemeMenu.addAction(exitAction)

        aboutAction = QAction("&A propos de", self, icon=QIcon('icon/about.png'), shortcut="Ctrl+?",statusTip="A propos de", triggered=self.about)
        helpMenu.addAction(aboutAction)

        resetAction = QAction("&Retour en arrière", self, icon=QIcon('icon/reset.png'), shortcut="Ctrl+R",statusTip="Dernier coup joué", triggered=self.resetButton)
        jeuMenu.addAction(resetAction)

        sonAction = QAction("&Son", self, icon=QIcon('icon/sound.png'), shortcut="Ctrl+S", statusTip="Ajuster le son", triggered=lambda : Son(self,self.playerMusic))
        jeuMenu.addAction(sonAction)

    def closeEvent(self, event):
        """
            Evenement si l'utilisateur ferme la fenêtre principale
            :param event: événement
            :type event: event
        """
        #Si la variable game existe et le type de la varible est Game alors on sauvegarde la partie en cours
        if(hasattr(self, 'game') and type(self.game) is Game): self.game.sauvegarder()

    def setCenter(self):
        """
            Centre la fenêtre de jeu
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def newGame(self,event):
        """
            Crée une varibale de la class Game pour initiliser le 2048 et met en place l'affichage
        """
        #On vide le fichier save.txt
        reset = open("save.txt",'w')
        reset.write("")
        reset.close()
        if (self.mode != "tetris"):
            self.iaRunning = False
            self.game = Game(self,self.mode)
            self.setRenderArea()
        else:
            #Si la variable game existe et le type de la varible est diffèrent de Game alors on reset la partie sinon on crée une variable game avec comme type GameTetris
            if(hasattr(self, 'game') and type(self.game) is not Game): self.game.resetGame()
            else: self.game = GameTetris(self)
            self.setRenderArea()

    def loadGame(self,event):
        """
            Permet de charger la dernière partie sauvegardée pour initialiser le 2048 et conserver le score et les combos
        """
        #Si le fichier save.txt est vide on lance une nouvelle
        if (os.path.getsize("save.txt") == 0):
            mess = QMessageBox(self)
            mess.setText("Aucune sauvegarde n'a été trouvé. Lancement d'une nouvelle partie !")
            mess.setWindowTitle("Erreur")
            mess.setIcon(QMessageBox.Information)
            mess.setStandardButtons(QMessageBox.Ok)
            mess.exec_()
        save = open("save.txt",'r')
        cpt = 0
        for i in save:
            if (cpt == 8):
                self.mode = i
            cpt+=1
        if (self.mode != "tetris"):
            self.game = Game(self,self.mode)
            self.setRenderArea()
            if (self.mode == "vsIa"):
                self.vsIa = IA(self.game.liste)
        else:
            self.game = GameTetris(self)
            self.setRenderArea()
        #On met à jour l'interface graphique avec les infos du fichier
        self.renderAreaGame.score = self.game.score
        self.renderAreaGame.liste = self.game.liste
        self.renderAreaGame.combo = self.game.combo
        self.renderAreaGame.comboSteps = self.game.comboSteps
        self.renderAreaGame.repaint()

    def about(self):
        """
            Fait apparaitre une fenêtre pour les differentes information du logiciel
        """
        dialog = QMessageBox(self)
        dialog.setText("Cette application a été créée par Justin MOTTIER, Sacha FOLCKE, Pierre COSSART et Romain DUBUC, étudiants en DUT1 Informatique, groupe B-1, IUT DE LENS. \nMusique de fond : Clean Soul - Kevin MacLeod\nLangage : Python 3 et PyQt5")
        dialog.setWindowTitle("A propos de")
        dialog.setIcon(QMessageBox.Information)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.exec_()

    def quit(self,event):
        """
            Fait apparaitre une fenêtre pour savoir si l'utilisateur veut quitter le logiciel
        """
        dialog = QMessageBox(self)
        dialog.setText("Souhaitez-vous quitter l'application ?")
        dialog.setWindowTitle("Quitter")
        dialog.setIcon(QMessageBox.Question)
        button_yes = dialog.addButton("Oui",QMessageBox.YesRole)
        dialog.addButton("Non",QMessageBox.NoRole)
        dialog.setDefaultButton(button_yes)
        dialog.exec_()
        if (button_yes == dialog.clickedButton()):
            #Si la variable game existe et que son type est Game alors tu sauvegarde la partie en cours
            if (hasattr(self, 'game') and type(self.game) is Game):
                self.game.sauvegarder()
            QCoreApplication.instance().quit()

    def setRenderArea(self):
        """
            Initialise l'affichage du jeu
        """
        self.renderAreaGame = RenderAreaGame(self)
        self.canPlay = True
        self.setCentralWidget(self.renderAreaGame)


    def resetButton(self, event):
        """
            Reset du coup joué et changement de l'état du bouton
        """
        if (self.canPlay and self.mode != "tetris"): #Verifie si l'utilisateur n'est plus dans le menu
            self.game.backupMove()
            self.checkButtonState()

    def highscores(self, event):
        """
            Ouvre la fenêtre des meilleurs scores
        """
        self.highscoreF = Highscores(self)
        self.highscoreF.show()

    def setIA(self, event):
        """
            Active l'IA
            :param event: événement
            :type event: event
        """
        if (self.canPlay): #Verifie si l'utilisateur n'est plus dans le menu
            #Initialise l'IA
            self.ia = IA(self.game.liste)
            #Tant que le bot n'a pas perdu ou gagné et qu'il est toujours activé
            while not (self.game.isWin() or self.game.isLose()) and self.iaRunning:
                QCoreApplication.processEvents()
                self.ia.liste = self.game.liste
                moves = self.ia.play()
                if(self.game.move(moves[0])):
                    self.game.spawnRandom()
                if(self.game.move(moves[1])):
                    self.game.spawnRandom()
                if(self.game.move(moves[2])):
                    self.game.spawnRandom()

    def setVsIa(self, event):
        """
            Crée une game en mode contre l'IA
            :param event: événement
            :type event: event
        """
        self.mode = "vsIa"
        self.newGame(None)
        self.vsIa = IA(self.game.liste)

    def miroir(self, event):
        """
            Crée une game en mode miroir
            :param event: événement
            :type event: event
        """
        self.mode = "miroir"
        self.newGame(None)

    def tetris(self, event):
        """
            Crée une game en mode tetris
            :param event: événement
            :type event: event
        """
        self.mode = "tetris"
        self.newGame(None)
