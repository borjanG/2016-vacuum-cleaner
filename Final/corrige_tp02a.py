#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "Mise en place du TP02a"
__date__ = "10.03.16"
__version__ = "0.1"

# remplacer XXX par votre fichier issu du TD2
#from XXX import objetsStatiques, Aspirateur, Monde
from corrige_tp00a import objetsStatiques, Aspirateur, Monde
from briques import ProgramGenetic, mmcUnaire, mmcBinaire, GeneratePercept
import copy, random
from fractions import Fraction

class Aspirateur_PG(Aspirateur):
    """
        prog: un programme genetique, par défaut None
        gp: un GeneratePercept, par défaut None
        lCap: valeur par défaut []
    """
    def __init__(self,prog=None,gp=None,lCap=[]):
        if gp is not None: self.__gp = gp
        elif lCap == []: self.__gp = None
        else: self.__gp = GeneratePercept(lCap,objetsStatiques)
        if prog is None:
            if lCap == []:
                self.__prog = ProgramGenetic(1,8,"AGDR",mmcUnaire)
            else:
                self.__prog = ProgramGenetic(1,self.__gp.howMany,
                                            "AGDR",mmcUnaire)
        elif isinstance(prog,ProgramGenetic):
            if self.__gp is not None:
                assert len(prog)==self.__gp.howMany,\
                  ("expected: {} found: {} 'prog' is not suitable"
                   .format(self.__gp.howMany,len(prog)))
            self.__prog = prog
        else:
            raise AssertionError("{} expected got {}"
                                 .format(ProgramGenetic,type(prog)))

        lAct = list(self.__prog.actions)
        super().__init__(lCap,lAct)
        self.__energy = 100
        self.reset()

    def reset(self):
        self.vivant = True
        self.cpt = 0
        self.__tour = 0

    @property
    def nbTours(self):
        """ permet de savoir combien de temps l'agent est resté vivant """
        return self.__tour
        
    @property
    def energie(self): return self.__energy
    @energie.setter
    def energie(self,v):
        #print("avt: {}, aprs: {}".format(self.energie,v))
        assert isinstance(v,int), "int expected found {}".format(type(v))
        self.__energy = max(0,min(100,v))
        if self.__energy == 0: self.vivant = False

    @property
    def vivant(self): return self.__alive
    @vivant.setter
    def vivant(self,v):
        if isinstance(v,bool): self.__alive = v

    @property
    def cpt(self): return self.__cpt
    @cpt.setter
    def cpt(self,v):
        assert isinstance(v,int)
        self.__cpt = v % len(self.__prog)
        
    @property
    def program(self): return self.__prog

    def getEvaluation(self):
        # On renvoie l'évaluation de l'agent
        # (nombre de pièces nettoyées + 1) / ( len(self.knowledge) + 1 )
        if hasattr(self,'nettoyage') and hasattr(self,'pieces_sales'):
            if self.pieces_sales == 0: _score = 0
            else: _score = (self.nettoyage / self.pieces_sales) * 10
        else:
            raise AttributeError("'nettoyage' or 'pieces_sales' missing")

        if not self.vivant: _score -= 100 ; _rho = 0
        elif self.energie < 25: _rho = Fraction(1,2)
        elif self.energie < 50: _rho = Fraction(2,3)
        elif self.energie < 75: _rho = Fraction(3,4)
        else: _rho = 1

        return _score + _rho * self.energie / 100
            
    def getDecision(self,percepts):
        self.__tour += 1 # aspi a survécu un tour de plus
        if percepts == []:
            _rep = self.program.decoder(self.cpt)
            self.cpt += 1
            return _rep

        return self.program.decoder(self.__gp.find(percepts))


