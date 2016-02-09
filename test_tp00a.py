#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__ = "tests unitaires pour la première réalisation aspi autonome"
__date__ = "09.02.16"
__version__ = "0.5"

## remplacer XXX par le nom de votre fichier
import data.monde as tp00
#import mmc_tp00 as tp00
#import corrige_tp00a as tp00

# NE RIEN MODIFIER A PARTIR D'ICI
import random
import copy
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
    

def subtest_readonly(obj,lattr):
    """ vérification de chaque attribut de obj en lecture seule """
    _s = ''
    for att in lattr:
        oldv = copy.deepcopy(getattr(obj,att))
        try:
            _s += '.'
            setattr(obj,att,42)
            if oldv != getattr(obj,att): _s += 'E'
        except Exception:
            _s += '.'
        if _s[-2:] != '..' : return '%s: avant %s apres %s' % (att,oldv,getattr(obj,att))
        
    return _s
    
    
#------ Tests Aspirateurs -------

def test_init_Aspirateur():
    """ tests sur le constructeur Aspirateur qui doit être 
        Aspirateur() == Aspirateur([],['Gauche''Droite','Aspirer'])
    """
    _out = ''
    _actions = "Droite Gauche Aspirer".split()
    try:
        _a = tp00.Aspirateur()
        _out += '.'
    except Exception:
        _out += 'a'
    if has_failure(_out): return _out
    _out += check_property(_a.capteurs == [],'capteurs par défaut trouvé %s' %  _a.capteurs,'b')  
    if has_failure(_out): return _out
    _out += check_property(len(_a.actions) == 3,'wrong number of actions','c')
    _out += check_property(sorted(_a.actions) == sorted(_actions),"bad actions",'d')
    return _out

def test_capteurs():
    """ les capteurs sont des listes de valeurs distinctes dans 0..8 """
    _out = ''
    try:
        _a = tp00.Aspirateur([ 0 ])
        _out += '.'
    except Exception:
        _out += 'a'
    if has_failure(_out): return _out
    try:
        _a = tp00.Aspirateur([ '0' ])
        _out += 'b'
    except Exception:
        _out += '.'
    try:
        _a = tp00.Aspirateur([ 0, 0 ])
        _out += 'c'
    except Exception:
        _out += '.'
    if has_failure(_out,2): return _out
    _lc = random.sample( range(9), 4 )
    _a = tp00.Aspirateur( _lc )
    
    _out += check_property( len(_a.capteurs) == len(_lc),"bad list of captors",'d')
    _out += check_property( _a.capteurs == _lc,"bad list of captors",'e')
    return _out

def test_actions():
    """
        actions renvoie la liste des actions disponibles
    """
    _out = ''
    try:
        _a = tp00.Aspirateur([],1)
        _out += check_property(isinstance(_a.actions,(list,tuple)),"list or tuple expected found %s" % type(_a.actions),'a')
    except Exception:
        _out += '.'
    if has_failure(_out): return _out
    _a = tp00.Aspirateur([],['o','u','t'])
    _out += check_property(len(_a.actions)==len("out"),"wrong number of actions",'b')
    _out += check_property(sorted(_a.actions) == sorted("out"),"wrong actions",'c')
    return _out
    
def test_vivant():
    _out = ''
    _a = tp00.Aspirateur()
    _out += check_property( isinstance(_a.vivant,bool), "boolean required", '1')
    _out += check_property( _a.vivant, "should be alive, found %s" % _a.vivant, '2')
    return _out
        
def test_setReward():
    _out = ''
    return _out

def test_getLastReward():
    _out = ''
    return _out

def test_getEvaluation():
    _out = ''
    return _out

def test_getDecision():
    _out = ''
    return _out

