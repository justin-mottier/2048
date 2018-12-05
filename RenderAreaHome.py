#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class RenderAreaHome(QWidget):
    def __init__(self , parent=None):
        super(RenderAreaHome,self).__init__(parent)

    def drawFigure(self,painter):
        """
            Affiche le logo au milieu de la fenêtre
            :param painter: painter
            :type painter: QPainter
        """
        logo = QPixmap("home/logo.png")
        logo = logo.scaledToWidth(logo.width()/2.3) #resize du logo
        painter.drawPixmap(self.geometry().width()/2-logo.width()/2, self.geometry().height()/2-logo.height()/2-170,logo.width(),logo.height(),logo)

    def paintEvent(self, event):
        """
            Crée le QPainter et affiche le logo
            :param event: événement
            :type event: event
        """
        painter = QPainter(self)
        self.drawFigure(painter)
