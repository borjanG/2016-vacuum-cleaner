#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mise en place de la correction en fonction du descriptif TP02-B
Complétez les informations en fonction des directives de la fiche
"""

__author__ = "mmc, Terral, Rodriguez, Geshkovski"
__version__ = "0.1"
__date__ = "09.04.16"
__usage__ = "Le simulateur"

# remplacer XXX par le fichier du TP02-A
from data.tp02 import objetsStatiques, Aspirateur_PG, Monde
#from corrige_tp02a import objetsStatiques, Aspirateur_PG, Monde
from briques import ProgramGenetic, mmcUnaire, mmcBinaire, GeneratePercept
from tools_tp02 import readerEnvts
import copy, random

# On ajoute dans objetsStatiques 2, 3 et 4 et -1
objetsStatiques[-1] = ("erreur", "?")
objetsStatiques[2] = ("station", "$")
objetsStatiques[3] = ("objet aspirable", "j")
objetsStatiques[4] = ("objet deplacable", "J")

class MondeSimulation(Monde):
    def __init__(self, agent, nbLignes=1, nbColonnes=2):
        assert hasattr(agent,'energie'), "attribut 'energie' is required"
        super().__init__(agent,nbLignes,nbColonnes)
        self.agent = agent

    def simulation(self, n, envt=None, position=None):
        """ 
            la simulation dure max n tours et s'arrete des que l'agent 
            n'est plus opérationnel
        """
        # A verifier, pas sur
        # assert n == 20 if len(self.agent.capteurs) = 0 else n = len(self.agent.program)
        self.max_tours = n

        self.initialisation(envt,position)
        while self.agent.vivant and n > 0:
            self.step()
            n-=1
        return self.perfGlobale

    def initialisation(self, envt=None, position=None):
        super().initialisation()
        self.aspirables_avant = [x for sousliste in self.table for x in sousliste].count(3)
        if envt is not None: self._table = [ envt ]
        if position is not None: self._pos = 0, position

        #variables ajoutées sur l'agent
        self.agent.nettoyage = 0
        self.agent.repos = 0
        self.agent.dirty = sum(self.table, []).count(1)
        # print(self.table) facultatif
        if hasattr(self.agent,'reset') and callable(self.agent.reset):
            self.agent.reset() 
        
    @property
    def perfGlobale(self):
        self.aspirables_apres = [x for sousliste in self.table for x in sousliste].count(3)
        return self.agent.energie/100 + self.agent.nettoyage/self.agent.dirty - self.agent.repos/len(self.agent.actions) + self.aspirables_apres/self.aspirables_avant + self.agent.nbTours/self.max_tours
        # Voir fiche TP02-B
        
    def getPerception(self,capteurs):
        """ 
           informe l'agent en fonction des capteurs 
           gestion des risques de panne (proba fixée à .1) 1 parmi k
        """
        _d = [ (-1,0), (-1,1), (0,1), (1,1),
                (1,0), (1,-1), (0,-1), (-1,-1), (0,0) ]

        kapteurs = capteurs[:] # on fait une copie pour les pannes
        if 8 in kapteurs: kapteurs.remove(8) # pas de panne sur le 8
        _panne = -1 # pas de panne
        if (hasattr(self.agent,'panne') and
            getattr(self.agent,'panne') and
            len(kapteurs) > 0):
            _proba = random.random()
            if _proba < .1 : _panne = random.choice(kapteurs)

        res = []
        for x in kapteurs:
            nx = self.posAgent[0] + _d[x][0]
            ny = self.posAgent[1] + _d[x][1]
            if self.__lignes > nx >= 0 and self.__cols > ny >= 0: 
                res.append(self.table[nx][ny])
            else: 
                res.append(-1)
        if _panne > -1: 
            res[_panne] = -1
            print("panne sur le capteur {}".format(_panne))
        return res

        # calculer ce que voit l'agent, s'il y a une panne sur le capteur
        # _panne : mettre -1 au lieu de l'information dans la table
        # renvoyer la réponse (une liste de la taille de capteurs)
        
    def applyChoix(self, choix):
        """
           Modifie table & posAgent en fonction de choix
           Modifie la fonction d'énergie de l'Aspirateur
           Renvoie la récompense numérique adéquate

           Récompenses :
           Aspirer : 2 si poussière, -3 si jouets aspirables, -1 sinon
           Gauche / Droite : 1 si possible, -1 sinon
           Repos : 2 si prise électrique, 0 sinon

           Effet Energie
           Aspirer: -5
           Gauche / Droite : -2
           Repos sans capteur +3
           Repos avec capteur +20 si prise électrique, 0 sinon
        """
        dx = self.posAgent[0]
        dy = self.posAgent[1]
        score = 0
        energedic = dict()          #Ha ha ha

        if len(self.agent.capteurs) == 0: energedic = {'Aspirer' : -5, 'Gauche' : -1, 'Droite': -1, 'Repos': (3, 3)}
        else: energedic = {'Aspirer' : -5, 'Gauche' : -1, 'Droite': -1, 'Repos': (0, 20)}

        self.agent.energie -= energedic[choix] if choix != 'Repos' else energedic[choix][1 if self._table[dx][dy] == 2 else 0] 
        if choix == 'Aspirer':
            if self.table[dx][dy] == 1:
                self._table[dx][dy] = 0
                self.agent.nettoyage += 1
                score = 2
            if self.table[dx][dy] == 3:
                self._table[dx][dy] = 0
                #score = ?
            else: score = -1
        elif choix == 'Gauche':
            if dy > 0: 
                if self.table[dx][dy-1] == 4:
                    if dy > 1 and self.table[dx][dy-2] == 0:
                        self._table[dx][dy-1] = 4
                        self._posAgent = (dx, dy-1)
                    else: score = -1
                else:
                    self._posAgent=(dx, dy-1)
                    score = 1
            else: score = -1
        elif choix == 'Droite':
            if dy < self.__cols-1:
                if self.table[dx][dy+1] == 4:
                    if dy < self.cols - 2 and self.table[dx][dy+2] == 0:
                        self._table[dx][dy+1] = 4
                        self._posAgent = (dx, dy+1)
                else: 
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
        self.agent.cpt = (self.agent.cpt + 1) % len(self.agent.chromosome)

        if self.agent.vivant:
            self.agent.__cptalive += 1 
        return score
        # Appliquer les opérations demandées
        # mise à jour de self.agent.energie
        # renvoie de la récompense
        # mise à jour des compteurs utiles

class Simulateur(objet):
    """ En entrée:
        - le nombre maximum d'itérations
        - le fichier des environnements
        - la liste des Capteurs
        - le fait qu'il peut y avoir des pannes
    """
    def __init__(self, nbMaxIter, ficEnvt, lCap=[], panne=False):
        self.__nbMaxIter = nbMaxIter
        self.__ficEnvt = ficEnvt
        self.__lCap = lCap
        self.__panne = panne
        # stocker les parametres dans 4 variables privées self.__XXX

    @property
    def panne(self): return self.__panne
    @panne.setter
    def panne(self, v):
        """
           si pas de capteur on se moque de v, on force xxx à False
           si capteur alors on prend bool(v) comme valeur
        """
        if len(self.__lCap) == 0: self.__panne = False
        else: self.__panne = bool(v) 

    def run(self, prog, gp=None):
        """
        prog est un ProgramGenetic
        gp est un GeneratePercept optionnel
        
        crée l'aspirateur Aspirateur_PG
        ajoute l'information panne à l'aspirateur
        met un compteur a 0
        détermine quels environnements seront utilisables 0, 1, 2
        pour chaque environnement
             s'il n'est pas utilisable : continue
             creer m = MondeSimulation(aspirateur,1,nbCol)
             pour chaque position a tester
                 compteur = compteur + m.simulation(nbIter,table,position)
        renvoyer compteur
        
        renvoie le score total obtenu pour chaque simulation,
        on aurait pu prendre non pas le score de la imulation mais
        celui de la performance de l'agent ou une combinaison des deux
            exemple: alpha perfGlobale + beta getEvaluation()
            total_sim = 0 ; total_agent = 0
            alpha = .5 ; beta = 1 - alpha
            ....
            for p in _lpos:
                total_sim += m.simulation( .... )
                total_agent += m.agent.getEvaluation()
            ...
            return alpha * total_sim + beta * total_agent
        """
        asp = Aspirateur_PG(prog, gp, self.__lCap)
        asp.panne = self.panne
        cpt = 0
        if len(self.__lCap) == 0: 
            mondes_ok = (0,2)
        else:
            mondes_ok = (1,2)

        with open(self.__ficEnvt,'r') as fic:
            for ligne in fic:
                data = ligne.split('')
                teep = data[0]
                if teep in mondes_ok:
                    nbCol = data[1]
                    objets = [data[2:2+nbCol]]
                    positions = [data[2+nbCol:]]
                    m = MondeSimulation(asp, 1, nbCol)
                    for x in positions:
                        cpt += m.simulation(self.__nbMaxIter, objets, x)
        return cpt