#------- Monde ------
def test_table():
    """ une nouvelle contrainte est apparue dans TP00 """
    _out = ''
    _a = tp00.Aspirateur()
    _old = tp00.objetsStatiques
    _fake = dict()
    for i in (-25,-2,-1,0,1,3,27,45,85,99,1001,101,228):
        _fake[i] = ('.'*abs(i),str(i))
    tp00.objetsStatiques = _fake
    _m = tp00.Monde(_a,11,10)
    _out += check_property(len(_m.table) == 11,'nbLig is wrong','a')
    _out += check_property(len(_m.table[0]) == 10, 'nbCol is wrong','b')
    _val = [ _m.table[i][j] for i in range(len(_m.table)) 
             for j in range(len(_m.table[0])) if 0 <= _m.table[i][j] < 100 ]
    _out += check_property( len(_val) == 11*10, 'bad number of elements', 'c')
    _out += check_property( _val.count(0)+_val.count(1) != 11*10, 'bad elements','d')
    return _out 
    
def test_agent():
    _out = ''
    return _out

def test_perfGlobale():
    _out = ''
    return _out

def test_historique():
    _out = ''
    return _out

def test_updateWorld():
    _out = ''
    return _out

def test_applyChoix():
    _out = ''
    return _out

def test_getPerception():
    _out = ''
    return _out

def test_step():
    _out = ''
    return _out

def test_simulation():
    _out = ''
    return _out

def main():
    _msg = ''
    _s = ''
    _toDO = []
    try:
        aspi = tp00.Aspirateur()
        world = tp00.Monde(aspi) 
    except Exception:
        return "test_tp00 is required to succeed"
        
    # Controle des attributs/méthodes requis
    _attr = "capteurs actions vivant".split()
    _toDO.extend( _attr )
    _meth = "setReward getLastReward getEvaluation getDecision".split()
    _toDO.extend( _meth )
    
    for _ in _attr:
        _msg += check_property(hasattr(tp00.Aspirateur,_),'%s inconnu' % _)
    print("attributs Aspirateur:",_msg)
    _s += _msg ; _msg = ''
    
    if '.'*len(_s) == _s:
        _msg = subtest_readonly(aspi,_attr)
        print("attributs are ReadOnly",_msg)
        _s += _msg ; _msg = ''
        
    
    for _ in _meth:
        _msg += check_property(hasattr(tp00.Aspirateur,_),'%s inconnu' % _)
        if _msg[-1] == '.' :
            _msg += check_property(callable(getattr(tp00.Aspirateur,_)), '%s pas une méthode' % _)
    print("méthodes Aspirateur:",_msg)
    _s += _msg ; _msg = ''
        
    _attr = "agent perfGlobale historique table".split()
    _toDO.extend( _attr )
    _meth = "updateWorld applyChoix getPerception step simulation".split()
    _toDO.extend( _meth )
    
    for _ in _attr:
        _msg += check_property(hasattr(tp00.Monde,_),'%s inconnu' % _)
    print("attributs Monde:",_msg)
    _s += _msg ; _msg = ''
    
    if '.'*len(_s) == _s:    
        _msg = subtest_readonly(world,_attr)
        print("attributs are ReadOnly",_msg)
        _s += _msg ; _msg = ''
    
    for _ in _meth:
        _msg += check_property(hasattr(tp00.Monde,_),'%s inconnu' % _)
        if _msg[-1] == '.' :
            _msg += check_property(callable(getattr(tp00.Monde,_)), '%s pas une méthode' % _)
    print("méthodes Monde:",_msg)
    _s += _msg ; _msg = ''

    _msg = test_init_Aspirateur()
    print("Constructeur Aspirateur",_msg)
    _s += _msg ; _msg = ''
    
    if '.'*len(_s) != _s :
        print(_s)
        print('correction needed, something missing')
    else:
        # On passe aux tests plus complexes
        for meth in _toDO :
            meth = 'test_'+meth
            _msg = eval(meth)()
            print(meth,_msg)
            _s += _msg
    
        
    # Bilan
    _all = len(_s) 
    _ok = _s.count('.')
    return _ok, (_all-_ok), _all, round(100 * _ok / _all, 2)

if __name__ == '__main__' :
    print("succ %d fail %d sum %d, rate = %.2f" % main())
    print("expected >> succ {0} fail 0 sum {0} rate = 100.00".format(57))