class Monde_AG(Monde):
    def __init__(self,agent,nbLignes=1,nbColonnes=2):
        assert hasattr(agent,'energie'), "attribut 'energie' is required"
        super().__init__(agent,nbLignes,nbColonnes)
    
    def initialisation(self):
        super().initialisation()
        nbL = len(self.table)
        nbC = len(self.table[0])
        if self.agent.capteurs != []:
            if 2 not in objetsStatiques:
                objetsStatiques[2] = ('prise électrique','p')
                # on place 3 prises au hasard si nbC > 3
                if nbC > 3: _l = random.sample(range(nbC),3)
                else: _l = []
                for x in _l: self._table[0][x] = 2
            else:
                if nbL > 1:
                    for i in range(1,nbL):
                        for j in range(nbC):
                            if self._table[i][j] == 2: self._table[i][j] = 1
                else:
                    nbP = self.table[0].count(2)
                    nbR = self.table[0].count(0)
                    if nbP < 3 and nbR > 3 - nbP:
                        _me = lambda _: _ == 0
                    elif nbP < 3:
                        _me = lambda _: _ != 2
                    if nbP < 3 and nbC > 3:
                        for j in range(nbC):
                            if _me(self.table[0][j]):
                                self._table[0][j] = 2
                                nbP += 1
                            if nbP == 3: break
                    elif nbP > 3:
                        for j in range(nbC):
                            if self.table[0][j] == 2:
                                self._table[0][j] = 1
                                nbP -= 1
                            if nbP == 3: break
                        
        self.agent.nettoyage = 0
        sales = [ self.table[i].count(1) for i in range(len(self.table)) ]
        self.agent.pieces_sales = sum(sales)
        #print(self.table)
        if hasattr(self.agent,'reset') and callable(self.agent.reset):
            self.agent.reset() 

    def getPerception(self,capteurs):
        """ informe l'agent en fonction des capteurs """
        _d = [ (-1,0), (-1,1), (0,1), (1,1),
                (1,0), (1,-1), (0,-1), (-1,-1), (0,0) ]
            
        _rep = [ ]
        i,j = self.posAgent
        nbl,nbc = len(self.table),len(self.table[0])
        for x in capteurs:
            nx = i + _d[x][0]
            ny = j + _d[x][1]
            if nx in range(nbl) and ny in range(nbc):
                _rep.append( self.table[nx][ny] )
            else:
                _rep.append( -1 )
        return _rep

    def applyChoix(self,choix):
        """ 
            modifie table & posAgent en fonction de choix 
            modifie l'energie de l'aspirateur

            # Les récompenses ne sont pas les couts énergétiques
            # Aspirer 2 si poussière, -1 sinon
            # Gauche 1 si possible, -1 sinon
            # Droite 1 si possible, -1 sinon
            # Repos 0 pour l'aspirateur sans capteur
            # Repos 2 si prise électrique, 0 sinon

        """
        _couts = {
            'Aspirer': (-5,2,-1), # energie, reward_succes, reward_failure
            'Gauche': (-1,1,-1),
            'Droite': (-1,1,-1)
            }
        if self.agent.capteurs == [] :
            _couts['Repos'] = (3,0,0)
        else:
            _couts['Repos'] = (20,2,0)

        i,j = self.posAgent
        self.agent.energie += _couts[choix][0]
        if choix == 'Aspirer' and self._table[i][j] != 1 :
            _reward = _couts[choix][2]
        elif choix == 'Aspirer' and self._table[i][j] == 1:
            _reward = _couts[choix][1]
            self.agent.nettoyage += 1
            self._table[i][j] = 0
        elif choix == 'Gauche' and j > 0 :
            _reward = _couts[choix][1]
            j -= 1
        elif choix == 'Droite' and j < len(self.table[0]) -1:
            _reward = _couts[choix][1]
            j += 1
        elif choix == 'Repos':
            if self.agent.capteurs == []: _reward = _couts[choix][1]
            elif self.table[i][j] == 2: _reward = _couts[choix][1]
            else:
                _reward = _couts[choix][2]
                self.agent.energie -= _couts[choix][0]
        else: _reward = _couts[choix][2]

        self._pos = i,j
        return _reward
        
        
    @property
    def perfGlobale(self):
        nbRepos = [act for ((_,_),act) in self.historique ].count('Repos')
        return self.agent.getEvaluation() - nbRepos + len(self.table[0])


def restInPeace(hist):
    """ calcul le nombre de "Repos" présent dans hist """
    return [act for ((_,_),act) in hist ].count('Repos')

def displayHist(hist):
    """ affiche position action """
    for ((_,p),a) in hist:
        print("position: {} action: {}".format(p,a))

if __name__ == "__main__":

    a = Aspirateur_PG(lCap=[6,8,2])
    m = Monde_AG(a,1,15)

    print(objetsStatiques)
    print(m)
