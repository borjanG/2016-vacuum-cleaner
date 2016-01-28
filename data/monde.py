#Custom libs
from data.aspirateur import Aspirateur
#Generic python libs
from random import randrange
from copy import deepcopy

__author__ = "Terral, Rodriguez, Geshkovski"
__date__ = "27.01.16"
__version__ = "0.1"

#Global variable (?)
objetsStatiques = {100: ('aspirateur', '@'),
                   0: ('rien', ' '),
                   1: ('poussiere', ':')}

class Monde(object):

  def __init__(self, a, l=1, c=2):
    """ Monde constructor """

    assert isinstance(a, Aspirateur), "il faut un Stochy en parametre"
    self.__lignes = l
    self.__cols = c
    self.__table = [[0 for j in range(c)] for i in range(l)]
    self.__posAgent = (0,0)

  #Deepcopy car hash table ^ liste de listes
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

    for i in range(len(self.table)):
      tab.append([])
      for j in range(len(self.table[0])):
        tab[i].append(self.objetsStatiques[self.table[i][j]][1])
    tab[self.posAgent[0]][self.posAgent[1]] += self.objetsStatiques[key][1]

    l = len(tab)
    c = len(tab[0])
    _=[]

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
                                                                      
  def initialisation(self):
    """ Initialisation du monde """
    self.__posAgent = (randrange(self.__lignes), randrange(self.__cols))
    self.__table = deepcopy([[randrange(len(self.objetsStatiques)-1)
                              for j in range(self.__cols)]
                              for i in range(self.__lignes)])
