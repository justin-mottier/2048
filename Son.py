#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Son(QDialog):

    def __init__(self,parent = None,sound = None):
        """
            Constructeur de la classe (initialisation des variables)

            :param sound: pointeur vers la variable (self.playerMusic) de la classe Window
            :type sound: QMediaPlayer
        """
        QDialog.__init__(self,parent)
        self.sound = sound
        self.value = self.sound.volume()
        self.initUI()


    def initUI(self):
        """
            Initialisation d'une fenêtre pour ajuster le volume de la musique de fond
        """
        self.setWindowTitle("Son")

        self.dial = QDial()
        self.dial.setNotchesVisible(True)
        self.dial.setRange(0,100)
        self.dial.setValue(self.value)
        self.spinbox = QSpinBox()
        self.spinbox.setRange(0,100)
        self.spinbox.setValue(self.value)
        self.button = QPushButton("&Ok")

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.dial)
        layout.addWidget(self.spinbox)
        layout.addWidget(self.button)

        self.dial.valueChanged.connect(self.spinbox.setValue)
        self.dial.valueChanged.connect(self.changeVolume)
        self.button.pressed.connect(self.accept)
        self.spinbox.valueChanged.connect(self.dial.setValue)
        self.exec_()

    def accept(self):
        """
            Ferme la fenêtre
        """
        self.close()

    def changeVolume(self):
        """
            Change le volume directement
        """
        self.sound.setVolume(self.spinbox.value())
