#Custom libs
from data.aspirateur import Aspirateur
#Generic python libs
from random import randrange
from copy import deepcopy

__author__ = "Terral, Rodriguez, Geshkovski"
__date__ = "29.01.16"
__version__ = "0.2"

#Global variable (?)
objetsStatiques = {100: ('aspirateur', '@'),
                   0: ('rien', ' '),
                   1: ('poussiere', ':')}
                   #2: ('inamovible','+')}

class Monde(object):

  def __init__(self, a, l=1, c=2):
    """ Monde constructor """

    assert isinstance(a, Aspirateur), "il faut un Stochy en parametre"
    
    self.__agent = a 
    self.__lignes = l
    self.__cols = c
    self.__table = [[0 for j in range(c)] for i in range(l)]
    self.__posAgent = (0,0)
    self.__historique = []
    self.__perfGlobale = 0.0


  #Deepcopy car hash table & liste de listes
  @property 
  def objetsStatiques(self):
    return deepcopy(objetsStatiques)
  @property
  def table(self):
    return deepcopy(self.__table)
  @property 
  def posAgent(self):
    #Shallow copy suffit
    return self.__posAgent[:]
  @property 
  def agent(self):
    return self.__agent 
  @property 
  def historique(self):
    return deepcopy(self.__historique)
  @property 
  def perfGlobale(self):
    return self.__perfGlobale


  def applyChoix(self, action):

    if action == "Gauche":
      if 0 < self.posAgent[1]:
        if self.table[self.posAgent[0]][self.posAgent[1]-1] == 2:
          pass
        else:
          self.__posAgent = (self.posAgent[0], self.posAgent[1]-1)
      else:
        pass

    if action == "Droite":
      if self.__cols > self.posAgent[1]:
        if self.table[self.posAgent[0]][self.posAgent[1]+1] == 2:
          pass
        else:
          self.posAgent = self.posAgent(self.posAgent[0], self.posAgent[1]+1)
      else:
        pass

    if action == "Aspirer":
      if self.table[self.posAgent[0]][self.posAgent[1]] == 1:
        self.__table[self.posAgent[0]][self.posAgent[1]] = 0
      else:
        pass

    return 0.0 

  def getPerception(self, capteurs = []):
    return []

  def __str__(self):
    """ Generic string method
        Unicode:
        \u2550: ═ ; \u2564: ╤
        \u2500: ─ ; \u253C: ┼
        \u2567: ╧ ; \u2554: ╔
        \u2557: ╗ ; \u2551: ║
        \u255A: ╚ ; \u255D: ╝
    """

    tab = []
    key = max(self.objetsStatiques.keys()) #Pas plus de 100 keys qd meme

    #Genere le tableau
    for i in range(len(self.table)):
      tab.append([])
      for j in range(len(self.table[0])):
        tab[i].append(self.objetsStatiques[self.table[i][j]][1])
    tab[self.posAgent[0]][self.posAgent[1]] += self.objetsStatiques[key][1]
    # tab[self.posAgent[0]][self.posAgent[1]] = self.objetsStatiques[key][1]

    l = len(tab)
    c = len(tab[0])
    _=[]

    #Strings utiles
    _head = "\u2550"*3 + "\u2564"
    _mid = "\u2500"*3 + "\u253C"
    _foot = "\u2550"*3 + "\u2567"

    header = "\u2554" +_head*(c-1) + "\u2550"*3 + "\u2557"
    middle = "\u2551" +_mid*(c-1) + "\u2500"*3 + "\u2551"
    footer = "\u255A" +_foot*(c-1) + "\u2550"*3 + "\u255D"

    #Header
    _.append(header)

    #Middle
    #Ligne 0
    _elt = "\u2551" + "%3s" %(tab[0][0]) #Premier element
    if c > 1:
      for j in range(1, c):
        _elt += "\u2502" + "%3s" %(tab[0][j])
    _elt += "\u2551"
    _.append(_elt)

    #Autres lignes (s'il y en a)
    if l > 1:
      for i in range(1, l):
        _.append(middle)
        _elt = "\u2551" + "%3s" %(tab[i][0]) #ligne i col 0
        if c > 1:                  #autres cols s'il y en a
          for j in range(1, c):
            _elt += "\u2502" + "%3s" %(tab[i][j])
        _elt += "\u2551"
        _.append(_elt)

    #Footer      
    _.append(footer)
    
    return "\n".join(_)

  def step(self):
    """ """

    percept = self.getPerception(self.agent.capteurs)
    choix = self.agent.getDecision(percept)
    self.agent.setReward(self.applyChoix(choix))
    self.updateWorld()
    self.__historique.append(((self.agent.posAgent, self.agent.table), choix))

  def simulation(self, n = 42):
    """ """

    self.initialisation()
    while self.agent.vivant and n > 0:
      self.step()
      perfGlobale += 0
      n-=1
    self.__historique = []
    self.agent.setReward(perfGlobale)
    return perfGlobale 


  def initialisation(self):
    """ Initialisation du monde """
    self.__posAgent = (randrange(self.__lignes), randrange(self.__cols))
    self.__table = deepcopy([[randrange(len(self.objetsStatiques)-1)
                              for j in range(self.__cols)]
                              for i in range(self.__lignes)])

  def updateWorld(self):
    #Agit sur table 
    pass 


