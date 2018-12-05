#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from Window import *
from Application import *

app = Application([])
app.setWindowIcon(QIcon("planets/sun.png")) #Ajout de l'icone sur la fenêtre
win = Window()
app.exec_()
