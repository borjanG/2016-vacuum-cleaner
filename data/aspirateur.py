# #Custom libs
# import data.monde 
# #Generic python libs
# from random import randrange

# #Circular dependencies.. Can't import Monde explicitly..
# #FFS Python :@ :/ .. 

# class Aspirateur(object):
#   """ Aspirateur constructor """

#   def __init__(self, capteurs = [], actions = ['Gauche', 'Droite', 'Aspirer']):
#     #
#     self.__vivant = True
#     self.__capteurs = capteurs
#     self.__actions = actions
#     self.__reward = 0

#   @property 
#   def vivant(self):
#     return self.__vivant

#   @property 
#   def capteurs(self):
#     return self.__capteurs 

#   @property 
#   def actions(self):
#     return self.__actions

#   def getDecision(self, content):
#     """"""
#     assert isinstance(content, int) and content in data.monde.objetsStatiques.keys(), 'No.'

#     index = randrange(len(self.actions))
#     action = self.actions[index]
#     return action 

#   def getEvaluation(self):
#     """ Recupere l'evaluation """
#     return self.__reward

#   def setReward(self, reward):
#     """ Associe une recompense au aspirateur """

#     assert isinstance(reward, float), ' Stochy veut un nombre!'
#     self.__reward = reward 

# class AspiClairvoyant(Aspirateur):
#   """ Aspirateur qui voit le contenu de sa propre case """

#   def __init__(self, capteurs = [8], actions = ['Gauche', 'Droite', 'Aspirer']):
#     super().__init__(capteurs, actions)

#   def getDecision(self, content):
#     """ J'arrive pas a comprendre l'enonce """
#     assert isinstance(content, int) and content in data.monde.objetsStatiques.keys(), 'No.'

#     # index = 
#     # action = self.

# class AspiVoyant(Aspirateur):
#   """ Aspirateur qui aspire la salete uniquement """

#   def __init__(self, capteurs = [8], actions = ['Gauche', 'Droite', 'Aspirer']):
#     super().__init__(capteurs, actions)

#   def getDecision(self, content):
#     """"""
#     assert isinstance(content, int) and content in data.monde.objetsStatiques.keys(), 'No.'

#     if content == 1:
#       action = self.actions[self.actions.index('Aspirer')]
#       #Because YOLO j'aime pas associer des string aux variables
#     else:
#       action = self.actions[randrange(len(self.actions))-1]
#     return action

#   #Il dit "qui apprenne a aspirer..", donc il faut peut-etre changer
#   #le mecanisme de feedback, donc modif setReward et getEvaluation.
