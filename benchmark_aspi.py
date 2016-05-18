#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "Exemple d'utilisation"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "25.04.16"
__version__ = "0.1"
__revision__ = "25.04.16"

#----- import ---------
from tools_tp02 import readChromlCap
from corrige_tp01 import Aspirateur_KB
from corrige_tp02a import Aspirateur_PG
from corrige_tp02b import objetsStatiques, MondeSimulation
from briques import Rule, KB, ProgramGenetic, mmcUnaire, mmcBinaire, GeneratePercept
from main_tp01 import test_performance
#----------------------
from fractions import Fraction
import random

import pylab as py 
import matplotlib.pyplot as plot 
#=======================

"""
   Plusieurs conceptions d'aspirateurs
   * aleatoire
   * basé sur les règles (avec et sans apprentissage)
   * basé sur les algorithmes génétiques
   
   Les aspirateurs basés sur algos génétiques sont produits par main_simulator qui
   enregistre dans un fichier le chromosome le meilleur ainsi que les capteurs
   
   On a besoin des classes spécifiques de chaque aspirateur type 
   On va devoir étendre la classe Aspirateur_KB pour gérer l'énergie comme dans Aspirateur_PG
   
   
   On va tester 3 points de départ, pendant maximum n**2 où n est la taille du monde
   
   ATTENTION: le choix a été fait pour Aspirateur_PG (et KBE) que le reset n'avait pas
   d'effet sur l'énergie. Ce choix est discutable
"""

class Aspirateur_KBE(Aspirateur_KB):
    """ Aspirateur KBE c'est Aspirateur_KB + gestion energie 
        On redéfinit reset (code identique à Aspirateur_PG)
        On rajoute nbTours, la façon dont l'énergie est gérée (idem Aspirateur_PG)
        On redféinit getEvaluation (idem Aspirateur_PG)
    """
    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        # ajout de energie
        self.__energy = 100
        self.__alive = True
        self.reset()
        
    def reset(self):
        """ fait le reset de la classe parente + la partie spécifique """
        super().reset()
        self.vivant = True
        self.__tour = 0 
        
    @property
    def nbTours(self):
        """ permet de savoir combien de temps l'agent est resté vivant """
        return self.__tour
        
    @property
    def energie(self): return self.__energy
    @energie.setter
    def energie(self,v):
        #print("avt: {}, aprs: {}".format(self.energie,v))
        assert isinstance(v,int), "int expected found {}".format(type(v))
        self.__energy = max(0,min(100,v))
        if self.__energy == 0: self.vivant = False

    @property
    def vivant(self): return self.__alive
    @vivant.setter
    def vivant(self,v):
        if isinstance(v,bool): self.__alive = v
        
    def getDecision(self,*args,**kargs):
        self.__tour += 1
        return super().getDecision(*args,**kargs)
        
    def getEvaluation(self):
        # On renvoie l'évaluation de l'agent
        # (nombre de pièces nettoyées + 1) / ( len(self.knowledge) + 1 )
        if hasattr(self,'nettoyage') and hasattr(self,'pieces_sales'):
            if self.pieces_sales == 0: _score = 0
            else: _score = (self.nettoyage / self.pieces_sales) * 10
        else:
            raise AttributeError("'nettoyage' or 'pieces_sales' missing")

        if not self.vivant: _score -= 100 ; _rho = 0
        elif self.energie < 25: _rho = Fraction(1,2)
        elif self.energie < 50: _rho = Fraction(2,3)
        elif self.energie < 75: _rho = Fraction(3,4)
        else: _rho = 1

        return _score + _rho * self.energie / 100
    
envt = [1,0,1,2,1,0,3,2,1,0,4,0,3] # juste un monde on aurait pu faire une initialisation aléatoire
nbc = len(envt)
nbMax = nbc * 2
lpos = random.sample(range(nbc),3) # on ne garde que 3 positions

# On a utilisé main_simulator pour avoir un chromosome, on lit le fichier et les capteurs
chrom, capteurs = readChromlCap( input("Donnez le fichier où est le chromosome ? ") )
if capteurs == [] : gp = None
else: gp = GeneratePercept(capteurs, objetsStatiques)
# on regarde chrom pour décider des informations
if chrom[0] in '01' : szG = 2 ; decoder = mmcBinaire ; alphabet = '01'
else: szG = 1 ; decoder = mmcUnaire ; alphabet = 'GADR'
if gp is None: taille = len(chrom)
else: taille = gp.howMany
prog = ProgramGenetic(szG,taille,alphabet,decoder)
# on charge le chromosome dans le prog
prog.program = chrom

