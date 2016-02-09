#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "Mise en place du TP01"
__date__ = "09.02.16"
__version__ = "0.1"

# remplacer XXX par votre fichier issu du TD2
from data.monde import objetsStatiques, Aspirateur, Monde
from briques import Rule, KB
import copy

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
        # initialisation de variables privées __XXX (nom à choisir)
        self.__XXX = KB() # base de données vide
        self.__XXX = probaExploitation
        self.__XXX = learn
        self.__XXX = None # dernière action choisie
        self.__XXX = None # dernier percept reçu

        
    @property
    def apprentissage(self): return la_variable_privée_contenant_learn
    @apprentissage.setter
    def apprentissage(self,v):
        # on vérifie que v est un booléen et si oui on affecte la_variable_privée_contenant_learn
        
    @property
    def knowledge(self): return copy.deepcopy(la_variable_privée_contenant_la_base_de_connaissance)
    @knowledge.setter
    def knowledge(self,v):
        # on vérifie que v est une KB, si oui on affecte la_variable_privée_contenant_la_base_de_connaissance
        
    @property
    def probaExploitation(self): return la_variable_privée_contenant_probaExploitation
    
    def getEvaluation(self):
        # On renvoie l'évaluation de l'agent
        # (nombre de pièces nettoyées + 1) / ( len(self.knowledge) + 1 )
        
    def getDecision(self,percepts):
        assert isinstance(percepts,(list,tuple)), "%s should be list or tuple" % percepts
        assert len(percepts) == len(self.capteurs), "percepts and capteurs do not match"
        assert all([ x in objetsStatiques for x in percepts ]), "bad percepts %s" % percepts
        # On sauvegarde percepts dans la_variable_privée_contenant_le_dernier_percept
        # On récupère la liste des règles dont la condition correspond aux percepts
        # Si la liste est vide on choisit une action au hasard
        # Sinon
        #     On calcule les actions les actions dans la base pour ce percept
        #     On calcule les actions pas dans la base pour ce percept
        #     On cherche l'action ayant le meilleur score moyen (elle existe)
        #     On tire un nombre aléatoire (r) que l'on compare à la probabilité d'exploitation
        #     si r < probaExploitation alors 
        #        l'action choisie est celle déterminée par le scoreMoyen maximum
        #     sinon on pioche de manière équiprobable dans les autres actions
        #        si pas d'autres on pioche aléatoirement dans les actions pas dans la base
        #        si elle existe mais que son score est négatif et qu'il y a des actions pas dans la base
        #           on prend une action aléatoire
        # On sauvegarde dans la_variable_privée_contenant_la_dernière_action_choisie
        # On renvoie l'action
        
    def setReward(self,value):
        super(Aspirateur_KB,self).setReward(value)
        if self.apprentissage:
            # On crée une Rule avec les 3 paramètres percepts,action,value r = Rule(....)
            # On ajoute cette règle dans la base grace à self.knowledge.add(r)
        
        
class World(Monde):
    """ constructeur avec 3 paramètres, syntaxe identique au constructeur de Monde """
    def __init__(self,agent,nbLignes=1,nbColonnes=2):
        super(World,self).__init__(agent,nbLignes,nbColonnes)
    
    def initialisation(self):
        super(World,self).initialisation()
        # creer une variable privée qui va servir à compter le nombre de fois ou l'agent est dans
        # une case donnée. La variable est donc une liste de liste dont chaque valeur est à 0
        # self._XXX = [ [0 for j in range(len(self.table[0])) ] for i in range(len(self.table) ]
        # i,j = self.posAgent
        # self.__XXX[i][j] = 1
        # ajoute à l'agent un compteur de pièces nettoyées, initalisé à 0
        # self.agent.nettoyage = 0
        
    def getPerception(self,capteurs):
        """ informe l'agent en fonction des capteurs """
        # renvoie la liste des valeurs contenues dans self.table[nx][ny]
        # on utilise delta = [ (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (0,0) ]
        # pour x dans capteurs faire
        #     nx = self.posAgent[0]+delta[x][0]
        #     ny = self.posAgent[1]+delta[x][1]
        #     si nx >= 0 et < nbLignes & ny >= 0 et < nbColonnes : table[nx][ny] existe
        #     sinon la valeur est -1
        # On renvoie une liste de la taille de capteurs
        
    def applyChoix(self,choix):
        """ modifie table & posAgent en fonction de choix """
        # si choix est Aspirer et que l'agent est sur une case poussiere
        # modifier la table (disparition poussière), augmenter self.agent.nettoyage, renvoyer le score 2
        # si choix est Aspirer et que l'agent est sur une case propre
        # pas de modification, renvoyer le score 0
        # si choix est un déplacement et que l'agent ne peut pas le faire
        # pas de modification, renvoyer -1
        # sinon, modifier la position de l'agent, renvoyer 1
        # ATTENTION AVANT de renvoyer le score, mais APRES avoir modifier table & posAgent
        # i,j = self.posAgent
        # variable_cachée_compteur[i][j] += 1
        
    
    @property
    def perfGlobale(self):
        # return nombre de pièces nettoyées − nombre de pièces visitées 3 fois ou plus


