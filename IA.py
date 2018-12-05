from math import *
from random import *
from copy import *
from Direction import *

class IA():

    def __init__(self,liste):
        """
        Constructeur de la classe, prend en paramètre la liste qui correspond à la grille du 2048
        Initialise également la liste de Direction qui servira dans play() et playAgainst()
        :param liste: grille du 2048
        :type liste: int[][]
        """
        self.liste = liste
        self.dir = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT] #Tableau des directions

    def play(self):
        """
        Simule toutes les matrices possibles sur 3 déplacements, ainsi que leur valeur
        Retourne les 3 déplacements à faire pour obtenir le meilleur coup.
        :param return: tableau des 3 directions à prendre
        :rtype: Direction[]
        """
        bestScore = -inf #init du meilleur score
        nonOpti= False #init du booléen
        for i in range(4): #p=1
            for j in range(4): #p=2
                for k in range(4): #p=3
                        grille = deepcopy(self.liste)
                        moved = self.move(grille, self.dir[i])
                        value = self.moveValue(grille) #Valeur de la grille
                        moved = moved or self.move(grille, self.dir[j])
                        value = value + self.moveValue(grille) #Valeur de la grille
                        moved = moved or self.move(grille, self.dir[k]) #True si la grille est différente de la liste
                        value = value + self.moveValue(grille) #Valeur de la grille
                        value = value/3

                        if self.maxCoin(grille) and (value > bestScore or nonOpti) and moved: #Si le nombre max est dans un coin et si la valeur est supérieure au meilleur score ou que le booléen est vraie et que la grille est différente de la grille de base
                            indexI = i
                            indexJ = j
                            indexK = k
                            bestScore = value
                            nonOpti = False
                        elif bestScore == -inf and value > bestScore and moved: #Si aucun move opti n'a été trouvé on prend juste le meilleur
                            indexI = i
                            indexJ = j
                            indexK = k
                            bestScore = value
                            nonOpti = True
        return(self.dir[indexI], self.dir[indexJ], self.dir[indexK]) #on retourne les directions à prendre

    def playAgainst(self):
        """
        Idem que play mais renvoie le pire move sur 1 de profondeur
        :param return: Pire direction
        :rtype: Direction
        """
        worstScore = inf
        nonOpti = False
        for k in range(4):
            grille = deepcopy(self.liste)
            self.move(grille, self.dir[k])
            value = self.moveValue(grille)
            if not self.maxCoin(grille) and (value < worstScore or nonOpti):
                worstScore = value
                indexK = k
                nonOpti = False
            elif worstScore == inf and value < worstScore:
                worstScore = value
                indexK = k
                nonOpti = True
        return self.dir[indexK]

    def move(self, grille, direction):
        """
        Déplace les nombres dans la direction choisie et retourne True si un mouvement a été fait
        :param grille: grille de 2048
        :param direction: direction à prendre
        :type grille: int[][]
        :type direction: Direction
        :param return: vrai si un mouvement a été fait
        :rtype: bool
        """
        ret = False
        modif = True
        if (direction == Direction.UP):
            while modif == True:
                modif = False
                for i in range(1,len(grille)):
                    for j in range(len(grille[i])):
                        if (grille[i][j] != 0 and (grille[i][j] == grille[i-1][j] or grille[i-1][j] == 0) and grille[i][j] >= 0):
                            if (grille[i][j] == grille[i-1][j] and grille[i][j]>0):
                                grille[i-1][j] = grille[i-1][j]*(-2)
                                grille[i][j] = 0
                            else:
                                grille[i-1][j] = grille[i][j]
                                grille[i][j] = 0
                            ret = True
                            modif = True
        elif (direction == Direction.RIGHT):
            while modif == True:
                modif = False
                for i in range(len(grille)):
                    for j in range(len(grille[i])-2,-1,-1):
                        if (grille[i][j] != 0 and (grille[i][j] == grille[i][j+1] or grille[i][j+1] == 0) and grille[i][j] >= 0):
                            if (grille[i][j] == grille[i][j+1] and grille[i][j]>0):
                                grille[i][j+1] = grille[i][j+1]*(-2)
                                grille[i][j] = 0
                            else:
                                grille[i][j+1] = grille[i][j]
                                grille[i][j] = 0
                            ret = True
                            modif = True
        elif (direction == Direction.LEFT):
            while modif == True:
                modif = False
                for i in range(len(grille)):
                    for j in range(1,len(grille[i])):
                        if (grille[i][j] != 0 and (grille[i][j] == grille[i][j-1] or grille[i][j-1] == 0) and grille[i][j] >= 0):
                            if (grille[i][j] == grille[i][j-1] and grille[i][j] > 0):
                                grille[i][j-1] = grille[i][j-1]*(-2)
                                grille[i][j] = 0
                            elif (grille[i][j] != grille[i][j-1]):
                                grille[i][j-1] = grille[i][j]
                                grille[i][j] = 0
                            ret = True
                            modif = True
        elif (direction == Direction.DOWN):
            while modif == True:
                modif = False
                for i in range(len(grille)-2,-1,-1):
                    for j in range(len(grille[i])):
                        if (grille[i][j] != 0 and (grille[i][j] == grille[i+1][j] or grille[i+1][j] == 0) and grille[i][j] >= 0):
                            if (grille[i][j] == grille[i+1][j] and grille[i][j] > 0):
                                grille[i+1][j] = grille[i+1][j]*(-2)
                                grille[i][j] = 0
                            else:
                                grille[i+1][j] = grille[i][j]
                                grille[i][j] = 0
                            ret = True
                            modif = True

        for i in range(len(grille)):
            for j in range(len(grille[i])):
                if (grille[i][j]<0):
                    grille[i][j]=grille[i][j]*(-1)
        return ret

    def moveValue(self, grille):
        """
        Evalue la valeur de la grille en fonction de sa position dans celle-ci et de sa position relative aux autres nombres
        :param grille: grille de 2048
        :type grille: int[][]
        :param return: valeur de grille
        :rtype: int
        """
        valeurs = {0:2000, 2:2, 4:4, 8:8, 16:16, 32:32, 64:64, 128:128, 256:512, 512:1024, 1024:2048, 2048:1000000}
        val = 0
        for i in range(len(grille)):
            for j in range(len(grille[0])):
                val += pow(valeurs[grille[i][j]], 3)

                if i == 0 and j == 0: #Coin Haut-Gauche
                    val += pow(valeurs[grille[i][j]], 4) #On ajoute la valeur ^14
                    if grille[i][j] == grille[i+1][j] or grille[i][j] == grille[i][j+1]: #si il est égal à un de ses voisins
                        val += pow(valeurs[grille[i][j]], 3) #On ajoute la valeur ^50
                    val -= pow(fabs(grille[i][j]-grille[i+1][j]), 2) + pow(fabs(grille[i][j]-grille[i][j+1]), 2) #Et on soustrait la valeur absolue de sa différence avec ses voisins ^10
                elif i == 0 and j == len(grille[0])-1: #Coin Haut-Droite
                    val += pow(valeurs[grille[i][j]], 4)
                    if grille[i][j] == grille[i+1][j] or grille[i][j] == grille[i][j-1]:
                        val += pow(valeurs[grille[i][j]], 3)
                    val -= pow(fabs(grille[i][j]-grille[i+1][j]), 2) + pow(fabs(grille[i][j]-grille[i][j-1]), 2)
                elif i == len(grille)-1 and j == len(grille[0])-1: #Coin Bas-Droite
                    val += pow(valeurs[grille[i][j]], 4)
                    if grille[i][j] == grille[i-1][j] or grille[i][j] == grille[i][j-1]:
                        val += pow(valeurs[grille[i][j]], 3)
                    val -= pow(fabs(grille[i][j]-grille[i-1][j]), 2) + pow(fabs(grille[i][j]-grille[i][j-1]), 2)
                elif i == len(grille)-1 and j == 0: #Coin Bas-Gauche
                    val += pow(valeurs[grille[i][j]], 4)
                    if grille[i][j] == grille[i-1][j] or grille[i][j] == grille[i][j+1]:
                        val += pow(valeurs[grille[i][j]], 3)
                    val -= pow(fabs(grille[i][j]-grille[i-1][j]), 2) + pow(fabs(grille[i][j]-grille[i][j+1]), 2)
                elif i == 0: #Ligne Haut
                    val += pow(valeurs[grille[i][j]], 4)
                    if grille[i][j] == grille[i+1][j] or grille[i][j] == grille[i][j+1] or grille[i][j] == grille[i][j-1]:
                        val += pow(valeurs[grille[i][j]], 3)
                    val -= pow(fabs(grille[i][j]-grille[i+1][j]), 2) + pow(fabs(grille[i][j]-grille[i][j+1]), 2) + pow(fabs(grille[i][j]-grille[i][j-1]), 2)
                elif j == 0: #Ligne Gauche
                    val += pow(valeurs[grille[i][j]], 4)
                    if grille[i][j] == grille[i+1][j] or grille[i][j] == grille[i][j+1] or grille[i][j] == grille[i-1][j]:
                        val += pow(valeurs[grille[i][j]], 3)
                    val -= pow(fabs(grille[i][j]-grille[i+1][j]), 2) + pow(fabs(grille[i][j]-grille[i][j+1]), 2) + pow(fabs(grille[i][j]-grille[i-1][j]), 2)
                elif i == len(grille)-1: #Ligne Bas
                    val += pow(valeurs[grille[i][j]], 4)
                    if grille[i][j] == grille[i-1][j] or grille[i][j] == grille[i][j+1] or grille[i][j] == grille[i][j-1]:
                        val += pow(valeurs[grille[i][j]], 3)
                    val -= pow(fabs(grille[i][j]-grille[i-1][j]), 2) + pow(fabs(grille[i][j]-grille[i][j+1]), 2) + pow(fabs(grille[i][j]-grille[i][j-1]), 2)
                elif j == len(grille[0])-1: #Ligne Droite
                    val += pow(valeurs[grille[i][j]], 4)
                    if grille[i][j] == grille[i+1][j] or grille[i][j] == grille[i-1][j] or grille[i][j] == grille[i][j-1]:
                        val += pow(valeurs[grille[i][j]], 3)
                    val -= pow(fabs(grille[i][j]-grille[i+1][j]), 2) + pow(fabs(grille[i][j]-grille[i-1][j]), 2) + pow(fabs(grille[i][j]-grille[i][j-1]), 2)
                else: #A l'intérieur
                    val += valeurs[grille[i][j]]
                    if grille[i][j] == grille[i+1][j] or grille[i][j] == grille[i-1][j] or grille[i][j] == grille[i][j+1] or grille[i][j] == grille[i][j-1]:
                        val += pow(valeurs[grille[i][j]], 3)
                    val -= pow(fabs(grille[i][j]-grille[i+1][j]), 2) + pow(fabs(grille[i][j]-grille[i][j+1]), 2) + pow(fabs(grille[i][j]-grille[i][j-1]), 2) + pow(fabs(grille[i][j]-grille[i-1][j]), 2)
        return val

    def maxCoin(self, grille):
        """
        Retourne True si le nombre maximum est dans un coin
        :param grille: grille de 2048
        :type grille: int[][]
        :param return: vrai si le max est dans un coin
        :rtype: bool
        """
        max = -inf
        for i in range(4):
            for j in range(4):
                if grille[i][j] > max:
                    max = grille[i][j]
                    iI = i
                    iJ = j
        couple = (iI, iJ)
        return couple in [(0, 0), (0, 3), (3, 0), (3, 3)] #True si les coordonnées du max sont dans un coin
