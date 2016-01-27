from aspirateur import Aspirateur
from random import randrange
from copy import deepcopy

class Monde(object):

	staticObjects = {100: ('aspirateur', '@'),
					0: ('rien', ' '), 
					1: ('poussiere', ':')}

	def __init__(self, a, l = 1, c = 2):
		"""bla"""

		self.__lignes = l
		self.__cols = c
		self.__table = [[None for j in range(c)] for i in range(l)]
		self.__posAgent = (0,0)

	@property
	def table(self):
		return self.__table
	@property 
	def posAgent(self):
		return self.__posAgent

	def __str__(self):
		return "%s" % ()

	def initialisation(self):
		self.__posAgent = (randrange(self.__lignes), randrange(self.__cols))
		self.__table = deepcopy([[randrange(len(self.staticObjects)-1) 
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
