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

    self.__lignes = l
    self.__cols = c
    self.__table = [[0 for j in range(c)] for i in range(l)]
    self.__posAgent = (0,0)

  @property 
  def objetsStatiques(self):
    return objetsStatiques
  @property
  def table(self):
    return self.__table
  @property 
  def posAgent(self):
    return self.__posAgent

  def __str__(self):
    """ Generic string method """

    tab=[]
    for i in range(len(self.table)):
      tab.append([])
      for j in range(len(self.table[0])):
        tab[i].append(self.objetsStatiques[self.table[i][j]][1])
    tab[self.posAgent[0]][self.posAgent[1]]+=self.objetsStatiques[100][1]

    l=len(tab)
    c=len(tab[0])

    truc_header="\u2550"*3+"\u2564"
    truc_middle="\u2500"*3+"\u253C"
    truc_footer="\u2550"*3+"\u2567"

    _=[]

    header="\u2554"+truc_header*(c-1)+"\u2550"*3+"\u2557"
    middle="\u2551"+truc_middle*(c-1)+"\u2500"*3+"\u2551"
    footer="\u255A"+truc_footer*(c-1)+"\u2550"*3+"\u255D"

    #header
    _.append(header)

    #ligne 0
    _elt="\u2551"+"%3s" %(tab[0][0]) #ligne 0 col 0
    if c>1:
      for j in range(1,c):
        _elt+="\u2502"+"%3s" %(tab[0][j])
    _elt+="\u2551"
    _.append(_elt)

    #autres lignes s'il y en a
    if l>1:
      for i in range(1,l):
        _.append(middle)
    
        _elt="\u2551"+"%3s" %(tab[i][0]) #ligne i col 0
        if c>1: #autres colonnes s'il y en a
          for j in range(1,c):
            _elt+="\u2502"+"%3s" %(tab[i][j])
        _elt+="\u2551"

        _.append(_elt)
      
    _.append(footer)
    return "\n".join(_)
  
##    header="\u2554"+"\u2550"*3+"\u2564"+"\u2550"*3+"\u2557"
##    middle="\u2551"+ "%3s" %(tab[0][0]) + "\u2502"+ "%3s" %(tab[0][1]) + "\u2551"
##    footer="\u255A"+"\u2550"*3+"\u2567"+"\u2550"*3+"\u255D"
##    return "\n".join([header,middle,footer])
                                                                     

  def initialisation(self):
    """ Initialisation du monde """
    self.__posAgent = (randrange(self.__lignes), randrange(self.__cols))
    self.__table = deepcopy([[randrange(len(self.objetsStatiques)-1)
                              for j in range(self.__cols)]
                             for i in range(self.__lignes)])
