#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "Mise en place du TP02a"
__date__ = "10.03.16"
__version__ = "0.2"

# remplacer XXX par votre fichier issu du TD2 (le 00a)
from XXX import objetsStatiques, Aspirateur, Monde
from briques import ProgramGenetic, GeneratePercept
import copy, random

class Aspirateur_PG(Aspirateur):
    """
        prog: un programme genetique, par défaut None
        gp: un GeneratePercept, par défaut None
        lCap: valeur par défaut []
    """
    def __init__(self,prog=None,gp=None,lCap=[]):
        # gestion du GeneratePercept choisir la variable de stockage
        if gp is not None: self.__YYY = gp
        elif lCap == []: self.__YYY = None
        else: self.__YYY = GeneratePercept(lCap,objetsStatiques)
        if prog is None:
            # choisir le nom de votre variable, remplacez les ...
            # traiter le cas lCap = [] vs lCap != []
            self.__XXX = ProgramGenetic(...)
        elif isinstance(prog,ProgramGenetic):
            # vérifier que prog est compatible si lCap != []
            # sinon provoquer une erreur
            self.__XXX = prog
        else:
            raise AssertionError("{} expected got {}"
                                 .format(ProgramGenetic,type(prog)))
        # récupération des actions depuis votre variable
        # attention ce n'est pas une 'list' c'est un 'set'
        lAct = 
        super().__init__(lCap,lAct)
        # choisir la variable pour energie
        self.__ZZZ = 100
        self.reset()

    def reset(self):
        """ initialisation de certaines variables pour chaque simulation """
        self.vivant = True
        self.cpt = 0
        # ici rajouter celles dont vous pensez avoir besoin
        
    @property
    def energie(self): return self.__XXX
    @energie.setter
    def energie(self,v):
        assert isinstance(v,int), "int expected found {}".format(type(v))
        self.__XXX = max(0,min(100,v)) # force la valeur entre 0 et 100
        # attention si energie passe a 0 ...

    # On surcharge vivant
    @property
    def vivant(self): return self.__XXX
    @vivant.setter
    def vivant(self,v):
        if isinstance(v,bool): self.__XXX = v

    @property
    def cpt(self): return self.__XXX
    @cpt.setter
    def cpt(self,v):
        assert isinstance(v,int)
        self.__XXX # attention cpt est contraint entre 0 et le nombre de genes

    @property
    def nbTours(self): 
	""" renvoie le nombre d'itérations pendant lesquelles aspi est vivant """
        
    @property
    def program(self): return self.__XXX

    def getEvaluation(self):
        """ renvoie l'évaluation de l'agent """

    def getDecision(self,percepts):
        """ deux cas à traiter suivant que percepts = [] ou pas """
        if percepts == []:
            # on utilise cpt pour savoir ce qu'il faut lire/récupérer
            return
        # a partir d'ici on est dans le cas ou l'agent percoit
        # il faut associer au percepts un numéro et aller regarder
        # quelle est l'instruction à renvoyer

        return


class Monde_AG(Monde):
    def __init__(self,agent,nbLignes=1,nbColonnes=2):
        # On regarde si l'agent à une variable energie
        assert hasattr(agent,'energie'), "attribut 'energie' is required"
        super().__init__(agent,nbLignes,nbColonnes)
    
    def initialisation(self):
        super().initialisation()
        # ajouter à l'agent un compteur de pièces nettoyées, initalisé à 0
        # ajouter à l'agent le nombre de pièces sales au départ
        # On regarde si l'agent a une commande reset
        if hasattr(self.agent,'reset') and callable(self.agent.reset):
            self.agent.reset()

 
  def getPerception(self,capteurs):
        """ informe l'agent en fonction des capteurs """
        # code similaire à celui de World

   def applyChoix(self,choix):
        """ 
            modifie table & posAgent en fonction de choix 
            modifie l'energie de l'aspirateur
        """
        # code similaire à World une action en plus Repos
        # nécessitant un traitement spécifique suivant que l'agent
        # dispose de capteurs ou pas (il suffit de poser la question
        # à self.agent)
        # Les récompenses ne sont pas les couts énergétiques
        # Aspirer 2 si poussière, -1 sinon
        # Gauche 1 si possible, -1 sinon
        # Droite 1 si possible, -1 sinon
        # Repos 0 pour l'aspirateur sans capteur
        # Repos 2 si prise électrique, 0 sinon
        # les couts energétiques sont appliqués par applyChoix
        # self.agent.energie est donc à mettre à jour

    @property
    def perfGlobale(self):
        # cf fiche TP02-A
