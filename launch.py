#Custom libs
from data.monde import Monde
from data.aspirateur import Aspirateur

if __name__ == "__main__":

  a = Aspirateur()
  m = Monde(a)
  # print(m.table)
  # print(m.posAgent)
  m.initialisation()
  print(m.table)
  print(m.posAgent)
  print(m)