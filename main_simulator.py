#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Et maintenant ... ça tourne:
Un chromosome pour aspi sans capteurs doit avoir 20 gènes
Un chromosome pour aspi avec capteurs sera basé sur GeneratePercept
"""

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__version__ = "0.7"
__date__ = "15.03.16"
__usage__ = "Utilisation de l'algo génétique"
__revision__ = "23.04.16"

from corrige_tp02b import objetsStatiques, Aspirateur_PG, MondeSimulation
from corrige_tp02b import Simulateur
from briques import ProgramGenetic, mmcUnaire, mmcBinaire, GeneratePercept
from tools_tp02 import generateEnvts
import agslib
import random
import os

"""
# comment marche le simulateur
# le nombre d'itérations, le fichier, les capteurs, la panne
# la méthode run prend en paramètre un ProgramGenetic
# un ProgamGenetic a besoin
# taille gène, nb Gènes, alphabet, un dictionnaire
# un GeneratePercept prend des capteurs non vide et un dictionnaire

# On crée un simulateur pour aspi sans capteur
# On crée deux simulateur pour aspi avec 2 capteurs 
# On crée un simulateur pour aspi avec 3 capteurs 

sim1 = Simulateur(25,"tyty.txt",[])
sim2 = Simulateur(25,"tyty.txt",[2,8])
sim3 = Simulateur(25,"tyty.txt",[6,8])
sim4 = Simulateur(25,"tyty.txt",[6,2,8])

g2 = GeneratePercept([2,8],objetsStatiques)
g3 = GeneratePercept([6,8],objetsStatiques)
g4 = GeneratePercept([6,2,8],objetsStatiques)
prog1 = ProgramGenetic(2,20,"01",mmcBinaire)
prog2 = ProgramGenetic(1,20,"ARGD",mmcUnaire)
prog3 = ProgramGenetic(2,g2.howMany,"01",mmcBinaire)
prog4 = ProgramGenetic(1,g3.howMany,"AGDR",mmcUnaire)
prog5 = ProgramGenetic(2,g4.howMany,"01",mmcBinaire)
print(1,sim1.panne,sim1.run(prog1))
sim1.panne = True
print(2,sim1.panne,sim1.run(prog2))
print(3,sim2.panne,sim2.run(prog3))
print(4,sim3.panne,sim3.run(prog3))
sim3.panne = True
print(5,sim3.panne,sim3.run(prog4,g3))

pannes = (False,True)
for sim4.panne in pannes: print(sim4.panne,sim4.run(prog5,g4))
"""

# Tentative d'héritage

class PopAspi(agslib.Population):
    """ création de l'aspect génétique avec accès au simulateur 
        pour faire l'évaluation 
    """
    def __init__(self, nbIteration, fichier, capteurs, envt,
                 nbIndiv, szGene, alphabet, decodeur, panne=False):
        
        self.__sim = Simulateur(nbIteration,fichier,capteurs,panne)
        if capteurs == []: self.__nbG = 20 ; self.__gp = None
        else:
            self.__gp = GeneratePercept(capteurs,envt)
            self.__nbG = self.__gp.howMany
            
        self.__prog = ProgramGenetic(szGene, self.nbGenes, alphabet, decodeur)
        super().__init__(nbIndiv, self.nbGenes, szGene, alphabet)
        # On associe la fitness
        for x in self.popAG : x.fitness = lambda _ : self.simEval( _ )
         
    @property
    def simulator(self): return self.__sim
    @property
    def prog(self): return self.__prog
    @property
    def gp(self): return self.__gp
    @property
    def nbGenes(self): return self.__nbG
    def simEval(self,chaine):
        self.prog.program = chaine # le lien entre une chaine et un aspi
        # garantit des scores positifs
        return max(.1,self.simulator.run( self.prog, self.gp )) 


def main_nocmd(fichier='environnements.txt', nbActions=10, szPop=50, nbGenerations=25,
               selection= 0, alphabet='01', panne=False, lCap=[], verbose=False):
    """ code identique à main_cmd, sauf controle de paramètres et nom de variables """
    assert isinstance(fichier,str), "{} not a valid file name".format(fichier)
    assert isinstance(nbActions,int) and nbActions >0, "nbActions {} is wrong".format(nbActions)
    assert isinstance(szPop,int) and szPop >0, "szPop {} is wrong".format(szPop)
    assert isinstance(nbGenerations,int) and nbGenerations >0, "nbGenerations {} is wrong".format(nbGenerations)
    assert isinstance(selection,int) and selection in (0,1,2), "selection {} is wrong".format(selection)
    assert isinstance(lCap,(list,tuple)), "lCap {} should be a list or tuple".format(lCap)
    assert len(list(set(lCap))) == len(lCap), "duplicate values in lCap {} are forbidden".format(lCap)
    assert all([x in range(9) for x in lCap]), "lCap {} contains bad values".format(lCap)
    assert isinstance(panne,bool), "panne {} should be boolean".format(panne)
    assert isinstance(verbose,bool), "verbose {} should be boolean".format(verbose)
    assert alphabet in ('01', 'AGDR'), "alphabet {} is unknown".format(alphabet)
    
    if lCap == []: panne = False # no capteurs no panne
    if alphabet == '01':
        size = 2 ; decodeur = mmcBinaire
    else:
        size = 1 ; decodeur = mmcUnaire

    ags = {} 
    ags['nbActions'] = nbActions
    ags['selection'] = selection
    ags['szPop'] = szPop
    ags['nbGenerations'] = nbGenerations
    ags['alphabet'] = alphabet
    
    print("""
