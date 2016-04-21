#!/usr/local/src/pyzo/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__ = "tests unitaires pour agslib"
__date__ = "22.03.16"
__version__ = "0.13"

#----- import ---------------------------------------
import copy
import random
from math import ceil, floor
import agslib as ags
#----------------------------------------------------

# NE RIEN MODIFIER A PARTIR D'ICI

# un test est de la forme test_xxx() où xxx est la méthode testée
# un test n'a pas de paramètre
# un sous-test est de la forme subtest_xxx_yyy( params ) il est normalement
# appelé depuis test_xxx pour controler plusieurs sous-cas

def check_property(p:bool,msg:str='default',letter:str='E') -> str:
    """ permet de tester une propriété
    @input p: propriété à tester (vraie ou fausse)
    @input msg: message spécifique en cas d'erreur [defaut=default]
    @input letter: code d'erreur [defaut=E]
    @return letter (echec) . (succes)
    """
    try:
        assert( p ), 'failure %s' % msg
        _ = '.'
    except Exception as _e:
        print(_e)
        _ = letter
        
    return _

def has_failure(string:str,sz:int=1) -> bool:
    """ vérifie si les sz derniers tests ont échoué """
    return string[-sz:] != '.'*sz

def check_integrity(string:str) -> bool:
    return '.'*len(string) == string

def subtest_hasConverged(k):
    _out = ''

    # initialisation
    pops = mmcPop(k) # les populations a tester
    for p in pops:
        ng = random.choice(range(p.nbGenes))\
          if p.nbGenes < 3 else random.choice(range(2,p.nbGenes,2))
        deb,fin = ng*p.szGenes,(ng+1)*p.szGenes
        _clist = random.sample(range(p.szPop),pops.subpop)
        pat = '0'*p.szGenes
        _out += check_property(not p.hasConverged(ng),
                                "hasConverged: convergence was unexpected for {}".format(ng))
        for i in _clist:
            pref = p.popAG[i].genotype[:deb]
            suff = p.popAG[i].genotype[fin:]
            p.popAG[i].genotype = pref+pat+suff
        _out += check_property(p.hasConverged(ng),
                                "hasConverged: convergence was expected for {}".format(ng))
    return _out

def subtest_isOver_shouldNot(k):
    """
    rate variable .5 .75 .9
    """
    _out =''
    for rate in (.5, .75, .9):
        pops = mmcPop(k,r=rate)
        for p in pops: # pour chaque cas
            hc = [p.hasConverged(i) for i in range(p.nbGenes)]
            nf = hc.count(False)
            th = ceil((1-rate) * p.nbGenes)
            _out += check_property(p.isOver() == (nf < th))
    return _out


def subtest_isOver_rateAlphabet(k,rate,alfaB):
    """
    TEST très couteux en temps
    """
    _out = ''
    pops = mmcPop(k,1,rate,alfaB)
    for p in pops:
        if p.szGenes == 1 and rate <= .5 and alfaB == "01": continue
        #avt = [p.hasConverged(i) for i in range(p.nbGenes)].count(True)
        modify(p)
        #apr = [p.hasConverged(i) for i in range(p.nbGenes)].count(True)
        #assert(avt <= apr and apr >= p.rateCVG*p.nbGenes),\
        #  "k={} rate={} alf={} avt={} apres={} objectif={}".format(k,rate,alfaB,avt,apr,p.rateCVG*p.nbGenes)
        _out += check_property(p.isOver(),
                                "isOver: nbGenes {0.nbGenes:02d} "
                                "szGene {0.szGenes:02d} szPop {0.szPop} "
                                "alphabet {0.alphabet:4} taux {0.rateCVG:0.2f}"
                                "".format(p))

    return _out
    
def subtest_isOver_should(k):
    """
    rate variable .5 .75 .9
    alphabet variable "01" "1234"
    On force les valeurs
    """
    _out =''
    for r in (.5, .75, .9):
        for a in "01 1234".split():
            _out += subtest_isOver_rateAlphabet(k,r,a)
    return _out

