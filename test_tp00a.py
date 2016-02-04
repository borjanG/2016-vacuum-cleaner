#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__ = "tests unitaires pour la première réalisation aspi autonome"
__date__ = "03.02.16"
__version__ = "0.1"

## remplacer XXX par le nom de votre fichier
import data.monde as tp00
# import mmc_tp00 as tp00

# NE RIEN MODIFIER A PARTIR D'ICI
import random
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

def main():
    _msg = ''
    _s = ''
    # Controle des attributs/méthodes requis
    _attr = "capteurs actions vivant".split()
    _meth = "setReward getEvaluation getDecision".split()
    for _ in _attr:
        _msg += check_property(hasattr(tp00.Aspirateur,_),'%s inconnu' % _)
    print("attributs Aspirateur:",_msg)
    _s += _msg ; _msg = ''
        
    for _ in _meth:
        _msg += check_property(hasattr(tp00.Aspirateur,_),'%s inconnu' % _)
        if _msg[-1] == '.' :
            _msg += check_property(callable(getattr(tp00.Aspirateur,_)), '%s pas une méthode' % _)
    print("méthodes Aspirateur:",_msg)
    _s += _msg ; _msg = ''
        
    _attr = "agent perfGlobale historique".split()
    _meth = "updateWorld applyChoix getPerception step simulation".split()
    for _ in _attr:
        _msg += check_property(hasattr(tp00.Monde,_),'%s inconnu' % _)
    print("attributs Monde:",_msg)
    _s += _msg ; _msg = ''
        
    for _ in _meth:
        _msg += check_property(hasattr(tp00.Monde,_),'%s inconnu' % _)
        if _msg[-1] == '.' :
            _msg += check_property(callable(getattr(tp00.Monde,_)), '%s pas une méthode' % _)
    print("méthodes Monde:",_msg)
    _s += _msg ; _msg = ''

        
    # Bilan
    _all = len(_s) 
    _ok = _s.count('.')
    return _ok, (_all-_ok), _all, round(100 * _ok / _all, 2)

if __name__ == '__main__' :
    print("succ %d fail %d sum %d, rate = %.2f" % main())
    print("expected >> succ {0} fail 0 sum {0} rate = 100.00".format(22))
