#Custom libs
import data.monde 
#Generic py libs
from random import randrange

#Circular dependencies.. Can't import Monde explicitly..
#FFS Python :@ :/ .. 

class Aspirateur(object):
  """ Aspirateur constructor """

  def __init__(self, capteurs = [], actions = ['Gauche', 'Droite', 'Aspirer']):
    #
    self.__vivant = True
    self.__capteurs = capteurs
    self.__actions = actions
    self.__reward = 0

  @property 
  def vivant(self):
    return self.__vivant

  @property 
  def capteurs(self):
    return self.__capteurs 

  @property 
  def actions(self):
    return self.__actions

  def getDecision(self, content):
    index = randrange(len(self.actions))
    action = self.actions[index]
    return action 

  def getEvaluation(self):
    return self.__reward

  def setReward(self, reward):
    assert isinstance(reward,(int,float)),'stochy veut un nombre!!!'
    self.__reward = reward 