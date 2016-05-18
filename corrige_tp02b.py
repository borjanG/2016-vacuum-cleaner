#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mise en place de la correction en fonction du descriptif TP02-B
"""

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__version__ = "0.1"
__date__ = "14.03.16"
__usage__ = "Le simulateur"

# remplacer XXX par le fichier du TP02-A
from corrige_tp02a import objetsStatiques, Aspirateur_PG, Monde
from briques import ProgramGenetic, mmcUnaire, mmcBinaire, GeneratePercept
from tools_tp02 import readerEnvts
import copy, random
from fractions import Fraction

# On ajoute dans objetsStatiques 2, 3 et 4 et -1
objetsStatiques[2] = ('prise électriques', 'p')
objetsStatiques[3] = ('jouet aspirable', 'j')
objetsStatiques[4] = ('jouet déplaçable', 'J')
objetsStatiques[-1] = ('erreur','?')

class MondeSimulation(Monde):
    def __init__(self,agent,nbLignes=1,nbColonnes=2):
        assert hasattr(agent,'energie'), "attribut 'energie' is required"
        super().__init__(agent,nbLignes,nbColonnes)

    def simulation(self,n,envt=None,position=None):
        """ 
            la simulation dure max n tours et s'arrete des que l'agent 
            n'est plus opérationnel
        """
        self.initialisation(envt,position)
        self.__nbMaxIter = n # utilisee dans perfGlobale
        i = 0
        while i < n and self.agent.vivant :
            self.step()
            i+= 1
        return self.perfGlobale

    def initialisation(self,envt=None,position=None):
        super().initialisation()
        if envt is not None: self._table = [ envt ]
        if position is not None: self._pos = 0,position
            
        #variables ajoutées sur l'agent
        self.agent.nettoyage = 0
        sales = [ self.table[i].count(1) for i in range(len(self.table)) ]
        jouets_avant = [ self.table[i].count(3)
                         for i in range(len(self.table)) ]
        self.__pieces_sales = sum(sales)
        self.__jouets_avant = sum(jouets_avant)
        #print(self.table)
        if hasattr(self.agent,'reset') and callable(self.agent.reset):
            self.agent.reset() 
        
    @property
    def perfGlobale(self):
        """ calcul en accord avec TP02-B """
        #input("sales {}, jouets {}, maxIter {}".format(self.__pieces_sales,
        #        self.__jouets_avant, self.__nbMaxIter))
        if len(self.historique) == 0: 
            print("{} has trouble energie = ".format(self.agent.__class__.__name__),self.agent.energie)
            return 0.
        assert self.__nbMaxIter != 0, "{} has trouble maxIter undef".format(self.agent.__class__.__name__)
        nbRepos = [act for ((_,_),act) in self.historique ].count('Repos')
        nbAct = len(self.historique)
        nbTours = len(self.historique)
        jouets_apres = sum([ self.table[i].count(3)
                            for i in range(len(self.table)) ])
        if self.__jouets_avant == 0: jouets = 0
        else: jouets = jouets_apres / self.__jouets_avant
        if self.__pieces_sales == 0: pieces = 0
        else: pieces = self.agent.nettoyage / self.__pieces_sales            
        return (self.agent.energie / 100 +
                pieces -
                nbRepos / nbAct +
                jouets +
                nbTours / self.__nbMaxIter)

    def getPerception(self,capteurs):
        """ 
           informe l'agent en fonction des capteurs 
           gestion des risques de panne (proba fixée à .1) 1 parmi k
        """
        _d = [ (-1,0), (-1,1), (0,1), (1,1),
                (1,0), (1,-1), (0,-1), (-1,-1), (0,0) ]

        kapteurs = capteurs[:]
        if 8 in kapteurs: kapteurs.remove(8)
        _panne = -1 # pas de panne
        if (hasattr(self.agent,'panne') and
            getattr(self.agent,'panne') and
            len(kapteurs) > 0):
            _proba = random.random()
            if _proba < .1 : _panne = random.choice(kapteurs)

        # décommenter la ligne suivante pour avoir un suivi des pannes
        #if _panne > -1: print("panne sur le capteur {}".format(_panne))
        _rep = [ ]
        i,j = self.posAgent
        nbl,nbc = len(self.table),len(self.table[0])
        for x in capteurs:
            nx = i + _d[x][0]
            ny = j + _d[x][1]
            if nx in range(nbl) and ny in range(nbc):
                if x != _panne: _rep.append( self.table[nx][ny] )
                else: _rep.append( -1 )
            else:
                _rep.append( -1 )
        return _rep

    def applyChoix(self,choix):
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

        i,j = self.posAgent
        if choix == 'Aspirer':
            _enRj = -5
            if self.table[i][j] == 1:
                _rew = 2
                self._table[i][j] = 0
                self.agent.nettoyage += 1
            elif self.table[i][j] == 3:
                _rew = -3
                self._table[i][j] = 0
            else: _rew = -1
                
        elif choix == 'Gauche':
            _enRj = -2
            if j > 0 and self.table[i][j-1] == 4:
                if j-1 > 0 and self.table[i][j-2] == 0:
                    # On peut le faire
                    self._table[i][j-2] = 4
                    self._table[i][j-1] = 0
                    j -= 1 # action acceptée
                    _rew = 1
                else: # soit au bord, soit qque chose derriere
                    _rew = -1
            elif j > 0:
                # On peut le faire
                j -= 1 # action acceptée
                _rew = 1
            else: # on est au bord
                _rew = -1
                
        elif choix == 'Droite':
            _enRj = -2
            _max = len(self.table[0]) - 1
            if j < _max and self.table[i][j+1] == 4:
                if j+1 < _max and self.table[i][j+2] == 0:
                    # On peut le faire
                    self._table[i][j+2] = 4
                    self._table[i][j+1] = 0
                    j += 1 # action acceptée
                    _rew = 1
                else: # soit au bord, soit qque chose derriere
                    _rew = -1
            elif j < _max:
                # On peut le faire
                j += 1 # action acceptée
                _rew = 1
            else: # on est au bord
                _rew = -1
                    
        elif choix == 'Repos':
            # effet energie
            if self.agent.capteurs == []: _enRj = 3
            elif self.table[i][j] == 2: _enRj = 20
            else: _enRj = 0
            # effet récompense
            if self.table[i][j] == 2: _rew = 2
            else: _rew = 0


        self._pos = i,j # met à jour la position
        self.agent.energie += _enRj # met à jour l'énergie
        return _rew # renvoie la récompense

class Simulateur(object):
    """ En entrée:
        - le nombre maximum d'itérations
        - le fichier des environnements
        - la liste des Capteurs
        - le fait qu'il peut y avoir des pannes
    """
    def __init__(self,nbMaxIter,ficEnvt,lCap=[],panne=False):
        self.__nbMaxIter = nbMaxIter
        self.__envt = readerEnvts(ficEnvt)
        self.__lcap = lCap
        self.panne = panne

    @property
    def panne(self): return self.__panne
    @panne.setter
    def panne(self,v):
        if self.__lcap == []: self.__panne = False
        else: self.__panne = bool(v)

    def run(self,prog,gp=None):
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
        on aurait pu prendre non pas le score de la simulation mais
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
        aspi = Aspirateur_PG(prog,gp,self.__lcap)
        aspi.panne = self.panne
        _total = 0
        # détermination de l'ensemble des typ_ admis en fonction de __lcap
        _ltyp = [0,1,2]
        if aspi.capteurs == []: _ltyp.remove(1)
        else: _ltyp.remove(0)
        for e in self.__envt.values():
            _typ,_nbCol,_table,_lpos = e
            if _typ not in _ltyp: continue
            m = MondeSimulation(aspi,1,_nbCol)
            for p in _lpos:
                _total += m.simulation(self.__nbMaxIter,_table,p)
        return _total