Vous avez choisi
lCap = {0} la liste des capteurs
panne = {1} possiblité de panne
nbActions = {nbActions} dans chaque environnement de test
paramètres pour l'AG
selection = {selection}
szPop = {szPop} taille de la population
nbGenerations = {nbGenerations} nombre d'itérations pour AG
alphabet = {alphabet}
szGene = {2} taille d'un gène
""".format(lCap,panne,size,**ags))
    input("Lancer le calcul <press any key>")

    # vérification que l'environnement de tests existe, sinon création
    if fichier in os.listdir():
        print("{} existe".format(fichier))
        _rep = "oO0Yy"
        _you = input("voulez vous utiliser ce fichier "+_rep+" ? ")
        if _you not in _rep :
            print("re-génération d'environnements de tests")
            generateEnvts(fichier)
    else:
        print("génération d'environnements de tests")
        generateEnvts(fichier)

    _base = '_'+fichier.split('.')[0]
    # fichier contenant le meilleur individu
    _oname = "{}_AG_{}.txt".format(_base[:3],alphabet)
    random.seed()

    p = PopAspi(nbActions, fichier, lCap, objetsStatiques,
                szPop, size, alphabet, decodeur, panne)
    # fichier contenant la sortie graphique dans le répertoire datas
    _plotname = "{}{}_{}{}".format(_base[:3], p.select(selection),
                                         alphabet,
                                         "_Pannes" if panne else '')
    p.run(nbGenerations, _oname, selection, verbose)
    # on ajoute des informations utiles
    with open(_oname,'a') as f:
        f.write("#capteurs\n")
        if lCap == [] : f.write("{}\n".format(-1))
        else:
            for x in lCap:
                f.write("{} ".format(x))
            f.write('\n')
        f.close()
    # ne marche que si vous avez pensé à utiliser historique dans run (agslib)
    p.plotHistory(_plotname)

    print("fichiers de sortie", _oname, _plotname)
    
def main_cmd():
    """ utilise fichier ou genere fichier 

    On va évaluer un aspirateur effectuant 10 actions dans différents envts
    On va mettre en compétition 50 aspirateurs du meme type
    p = PopAspi(10,...,50,...)

    L'algorithme génétique fait 25 itérations
    p.run(25,...)
    """
    import argparse
    
    # le parser de ligne de commandes
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\
Chercher le chromosome d'un aspirateur avec ou sans capteurs
que l'on teste dans différents environnements se trouvant dans un fichier
On donne :
  * La taille de la population (le nombre d'aspirateurs en concurrence)
  * Le nombre de générations pour l'algo génétique

  En sortie on trouve le fichier contenant le meilleur chromosome

""")
    parser.print_help()
    parser.add_argument("-f", '--file', default='environnements.txt',
                        help="fichier contenant les envts de simulation")
    parser.add_argument("-n", '--nbActions', type=int,
                        help="nombre d'actions effectuées", default=10)
    parser.add_argument("szPop", type=int, help="taille de la population",
                        default=50)
    parser.add_argument("nbGenerations", type=int,
                        help="nombre d'itérations pour l'algo génétique",
                        default=25)
    parser.add_argument('-c', '--capteurs', nargs='+', type=int,
                        help="capteurs",
                        choices=range(9), default=[])
    parser.add_argument('-s', '--selection', type=int, default=0,
                        choices=range(3), help="méthode de sélection de l'AG")
    parser.add_argument('-a', '--alphabet', type=str, default='01',
                        choices=['01', 'AGDR'], help="choix de l'alphabet")
    parser.add_argument('-p', '--panne', action="store_true",
                        help="indique si les capteurs sont sujets à panne")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true",
                        help="active le mode verbeux")
    group.add_argument("-q", "--quiet", action="store_true",
                        help="active le mode silencieux")

    
    args = parser.parse_args()
    # Gestion des arguments
    lCap = args.capteurs
    if lCap == []: panne = False
    else: panne = args.panne

    fichier = args.file
    if args.alphabet == '01':
        size = 2 ; decodeur = mmcBinaire
    else:
        size = 1 ; decodeur = mmcUnaire

    print("""
Vous avez choisi
lCap = {0} la liste des capteurs
panne = {1} possiblité de panne
nbActions = {2.nbActions} dans chaque environnement de test
paramètres pour l'AG
selection = {2.selection}
szPop = {2.szPop} taille de la population
nbGenerations = {2.nbGenerations} nombre d'itérations pour AG
alphabet = {2.alphabet}
szGene = {3} taille d'un gène
""".format(lCap,panne,args,size))
    input("Lancer le calcul <press any key>")

    # vérification que l'environnement de tests existe, sinon création
    if fichier in os.listdir():
        print("{} existe".format(fichier))
        _rep = "oO0Yy"
        _you = input("voulez vous utiliser ce fichier "+_rep+" ? ")
        if _you not in _rep :
            print("re-génération d'environnements de tests")
            generateEnvts(fichier)
    else:
        print("génération d'environnements de tests")
        generateEnvts(fichier)

    _base = '_'+fichier.split('.')[0]
    # fichier contenant le meilleur individu
    _oname = "{}_AG_{}.txt".format(_base[:3],args.alphabet)
    random.seed()

    p = PopAspi(args.nbActions,fichier,lCap,objetsStatiques,
                args.szPop,size,args.alphabet, decodeur, panne)
    # fichier contenant la sortie graphique dans le répertoire datas
    _plotname = "{}{}_{}{}".format(_base[:3], p.select(args.selection),
                                         args.alphabet,
                                         "_Pannes" if panne else '')
    p.run(args.nbGenerations,_oname,args.selection,args.verbose)
    # on ajoute des informations utiles
    with open(_oname,'a') as f:
        f.write("#capteurs\n")
        if lCap == [] : f.write("{}\n".format(-1))
        else:
            for x in lCap:
                f.write("{} ".format(x))
            f.write('\n')
        f.close()    # ne marche que si vous avez pensé à utiliser historique dans run (agslib)
    p.plotHistory(_plotname)

    print("fichiers de sortie", _oname, _plotname)
if __name__ == "__main__" :
    if os.name =='nt' :
        # si on ne passe par la ligne de commande c'est fastidieux, il faut définir un moyen
        # de saisir les informations, genre input ... je vous laisse faire
        main_nocmd(alphabet='AGDR',selection=1,lCap=[6,8,2],szPop=75,nbGenerations=100,verbose=True)
    else:
        main_cmd()