def subtest_raz_select(pop):
    _out = ''
    ev = '_SomeOne__evaluation'
    vic = 'victoires'
    for x in pop:
        _out += check_property(hasattr(x,ev))
        if not has_failure(_out):
            _out += check_property(getattr(x,ev) is None,
                                   "adequation: expected None found {}"
                                    "".format(getattr(x,ev)))
        _out += check_property(hasattr(x,vic))
        if not has_failure(_out):
            _out += check_property(getattr(x,vic) == 0,
                                   "victoires: expected 0 found {}"
                                    "".format(getattr(x,vic)))
    return _out

def subtest_selection(code,nb):
    """ vérifie les types et les demandes de remise a zero """
    _out = ''
    pops = mmcPop(p=1)
    for pop in pops:
        newPop = pop.selection(code,nb)
        _out += check_property( isinstance(newPop,(list,tuple)),
                                "TypeError for selectWheel")
        _out += check_property( len(newPop) == nb,
                                "ValueError expected {} got {}"
                                "".format(nb,len(newPop)))
        if check_integrity(_out): _out += subtest_raz_select(newPop)
        else: break
        if check_integrity(_out):
            _old = [x.genotype for x in pop.popAG ]
            for x in newPop:
                _out += check_property(x.genotype in _old,
                                       "{} is not member of population"
                                        "".format(x.genotype))
            
    return _out

def subtest_run_selectBest(kode):
    """ a-t-on le meilleur individu ? """
    _out = ''
    best_att = '_Population__bestIndividu'
    pops = mmcPop() # création de 3 populations
    _output = []
    _avant,_apres = [],[]
    for pop in pops:
        _out += check_property( getattr(pop,best_att) is None)
        _avant.append( pop.evaluation() )
        _output.append( pop.run(20,code=kode) )
        # print("*"*10)
        _apres.append( pop.evaluation() )
        # best est-il affecté ?
        _out += check_property( getattr(pop,best_att) is not None,
                                "'best' is not set")

    if not check_integrity(_out): return _out
    # la sortie de run est-elle bien best
    for pop,sortie in zip(pops,_output):
        _best = pop.best[0].genotype
        _out += check_property( sortie == _best,
                                "expected {} got {}".format(sortie,_best))
    # controle de la bonne évolution des stats
    for b,a in zip(_avant,_apres):
        for i in range(4):
            # print("here", b[i] <= a[i] if i == 2 else b[i] < a[i], i)
            _out += check_property(b[i] <= a[i] if i == 2 else b[i] < a[i],
                                   "something odds in the computation")
    # print(_out,'ggggggggggggggggggggggggggggggggggggggggggggggggggggg')
    # il faut controler que c'est effectivement le best de popAG
    # bug douloureux de mmcPop
    for pop,sortie in zip(pops,_output):
        v = similarite(pop.target,sortie)
        m = max(pop.popAG)
        _out += check_property(v >= m.adequation,
                               "{}:{} is less than {}\n{} vs {} - {}"
                               "".format(pop.select(kode),v,m.adequation,
                                         sortie,m.genotype,
                                         pop.target))
        if has_failure(_out): break
    return _out

def subtest_run_useSelect(kode):
    """ On remplace la méthode de sélection à la volée """
    _out = ''
    meth = {0: "_selectWheel", 1: "_selectFraction", 2: "_selectRank"}
    pops = mmcPop()
    for pop in pops:
        try:
            old = getattr(pop, meth[kode])
            setattr(pop, meth[kode], fake)
            pop.run(1, code=kode)
            # si on est ici c'est qu'il y a problème
            _out += 'E'
        except ValueError as _e:
            _out += check_property(str(_e) == 'fake', "got {}".format(_e))
            setattr(pop, meth[kode], fake)
    return _out
        
    
