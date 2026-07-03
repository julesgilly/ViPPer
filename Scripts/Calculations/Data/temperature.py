# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""


class Temperature:
    def __init__(self, coeffThermique, deltaTemperature):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param coeffThermique: Is the water pressure taken into account in the calculation (True or False)
        :type coeffThermique: flaot
        :param deltaTemperature: Water level for calculations
        :type deltaTemperature: float
        :return: A dictionary representing the caracteristics 
        :rtype: dict
        """
        # The 'coeffThermique' should be a float or a int
        if not isinstance(coeffThermique, (float, int)):
            raise ValueError("Récupération des Données - La valeur du coefficient thermique est incorrecte")
        
        # The 'deltaTemperature' should be a float or a int
        if not isinstance(deltaTemperature, (float, int)):
            raise ValueError("Récupération des Données - La valeur du delta de température est incorrecte")

        self.caracteristics = {"Coefficient Thermique": coeffThermique,
                               "Delta": deltaTemperature,
                               }