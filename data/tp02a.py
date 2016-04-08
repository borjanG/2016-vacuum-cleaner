#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "Mise en place du TP02a"
__author__ = "mmc, Terral, Rodriguez, Geshkovski"
__date__ = "22.03.16"
__version__ = "0.1"

from data.monde import objetsStatiques, Aspirateur, Monde
from data.briques import ProgramGenetic, GeneratePercept
import copy, random

plagiatUnaire = {'A': "Aspirer", 'D': "Droite", 'G': "Gauche", 'R': "Repos"}
# objetsStatiques[-1] = ("erreur", "?")
# objetsStatiques[2] = ("station", '$')
objetsStatiques = {100: ('Aspirateur','@'), 0: ('rien',' '), 1: ('poussiere',':'),
-1:("erreur", "?"),2:("station", '$')}
objetsStatiques_pasCapteurs={100: ('Aspirateur','@'), 0: ('rien',' '), 1: ('poussiere',':'),
-1:("erreur", "?")}

#cd pdf tp02a : aspi sans capteur : pas de prise?

class Aspirateur_PG(Aspirateur):
    """
        prog: un programme genetique, par défaut None
        gp: un GeneratePercept, par défaut None
        lCap: valeur par défaut []
    """
    def __init__(self, prog = None, gp = None, lCap = []):
        # assert isinstance(lCap, list), "I'm blind!"
        # assert lCap in {[6,8], [8,2], [6,8,2]}, "I'm hallucinating!"
        # assert len(set(lCap)) == len(lCap), "I'm astygmatic!"

        if gp is not None: self.__stock = gp
        elif lCap == []: self.__stock = None
        else: self.__stock = GeneratePercept(lCap, objetsStatiques)
        if prog is None:
            if lCap == []: self.__chromosome = ProgramGenetic(1, 8, "A G D R".split(), plagiatUnaire)
            else:
                # decode = dict()
                # for p in range(self.__stock.howMany):
                #     _ = random.choice("A G D R".split())
                #     decode[_] = plagiatUnaire[_]
                # self.__chromosome = ProgramGenetic(1, 8, "A G D R".split(), decode) 

                self.__chromosome = ProgramGenetic(1, self.__stock.howMany, "A G D R".split(), plagiatUnaire) 
        elif isinstance(prog, ProgramGenetic):
            if lCap != []:
                assert (len(prog) == self.__stock.howMany), "pas compatible"
            self.__chromosome = prog
        else:
            raise AssertionError("{} expected got {}"
                                 .format(ProgramGenetic, type(prog)))
        lAct = list(self.__chromosome.actions)
        super().__init__(lCap, lAct)
        self.__energy = 100
        self.__cpt = 0
        # self.__cptalive = 0 #inutile car on appelle reset
        self.reset()

    def reset(self):
        """ initialisation de certaines variables pour chaque simulation """
        self.vivant = True
        self.cpt = 0
        self.repos = 0
        self.energie = 100
        self.__cptalive = 0
        
    @property 
    def stock(self): return self.__stock
    @property
    def energie(self): return self.__energy
    @energie.setter
    def energie(self,v):
        assert isinstance(v, int), "int expected found {}".format(type(v))
        self.__energy = max(0, min(100, v)) # force la valeur entre 0 et 100
        if self.__energy == 0:
            self.vivant = False

    @property
    def vivant(self): return self.__vivant
    @vivant.setter
    def vivant(self, v):
        if isinstance(v, bool): self.__vivant = v

    @property
    def cpt(self): return self.__cpt
    @cpt.setter
    def cpt(self, v):
        assert isinstance(v,int)
        self.__cpt = min(max(0,v % len(self.program)),len(self.program)-1)
        
    @property
    def nbTours(self): 
        """ renvoie le nombre d'itérations pendant lesquelles aspi est vivant """
        return self.__cptalive

    @property
    def program(self): return self.__chromosome

    def getEvaluation(self):
        """ renvoie l'évaluation de l'agent """

        # score = (self.nettoyage / self.dirty) * 10 if self.dirty != 0 else self.nettoyage * 10
        
        score = (self.nettoyage / self.dirty) * 10 if self.dirty != 0 else 0
        index = int(self.energie / 25)
        index=min(index,3) ###########
        link = [1/2 * self.energie / 100, 2/3 * self.energie / 100, 3/4 * self.energie / 100, self.energie / 100]
        if not self.vivant: score -= 100
        else: score += link[index]
        return score

        # score = (self.nettoyage / self.dirty) * 10 if self.dirty != 0 else 0
        # if not self.vivant:
        #     score -= 100;ener=-100
        # elif self.energie < 25 : score += 1/2 * self.energie / 100;ener=1/2 * self.energie / 100
        # elif self.energie < 50 : score += 2/3 * self.energie / 100;ener=2/3 * self.energie / 100
        # elif self.energie < 75 : score += 3/4 * self.energie / 100;ener=3/4 * self.energie / 100
        # else: score += self.energie / 100;ener=self.energie / 100
        # return score

    def getDecision(self, percepts):
        """ deux cas à traiter suivant que percepts = [] ou pas """

        if self.vivant:#pas vraiment besoin de tester au final, si?
            self.__cptalive += 1 
        if percepts == []:
            return self.program.decoder(self.cpt)
        #return self.program[self.__stock.find(percepts)]
        return self.program.decoder(self.__stock.find(percepts))

