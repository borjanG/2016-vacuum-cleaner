#Custom libs
from aspirateur import Aspirateur
#Generic python libs
from random import randrange
from copy import deepcopy

#Global variable (?)
objetsStatiques = {100: ('aspirateur', '@'),
                   0: ('rien', ' '),
                   1: ('poussiere', ':')}

class Monde(object):

  def __init__(self, a, l = 1, c = 2):
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
    
    header="\u2554"+"\u2550"*3+"\u2564"+"\u2550"*3+"\u2557"
    middle="\u2551"+ "%3s" %(tab[0][0]) + "\u2502"+ "%3s" %(tab[0][1]) + "\u2551"
    footer="\u255A"+"\u2550"*3+"\u2567"+"\u2550"*3+"\u255D"

    return "\n".join([header,middle,footer])
                                                                     

  def initialisation(self):
    """ Initialisation du monde """
    self.__posAgent = (randrange(self.__lignes), randrange(self.__cols))
    self.__table = deepcopy([[randrange(len(self.objetsStatiques)-1)
                              for j in range(self.__cols)]
                             for i in range(self.__lignes)])

if __name__ == "__main__":

  a = Aspirateur()
  m = Monde(a)
  # print(m.table)
  # print(m.posAgent)
  m.initialisation()
  print(m.table)
  print(m.posAgent)
  print(m)