# utilise-t-on des pannes
panne = False
# if capteurs != []:
#     _ok = "oO0Yy"
#     _rep = input("L'aspirateur peut etre en panne [oui in {}] ? ".format(_ok))
#     panne = _rep in _ok
     
actions = "Aspirer Gauche Droite Repos".split()
aspirateurs = {}
# aspirateurs['genetique'] = Aspirateur_PG(prog, gp, capteurs)
# assert aspirateurs['genetique'].program.program == chrom, "something odd is happening"

aspirateurs['aleatoire'] = Aspirateur_KBE(0, capteurs, actions )
aspirateurs['apprenant'] = Aspirateur_KBE(.75, capteurs, actions, True)
aspirateurs['genetique_kapt_panne'] = Aspirateur_PG(prog, gp, capteurs)
aspirateurs['genetique_kapt_npanne'] = Aspirateur_PG(prog, gp, capteurs)
aspirateurs['genetique_nkapt'] = Aspirateur_PG(prog, gp)
aspirateurs['genetique_kapt_panne'].panne = True
aspirateurs['genetique_kapt_npanne'].panne = False

# for k in aspirateurs:
#     aspirateurs[k].panne = panne

stocker_eval = dict()
stocker_perf = dict()    
# création des mondes et récupérations des résultats
# on manipule une copie de l'environnement pour éviter les pbs
resultats = {}

#===============#
#  taille monde #
#===============#

for nbc in range(2,50):
    for k in aspirateurs:
        m = MondeSimulation(aspirateurs[k],1,nbc)
        
        if not hasattr(aspirateurs[k],'pieces_sales'):
            aspirateurs[k].pieces_sales = envt[:].count(1)

        # for pos in lpos:
        #     if not hasattr(aspirateurs[k],'pieces_sales'):
        #         aspirateurs[k].pieces_sales = envt[:].count(1)
        #     perf = m.simulation(nbMax, envt[:], pos)
        #     score = m.agent.getEvaluation(  )

        dico = test_performance(m, 2*nbc, 10)
        perf = dico['Performance Globale']
        score = dico['Evaluation Agent']

        if k in stocker_eval:
            stocker_eval[k].append(perf)
        else:
            stocker_eval[k] = list()
        resultats[k] = resultats.get(k,[]) + [ (perf,score,m.agent.energie,m.agent.vivant,m.agent.nbTours) ]

#=======#
# Plots #
#=======#

py.plot(list(range(2, nbc)), stocker_eval['aleatoire'], "Orange", label='Stochy')
py.plot(list(range(2, nbc)), stocker_eval['genetique_nkapt'], "Blue", label='Genetic pas capt')
py.plot(list(range(2, nbc)), stocker_eval['apprenant'], "Red", label='Learny')
py.plot(list(range(2, nbc)), stocker_eval['genetique_kapt_panne'], "Purple", label="Genetic capt panne")
py.plot(list(range(2, nbc)), stocker_eval['genetique_kapt_npanne'], "Green", label="Genetic capt no panne")
py.title("Point de vue : entreprise (perfGlobale)")
py.legend(loc = "upper right")
py.xlabel("Taille du monde (# de colonnes)")
py.ylabel("Performance")
plot.show()

#================#
# nb simulations #
#================#

# a = range(1,100,5)
# for i in a:
#     for k in aspirateurs:
#         m = MondeSimulation(aspirateurs[k],1,5)
        
#         if not hasattr(aspirateurs[k],'pieces_sales'):
#             aspirateurs[k].pieces_sales = envt[:].count(1)

#         # for pos in lpos:
#         #     if not hasattr(aspirateurs[k],'pieces_sales'):
#         #         aspirateurs[k].pieces_sales = envt[:].count(1)
#         #     perf = m.simulation(nbMax, envt[:], pos)
#         #     score = m.agent.getEvaluation(  )

#         dico = test_performance(m, i, 10)
#         perf = dico['Performance Globale']
#         score = dico['Evaluation Agent']

#         if k not in stocker_eval:
#             stocker_eval[k] = list()
#         stocker_eval[k].append(score)

