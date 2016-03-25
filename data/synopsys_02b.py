#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mise en place de la correction en fonction du descriptif TP02-B
Complétez les informations en fonction des directives de la fiche
"""

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__version__ = "0.1"

__date__ = "14.03.16"
__usage__ = "Le simulateur"

# remplacer XXX par le fichier du TP02-A
from tp02a import objetsStatiques, Aspirateur_PG, Monde
#from corrige_tp02a import objetsStatiques, Aspirateur_PG, Monde
from briques import ProgramGenetic, mmcUnaire, mmcBinaire, GeneratePercept
from tools_tp02 import readerEnvts
import copy, random

# On ajoute dans objetsStatiques 2, 3 et 4 et -1
objetsStatiques[3] = ('jouets aspirables', 'j')
objetsStatiques[4] = ('jouets deplacables', 'J')

class MondeSimulation(Monde):
    def __init__(self,agent,nbLignes=1,nbColonnes=2):
        assert hasattr(agent,'energie'), "attribut 'energie' is required"
        super().__init__(agent,nbLignes,nbColonnes)

    def simulation(self,n,envt=None,position=None):
        """ 
            la simulation dure max n tours et s'arrete des que l'agent 
            n'est plus opérationnel
        """
        self.initialisation(envt,position)
        ...
        return self.perfGlobale

    def initialisation(self,envt=None,position=None):
        super().initialisation()
        if envt is not None: self._table = [ envt ]
        if position is not None: self._pos = 0,position
            
        #variables ajoutées sur l'agent
        ...
        # print(self.table) facultatif
        if hasattr(self.agent,'reset') and callable(self.agent.reset):
            self.agent.reset() 
        
    @property
    def perfGlobale(self):
        # Voir fiche TP02-B
        
    def getPerception(self,capteurs):
        """ 
           informe l'agent en fonction des capteurs 
           gestion des risques de panne (proba fixée à .1) 1 parmi k
        """
        _d = [ (-1,0), (-1,1), (0,1), (1,1),
                (1,0), (1,-1), (0,-1), (-1,-1), (0,0) ]

        kapteurs = capteurs[:] # on fait une copie pour les pannes
        if 8 in kapteurs: kapteurs.remove(8) # pas de panne sur le 8
        _panne = -1 # pas de panne
        if (hasattr(self.agent,'panne') and
            getattr(self.agent,'panne') and
            len(kapteurs) > 0):
            _proba = random.random()
            if _proba < .1 : _panne = random.choice(kapteurs)

        if _panne > -1: print("panne sur le capteur {}".format(_panne))

        # calculer ce que voit l'agent, s'il y a une panne sur le capteur
        # _panne : mettre -1 au lieu de l'information dans la table
        # renvoyer la réponse (une liste de la taille de capteurs)
        
    def applyChoix(self,choix):
        """
           Modifie table & posAgent en fonction de choix
           Modifie la fonction d'énergie de l'Aspirateur
           Renvoie la récompense numérique adéquate

           Récompenses :
           Aspirer : 2 si poussière, -3 si jouets aspirables, -1 sinon
           Gauche / Droite : 1 si possible, -1 sinon
           Repos : 2 si prise électrique, 0 sinon

           Effet Energie
           Aspirer: -5
           Gauche / Droite : -2
           Repos sans capteur +3
           Repos avec capteur +20 si prise électrique, 0 sinon
        """

        # Appliquer les opérations demandées
        # mise à jour de self.agent.energie
        # renvoie de la récompense
        # mise à jour des compteurs utiles

class Simulateur(objet):
    """ En entrée:
        - le nombre maximum d'itérations
        - le fichier des environnements
        - la liste des Capteurs
        - le fait qu'il peut y avoir des pannes
    """
    def __init__(self,nbMaxIter,ficEnvt,lCap=[],panne=False):
        # stocker les parametres dans 4 variables privées self.__XXX

    @property
    def panne(self): return self.__xxx
    @panne.setter
    def panne(self,v):
        """
           si pas de capteur on se moque de v, on force xxx à False
           si capteur alors on prend bool(v) comme valeur
        """
        

    def run(self,prog,gp=None):
        """
        prog est un ProgramGenetic
        gp est un GeneratePercept optionnel
        
        crée l'aspirateur Aspirateur_PG
        ajoute l'information panne à l'aspirateur
        met un compteur a 0
        détermine quels environnements seront utilisables 0, 1, 2
        pour chaque environnement
             s'il n'est pas utilisable : continue
             creer m = MondeSimulation(aspirateur,1,nbCol)
             pour chaque position a tester
                 compteur = compteur + m.simulation(nbIter,table,position)
        renvoyer compteur
        
        renvoie le score total obtenu pour chaque simulation,
        on aurait pu prendre non pas le score de la imulation mais
        celui de la performance de l'agent ou une combinaison des deux
            exemple: alpha perfGlobale + beta getEvaluation()
            total_sim = 0 ; total_agent = 0
            alpha = .5 ; beta = 1 - alpha
            ....
            for p in _lpos:
                total_sim += m.simulation( .... )
                total_agent += m.agent.getEvaluation()
            ...
            return alpha * total_sim + beta * total_agent
        """
