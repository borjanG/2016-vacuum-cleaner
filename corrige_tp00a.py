#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "correction de la première séance de TD : test_tp00"
__version__ = "00a"

import random
import copy
from ezCLI import grid

# les éléments du monde dans un dictionnaire
objetsStatiques = {100: ('Aspirateur','@'),
                    0: ('nothing','.'),
                    1: ('poussière','x'),
                    -1: ('erreur','?'),
                }
                
class Aspirateur(object):
    """ classe de base pour l'agent mobile """
    def __init__(self, capteurs=[], actions="Gauche Droite Aspirer".split()):
        assert isinstance(capteurs,(list,tuple)), "a list/tuple is required"
        #assert len(set(capteurs)) == len(capteurs), "no duplication"
        #assert all([_ in range(9) for _ in capteurs]), "only 0..8 allowed"
        _c = [False for _ in range(9)]
        for x in capteurs:
            assert x in range(9), "%s is not in 0..8" % x
            assert not _c[x], "%d has multiple instance in %s" % (x,capteurs)
            _c[x] = True
        
        assert isinstance(actions,(list,tuple)), "a list/tuple is required"
        self.__capteurs = capteurs
        self.__actions = actions
        self.__alive = True
        self.__value = list()
        self.__total = 0
        
    @property
    def capteurs(self): return self.__capteurs
    @property
    def actions(self): return self.__actions
    @property
    def vivant(self): return self.__alive

    def setReward(self,value):
        """ récupère le reward exterieur """
        assert isinstance(value,(int,float))
        self.__value.append(value)
        self.__total += value
        
    def getLastReward(self): 
        return self.__value[-1]
        # return self.__value

    def getDecision(self,percepts):
        assert isinstance(percepts,(list,tuple))
        assert len(percepts) == len(self.capteurs)
        assert all([ x in objetsStatiques for x in percepts ])
        return random.choice( self.actions )
        
    def getEvaluation(self): 

        # return self.__total
        return self.__total / max(1, len(self.__value))
        
class Monde(object):
    """ l'environnement et les interactions avec l'agent """
    def __init__(self,agent,nbl=1,nbc=2):
        self.__nbl = nbl
        self.__nbc = nbc
        assert(isinstance(agent,Aspirateur)),\
          "TypeError Aspirateur expected got %s" % agent.__class__
        self._table = None # la grille du monde
        self._pos = None # la position de l'agent dans le monde
        self.__agent = agent
        self.initialisation()
        
    def __str__(self):
        """ utilisation de ezCLI.grid """
        _t = self.table
        # On place l'agent dans la grille
        _t[self.posAgent[0]][self.posAgent[1]] = 100 
        _coder = lambda ly: [ objetsStatiques[_][1] for _ in ly ]
        return grid(list( map(_coder,_t) ),label=True)

    def initialisation(self):
        """ place l'agent et remplit la table aléatoirement """
        self._pos = random.choice(range(self.__nbl)),random.choice(range(self.__nbc))
        _ = [ k for k in objetsStatiques if 0 <= k < 100 ]

        self._table = [ [ random.choice( _ ) for j in range(self.__nbc) ]
                         for i in range(self.__nbl) ]
                         
        self.__h = []

    #--- attributs readonly
    @property
    def posAgent(self): return self._pos
    @property
    def table(self): 
        return copy.deepcopy(self._table) # empeche de modifier un element de la table
    @property
    def agent(self): return self.__agent
    @property
    def perfGlobale(self): return 0
    @property
    def historique(self): return self.__h
    
    #----- méthodes
    def applyChoix(self,choix):
        """ 
            modifie table & posAgent en fonction de choix 
            renvoie une évaluation 
        """
        return 0
        
    def getPerception(self,capteurs):
        """ informe l'agent en fonction des capteurs """
        if len(capteurs)==0 : return []
        else: raise NotImplementedError("TODO")
        
    def updateWorld(self):
        """ modifie table evts stochastiques """
        pass
        
    def step(self):
        """ une étape de calcul c'est
            (a) connaitre les besoins de l'agent aka perception
            (b) demander a l'agent son choix en fonction de ses percepts
            (b') sauvegarder l'état du monde au moment de l'action
            (c) mettre à jour le monde et envoyer un feedback à l'agent
            (d) mettre à jour le monde pour les evts stochastiques
        """
        percept = self.getPerception( self.agent.capteurs )
        choix = self.agent.getDecision( percept )
        self.__h.append( ((self.table,self.posAgent),choix) )
        self.agent.setReward( self.applyChoix( choix ) )
        self.updateWorld()
        
    def simulation(self,n):
        """ 
            la simulation dure max n tours et s'arrete des que l'agent 
            n'est plus opérationnel
        """
        self.initialisation()
        i = 0
        while i < n and self.agent.vivant :
            self.step()
            i+= 1
        return self.perfGlobale
    

