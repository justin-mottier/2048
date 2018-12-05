#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()

    def initUI(self):
        self.setStyle(QStyleFactory.create('fusion'))
        p = self.palette();
        p.setColor(QPalette.Button, QColor(53,53,53))
        p.setColor(QPalette.Highlight, QColor(142,45,197))
        p.setColor(QPalette.ButtonText, QColor(255,255,255))
        p.setColor(QPalette.WindowText, QColor(255,255,255))
        p.setColor(QPalette.Window, QColor(53,53,53))
        self.setPalette(p)
