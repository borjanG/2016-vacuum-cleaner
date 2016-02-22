class Base:
    def __init__(self,v,w):
        self._a = v
        self.__b = w
    @property
    def un(self): return self._a
    @property
    def deux(self): return self.__b
        
    def __str__(self): return "un={0.un} deux={0.deux}".format(self)
    
class Derivee(Base):
    def __init__(self,x,y):
        super().__init__(x,y)
        
if __name__ == "__main__" :
    print("Création de u instance de Derivee") 
    u = Derivee(100,200)
    print(u)
    print("le contenu de l'instance u",u.__dict__)   
    print("_"*10) 
    for att in "un deux _a __b".split():
        try:
            print("acces en écriture sur u.%s" % att)
            setattr(u,att,42)
            print("modifié",u)
            print("le contenu de l'instance u",u.__dict__)
        except Exception as _e:
            print("> Erreur",_e)
            print("non modifié",u)
        print("-"*7)