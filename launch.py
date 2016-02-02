#Custom libs
from data.monde import Monde
from data.aspirateur import Aspirateur

if __name__ == "__main__":

  a = Aspirateur()
  m = Monde(a,1,4)
  # print(m.table)
  # print(m.posAgent)
  #m.initialisation()
  #print('debut\n\n', m)
  m.simulation(5)
  print(m.table)
  print(m.posAgent)
  # print(m)

  # m = Monde(a,2,3)
  # # print(m.table)
  # # print(m.posAgent)
  # m.initialisation()
  # m.simulation(5)
  # print(m.table)
  # print(m.posAgent)
  # print(m)

  # m = Monde(a,4,4)
  # # print(m.table)
  # # print(m.posAgent)
  # m.initialisation()
  # m.simulation(10)
  # print(m.table)
  # print(m.posAgent)
  # print(m)

  # m.table[0][0]=56
  # print(m.table)
  # print(m.posAgent)
  # print(m)

  
