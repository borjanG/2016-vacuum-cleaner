#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "Mise en place du TP01"
__author__ = "mmc, Terral, Rodriguez, Geshkovski"
__date__ = "19.02.16"
__version__ = "0.1"

from data.monde import objetsStatiques, Aspirateur, Monde
from briques import Rule, KB
import copy
from random import randint, choice, random

class Aspirateur_KB(Aspirateur):
    """ 4 paramètres
        probaExploitation: pas de valeur par défaut
        lCap: valeur par défaut []
        lAct: valeur par défaut la liste des 3 actions Gauche Droite Aspirer
        learn: valeur par défaut False (pas d'apprentissage)
    """
    def __init__(self,probaExploitation,lCap=[],lAct="Gauche Droite Aspirer".split(),learn=False):
        super(Aspirateur_KB,self).__init__(lCap,lAct)
        assert 0 <= probaExploitation <= 1, "Probability expected"
        assert isinstance(learn,bool), "Boolean expected got %s" % type(learn)
        self.__la_variable_privee_contenant_la_base_de_connaissance = KB() # base de données vide
        self.__probaExploitation = probaExploitation
        self.__learn = learn
        self.__last_action = None # dernière action choisie
        self.__last_percept = None # dernier percept reçu
        
    @property
    def apprentissage(self): return self.__learn
    @apprentissage.setter
    def apprentissage(self,v):
        assert isinstance(v, bool), "pas bool."
        self.__learn = v
        
    @property
    def knowledge(self): return copy.deepcopy(self.__la_variable_privee_contenant_la_base_de_connaissance)
    @knowledge.setter
    def knowledge(self,v):
        assert isinstance(v, KB), "pas KB"
        self.__la_variable_privee_contenant_la_base_de_connaissance = v
        
    @property
    def probaExploitation(self): return self.__probaExploitation
    
    def getEvaluation(self): return (self.nettoyage+1)/(len(self.knowledge)+1)
        
    def getDecision(self,percepts):
        assert isinstance(percepts,(list,tuple)), "%s should be list or tuple" % percepts
        assert len(percepts) == len(self.capteurs), "percepts and capteurs do not match"
        assert all([ x in objetsStatiques for x in percepts ]), "bad percepts %s" % percepts

        self.__last_percept = percepts
        liste_de_regles = self.__la_variable_privee_contenant_la_base_de_connaissance.find(percepts)

        if len(liste_de_regles) == 0:
            action = choice(self.actions)
        else:
            liste_action_base = [regle.conclusion for regle in liste_de_regles]
            liste_action_pas_base = list(set(actions).difference(liste_action_base))
            meilleure_regle = max(liste_de_regles, key=lambda action: action.scoreMoyen)
            r = random()

            if r < self.probaExploitation:
                action = meilleure_regle
            else:
                liste_autres_action_base = liste_action_base.remove(meilleure_regle.conclusion)
                if len(liste_autres_action_base) != 0:
                    action = choice(liste_autres_action_base)
                    if action.scoreMoyen < 0:
                        action = choice(liste_action_pas_base)
                else:
                    action = choice(liste_action_pas_base)

        self.__last_action = action
        return self.__last_action
        
    def setReward(self,value):
        super(Aspirateur_KB,self).setReward(value)
        if self.apprentissage:
            action = self.__last_action
            percepts = self.__last_percept
            r = Rule(percepts, action, value)
            self.knowledge.add(r)
            
class World(Monde):
    """ constructeur avec 3 paramètres, syntaxe identique au constructeur de Monde """
    def __init__(self,agent,nbLignes=1,nbColonnes=2):
        # super(World,self).__init__(agent,nbLignes,nbColonnes)
        super().__init__(agent, nbLignes, nbColonnes)
        self.__cols = nbColonnes
        self.__lignes = nbLignes
        self.__table = [[0 for j in range(self.__cols)] for i in range(self.__lignes)]
        self.initialisation()
    
    def initialisation(self):
        super(World,self).initialisation()
        self._passage = [ [0 for j in range(len(self.table[0])) ] for i in range(len(self.table)) ]
        i,j = self.posAgent
        self._passage[i][j] = 1
        self.agent.nettoyage = 0
        
    def getPerception(self,capteurs):
        """ informe l'agent en fonction des capteurs """

        delta = [ (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (0,0) ]
        res = []
        for x in capteurs:
            nx = self.posAgent[0]+delta[x][0]
            ny = self.posAgent[1]+delta[x][1]
            if self.__lignes > nx >= 0 and self.__cols > ny >= 0: res.append(self.table[nx][ny])
            else: res.append(-1)
        return res   

        
    def applyChoix(self,choix):
        """ modifie table & posAgent en fonction de choix """

        if choix == 'Aspirer':
            if self.table[self.posAgent[0]][self.posAgent[1]] == 1:
                self.__table[self.posAgent[0]][self.posAgent[1]] = 0
                self.agent.nettoyage+=1
                score = 2
            else:
                score = 0
        else:
            ny = self.posAgent[1]
            if choix == 'Gauche':
                if ny > 0: 
                    self.__posAgent = (self.posAgent[0], self.posAgent[1]-1)
                    score = 1
                else:
                    score = -1
            elif choix == 'Droite':
                if ny < self.__cols: 
                    self.__posAgent = (self.posAgent[0], self.posAgent[1]+1)
                    score = 1
                else:
                    score = -1
        i,j = self.posAgent
        self._passage[i][j] += 1  
        return score
        
    @property
    def perfGlobale(self):

        #Charlotte
        # compteur=0
        # for elem in self._passage:
        #     for x in elem:
        #         if x >= 3: compteur+=1
        # return self.agent.nettoyage - compteur

        #Borjan
        T = 0
        for i in range(len(self._passage)):
            T += len(list(filter(lambda x: x>2, self._passage[i])))
        return self.agent.nettoyage - T


