#Custom libs
from data.monde import Monde
from data.aspirateur import Aspirateur

if __name__ == "__main__":

  a = Aspirateur()
  m = Monde(a,1,2)
  # print(m.table)
  # print(m.posAgent)
  m.initialisation()
  print(m.table)
  print(m.posAgent)
  print(m)

  m = Monde(a,2,3)
  # print(m.table)
  # print(m.posAgent)
  m.initialisation()
  print(m.table)
  print(m.posAgent)
  print(m)

  m = Monde(a,4,4)
  # print(m.table)
  # print(m.posAgent)
  m.initialisation()
  print(m.table)
  print(m.posAgent)
  print(m)
