#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ButtonHome(QLabel):
    def __init__(self,movie,x,y,parent=None):
        QLabel.__init__(self, parent)
        self.movie = movie
        self.x = x
        self.y = y
        self.initUI()

    def initUI(self):
        """
            Initialisation du bouton avec comme image (movie) à la position (x,y)
        """
        playGif = QMovie(self.movie)
        playGif.setCacheMode(QMovie.CacheAll)
        playGif.start()
        self.move(self.x-playGif.currentImage().size().width()/2, self.y)
        self.setMovie(playGif)
