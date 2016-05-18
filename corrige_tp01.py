#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "Mise en place du TP01"
__date__ = "09.02.16"
__version__ = "0.1"

# remplacer XXX par votre fichier issu du TD2
#from XXX import objetsStatiques, Aspirateur, Monde
from corrige_tp00a import objetsStatiques, Aspirateur, Monde
from briques import Rule, KB
import copy, random

TupLst = tuple,list

class Aspirateur_KB(Aspirateur):
    """ 4 paramètres
        probaExploitation: pas de valeur par défaut
        lCap: valeur par défaut []
        lAct: valeur par défaut la liste des 3 actions Gauche Droite Aspirer
        learn: valeur par défaut False (pas d'apprentissage)
    """
    def __init__(self, probaExploitation : float,
                 lCap: TupLst = [],
                 lAct: TupLst = "Gauche Droite Aspirer".split(),
                 learn: bool =False) -> None :
        super().__init__(lCap,lAct)
        assert 0 <= probaExploitation <= 1, "Probability expected"
        assert isinstance(learn,bool), "Boolean expected got %s" % type(learn)
        # initialisation de variables privées __XXX (nom à choisir)
        self.__kb = KB() # base de données vide
        self.__proba = probaExploitation
        self.__learn = learn
        self.reset()
        
    def reset(self):
        """ réinitialisation de variables possibles """
        self.__lastAction = None # dernière action choisie
        self.__lastPercept = None # dernier percept reçu
        # compteurs pour statistiques
        self.compteurs = {'alea': 0, 'exploration': 0, 'exploitation': 0, 'total': 0 }
        
    @property
    def apprentissage(self): return self.__learn
    @apprentissage.setter
    def apprentissage(self,v):
        # on vérifie que v est un booléen et si oui on affecte la_variable_privée_contenant_learn
        if isinstance(v,bool): self.__learn = v
        
    @property
    def knowledge(self): return copy.deepcopy(self.__kb)
    @knowledge.setter
    def knowledge(self,v):
        # on vérifie que v est une KB, si oui on affecte la_variable_privée_contenant_la_base_de_connaissance
        if isinstance(v,KB): self.__kb = v
        
    @property
    def probaExploitation(self): return self.__proba
    
    def getEvaluation(self):
        # On renvoie l'évaluation de l'agent
        # (nombre de pièces nettoyées + 1) / ( len(self.knowledge) + 1 )
        if hasattr(self,'nettoyage'):
            return (self.nettoyage +1) / (len(self.knowledge) + 1)
        else: raise AttributeError("no attribut 'nettoyage' found")

        
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
        self.__lastPercept = percepts
        _rules = self.knowledge.find(percepts)
        if _rules == [] : 
            _a = random.choice(self.actions)
            self.compteurs['alea'] += 1
        else:
            _possibles = [_.conclusion for _ in _rules ] 
            _newActions = [_ for _ in self.actions if _ not in _possibles ]
            _best = _rules[0] # existe
            for r in _rules:
                if r.scoreMoyen > _best.scoreMoyen : _best = r
            if random.random() < self.probaExploitation: # Exploitation
                _a = _best.conclusion
                self.compteurs['exploitation'] += 1
            elif len(_rules) == 1:
                _a = random.choice( _newActions )
                self.compteurs['alea']+= 1
            else: # d'autres choix possible
                _residu = _rules[:]
                _residu.remove( _best )
                _choix = random.choice( _residu )
                if _choix.scoreTotal < 0 and _newActions != [] :
                    _a = random.choice( _newActions )
                    self.compteurs['alea'] +=1
                else:
                    _a = _choix.conclusion
                    self.compteurs['exploration'] += 1
        self.__lastAction = _a # sauvegarde
        self.compteurs['total'] += 1
        return self.__lastAction
        
                
        
    def setReward(self,value):
        super(Aspirateur_KB,self).setReward(value)
        if self.apprentissage:
            # On crée une Rule avec les 3 paramètres percepts,action,value r = Rule(....)
            # On ajoute cette règle dans la base grace à self.knowledge.add(r)
            self.__kb.add(Rule(self.__lastPercept,self.__lastAction,value))
        
class World(Monde):
    """ constructeur avec 3 paramètres, syntaxe identique au constructeur de Monde """
    def __init__(self,agent,nbLignes=1,nbColonnes=2):
        super().__init__(agent,nbLignes,nbColonnes)
    
    def initialisation(self):
        super().initialisation()
        # creer une variable privée qui va servir à compter le nombre de fois ou l'agent est dans
        # une case donnée. La variable est donc une liste de liste dont chaque valeur est à 0
        # self._XXX = [ [0 for j in range(len(self.table[0])) ] for i in range(len(self.table) ]
        # i,j = self.posAgent
        # self.__XXX[i][j] = 1
        # ajoute à l'agent un compteur de pièces nettoyées, initalisé à 0
        # self.agent.nettoyage = 0
        self.__visitees = [ [0 for j in range(len(self.table[0]))] for i in range(len(self.table)) ]
        i,j = self.posAgent
        self.__visitees[i][j] = 1
        self.agent.nettoyage = 0
        # On regarde si l'agent a une commande reset
        if hasattr(self.agent,'reset') and callable(self.agent.reset):
            self.agent.reset() 
        
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
        _d = [ (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (0,0) ]
        _rep = [ ]
        nbl,nbc = len(self.table),len(self.table[0])
        for x in capteurs:
            nx = self.posAgent[0]+_d[x][0]
            ny = self.posAgent[1]+_d[x][1]
            if nx in range(nbl) and ny in range(nbc):
                _rep.append( self.table[nx][ny] )
            else:
                _rep.append( -1 )
        return _rep
        
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
        i,j = self.posAgent
        _reward = -1
        if choix == 'Aspirer' and self._table[i][j] != 1 : _reward = 0
        elif choix == 'Aspirer' and self._table[i][j] == 1:
            _reward = 2
            self.agent.nettoyage += 1
            self._table[i][j] = 0
        elif choix == 'Gauche' and j > 0 :
            _reward = 1
            j -= 1
        elif choix == 'Droite' and j < len(self.table[0]) -1:
            _reward = 1
            j += 1
        else: _reward = -1
        
        self.__visitees[i][j] += 1
        self._pos = (i,j)
        
        return _reward
    
    @property
    def perfGlobale(self):
        # return nombre de pièces nettoyées − nombre de pièces visitées 3 fois ou plus
        _c = 0
        nbl,nbc = len(self.table),len(self.table[0])
        for i in range(nbl):
            for j in range(nbc):
                if self.__visitees[i][j] > 2: _c += 1
        if hasattr(self.agent,'nettoyage'):
            return self.agent.nettoyage - _c
        else: raise AttributeError("agent has no attribut nettoyage")