#------- Var & Tools --------
def test_fake(): return '..E..' # génère une erreur intentionnelle

def fake(*args,**kwargs):  raise ValueError("fake")
    
def similarite(target,b):
    """ calcul via Fraction: Fraction(a,b) a pour valeur (a/b) 
        intéret, évite les erreurs d'arrondis, 
        inconvénient pas tjrs lisible
           Fraction(3793,400) au lieu de 9.4825
           Fraction(10963,1250) au lieu de 8.770400000000002
    """
    try:
        from fractions import Fraction
    except:
        def Fraction(a,b): return round(a/b,2)
            
    _cpt = 0
    for x,y in zip(target,b):
        _cpt += 1 if x==y else Fraction(1, abs(int(x) - int(y)) + 3 )
    return _cpt

def modify(population):
    """ construction d'une population ayant convergée """
    nbG,szG,szP = population.nbGenes,population.szGenes,population.szPop
    alf,taux = population.alphabet,population.rateCVG
    popAG = [x.genotype for x in population.popAG]
    
    nbg, szp = ceil(taux*nbG), ceil(taux*szP)
    glst = random.sample(range(nbG),nbg) # gènes ayant convergés
    patterns = [ ''.join([random.choice(alf) for i in range(szG)])
                 for _ in glst ]
    # pour chaque chaque gène
    for pat,g in zip(patterns,glst):
        lc = random.sample(range(szP),szp) # choix population

        deb,fin = g*szG,(g+1)*szG
        for i in lc :
            un = popAG[i][:deb]
            deux = popAG[i][fin:]
            popAG[i] = un+pat+deux
            
            
    # choisir une catégorie d'individus
    # altérer le gène
    for i in range(szP): population.popAG[i].genotype = popAG[i]
    #diagnostic = [ population.hasConverged(i) for i in range(nbG) ].count(True)
    #
    #print("diag: {0} rate {1.rateCVG} decision {1.stable} nbG {1.nbGenes} {2}"
    #      "".format(diagnostic,population,nbG))

