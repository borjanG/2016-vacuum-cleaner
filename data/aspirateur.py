#Custom libs
import data.monde

#Circular dependencies.. Can't import Monde explicitly..
#FFS Python :@ :/ .. 

class Aspirateur(object):
	""" Aspirateur constructor """

	def __init__(self):
	  self.__stock = 150    #a varier plus tard
	  self.__run = True     
	  self.__batterie = 100 #a varier plus tard
		# pass

	@property 
	def vider(self):
		self.__stock = 0
		
	@property 
	def arret(self):
		self.__run = False

	# #def aspirer(self, t, pos@):
	# #def gauche(self, t, pos@):
	# #def droite(self, t, pos@):