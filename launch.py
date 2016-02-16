#Custom libs
from data.monde import *
from tp01 import *

if __name__ == "__main__":

  # a = AspiVoyant()
  a = Aspirateur_KB(0.5)
  # a = Aspirateur()
  m = Monde(a,1,5)
  m.simulation(10)
  # print(m.historique)
  # print(m.table)
  # print(m.posAgent)
  # a.setReward(42)
  # print(a.getEvaluation())

  