class mmcPop(object):
    """ 
       v nombre vertical, h nombre horizontal 
       On crée une cible artificielle (makeTarget)
       La fitness c'est le nombre de ressemblances

    """
    def __init__(self,k=1,p=10,r=.75,a='01'):
        assert(isinstance(k,int) and k > 0),\
          "{} strictly positive integer expected".format(k)
        n = p*10
        self.__a = a
        self.__v = int(n*r)
        self.__h = ceil(k*10*r)
        self.__pops = [ ags.Population(n,k*10//szG,szG,self.__a)
                        for szG in (1,2,5) ]
        self.__sols = [ self.makeTarget(pop.popAG) for pop in self.__pops]
        for pop,sol in zip(self.__pops,self.__sols):
            # pas de lien fitness ici, ca plante dans subtest_run_selectBest
            pop.target = sol
            pop.rateCVG = r

    @property
    def subpop(self): return self.__v
    @property
    def subsz(self): return self.__h
    @property
    def targets(self): return self.__sols

    def makeTarget(self,popAG):
        """ renvoie un pattern rare """
        _out = ''
        lg = [p.genotype for p in popAG]
        d = {}
        sz = len(lg[0])
        for i in range(sz):
            d[i] = {}
            for g in lg:
                d[i][g[i]] = d[i].get(g[i],0) +1
            # on cherche la lettre la plus rare
            _out += sorted(d[i], key=lambda _: d[i][_])[0]
        return _out
    
    def __iter__(self):
        """ 
            on fait le lien ici parce que dans __init__ ça bug 
            je ne sais pas pourquoi ... (25.03 01:46)
        """
        for p in self.__pops:
            for x in p.popAG:
                x.fitness = lambda _: similarite(p.target,_)
            yield(p)
#------ tests ------------------
def test_hasConverged():
    """ regarde si on sait détecter la convergence d'un gène ::DONE::
        On construit un cas particulier pour
        des genes de taille 1, de taille 2, de taille 5
        et pour différentes tailles de chromosomes ::DONE::
    """
    _out = ''
    for k in range(0,10,2): _out += subtest_hasConverged(k+1)
    return _out

def test_isOver():
    _out = ''
    # ça n'a pas convergé
    for k in range(0,10,2): _out += subtest_isOver_shouldNot(k+1)
    if not check_integrity(_out): 
        return _out
    # ça devrait
    for k in range(10,20,2): _out += subtest_isOver_should(k+1)
    return _out


def test__selectWheel():
    """ On construit une population fictive ::DONE::
        On vérifie que l'on a le bon nombre de sélectionné ::DONE::
        On vérifie que les individus n'ont pas de scores associés ::DONE::
    """
    _out = ''
    _out += subtest_selection(0,10)
    if not check_integrity(_out): return _out

    # On vérifie que si on ne donne pas de paramètre on obtient le
    # bon nombre d'individus
    pops = mmcPop(p=1) # 10 individus
    for pop in pops:
        newPop = pop.selection(0)
        _out += check_property(len(newPop)==10,
                               "Wrong selection expected 10, found {}"
                                "".format(len(newPop)))
    return _out

def test__selectFraction():
    """ On construit une population fictive ::DONE::
        On vérifie que ceux qui ont plus que la moyenne sont pris ::DONE::
        On vérifie que les individus n'ont pas de scores associés ::DONE::
    """
    _out = ''
    _out += subtest_selection(1,10)
    if not check_integrity(_out): return _out
    # On vérifie que si on ne donne pas de paramètre on obtient le
    # bon nombre d'individus
    pops = mmcPop(p=1) # 10 individus
    for pop in pops:
        newPop = pop.selection(1)
        _out += check_property(len(newPop)==10,
                               "Wrong selection expected 10, found {}"
                                "".format(len(newPop)))
        # les individus ayant un score > moyenne sont présents
        # (0) selection
        # (1) On récupère les évaluations
        # _m,_a,_M,_s = pop.evaluation()
        # (2) vérification
        _mi,_mo,_ma,_to = pop.evaluation()
        # un peu de bricolage car certains sont en multiples exemplaires
        _l = [ (x.genotype,x.adequation / _mo) for x in pop.popAG ]
        _select = [ (x,floor(y)) for x,y in _l if y >= 1 ]
        _might = [x for x,y in _l if y < 1]

        _found = [x.genotype for x in newPop]
        for a,b in _select:
            _out += check_property( a in _found, "bad selection")
            k = _select.count( (a,b) )
            _out += check_property(k*(b+1) >= _found.count(a) >= k*b,
                                   "bad quantity for fitness above average"
                                   " expected {} found {}"
                                   "".format(k*b,_found.count(a)))

        for a in _might:
            k = _might.count(a)
            _out += check_property(k*1 >= _found.count(a) >= 0,
                                    "bad quantity for fitness below average")
            
    return _out

def test_run():
    """
    On va vérifier que l'on utilise la bonne selection ::DONE::
    On va vérifier qu'on ne fait pas plus d'itérations que requis ::DONE::
    On va vérifier que la sortie est la meilleure ::DONE::
    On va vérifier qu'il y a progression des evaluations ::DONE::
    """
    print('test_run en cours ... soyez patient(e)')
    _out = ''
    for x in (0,1):
        try:
            _out += subtest_run_selectBest(x)
        except:
            print("failure subtest_run_selectBest({})".format(x))
            _out += '{}'.format(x)
    for x in range(3): _out += subtest_run_useSelect(x)
    # il faudrait récupérer le nombre d'itérations ....
    # tester une population qui a convergé et vérifier que ça marche

    for x in (0,1,2):
        for alf in ("012","3456","789012"):
            pops = mmcPop(k=1,p=2,r=.9,a=alf)
            for p in pops:
                modify(p)
                _yo = [_.genotype for _ in p.popAG]
                _rep = p.run(20,code=x)
                _out += check_property(_rep in _yo,"{} not found".format(_rep))
    return _out

#------ main --------------------
def main():
    # l'existence de certaines choses est requise
    _s = ''
    _all = "hasConverged isOver _selectWheel _selectFraction run".split()
    _args = { 'run': ((10,None,2),str),
              'isOver': (None,bool),
              'hasConverged': ((5,),bool),
              '_selectWheel': (None,list),
              '_selectFraction': (None,list),
              }
    try:
        pop = ags.Population(100,10,1,'01')
        for x in pop.popAG: x.fitness = lambda _: _.count('1')
    except Exception as _e:
        print(_e)
        print("constructeur are required to succeed")
        return 0,1,1,0
    #--- existence des méthodes --------------------------------------
    _msg = ''
    for att in _all:
        _msg += check_property(hasattr(pop,att),"{} missing".format(att))
        if not has_failure(_msg):
            _msg += check_property(callable(getattr(pop,att)),
                                   "{} should be function".format(att))
    print("Existence",_msg)
    stats['Existence'] = len(_msg)
    _s += _msg ; _msg = ''
    #--- codage fait --------------------------------------------------
    _ok1 = []
    _rep = []
    for att in _all:
        try:
            if _args[att][0] is None:
                _out = getattr(pop,att)()
            else:
                _out = getattr(pop,att)(*_args[att][0])
            _msg += '.'
            _ok1.append(att)
            _rep.append(_out)
        except Exception as _e:
            print(att+':',_e)
            _msg += 'E'

    stats['Codage'] = len(_msg)
    print("Codage",_msg)
    _s += _msg ; _msg = ''

    _ok = []
    for att,rep in zip(_ok1,_rep) :
        _msg += check_property(isinstance(rep,_args[att][1]),
                               "{}: expected {} found {}"
                               "".format(att,_args[att][1],type(rep)))
        if _msg[-1] == '.' : _ok.append(att)

    stats['Typage'] = len(_msg)
    print("Typage sortie",_msg)
    _s += _msg ; _msg = ''

    #========= test_XXX est appelé =====================================
    for att in _ok:
        meth = 'test_'+att
        try:
            _msg = eval(meth)()
            if _msg == '': print(meth,': en cours de développement')
            else: print(meth,_msg) ; stats[meth] = len(_msg)
        except Exception as _e:
            print("failure: {}".format(meth))
            print(_e)
            _msg = 'X'
        if _msg == '': continue # pas de test effectué
        _s += _msg
        if has_failure(_msg): break
        
    # Bilan
    _all = len(_s) 
    _ok = _s.count('.')
    return _ok, (_all-_ok), _all, round(100 * _ok / _all, 2)


if __name__ == "__main__" :
    stats = {}
    expected = {
        'Existence': 10,
        'Codage': 5,
        'Typage': 5,
        'test_hasConverged': 30,
        'test_isOver': 130,
        'test_run': 84,
        'test__selectWheel': 159,
        'test__selectFraction': "{} .. {}".format(198,211),
        }
    somme = sum([x for x in expected.values() if isinstance(x,int)])
    vals = [int(x) for x in expected['test__selectFraction'].split(' .. ')]
    mini,maxi = min(vals),max(vals)
    print("succ %d fail %d sum %d, rate = %.2f" % main())
    print("expected >> succ {0} fail 0 sum {0} rate = 100.00"
          "".format('{}..{}'.format(somme+mini,somme+maxi)))
    print("_"*10,"résumé","_"*10)
    for x in stats:
        if x != 'test__selectFraction':
            diag = 'ok' if stats[x]==expected[x] else 'nok'
        else:
            diag = 'ok' if mini <= stats[x] <= maxi else 'nok'
        print("{}: got {} expected {} : {}"
              "".format(x,stats[x],expected[x],diag))
            
            
