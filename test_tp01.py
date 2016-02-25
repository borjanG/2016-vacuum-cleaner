#!/usr/local/src/pyzo/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__ = "tests unitaires pour tp01"
__date__ = "11.02.16"
__version__ = "0.5"

#----- import ---------------------------------------
from test_tp00a import test_table, test_perfGlobale, test_historique
import copy

## remplacer XXX par le nom de votre fichier à tester
#import XXX as tp01
import data.tp01 as tp01
#----------------------------------------------------

# NE RIEN MODIFIER A PARTIR D'ICI

# un test est de la forme test_xxx() où xxx est la méthode testée
# un test n'a pas de paramètre
# un sous-test est de la forme subtest_xxx_yyy( params ) il est normalement
# appelé depuis test_xxx pour controler plusieurs sous-cas

def check_property(p,msg='default',letter='E'):
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

def has_failure(string,sz=1):
    """ vérifie si les sz derniers tests ont échoué """
    return string[-sz:] != '.'*sz

def check_integrity(string:str) -> bool:
    return '.'*len(string) == string

def subtest_readonly(obj,lattr):
    """ vérification de chaque attribut de obj en lecture seule """
    _s = ''
    for att in lattr:
        oldv = copy.deepcopy(getattr(obj,att))
        for val in ("a",42,0.2,-3,[],"a b".split(),True,False):
            if val == oldv : continue
            try:
                setattr(obj,att,val)
                if getattr(obj,att) == val : _s += 'E'
                else: _s += '.'
            except Exception:
                _s += '.'
            if has_failure(_s):
                print('%s: avant %s apres %s' % (att,str(oldv),
                                                  str(val)))

    return _s
def subtest_rw_knowledge(obj):
    _s = ''
    kb = tp01.KB()
    _rul = tp01.Rule([],'a',.2)
    kb.add(_rul)
    try:
        obj.knowledge = kb
        _s += '.'
    except:
        _s += '1'

    _s += check_property(str(kb) ==str(obj.knowledge),"knowledge",letter='x')
    _rul = tp01.Rule([],'a',.3)
    kb.add(_rul)
    try:
        obj.knowledge.add(_rul)
        _s += '.'
    except:
        _s += '2'

    _s += check_property(str(obj.knowledge) == str(kb),letter='y')
    return _s

def subtest_rw_apprentissage(obj):
    _s = ''
    _s += check_property(obj.apprentissage == False,letter='1')
    try:
        obj.apprentissage = True
        _s += '.'
    except:
        _s += '2'
    _s += check_property(obj.apprentissage, letter='3')

    for i,v in enumerate([42,0,1,'a',.1,-1,'a b'.split(),[]]):
        try:
            obj.apprentissage = v
            if not obj.apprentissage: _s += str(i+4)
            else: _s += '.'
        except:
            _s += '.'
    
    return _s

#------- Var & Tools --------
class MyEnv(object):
    """ On force les attributs à etre dans aspi et world """
    __slots__ = ('aspi','world')
    for i in (-25, -2, -1, 3, 13, 27, 45, 85, 99, 1011, 101, 228, 42):
        tp01.objetsStatiques[i] = ('.'*min(abs(i),5),str(i))
    def __init__(self,kap=[],nbl=1,nbc=2):
        self.aspi = tp01.Aspirateur_KB(.75,kap)
        self.world = tp01.World(self.aspi,nbl,nbc)
    def __getattr__(self,att):
        if hasattr(self.aspi,att): return getattr(self.aspi,att)
        else: return getattr(self.world,att)
    def gauche(self):
        i,j = self.posAgent
        j -= 1
        if j < 0: return self.posAgent
        return i,j
    def droite(self):
        i,j = self.posAgent
        j += 1
        if j >= len(self.table[0]): return self.posAgent
        return i,j
    def ici(self):
        return self.posAgent

# des raccourcis pour les controle de type
numeric = float,int
ltup = list,tuple

def getArgs(cls,meth):
    """ On récupère les arguments formels """
    import inspect
    return inspect.getfullargspec(getattr(cls,meth))._asdict()['args']

# Definition des signatures pour chaque méthode
aspiSig = {'setReward': (2,0),
            'getEvaluation': (1,1,numeric),
            'getLastReward': (1,1,numeric),
            'getDecision': (2,1,str)}
mondeSig = {'getPerception': (2,1,ltup),
            'applyChoix': (2,1,numeric),
            'updateWorld': (1,0),
            'step': (1,0),
            'simulation': (2,1,numeric)}