# py.plot(list(a), stocker_eval['aleatoire'], "Orange", label='Stochy')
# py.plot(list(a), stocker_eval['genetique_nkapt'], "Blue", label='Genetic pas capt')
# py.plot(list(a), stocker_eval['apprenant'], "Red", label='Learny')
# py.plot(list(a), stocker_eval['genetique_kapt_panne'], "Purple", label="Genetic capt panne")
# py.plot(list(a), stocker_eval['genetique_kapt_npanne'], "Green", label="Genetic capt no panne")
# py.title("Point de vue agent : agent (getEval -> Original)")
# py.legend(loc = "upper right")
# py.xlabel("Nombre de simulations")
# py.ylabel("Performance")
# plot.show()

#=======#
# Plots #
#=======#

# for k in aspirateurs:
#     print("_"*5,k,"_"*5)
#     for datas in resultats[k]:
#         print("perfG {0:.3} eval {1:.3} energie {2} vivant {3} nbIterations {4}".format(*datas))

        
"""
Trace utilisation 2 fois sans panne, 2 fois avec pannes:
Remarques: 
 * les positions de départ sont aléatoires mais identiques pour les aspis
 * les pannes sont aléatoires, il faudrait donc faire bcp de simulations

Running script: "G:\WorkInProgress\Aspirateur_1516\Code\Final\main_simulator.py"

Vous avez choisi
lCap = [6, 8, 2] la liste des capteurs
panne = False possiblité de panne
nbActions = 10 dans chaque environnement de test
paramètres pour l'AG
selection = 1
szPop = 75 taille de la population
nbGenerations = 100 nombre d'itérations pour AG
alphabet = AGDR
szGene = 1 taille d'un gène

Lancer le calcul <press any key>
environnements.txt existe
voulez vous utiliser ce fichier oO0Yy ? n
re-génération d'environnements de tests
création d'un GeneratePercept pour [6, 8, 2] taille envt 7
méthode de sélection: _selectFraction
....................................................................................................max obtenu à l'iteration 31 adéquation 68.69999999999999
0 : ((0.1, 18.0928822055138, 41.05, 1375.0590476190487), (GGRGARDAARRADRRRDDARAGGDGAAAGRDARGRAGGDRGRRDAGGDDARARRDGAGRGGAGRDRRRARDGGRADGDDRGRRAAAADGGGDDAGRGAGGGRGGDDDAAGDGDDRGDRGDGADDDDADDGGGAGRAARDAADDAGARAGRRRARDDDRGRDGRAGRGRRGADARADADAA, 41.05))
100 : ((28.90000000000004, 68.03289473684212, 68.69999999999999, 5170.500000000002), (RDDDGRRDRGRRRARDGDRARRDAGRGDGDDDGGDDADRRDRGDGGRRGDGRDRGDDDDRGDDAGDRAARAADGRDDADDADDRADARDGDRAGAGGDAAGRGDRRDGADAAGADDADARGGGDGGGDARAAGAGAGGDADRRGDRARAGRAGARGRGGGRGGRARAGRARAARDRGRAG, 68.69999999999999))
sauvegarde dans datas/graph_en_selectFraction_AGDR_AGDR_76-100
fichiers de sortie _en_AG_AGDR.txt _en_selectFraction_AGDR

Running script: "G:\WorkInProgress\Aspirateur_1516\Code\Final\benchmark_aspi.py"
Donnez le fichier où est le chromosome ? _en_AG_AGDR.txt
création d'un GeneratePercept pour [6, 8, 2] taille envt 7
L'aspirateur peut etre en panne [oui in oO0Yy] ? n
Début simulation Aspirateur genetique energie 100 capteurs [6, 8, 2]
Début simulation Aspirateur aleatoire energie 100 capteurs [6, 8, 2]
Début simulation Aspirateur apprenant energie 100 capteurs [6, 8, 2]
_____ genetique _____
perfG 2.48 eval 0.32 energie 48 vivant True nbIterations 26
perfG 1.48 eval 0.32 energie 48 vivant True nbIterations 26
perfG 1.42 eval -1e+02 energie 0 vivant False nbIterations 11
_____ aleatoire _____
perfG 2.18 eval 0.327 energie 49 vivant True nbIterations 26
perfG 1.62 eval -1e+02 energie 0 vivant False nbIterations 20
perfG 0.0385 eval -1e+02 energie 0 vivant False nbIterations 1
_____ apprenant _____
perfG 2.42 eval 0.405 energie 54 vivant True nbIterations 26
perfG 1.95 eval 0.015 energie 3 vivant True nbIterations 26
perfG 1.08 eval -1e+02 energie 0 vivant False nbIterations 2

Running script: "G:\WorkInProgress\Aspirateur_1516\Code\Final\benchmark_aspi.py"
Donnez le fichier où est le chromosome ? _en_AG_AGDR.txt
création d'un GeneratePercept pour [6, 8, 2] taille envt 7
L'aspirateur peut etre en panne [oui in oO0Yy] ? n
Début simulation Aspirateur apprenant energie 100 capteurs [6, 8, 2]
Début simulation Aspirateur aleatoire energie 100 capteurs [6, 8, 2]
Début simulation Aspirateur genetique energie 100 capteurs [6, 8, 2]
_____ apprenant _____
perfG 2.07 eval 2.77 energie 40 vivant True nbIterations 26
perfG 1.77 eval -1e+02 energie 0 vivant False nbIterations 26
perfG 0.0385 eval -1e+02 energie 0 vivant False nbIterations 1
_____ aleatoire _____
perfG 2.47 eval 0.465 energie 62 vivant True nbIterations 26
perfG 1.33 eval 0.01 energie 2 vivant True nbIterations 26
perfG 1.04 eval -1e+02 energie 0 vivant False nbIterations 1
_____ genetique _____
perfG 2.0 eval 1.0 energie 100 vivant True nbIterations 26
perfG 2.48 eval 0.32 energie 48 vivant True nbIterations 26
perfG 1.92 eval -1e+02 energie 0 vivant False nbIterations 24

Running script: "G:\WorkInProgress\Aspirateur_1516\Code\Final\benchmark_aspi.py"
Donnez le fichier où est le chromosome ? _en_AG_AGDR.txt
création d'un GeneratePercept pour [6, 8, 2] taille envt 7
L'aspirateur peut etre en panne [oui in oO0Yy] ? o
Début simulation Aspirateur apprenant energie 100 capteurs [6, 8, 2]
Début simulation Aspirateur genetique energie 100 capteurs [6, 8, 2]
Début simulation Aspirateur aleatoire energie 100 capteurs [6, 8, 2]
_____ apprenant _____
perfG 1.67 eval 0.213 energie 32 vivant True nbIterations 26
perfG 1.58 eval -1e+02 energie 0 vivant False nbIterations 23
perfG 1.04 eval -1e+02 energie 0 vivant False nbIterations 1
_____ genetique _____
perfG 2.0 eval 1.0 energie 100 vivant True nbIterations 26
perfG 2.26 eval 3.43 energie 93 vivant True nbIterations 26
perfG 2.39 eval 0.287 energie 43 vivant True nbIterations 26
_____ aleatoire _____
perfG 2.47 eval 2.8 energie 45 vivant True nbIterations 26
perfG 2.43 eval 2.9 energie 53 vivant True nbIterations 26
perfG 1.87 eval -97.5 energie 0 vivant False nbIterations 23

Running script: "G:\WorkInProgress\Aspirateur_1516\Code\Final\benchmark_aspi.py"
Donnez le fichier où est le chromosome ? _en_AG_AGDR.txt
création d'un GeneratePercept pour [6, 8, 2] taille envt 7
L'aspirateur peut etre en panne [oui in oO0Yy] ? o
Début simulation Aspirateur genetique energie 100 capteurs [6, 8, 2]
Début simulation Aspirateur aleatoire energie 100 capteurs [6, 8, 2]
Début simulation Aspirateur apprenant energie 100 capteurs [6, 8, 2]
_____ genetique _____
perfG 2.1 eval 0.22 energie 33 vivant True nbIterations 26
perfG 1.65 eval -1e+02 energie 0 vivant False nbIterations 17
perfG 0.0385 eval -1e+02 energie 0 vivant False nbIterations 1
_____ aleatoire _____
perfG 2.76 eval 3.28 energie 78 vivant True nbIterations 26
perfG 2.72 eval 3.06 energie 74 vivant True nbIterations 26
perfG 2.45 eval 5.07 energie 14 vivant True nbIterations 26
_____ apprenant _____
perfG 2.13 eval 3.26 energie 76 vivant True nbIterations 26
perfG 2.35 eval 2.72 energie 33 vivant True nbIterations 26
perfG 1.82 eval -95.0 energie 0 vivant False nbIterations 14

"""
