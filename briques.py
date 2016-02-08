#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__ = "briques de base pour la réalisation aspi autonome"
__date__ = "05.02.16"
__version__ = "0.1"

#------------ import -------------
import random
#---------------------------------

class UT(object):
    """ le temps ne s'arrete jamais """
    def __init__(self,v=10):
        self.__base = v

    @property
    def minute(self): return self.__base
    @property
    def heure(self): return self.minute * 60
    @property
    def jour(self): return self.heure * 24
    @property
    def semaine(self): return self.jour * 7
    @property
    def mois(self): return self.jour * 30
    @property
    def trimestre(self): return self.mois * 3
    @property
    def an(self): return self.mois * 12
    

class Fiabilite(object):
    """ fiabilite c'est 1-proba panne """
    def __init__(self,fiabiliteInitiale,latence,raison,periode):
        assert(0 <= fiabiliteInitiale <= 1), "fiabilité entre 0 et 1"
        assert(latence >= 0 and isinstance(latence,int)),\
               "temps de latance positif ou nul"
        assert(0 <= raison <= 1), "raison est entre 0 et 1"
        assert(periode > 0 and isinstance(periode,int)),\
               "temps est un entier positif"
        self.__u0 = fiabiliteInitiale
        self.__latence = latence
        self.__raison = raison
        self.__periode = periode
        
    def __call__(self,temps):
        """ renvoie la probabilité associé """
        if temps <= self.latence : return 1 - self.fiabiliteInitiale
        else:
            return 1 - self.fiabiliteInitiale * ( self.raison ** ((temps - self.latence) // self.periode))
        
    @property
    def fiabiliteInitiale(self): return self.__u0
    @property
    def latence(self): return self.__latence
    @property
    def raison(self): return self.__raison
    @property
    def periode(self): return self.__periode
    
class Rule(object):
    """ 
        permet de créer une règle percept, action, nbusage, 
        scoretotal, scoremoyen 
    """
    def __init__(self,percept,action,score):
        self.__percept = ','.join([str(_) for _ in percept])
        self.__action = action
        self.__nb = 1
        self.__total = score
        
    @property
    def condition(self): return self.__percept
    @property
    def conclusion(self): return self.__action
    @property
    def nbUsage(self): return self.__nb
    @nbUsage.setter
    def nbUsage(self,valeur):
        assert isinstance(valeur,int) and valeur > 0
        self.__nb = valeur
    @property
    def scoreTotal(self): return self.__total
    @scoreTotal.setter
    def scoreTotal(self,value):
        assert isinstance(value,(int,float))
        self.__total = value
    @property
    def scoreMoyen(self): return self.__total / self.__nb
    
    @property
    def head(self): # partie gauche de la règle
        return self.condition
    @property
    def tail(self): # partie droite de la règle
        return self.conclusion,self.nbUsage,self.scoreTotal,self.scoreMoyen
    
    def fusion(self,other,rate=1.):
        """ permet de fusionner deux règles
            - la fusion se fait avec modification des valeurs
              self = (cond,concl,nb,sc,scm)
              other = (cond,concl,nb1,sc1,scm1)
              self.fusion(other,r) = (cond,concl,nb+nb1,r*sc + sc1, scm2)
        """
        assert 0 <= rate <= 1, "rate should be in [0,1] found %s" % rate
        assert (isinstance(other,Rule) and
           self.condition == other.condition and
           self.conclusion == other.conclusion), "no match"
        self.nbUsage += other.nbUsage
        self.scoreTotal *= rate
        self.scoreTotal += other.scoreTotal
        
    def __str__(self):
        return "%s -> %7s (nbUsage = %d Total= %+.2f Moyenne %+.2f)" %\
           (self.condition,self.conclusion,self.nbUsage,
            self.scoreTotal,self.scoreMoyen)
        
class KB(object):
    """ gestion de la base de connaissances """
    def __init__(self):
        self.__kb = dict()
        
    def eraseBase(self): self.__kb = dict()
    def deletePercept(self,percept):
        _k = ','.join([str(_) for _ in percept ])
        self.__kb[_k] = []
            
    def find(self,percept):
        """ renvoie la liste des règles applicables pour percept """
        _k = ','.join([str(_) for _ in percept ])
        return self.__kb.get(_k,[])
        
    def add(self,rule, rate= 1.):
        assert  0 <= rate <= 1, "rate should be in [0,1] found %s" % rate
        assert isinstance(rule,Rule), "Rule needed, found %s" % type(rule)
        _candidats = self.__kb.get(rule.head,[])
        _found = False
        for regle in _candidats:
            if regle.conclusion == rule.conclusion : 
                regle.fusion( rule, rate ) ; _found = True
                break
        if not _found:
            _candidats.append(rule)
            self.__kb[rule.head] = _candidats
     
    def __str__(self):
        _out =  ""
        _keys = sorted(self.__kb.keys())
        for k in _keys:
            for r in self.__kb[k]: _out += str(r)+'\n'
            _out += '_'*8+'\n'
        return _out
        
    def __len__(self): return len(self.__kb)

if __name__ == "__main__" :
    #----- UT ---------------------------
    timer = UT()
    print("une minute vaut",timer.minute,"UTs")
    print("un an vaut",timer.an,"UTs")
    #----- Base de données ---------------
    kb = KB()
    r = Rule([0,0,2],"Droite",-1)
    kb.add(r)
    print(kb)
    r = Rule([0,0,2],"Gauche",1)
    kb.add(r)
    print(kb)
    r = Rule([0,0,2],"Droite",-1)
    kb.add(r,.9)
    print(kb)
    #------- fiabilité ------------#
    base = .9
    delay = 3
    rate = .9
    period = 2
    f = Fiabilite(base,delay,rate,period)
    for i in range(20):
        if i < delay: 
            _msg = "expected %.3f, " % (1 - base)
            assert( 1-base == f(i) )
        else: 
            j = (i-delay) // period
            _msg = "expected %.3f, " % (1 - base*rate**j)
            assert( 1 - base*rate**j == f(i) )
        _s = _msg + "proba panne[t= %02d] = %0.3f" % (i,f(i))
        print(_s) 
        
