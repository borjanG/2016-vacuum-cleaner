#Custom libs
from data.monde import *
from data.tp01 import *

if __name__ == "__main__":

  # a = AspiVoyant()
  # a = Aspirateur_KB(0.1)
  # a = Aspirateur()
  # m = Monde(a,1,5)
  # m.simulation(10)
  # print(m.historique)
  # print(m.table)
  # print(m.posAgent)
  # a.setReward(42)
  # print(a.getEvaluation())

  stochy = Aspirateur()
  deter = AspiVoyant()
  nerdy = Aspirateur_KB(0.1)

  aspiz = [stochy, deter, nerdy]

  for i in range(10):
    for a in aspiz:
      m2 = Monde(a,1,2)
      m5 = Monde(a,1,5)
      m2.simulation(4)
      m5.simulation(10)

