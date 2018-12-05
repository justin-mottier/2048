from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Highscores(QDialog):
	def __init__(self, parent=None):
		super(Highscores,self).__init__(parent)
		# Création des onglets
		self.tabBar = QTabWidget()
		self.classique = QWidget()
		self.vPop = QWidget()
		self.miroir = QWidget()
		self.tetris = QWidget()
		self.tabBar.addTab(self.classique, "Classique")
		self.tabBar.addTab(self.vPop, "Versus Pop")
		self.tabBar.addTab(self.miroir, "Parallèle")
		self.tabBar.addTab(self.tetris, "Tetris")
		self.layout2 = QGridLayout()
		self.layout2.addWidget(self.tabBar,0,0,2,0)
		self.setLayout(self.layout2)
		self.tabClassiqueUI()
		self.tabVPopUI()
		self.tabMiroir()
		self.tabTetris()

		# Initialisation de la fenêtre
		self.high = QDialog()
		pt = QDesktopWidget().availableGeometry().center()
		rect = QRect(pt-QPoint(335/2,130/2),QSize(350,130))
		self.setGeometry(rect)
		self.setWindowTitle("Meilleurs scores")

	def tabClassiqueUI(self):
		"""
			Initiliase l'onglet du tableau des scores dédié au mode "Classique"
		"""
		layout = QGridLayout()
		self.classique.setLayout(layout)

		# Création du bouton "Effacer scores et initialisation de l'action quand cliqué"
		self.reset = QPushButton("Effacer scores", self)
		self.reset.clicked.connect(self.resetScoresClassique)

		# Création des labels (textes modifiables dans la fenêtre)
		self.titre = QLabel("Highscores")
		self.titre.setAlignment(Qt.AlignCenter)

		# Labels des petites images de médailles
		self.med1 = QLabel()
		self.med2 = QLabel()
		self.med3 = QLabel()
		self.med1.setPixmap(QPixmap("icon/1er_small.png"))
		self.med2.setPixmap(QPixmap("icon/2eme_small.png"))
		self.med3.setPixmap(QPixmap("icon/3eme_small.png"))
		self.med1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.med2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.med3.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		# Labels pour les noms des joueurs
		self.nom1 = QLabel()
		self.nom2 = QLabel()
		self.nom3 = QLabel()
		self.nom4 = QLabel()
		self.nom5 = QLabel()

		# Mise en liste afin de compacter le score plus tard (for)
		nLabels = [self.nom1,self.nom2,self.nom3,self.nom4,self.nom5]

		# Labels pour les scores
		self.score1 = QLabel()
		self.score2 = QLabel()
		self.score3 = QLabel()
		self.score4 = QLabel()
		self.score5 = QLabel()

		# Mise en liste afin de compacter le score plus tard (for)
		sLabels = [self.score1,self.score2,self.score3,self.score4,self.score5]

		# Affichage du bouton et des images des médailles
		layout.addWidget(self.reset,7,0,2,0)
		layout.addWidget(self.med1,2,0)
		layout.addWidget(self.med2,3,0)
		layout.addWidget(self.med3,4,0)

		# Affichage des noms et scores (ce "for" économise 11 lignes)
		for i in range(len(nLabels)) :
			layout.addWidget(nLabels[i],i+2,1)
			sLabels[i].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
			layout.addWidget(sLabels[i],i+2,3)

		# Ouverture et lecture du fichier où sont stockés les scores
		f = open("highscores.txt", 'r')
		a = f.read()
		f.close()

		# Traitement du fichier
		b = a.split("//////////")
		c = b[0].split("\n")
		tab = {1 : ["", ""], 2 : ["", ""], 3 : ["", ""], 4 : ["", ""], 5 : ["", ""]}
		for i in range(len(c)) :
			if c[i] != '' :
				tmp = c[i].split('###')
				tab[i+1] = [tmp[0], int(tmp[1])]

		# Initialisation liste vierge qui va remplir les champs
		self.noms = ["Vide 1","Vide 2","Vide 3","Vide 4","Vide 5"]
		self.scores = [0,0,0,0,0]

		# Tri des scores récupérés dans le fichier
		while len(tab) > 0 :
			c = 0
			joueur = ""
			maxScore = -1
			for i in tab.keys() :
				if tab[i][1] > maxScore :
					ind = i
					joueur = tab[i][0]
					maxScore = tab[i][1]
			for i in range(c, 5) :
				if self.noms[i] == "Vide "+str(i+1) :
					self.noms[i] = joueur
					self.scores[i] = maxScore
					tab.pop(ind)
					break
			c += 1

		# Après le tri, on affecte les noms et les scores dans le bon ordre
		for i in range(len(nLabels)) :
			nLabels[i].setText(self.noms[i])
			sLabels[i].setText(str(self.scores[i]))

	def tabVPopUI(self) :
		"""
			Initiliase l'onglet du tableau des scores dédié au mode "Versus Pop"
		"""
		layout = QGridLayout()
		self.vPop.setLayout(layout)

		# Création du bouton "Effacer scores et initialisation de l'action quand cliqué"
		self.resetVP = QPushButton("Effacer scores", self)
		self.resetVP.clicked.connect(self.resetScoresVPop)

		# Création des labels (textes modifiables dans la fenêtre)
		self.titreVP = QLabel("Highscores")
		self.titreVP.setAlignment(Qt.AlignCenter)

		# Labels des petites images de médailles
		self.med1VP = QLabel()
		self.med2VP = QLabel()
		self.med3VP = QLabel()
		self.med1VP.setPixmap(QPixmap("icon/1er_small.png"))
		self.med2VP.setPixmap(QPixmap("icon/2eme_small.png"))
		self.med3VP.setPixmap(QPixmap("icon/3eme_small.png"))
		self.med1VP.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.med2VP.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.med3VP.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		# Labels pour les noms des joueurs
		self.nom1VP = QLabel()
		self.nom2VP = QLabel()
		self.nom3VP = QLabel()
		self.nom4VP = QLabel()
		self.nom5VP = QLabel()

		# Mise en liste afin de compacter le score plus tard (for)
		nLabels = [self.nom1VP,self.nom2VP,self.nom3VP,self.nom4VP,self.nom5VP]

		# Labels pour les scores
		self.score1VP = QLabel()
		self.score2VP = QLabel()
		self.score3VP = QLabel()
		self.score4VP = QLabel()
		self.score5VP = QLabel()

		# Mise en liste afin de compacter le score plus tard (for)
		sLabels = [self.score1VP,self.score2VP,self.score3VP,self.score4VP,self.score5VP]

		# Affichage du bouton et des images des médailles
		layout.addWidget(self.resetVP,7,0,2,0)
		layout.addWidget(self.med1VP,2,0)
		layout.addWidget(self.med2VP,3,0)
		layout.addWidget(self.med3VP,4,0)

		# Affichage des noms et scores (ce "for" économise 11 lignes)
		for i in range(len(nLabels)) :
			layout.addWidget(nLabels[i],i+2,1)
			sLabels[i].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
			layout.addWidget(sLabels[i],i+2,3)

		# Ouverture et lecture du fichier où sont stockés les scores
		f = open("highscores.txt", 'r')
		a = f.read()
		f.close()

		# Traitement du fichier
		b = a.split("//////////")
		c = b[1].split("\n")
		tab = {1 : ["", ""], 2 : ["", ""], 3 : ["", ""], 4 : ["", ""], 5 : ["", ""]}
		for i in range(len(c)) :
			if c[i] != '' :
				tmp = c[i].split('###')
				tab[i+1] = [tmp[0], int(tmp[1])]

		# Initialisation liste vierge qui va remplir les champs
		self.nomsVP = ["Vide 1","Vide 2","Vide 3","Vide 4","Vide 5"]
		self.scoresVP = [0,0,0,0,0]

		# Tri des scores récupérés dans le fichier
		while len(tab) > 0 :
			c = 0
			joueur = ""
			maxScore = -1
			for i in tab.keys() :
				if tab[i][1] > maxScore :
					ind = i
					joueur = tab[i][0]
					maxScore = tab[i][1]
			for i in range(c, 5) :
				if self.nomsVP[i] == "Vide "+str(i+1) :
					self.nomsVP[i] = joueur
					self.scoresVP[i] = maxScore
					tab.pop(ind)
					break
			c += 1

		# Après le tri, on affecte les noms et les scores dans le bon ordre
		for i in range(len(nLabels)) :
			nLabels[i].setText(self.nomsVP[i])
			sLabels[i].setText(str(self.scoresVP[i]))

	def tabMiroir(self) :
		"""
			Initiliase l'onglet du tableau des scores dédié au mode "Dimension parallèle" (aussi appelé "Miroir")
		"""
		layout = QGridLayout()
		self.miroir.setLayout(layout)

		# Création du bouton "Effacer scores et initialisation de l'action quand cliqué"
		self.resetM = QPushButton("Effacer scores", self)
		self.resetM.clicked.connect(self.resetScoresMiroir)

		# Création des labels (textes modifiables dans la fenêtre)
		self.titreM = QLabel("Highscores")
		self.titreM.setAlignment(Qt.AlignCenter)

		# Labels des petites images de médailles
		self.med1M = QLabel()
		self.med2M = QLabel()
		self.med3M = QLabel()
		self.med1M.setPixmap(QPixmap("icon/1er_small.png"))
		self.med2M.setPixmap(QPixmap("icon/2eme_small.png"))
		self.med3M.setPixmap(QPixmap("icon/3eme_small.png"))
		self.med1M.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.med2M.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.med3M.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		# Labels pour les noms des joueurs
		self.nom1M = QLabel()
		self.nom2M = QLabel()
		self.nom3M = QLabel()
		self.nom4M = QLabel()
		self.nom5M = QLabel()

		# Mise en liste afin de compacter le score plus tard (for)
		nLabels = [self.nom1M,self.nom2M,self.nom3M,self.nom4M,self.nom5M]

		# Labels pour les scores
		self.score1M = QLabel()
		self.score2M = QLabel()
		self.score3M = QLabel()
		self.score4M = QLabel()
		self.score5M = QLabel()

		# Mise en liste afin de compacter le score plus tard (for)
		sLabels = [self.score1M,self.score2M,self.score3M,self.score4M,self.score5M]

		# Affichage du bouton et des images des médailles
		layout.addWidget(self.resetM,7,0,2,0)
		layout.addWidget(self.med1M,2,0)
		layout.addWidget(self.med2M,3,0)
		layout.addWidget(self.med3M,4,0)

		# Affichage des noms et scores (ce "for" économise 11 lignes)
		for i in range(len(nLabels)) :
			layout.addWidget(nLabels[i],i+2,1)
			sLabels[i].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
			layout.addWidget(sLabels[i],i+2,3)

		# Ouverture et lecture du fichier où sont stockés les scores
		f = open("highscores.txt", 'r')
		a = f.read()
		f.close()

		# Traitement du fichier
		b = a.split("//////////")
		c = b[2].split("\n")
		tab = {1 : ["", ""], 2 : ["", ""], 3 : ["", ""], 4 : ["", ""], 5 : ["", ""]}
		for i in range(len(c)) :
			if c[i] != '' :
				tmp = c[i].split('###')
				tab[i+1] = [tmp[0], int(tmp[1])]

		# Initialisation liste vierge qui va remplir les champs
		self.nomsM = ["Vide 1","Vide 2","Vide 3","Vide 4","Vide 5"]
		self.scoresM = [0,0,0,0,0]

		# Tri des scores récupérés dans le fichier
		while len(tab) > 0 :
			c = 0
			joueur = ""
			maxScore = -1
			for i in tab.keys() :
				if tab[i][1] > maxScore :
					ind = i
					joueur = tab[i][0]
					maxScore = tab[i][1]
			for i in range(c, 5) :
				if self.nomsM[i] == "Vide "+str(i+1) :
					self.nomsM[i] = joueur
					self.scoresM[i] = maxScore
					tab.pop(ind)
					break
			c += 1

		# Après le tri, on affecte les noms et les scores dans le bon ordre
		for i in range(len(nLabels)) :
			nLabels[i].setText(self.nomsM[i])
			sLabels[i].setText(str(self.scoresM[i]))

	def tabTetris(self) :
		"""
			Initiliase l'onglet du tableau des scores dédié au mode "Tetris"
		"""
		layout = QGridLayout()
		self.tetris.setLayout(layout)

		# Création du bouton "Effacer scores et initialisation de l'action quand cliqué"
		self.resetT = QPushButton("Effacer scores", self)
		self.resetT.clicked.connect(self.resetScoresTetris)

		# Création des labels (textes modifiables dans la fenêtre)
		self.titreT = QLabel("Highscores")
		self.titreT.setAlignment(Qt.AlignCenter)

		# Labels des petites images de médailles
		self.med1T = QLabel()
		self.med2T = QLabel()
		self.med3T = QLabel()
		self.med1T.setPixmap(QPixmap("icon/1er_small.png"))
		self.med2T.setPixmap(QPixmap("icon/2eme_small.png"))
		self.med3T.setPixmap(QPixmap("icon/3eme_small.png"))
		self.med1T.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.med2T.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.med3T.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		# Labels pour les noms des joueurs
		self.nom1T = QLabel()
		self.nom2T = QLabel()
		self.nom3T = QLabel()
		self.nom4T = QLabel()
		self.nom5T = QLabel()

		# Mise en liste afin de compacter le score plus tard (for)
		nLabels = [self.nom1T,self.nom2T,self.nom3T,self.nom4T,self.nom5T]

		# Labels pour les scores
		self.score1T = QLabel()
		self.score2T = QLabel()
		self.score3T = QLabel()
		self.score4T = QLabel()
		self.score5T = QLabel()

		# Mise en liste afin de compacter le score plus tard (for)
		sLabels = [self.score1T,self.score2T,self.score3T,self.score4T,self.score5T]

		# Affichage du bouton et des images des médailles
		layout.addWidget(self.resetT,7,0,2,0)
		layout.addWidget(self.med1T,2,0)
		layout.addWidget(self.med2T,3,0)
		layout.addWidget(self.med3T,4,0)

		# Affichage des noms et scores (ce "for" économise 11 lignes)
		for i in range(len(nLabels)) :
			layout.addWidget(nLabels[i],i+2,1)
			sLabels[i].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
			layout.addWidget(sLabels[i],i+2,3)

		# Ouverture et lecture du fichier où sont stockés les scores
		f = open("highscores.txt", 'r')
		a = f.read()
		f.close()

		# Traitement du fichier
		b = a.split("//////////")
		c = b[3].split("\n")
		tab = {1 : ["", ""], 2 : ["", ""], 3 : ["", ""], 4 : ["", ""], 5 : ["", ""]}
		for i in range(len(c)) :
			if c[i] != '' :
				tmp = c[i].split('###')
				tab[i+1] = [tmp[0], int(tmp[1])]

		# Initialisation liste vierge qui va remplir les champs
		self.nomsT = ["Vide 1","Vide 2","Vide 3","Vide 4","Vide 5"]
		self.scoresT = [0,0,0,0,0]

		# Tri des scores récupérés dans le fichier
		while len(tab) > 0 :
			c = 0
			joueur = ""
			maxScore = -1
			for i in tab.keys() :
				if tab[i][1] > maxScore :
					ind = i
					joueur = tab[i][0]
					maxScore = tab[i][1]
			for i in range(c, 5) :
				if self.nomsT[i] == "Vide "+str(i+1) :
					self.nomsT[i] = joueur
					self.scoresT[i] = maxScore
					tab.pop(ind)
					break
			c += 1

		# Après le tri, on affecte les noms et les scores dans le bon ordre
		for i in range(len(nLabels)) :
			nLabels[i].setText(self.nomsT[i])
			sLabels[i].setText(str(self.scoresT[i]))

	def resetScoresClassique(self) :
		"""
			Cette fonction se lance lors de la pression du bouton "Effacer scores" dans l'onglet "Classique".
			Elle remplace tous les scores du mode "Classique" par des entrées blanches.
		"""
		a = open('highscores.txt', 'r')
		b = a.read()
		a.close()

		c = b.split("//////////")
		d = c[1] + "//////////" + c[2] + "//////////" + c[3]

		f = open('highscores.txt', 'w')
		for i in range(0,5) :
			if i != 4 :
				f.write("Place "+str(i+1)+"###0\n")
			else :
				f.write("Place "+str(i+1)+"###0//////////")
				f.write(d)
		f.close()
		self.close()

	def resetScoresVPop(self) :
		"""
			Cette fonction se lance lors de la pression du bouton "Effacer scores" dans l'onglet "Versus Pop".
			Elle remplace tous les scores du mode "Versus Pop" par des entrées blanches.
		"""
		a = open('highscores.txt', 'r')
		b = a.read()
		a.close()

		c = b.split("//////////")
		d = c[0] + "//////////"
		e = "//////////" + c[2] + "//////////" + c[3]

		f = open('highscores.txt', 'w')
		f.write(d)
		for i in range(0,5) :
			if i != 4 :
				f.write("Place "+str(i+1)+"###0\n")
			else :
				f.write("Place "+str(i+1)+"###0")
		f.write(e)
		f.close()
		self.close()

	def resetScoresMiroir(self) :
		"""
			Cette fonction se lance lors de la pression du bouton "Effacer scores" dans l'onglet "Dimension parallèle".
			Elle remplace tous les scores du mode "Dimension parallèle" par des entrées blanches.
		"""
		a = open('highscores.txt', 'r')
		b = a.read()
		a.close()

		c = b.split("//////////")
		d = c[0] + "//////////" + c[1] + "//////////"
		e = "//////////" + c[3]

		f = open('highscores.txt', 'w')
		f.write(d)
		for i in range(0,5) :
			if i != 4 :
				f.write("Place "+str(i+1)+"###0\n")
			else :
				f.write("Place "+str(i+1)+"###0")
		f.write(e)
		f.close()
		self.close()

	def resetScoresTetris(self) :
		"""
			Cette fonction se lance lors de la pression du bouton "Effacer scores" dans l'onglet "Tetris".
			Elle remplace tous les scores du mode "Tetris" par des entrées blanches.
		"""
		a = open('highscores.txt', 'r')
		b = a.read()
		a.close()

		c = b.split("//////////")
		d = c[0] + "//////////" + c[1] + "//////////" + c[2] + "//////////"

		f = open('highscores.txt', 'w')
		f.write(d)
		for i in range(0,5) :
			if i != 4 :
				f.write("Place "+str(i+1)+"###0\n")
			else :
				f.write("Place "+str(i+1)+"###0")
		f.close()
		self.close()

	def testScoreSuffisant(self, score, mode) :
		"""
			Fonction lancée en fin de partie.
			Vérifie si le score effectué est suffisant pour entrer dans le tableau des meilleurs scores du mode de jeu correspondant.
			:param score : Score du joueur
			:type score : int
			:param mode : Mode de jeu actuel
			:type mode : String
			:rtype : boolean
		"""
		if mode == "" :
			return score > self.scores[self.indScoreMini(mode)]
		elif mode == "vsIa" :
			return score > self.scoresVP[self.indScoreMini(mode)]
		elif mode == "miroir" :
			return score > self.scoresM[self.indScoreMini(mode)]
		elif mode == "tetris" :
			return score > self.scoresT[self.indScoreMini(mode)]

	def ajouterScoreClassique(self, nom, score) :
		"""
			Fonction permettant d'ajouter un score dans le tableau des scores du mode "Classique".
			Le score le plus petit est écrasé.
			:param nom : Nom du joueur
			:type nom : String
			:param score : Score du joueur
			:type score : int
		"""
		mini = self.indScoreMini("")
		if self.scores[mini] < score :
			self.noms[mini] = nom
			self.scores[mini] = score

		a = open('highscores.txt', 'r')
		b = a.read()
		a.close()

		c = b.split("//////////")
		d = c[1] + "//////////" + c[2] + "//////////" + c[3]

		f = open('highscores.txt', 'w')
		for i in range(len(self.noms)) :
			if i != 4 :
				f.write(self.noms[i]+"###"+str(self.scores[i])+"\n")
			else :
				f.write(self.noms[i]+"###"+str(self.scores[i])+"//////////")
				f.write(d)
		f.close()
		self.close()

	def ajouterScoreVPop(self, nom, score) :
		"""
			Fonction permettant d'ajouter un score dans le tableau des scores du mode "Versus Pop".
			Le score le plus petit est écrasé.
			:param nom : Nom du joueur
			:type nom : String
			:param score : Score du joueur
			:type score : int
		"""
		mini = self.indScoreMini("vsIa")
		if self.scoresVP[mini] < score :
			self.nomsVP[mini] = nom
			self.scoresVP[mini] = score

		a = open('highscores.txt', 'r')
		b = a.read()
		a.close()

		c = b.split("//////////")
		d = c[0] + "//////////"
		e = c[2] + "//////////" + c[3]

		f = open('highscores.txt', 'w')
		f.write(d)
		for i in range(len(self.nomsVP)) :
			if i != 4 :
				f.write(self.nomsVP[i]+"###"+str(self.scoresVP[i])+"\n")
			else :
				f.write(self.nomsVP[i]+"###"+str(self.scoresVP[i])+"//////////")
		f.write(e)
		f.close()
		self.close()

	def ajouterScoreMiroir(self, nom, score) :
		"""
			Fonction permettant d'ajouter un score dans le tableau des scores du mode "Dimension parallèle".
			Le score le plus petit est écrasé.
			:param nom : Nom du joueur
			:type nom : String
			:param score : Score du joueur
			:type score : int
		"""
		mini = self.indScoreMini("miroir")
		if self.scoresM[mini] < score :
			self.nomsM[mini] = nom
			self.scoresM[mini] = score

		a = open('highscores.txt', 'r')
		b = a.read()
		a.close()

		c = b.split("//////////")
		d = c[0] + "//////////" + c[1] + "//////////"
		e = c[3]

		f = open('highscores.txt', 'w')
		f.write(d)
		for i in range(len(self.nomsM)) :
			if i != 4 :
				f.write(self.nomsM[i]+"###"+str(self.scoresM[i])+"\n")
			else :
				f.write(self.nomsM[i]+"###"+str(self.scoresM[i])+"//////////")
		f.write(e)
		f.close()
		self.close()

	def ajouterScoreTetris(self, nom, score) :
		"""
			Fonction permettant d'ajouter un score dans le tableau des scores du mode "Tetris".
			Le score le plus petit est écrasé.
			:param nom : Nom du joueur
			:type nom : String
			:param score : Score du joueur
			:type score : int
		"""
		mini = self.indScoreMini("tetris")
		if self.scoresT[mini] < score :
			self.nomsT[mini] = nom
			self.scoresT[mini] = score

		a = open('highscores.txt', 'r')
		b = a.read()
		a.close()

		c = b.split("//////////")
		d = c[0] + "//////////" + c[1] + "//////////" + c[2] + "//////////"

		f = open('highscores.txt', 'w')
		f.write(d)
		for i in range(len(self.nomsT)) :
			if i != 4 :
				f.write(self.nomsT[i]+"###"+str(self.scoresT[i])+"\n")
			else :
				f.write(self.nomsT[i]+"###"+str(self.scoresT[i]))
		f.close()
		self.close()

	def indScoreMini(self, mode) :
		"""
			Retourne l'indice du plus petit score enregistré du mode de jeu renseigné.
			:param mode : nom du mode de jeu
			:type mode : String
			:rtype : int
		"""
		if mode == "" :
			mini = self.scores[0]
			ind = 0
			for i in range(1,len(self.scores)) :
				if self.scores[i] < mini :
					mini = self.scores[i]
					ind = i
			return ind

		elif mode == "vsIa" :
			mini = self.scoresVP[0]
			ind = 0
			for i in range(1,len(self.scoresVP)) :
				if self.scoresVP[i] < mini :
					mini = self.scoresVP[i]
					ind = i
			return ind

		if mode == "miroir" :
			mini = self.scoresM[0]
			ind = 0
			for i in range(1,len(self.scoresM)) :
				if self.scoresM[i] < mini :
					mini = self.scoresM[i]
					ind = i
			return ind

		if mode == "tetris" :
			mini = self.scoresT[0]
			ind = 0
			for i in range(1,len(self.scoresT)) :
				if self.scoresT[i] < mini :
					mini = self.scoresT[i]
					ind = i
			return ind
