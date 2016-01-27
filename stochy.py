from aspirateur import Aspirateur
from random import randrange
from copy import deepcopy

objetsStatiques = {100: ('aspirateur', '@'),
					0: ('rien', ' '), 
					1: ('poussiere', ':')}

class Monde(object):

	

	def __init__(self, a, l = 1, c = 2):
		"""bla"""

		self.__objetsStatiques = {100: ('aspirateur', '@'),
					0: ('rien', ' '), 
					1: ('poussiere', ':')}
		self.__lignes = l
		self.__cols = c
		self.__table = [[0 for j in range(c)] for i in range(l)]
		self.__posAgent = (0,0)

	@property 
	def objetsStatiques(self):
		return self.__objetsStatiques

	@property
	def table(self):
		return self.__table
	@property 
	def posAgent(self):
		return self.__posAgent

	def __str__(self):
                tab=[]
		for i in range(len(self.table)):
                    tab.append([])
                    for j in range(len(self.table[0])):
                        tab[i][j]=self.objetsStatiques[self.table[i][j]][1]
                return str(tab)
                                       

	def initialisation(self):
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
