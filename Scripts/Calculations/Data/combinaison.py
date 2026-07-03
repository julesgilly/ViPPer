# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""


class Combinaison:
    def __init__(self, coeffG, coeffQ):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param coeffG: coefficient pour les charges permanentes
        :type coeffG: float
        :param coeffQ: coefficient pour les charges d'exploitation
        :type coeffQ: float
        :return: A dictionary representing the caracteristics 
        :rtype: dict
        """
        # The 'coeffG' should be a float or a int
        if not isinstance(coeffG, (float, int)):
            raise ValueError("Récupération des Données - La valeur du coefficient pour les charges permanente est incorrecte")
        
        # The 'coeffQ' should be a float or a int
        if not isinstance(coeffQ, (float, int)):
            raise ValueError("Récupération des Données - La valeur du coefficient pour les charges d'exploitation est incorrecte")

        self.caracteristics = {"G": coeffG,
                               "Q": coeffQ,
                               }