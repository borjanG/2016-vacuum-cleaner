#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Outils pour la simulation
* generateEnvts : écrit dans un fichier différents monde
* readerEnvts : lit un fichier produit par generateEnvts et stocke 
  les informations dans un dictionnaire
"""

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__version__ = "0.2"
__date__ = "14.03.16"
__usage__ = "Quelques outils nécessaires pour la simulation génétique"


import random

def generateEnvts(fic,sample=5):
    """
    des tailles 3, 7, 11 pour les mondes avec deux objets
    des tailles 7, 11, 13 pour les mondes avec tous les objets
    un monde de taille 17.

    sample nombre de positions envisagées
    """
    def where(_t):
        """ cherche une position ou inserer un typ_ dans _t, 
            renvoie l'index choisi, on cherche en priorité une case propre
            On cherche a partir d'une position aléatoire entre _ et _ -1
        """
        _ = random.randrange(sz)
        _proba = random.random()
        if _proba <= .5:
            _found = False
            i = _
            _propre = _t.count(0)
            _val = 1 if _propre == 0 else 0
            while not _found:
                if _t[i] != _val: i = (i+1)%sz
                else: _found = True
            return i
        return -1

    random.seed() # initialisation du générateur aléatoire
    _obj = (0,1)
    with open(fic,"w") as f:
        # environement uniquement pour aspi sans capteurs (0)
        # que des 0,1 comme objets
        _taille = (3,5,7)
        for sz in _taille:
            _table = [ random.choice (_obj) for _ in range(sz)]
            if sample > sz: _pos = list(range(sz))
            else: _pos = random.sample( range(sz), sample)
            _ligne = [0, sz]+_table+_pos
            for x in _ligne: f.write("{} ".format(x))
            f.write('\n')
        # environement uniquement pour aspi sans et avec capteurs (2)
        # que des 0,1 comme objets
        _taille = (3,3,7,7,11,11)
        for sz in _taille:
            _table = [ random.choice (_obj) for _ in range(sz)]
            if sample > sz: _pos = list(range(sz))
            else: _pos = random.sample( range(sz), sample)
            _ligne = [2, sz]+_table+_pos
            for x in _ligne: f.write("{} ".format(x))
            f.write('\n')
        # environement uniquement pour aspi sans et avec capteurs (2)
        # 3 prises, au plus un objet deplaçable et un objet aspirable
        _taille = (7,7, 11,11,13,13,17)
        for sz in _taille:
            _table = [ random.choice (_obj) for _ in range(sz)]
            # 3 prises
            _prises = random.sample(range(sz),3)
            for _ in _prises: _table[_] = 2
            for v in (3,4):
                i = where(_table)
                if i > -1 : _table[i] = v
            if sample > sz: _pos = list(range(sz))
            else: _pos = random.sample( range(sz), sample)
            _ligne = [1, sz]+_table+_pos
            for x in _ligne: f.write("{} ".format(x))
            f.write('\n')
        f.close()

def readerEnvts(fic):
    """
    lit un fichier dont les lignes sont de la forme
    type colonne table p1 ... pk
    Toutes les valeurs sont des entiers
    renvoie un dictionnaire (typ,nbCol,table,positions) indexé sur les lignes
    """

    with open(fic,"r") as f:
        l = f.readlines()
        f.close()

    dic = {}
    #l contient des chaines
    for i,ligne in enumerate(l):
        values = [int(x) for x in ligne.strip().split()] # des entiers
        dic[i+1] = (values[0],values[1],
                    values[2:2+values[1]],values[2+values[1]:])

    return dic
