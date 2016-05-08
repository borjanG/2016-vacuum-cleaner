#Custom libs
from data.monde import *
from data.tp01 import *
import numpy as np 
import matplotlib.pyplot as plot 
import pylab as py
from scipy.stats import linregress

if __name__ == "__main__":

  a = AspiVoyant()
  # a = Aspirateur_KB(0.1)
  # a = Aspirateur()
  # m = Monde(a,1,5)
  mondes = [Monde(a, 1, i) for i in range(1, 20)]
  ord = list()
  for monde in mondes:
    # monde.simulation(2*len(monde.table[0]))
    ord.append(monde.simulation(2*len(monde.table[0])))
  # coeff = linregress(list(range(1, 20)), ord)
  # a = coeff[0]
  # b = coeff[1]
  # ordo = list()
  # for i in range(1, 20):
    # ordo.append(a*i + b)

  py.plot(list(range(1, 20)), ord, "Green")
  py.xlabel("Taille du monde (nombre de colonnes)")
  # py.ylabel("#Cases avec poussiere debut / #Cases avec poussiere fin")
  # py.ylabel("#Pieces netoyees - #de cases ou il passe 3+ fois")
  py.title("Aspi v1 (Deter)")
  plot.show()
  # m.simulation(10)
  # print(m.historique)
  # print(m.table)
  # print(m.posAgent)
  # a.setReward(42)
  # print(a.getEvaluation())

  # a = Aspirateur_KB(0.7, learn=True)
  # m = World(a,1,2)
  # print(m)
  # m.simulation(4)
  # print(m)


  # stochy = Aspirateur()
  # deter = AspiVoyant()
  # nerdy = Aspirateur_KB(0.1)

  # aspiz = [stochy, deter, nerdy]

  # for i in range(10):
  #   for a in aspiz[:2]:
  #     m2 = Monde(a,1,2)
  #     m5 = Monde(a,1,5)
  #     m2.simulation(4)
  #     m5.simulation(10)
  #   a=aspiz[2]
  #   m2 = World(a,1,2)
  #   m5 = World(a,1,5)
  #   m2.simulation(4)
  #   m5.simulation(10)

