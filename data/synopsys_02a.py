#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "Mise en place du TP02a"
__date__ = "10.03.16"
__version__ = "0.1"

# remplacer XXX par votre fichier issu du TD2 (le 00a)
#from XXX import objetsStatiques, Aspirateur, Monde
from data.monde import objetsStatiques, Aspirateur, Monde
from briques import ProgramGenetic, mmcUnaire
import copy, random, functools

class Aspirateur_PG(Aspirateur):
    """
        lCap: valeur par défaut []
        prog: un programme genetique, par défaut None
    """
    def __init__(self,prog=None,lCap=[]):
        if prog is None:
            # choisir le nom de votre variable, remplacez les ...
            self.__chromosome = ProgramGenetic(1, 8, "A G D R".split(), mmcUnaire)
        elif isinstance(prog,ProgramGenetic):
            self.__chromosome = prog
        else:
            raise AssertionError("{} expected got {}"
                                 .format(ProgramGenetic,type(prog)))
        # récupération des actions depuis votre variable
        # attention ce n'est pas une 'list' c'est un 'set'
        lAct = set(self.actions)
        super().__init__(lCap,lAct)
        # choisir la variable pour energie
        self.__energy = 100
        self.__cpt = 0
        self.reset()

    def reset(self):
        """ initialisation de certaines variables pour chaque simulation """
        self.vivant = True
        self.cpt = 0
        self.repos = 0
        # ici rajouter celles dont vous pensez avoir besoin
        
    @property
    def energie(self): return self.__energy
    @energie.setter
    def energie(self,v):
        assert isinstance(v,int), "int expected found {}".format(type(v))
        self.__energy = max(0,min(100,v)) # force la valeur entre 0 et 100
        if self.__energy == 0:
            self.vivant = False

    # On surcharge vivant
    @property
    def vivant(self): return self.__vivant
    @vivant.setter
    def vivant(self,v):
        if isinstance(v,bool): self.__vivant = v

    @property
    def cpt(self): return self.__cpt
    @cpt.setter
    def cpt(self,v):
        assert isinstance(v,int)
        self.__cpt = min(0, max(self.__cpt, len(program))) # attention cpt est contraint entre 0 et le nombre de genes
        
    @property
    def program(self): return self.__chromosome

    def getEvaluation(self):
        """ renvoie l'évaluation de l'agent """

        score = (self.nettoyage / self.dirty) * 10
        if not self.vivant:
            score -= 100
        elif self.energie < 25 : score += 1/2 * self.energie / 100
        elif self.energie < 50 : score += 2/3 * self.energie / 100
        elif self.energie < 75 : score += 3/4 * self.energie / 100
        else: score += self.energie / 100
        return score

    def getDecision(self,percepts):
        """ deux cas à traiter suivant que percepts = [] ou pas """
        if percepts == []:
            # on utilise cpt pour savoir ce qu'il faut lire/récupérer
            return
        # a partir d'ici on est dans le cas ou l'agent percoit
        # il faut associer au percepts un numéro et aller regarder
        # quelle est l'instruction à renvoyer

        return


class Monde_AG(Monde):
    def __init__(self,agent,nbLignes=1,nbColonnes=2):
        # On regarde si l'agent à une variable energie
        assert hasattr(agent,'energie'), "attribut 'energie' is required"
        super().__init__(agent,nbLignes,nbColonnes)
        self.__lignes = nbLignes
        self.__cols = nbColonnes
        self.optimumTheorique = 0
    
    def initialisation(self):
        super().initialisation()
        # ajouter à l'agent un compteur de pièces nettoyées, initalisé à 0
        self.agent.nettoyage = 0
        self.agent.repos = 0
        # ajouter à l'agent le nombre de pièces sales au départ
        #3 methodes:
        self.agent.dirty = sum(self.table, []).count(1)
        # self.agent.dirty = functools.reduce(lambda x, y: x+y, self.table).count(1)
        # self.agent.dirty = [x for sousliste in self.table for x in sousliste].count(1)

        # On regarde si l'agent a une commande reset
        if hasattr(self.agent,'reset') and callable(self.agent.reset):
            self.agent.reset()

 
  def getPerception(self,capteurs):
        """ informe l'agent en fonction des capteurs """
        # code similaire à celui de World
        delta = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (0,0)]
        res = []
        for x in capteurs:
            nx = self.posAgent[0] + delta[x][0]
            ny = self.posAgent[1] + delta[x][1]
            if self.__lignes > nx >= 0 and self.__cols > ny >= 0: 
                res.append(self.table[nx][ny])
            else: 
                res.append(-1)
        return res

   def applyChoix(self,choix):
        """ 
            modifie table & posAgent en fonction de choix 
            modifie l'energie de l'aspirateur
        """
        dx = self.posAgent[0]
        dy = self.posAgent[1]
        score = 0
        energedic = dict()          #Ha ha ha

        if len(self.capteurs) == 0:
            energedic = {'Aspirer' : 5, 'Gauche' : 1, 'Droite': 1, 'Repos': 3}
        else:
            energedic = {'Aspirer' : 5, 'Gauche' : 1, 'Droite': 1, 'Repos': (0, 20)}

        #Borjan (mode Schlickienne)
        self.agent.energie = energedic[choix] if choix != 'Repos' else energedic[choix][1 if self._table[dx][dy] == 2 else 0] 

        #Charlotte
        # if choix != 'Repos': self.agent.energie = energedic[choix]
        # else:
        #     idx = 1 if self._table[dx][dy] == 2 else 0
        #     self.agent.energie = energedic[choix][idx]

        if choix == 'Aspirer':
            if self.table[dx][dy] == 1:
                self._table[dx][dy] = 0
                self.agent.nettoyage += 1
                score = 2
            else: score = -1
        elif choix == 'Gauche':
            if dy > 0: 
                self._posAgent = (dx, dy-1)
                score = 1
            else: score = -1
        elif choix == 'Droite':
            if dy < self.__cols-1: 
                self._posAgent = (dx, dy+1)
                score = 1
            else: score = -1
        else:
            if len(self.capteurs) == 0:
                score = 0
            else:
                if self._table[dx][dy] == 2:
                    score = 2
                else:
                    score = 0
            self.agent.repos += 1

        i, j = self.posAgent
        self._passage[i][j] += 1  
        return score

        # code similaire à World une action en plus Repos
        # nécessitant un traitement spécifique suivant que l'agent
        # dispose de capteurs ou pas (il suffit de poser la question
        # à self.agent)
        # Les récompenses ne sont pas les couts énergétiques
        # Aspirer 2 si poussière, -1 sinon
        # Gauche 1 si possible, -1 sinon
        # Droite 1 si possible, -1 sinon
        # Repos 0 pour l'aspirateur sans capteur
        # Repos 2 si prise électrique, 0 sinon
        # les couts energétiques sont appliqués par applyChoix
        # self.agent.energie est donc à mettre à jour

    @property
    def perfGlobale(self):
        # cf fiche TP02-A
        return agent.getEvaluation()/self.optimumTheorique - self.agent.repos + self.__lignes*self.__cols
