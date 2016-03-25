#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Et maintenant ... ça tourne:
Un chromosome pour aspi sans capteurs doit avoir 20 gènes
Un chromosome pour aspi avec capteurs sera basé sur GeneratePercept
"""

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__version__ = "0.2"
__date__ = "15.03.16"
__usage__ = "Utilisation de l'algo génétique"

# remplacer XXXX par votre fichier correspondant au tp02b
from XXXX import objetsStatiques, Aspirateur_PG, MondeSimulation
from XXXX import Simulateur
from briques import ProgramGenetic, mmcUnaire, mmcBinaire, GeneratePercept
import agslib

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
    """ création de l'aspect généique avec accès au simulateur pour faire l'évaluation """
    def __init__(self,nbIteration,fichier,capteurs,envt,nbIndiv,szGene,alphabet,decodeur,panne=False):
        self.__sim = Simulateur(nbIteration,fichier,capteurs,panne)
        if capteurs == []: self.__nbG = 20 ; self.__gp = None
        else: self.__gp = GeneratePercept(capteurs,envt) ; self.__nbG = self.__gp.howMany
        self.__prog = ProgramGenetic(szGene,self.__nbG,alphabet,decodeur)
        super().__init__(nbIndiv,self.__nbG,szGene,alphabet)
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
        self.prog.program = chaine
        return max(.1,self.simulator.run( self.prog, self.gp )) # garantit des scores positifs

p = PopAspi(25,'tyty.txt',[2,6,8],objetsStatiques,30,2,'01',mmcBinaire,True)
p.run(50,"tyty_AG_01.txt",1)
p.plotHistory(p.select(2)+'_genes_'+'01'+'_withPanne')
p.run(50,"tyty_AG_01_b.txt")
p.plotHistory(p.select(1)+'_genes_'+'01'+'_withPanne')
p = PopAspi(25,'tyty.txt',[2,6,8],objetsStatiques,30,1,'AGDR',mmcUnaire,False)
p.run(50,"tyty_AG_AGDR.txt",1)
p.plotHistory(p.select(2)+'_genes_'+'AGDR'+'_noPanne')
p.run(50,"tyty_AG_AGDR_b.txt",1)
p.plotHistory(p.select(1)+'_genes_'+'AGDR'+'_noPanne')
