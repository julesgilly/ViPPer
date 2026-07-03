# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in December 2022 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""


class Acier:
    def __init__(self, fyk, palier, classe, Coeff_securite, Module):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param fyk: 'Limite d'élasticité des aciers' (units: MPa)
        :type fck: float or int
        :param palier: ''palier d'inclinaison horizontal ou incliné pour le calcul'
        :type palier: str
        :param classe: steel class. Per Eurocodes, classes are: A, B or C
        :type classe: str
        :param Coeff_securite: steel security coefficient per Eurocode (units: None)
        :type Coeff_securite: float
        :param Module: steel Young's modulus (units: MPa)
        :type Module: float or int
        :raise ValueError: If fck, Coeff_securite or Module are not a float/int
        :return: A dictionary representing the caracteristics of steel
        :rtype: dict
        """

        # The 'palier' variable can only take two values: "Horizontal" or "Incliné"
        # By default, 'palier' should take the value "Horizontal" if an error is encountered
        if palier.lower() not in ["horizontal", "incliné"]:
            palier = "Horizontal"
        
        # The 'classe' variable can only take three values: "A", "B" or "C"
        # By default, 'classe' should take the value "B" if an error is encountered
        if classe not in ["A", "B", "C"]:
            classe = "B"

        # Check if 'fyk' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(fyk, (int, float)):
            raise ValueError("Récupération des Données - La valeur de fyk n'est pas acceptable")

        # Check if 'Coeff_securite' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(Coeff_securite, (int, float)):
            raise ValueError("Récupération des Données - La valeur du coefficient de sécurité de l'acier n'est pas acceptable")

        # Check if 'Module' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(Module, (int, float)):
            raise ValueError("Récupération des Données - La valeur du module d'élasticité de l'acier n'est pas acceptable")

        self.caracteristics = {"fyk": fyk,
                               "Palier": palier,
                               "Classe": classe,
                               "Coefficient sécurité": Coeff_securite,
                               "Module élasticité": Module
                               }

