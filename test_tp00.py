#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__ = "tests unitaires pour la première réalisation aspi autonome"
__date__ = "27.01.16"
__version__ = "0.2a"

## remplacer XXX par le nom de votre fichier
import data.monde as tp00

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

def subtest_table_size(table,nbl,nbc):
    """ vérifie qu'une table a le bon nombre de lignes et de colonnes 

    In [20]: subtest_table_size( [ [], [1], [1,2,3] ],5,1)
    failure bad lines
    failure bad columns at line 0
    failure bad columns at line 2
    line 3 missing
    line 4 missing
    Out[20]: 'EE.EEE'

    """
    _out = ''
    _out += check_property(len(table) == nbl,'bad lines')
    for k in range(nbl):
        try:
            _out += check_property(len(table[k]) == nbc,'bad columns at line %d' % k)
        except:
            print("line %d" % k,'missing')
            _out += 'E'
    return _out
    
def test_table():
    """ la table existe
    On vérifie que c'est un attribut en lecture seule
    On vérifie que c'est bien une liste de listes d'entiers
    """
    _out = ''
    _a = tp00.Aspirateur()
    nl,nc=3,3
    _m = tp00.Monde(_a,nl,nc)
    _out += check_property(isinstance(_m.table, list ),'list expected found %s' % type(_m.table))
    if _out[-1] != '.' : return _out
    _tmp = subtest_table_size(_m.table,nl,nc) ; _out += _tmp
    if _tmp != '.'*nl+'.' :
        return _out
    for x in _m.table[0]: 
        _out += check_property(x in tp00.objetsStatiques,'unknown object %d' % x)
    if _out.count('.') != len(_out): return _out
    # non modifiable
    try:
        _m.table = 'glob'
        if _m.table == 'glob': 
            _out += '1'
        else: _out += '.'
    except:
        _out += '.'
    if _out[-1] != '.' : return _out
    
    try:
        j = random.randrange(len(_m.table[0]))
        _m.table[0][j] = -42 #tentative d'affectation
        if _m.table[0][j] == -42 : #réussite c'est mauvais
            _out += '2'
        else:
            _out += '.'
    except:
        _out += '.'
    return _out
        
def test_init():
    """ test le constructeur 
    1 parametre obligatoire (l'agent)
    2 parametres optionnels par defaut 1 & 2: ligne colonne
    """
    _out = ''
    try:
        _ = tp00.Monde()
        _out = '1'
    except:
        _out = '.'
    if '1' in _out: return _out
    
    try:
        _ = tp00.Monde(1)
        _out = 'a'
    except:
        _out = '.'
    if 'a' in _out: return _out

    _a = tp00.Aspirateur()
    try:
        _ = tp00.Monde(_a)
        _out += '.'
        _out += subtest_table_size(_.table,1,2)
    except:
        _out += '2'
    if '2' in _out: return _out
    
    try:
        _ = tp00.Monde(_a,23)
        _out += '.'
        _out += subtest_table_size(_.table,23,2)
    except:
        _out += '3'
    if '3' in _out: return _out        
    
    try:
        _ = tp00.Monde(_a,2,3)
        _out += '.'
        _out += subtest_table_size(_.table,2,3)
    except:
        _out += '4'

    return _out
    
def test_str():
    """ test l'affichage """
    _out = ''
    _ = tp00.Aspirateur()
    _m = tp00.Monde(_)
    _s = str(_m)
    _out += check_property(isinstance(_s,str),'str is not %s' % type(_s))
    _out += check_property(tp00.objetsStatiques[100][1] in _s,'no agent in world')
    # le monde contient obligatoirement des 0 ou des 1
    prop = tp00.objetsStatiques[0][1] in _s
    prop = prop or tp00.objetsStatiques[1][1] in _s
    _out += check_property(prop,'no basic item in world')
    return _out

def subtest_initialisation_nbSol(world,nl,nc):
    """ test couteux on limite la taille nl*nc """
    _rep = set([])
    if nl*nc < 3 : _m = 200
    elif nl*nc < 5 : _m = 700
    else: _m = 5000 # nl*nc * 2**(nl*nc) ça monte vite
    for i in range(_m):
        world.initialisation()
        _o = [ world.table[i][j] for i in range(nl) for j in range(nc) ]
        _o.append(world.posAgent[0]*nc+world.posAgent[1])
        _rep.add( str(_o) )
    return len( _rep )
            
def test_initialisation():
    """ test l'initialisation 
        On vérifie que toutes les solutions sont possibles
    """
    _out = ''
    _ = tp00.Aspirateur()
    _m = tp00.Monde( _ )
    _rep = subtest_initialisation_nbSol(_m,1,2)
    _out += check_property( 8 == _rep , "nb sol found %d" % _rep )
    _m = tp00.Monde( _, 2, 1 )
    _rep = subtest_initialisation_nbSol(_m,2,1)
    _out += check_property( 8 == _rep , "nb sol found %d" % _rep )
    _m = tp00.Monde( _, 2 )
    _rep = subtest_initialisation_nbSol(_m,2,2)
    _out += check_property( 64 == _rep , "nb sol found %d" % _rep )
    nl,nc = 2,3
    _m = tp00.Monde( _, nl,nc)
    _rep = subtest_initialisation_nbSol(_m,nl,nc)
    _sz = nl*nc
    _out += check_property( _sz * 2**_sz == _rep , "vues %d attendues %d" % (_rep,_sz * 2**_sz ))
        
    return _out
    
def test_posAgent():
    """ test la position de l'agent """
    _out = ''
    _ = tp00.Aspirateur()
    _m = tp00.Monde(_)
    _out += check_property(isinstance(_m.posAgent,tuple),"tuple expected, got %s" % type(_m.posAgent))
    _out += check_property(len(_m.posAgent) == 2, "wrong size")
    for nl,nc in ( (4,3), (11,5), (7,13), (3,1), (1,7) ):
        _m = tp00.Monde(_,nl,nc)
        _bag = set([])
        _nmax = 13
        for i in range(_nmax):
            _m.initialisation()
            _bag.add( _m.posAgent )
            _out += check_property(_m.posAgent[0] in range(nl),"position ligne")
            _out += check_property(_m.posAgent[1] in range(nc),"position colonne")
        _out += check_property(2 < len(_bag) <= _nmax, 'found %d posAgent' % len(_bag))
    return _out
    
def main():
    # l'existence de certaines choses est requise
    _s = ''
    _trois = "Aspirateur Monde objetsStatiques".split()
    for att in _trois:
        _s += check_property(hasattr(tp00,att),att)
    _s += check_property(len(tp00.objetsStatiques) == 3,"nb entités")
    _s += check_property(all([_ in tp00.objetsStatiques for _ in (0,1,100)]),'key objets')
    _s += check_property(all([len(tp00.objetsStatiques[_])==2 for _ in (0,1,100)]),'descr objets')
    _attrs = 'table posAgent initialisation __init__ __str__'.split()
    for att in _attrs: _s += check_property(hasattr(tp00.Monde,att),att)
    if '.'*len(_s) != _s :
        print(_s)
        print('correction needed, something missing')
    else:
        # On passe aux tests plus complexes
        _s += test_init()
        _s += test_str()
        _s += test_initialisation()
        _s += test_posAgent()
        _s += test_table()
        
    # Bilan
    _all = len(_s) 
    _ok = _s.count('.')
    return _ok, (_all-_ok), _all, round(100 * _ok / _all, 2)
    
if __name__ == "__main__" :

    print("succ %d fail %d sum %d, rate = %.2f" % main())
    print("expected >> succ {0} fail 0 sum {0} rate = 100.00".format(198))
    