# Controle de type pour les cas de base
def check_out(dic,meth,*args):
    _mmc = MyEnv()
    _ = getattr(_mmc,meth)(*args)
    if dic[meth][1] == 0: _prop = (_ is None)
    elif dic[meth][1] == 1: _prop = (isinstance(_,dic[meth][2]))
    else: _prop = (dic[meth][1]==len(_)) # à refléchir si le cas arrive
    return check_property(_prop,'%s: bad output type' % meth)

def test_fake(): return '..E..' # génère une erreur intentionnelle
def do_loop(lmeth):
    _s = ''
    for meth in lmeth:
        _meth = 'test_'+meth
        try:
            _msg = eval(_meth)()
            print(meth,_msg)
        except Exception as _e:
            print("failure: {}".format(meth))
            print(_e)
            _msg = 'X'
        _s += _msg
        if not check_integrity(_msg): break
    return _s
#------ oldies ------------------
def test_oldies():
    _s = ''
    _test = "table perfGlobale historique".split()
    for k in _test:
        _out = eval("test_"+k)()
        _s += _out
        if not check_integrity(_out):
            print(k,_out)
            break

    return _s
    
#------ Tests Aspirateurs -------
#------ Tests Mondes ------------
def test_applyChoix():
    _s = ''
    _mmc = MyEnv(nbc=7)
    _mvt = {"Gauche": _mmc.gauche,
            "Droite": _mmc.droite,
            "Aspirer": _mmc.ici }
    _reward = {# succes, echec
        "Gauche": (1,-1),
        "Droite": (1,-1),
        "Aspirer": (2,0),
        }
    for i in range(10):
        for k in _mvt:
            _old = _mmc.posAgent
            _ovu = _mmc.table[_old[0]][_old[1]]
            _moi = _mvt[k]()
            _toi = _mmc.applyChoix(k)
            _lui = _mmc.posAgent
            _nvu = _mmc.table[_moi[0]][_moi[1]]
            _s += check_property(_moi == _lui,
                                "{}: bad position expected {} got {}".format(k,_moi,_lui),
                                str(i+1))
            if has_failure(_s): break
            if k in "Gauche Droite".split():
                _val = _reward[k][_moi == _old]
            else:
                _val = _reward[k][_ovu == _nvu]
            _s += check_property(_toi == _val,
                                 "bad return at {} for {}".format(i,k),str(i+1))
            if has_failure(_s): break

    return _s
#------ main --------------------
def main():
    # l'existence de certaines choses est requise
    _s = ''
    try:
        _mmc = MyEnv()
    except Exception:
        print("constructeur are required to succeed")
        return 0
    
    _all = "Aspirateur Aspirateur_KB Monde World objetsStatiques".split()
    for att in _all:
        _s += check_property(hasattr(tp01,att),att)
    print("existence:",_s)

    _s += check_property(issubclass(tp01.Aspirateur_KB,tp01.Aspirateur),
                         "Aspirateur_KB wrong class")
    _s += check_property(issubclass(tp01.World,tp01.Monde),
                         "World wrong class")
    _atts = "knowledge apprentissage probaExploitation".split()
    _msg =''
    for _ in _atts:
        _msg += check_property(hasattr(tp01.Aspirateur_KB,_),
                               "{} missing".format(_))
        _msg += check_property(not hasattr(tp01.Aspirateur,_),
                               "{} misplaced".format(_))

    _aspi = tp01.Aspirateur_KB(.75)
    _msg += subtest_readonly(_aspi,["probaExploitation"])
    _msg += subtest_rw_knowledge(_aspi)
    _msg += subtest_rw_apprentissage(_aspi)
    print("Attributs Aspirateurs:",_msg)
    _s += _msg ; _msg = ''

    _atts = "table posAgent".split()
    for cls in (tp01.Monde,tp01.World):
        for _a in _atts:
            _msg += check_property(hasattr(cls,_a),
                               "{1} is missing in {0}".format(cls.__class__.__name__,_a))
    # attributs doivent etre read-only
    _msg += subtest_readonly(tp01.World(_aspi),_atts)
    print("Attributs Monde:",_msg)
    _s += _msg ; _msg = ''
    
    if not check_integrity(_s):
        print("something missing")
    else:
        _msg = test_oldies()
        print("oldies:",_msg)
        _s += _msg ; _msg = ''

    _todo = "applyChoix".split()
    _s += do_loop(_todo)
    # Bilan
    _all = len(_s) 
    _ok = _s.count('.')
    return _ok, (_all-_ok), _all, round(100 * _ok / _all, 2)


if __name__ == "__main__" :

    print("succ %d fail %d sum %d, rate = %.2f" % main())
    print("expected >> succ {0} fail 0 sum {0} rate = 100.00".format(164))