class Monde_AG(Monde):
    def __init__(self, agent, nbLignes = 1, nbColonnes = 2):
        assert hasattr(agent,'energie'), "attribut 'energie' is required"
        super().__init__(agent,nbLignes,nbColonnes)
        self.__lignes = nbLignes
        self.__cols = nbColonnes
        self.optimumTheorique = 10

    def initialisation(self):
        super().initialisation()
        self.agent.nettoyage = 0
        self.agent.repos = 0

        self._posAgent = (random.randrange(self.__lignes), random.randrange(self.__cols))
        _ = list(set(objetsStatiques.keys()).intersection(range(100)))
        _.remove(2)
        self._table = [[random.choice(_) for j in range(self.__cols)] for i in range(self.__lignes)]

        if self.__cols > 3:
            liste = [(i,j) for i in range(self.__lignes) for j in range(self.__cols)]
            for i in range(3):
                elem = random.choice(liste)
                l,c = elem
                self._table[l][c] = 2
                liste.remove(elem)
        
        self.agent.dirty = sum(self.table, []).count(1)

        self.__historique = [] #on ne peut pas le faire d ici. de tte facon deja fait dans initialisation
        #de la classe mere

        if hasattr(self.agent,'reset') and callable(self.agent.reset):
            self.agent.reset()
 
    def getPerception(self, capteurs):
        """ informe l'agent en fonction des capteurs """
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
        if len(self.agent.capteurs) == 0: 
            energedic = {'Aspirer' : -5, 'Gauche' : -1, 'Droite': -1, 'Repos': (3, 3)}
        else: energedic = {'Aspirer' : -5, 'Gauche' : -1, 'Droite': -1, 'Repos': (0, 20)}
        self.agent.energie += energedic[choix] if choix != 'Repos' else energedic[choix][1 if self._table[dx][dy] == 2 else 0] 
    
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
            if len(self.agent.capteurs) == 0:
                score = 0
            else:
                if self._table[dx][dy] == 2:
                    score = 2
                else:
                    score = 0
            self.agent.repos += 1

        i, j = self.posAgent
        if self.agent.capteurs == []: 
            self.agent.cpt +=1
            # self.agent.cpt = (self.agent.cpt + 1) % len(self.agent.program)
        return score

    @property
    def perfGlobale(self):
        return self.agent.getEvaluation()/self.optimumTheorique - self.agent.repos + self.__lignes*self.__cols
