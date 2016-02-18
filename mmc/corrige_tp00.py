#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "correction de la première séance de TD : test_tp00"
__version__ = "00"

import random
import copy
from ezCLI import grid

# les éléments du monde dans un dictionnaire
objetsStatiques = {100: ('Aspirateur','@'),
                    0: ('nothing','.'),
                    1: ('poussière','x'),
                }
                
class Aspirateur(object):
    """ classe de base pour l'agent mobile """
    def __init__(self):
        pass
        
class Monde(object):
    """ l'environnement et les interactions avec l'agent """
    def __init__(self,agent,nbl=1,nbc=2):
        self.__nbl = nbl
        self.__nbc = nbc
        assert(isinstance(agent,Aspirateur)), "TypeError Aspirateur expected got %s" % agent.__class__
        self.__table = None # la grille du monde
        self.__pos = None # la position de l'agent dans le monde
        self.initialisation()
        
    def __str__(self):
        """ utilisation de ezCLI.grid """
        _t = self.table
        _t[self.posAgent[0]][self.posAgent[1]] = 100 # On place l'agent dans la grille
        _coder = lambda ly: [ objetsStatiques[_][1] for _ in ly ]
        return grid(list( map(_coder,_t) ),label=True)

    def initialisation(self):
        """ place l'agent et remplit la table aléatoirement """
        self.__pos = random.choice(range(self.__nbl)),random.choice(range(self.__nbc))
        _ = [ k for k in objetsStatiques if 0 <= k < 100 ]

        self.__table = [ [ random.choice( _ ) for j in range(self.__nbc) ]
                         for i in range(self.__nbl) ]

    #--- attributs readonly
    @property
    def posAgent(self): return self.__pos
    @property
    def table(self): 
        return copy.deepcopy(self.__table) # empeche de modifier un element de la table
