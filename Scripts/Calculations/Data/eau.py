# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""


class Eau:
    def __init__(self, presenceEau, waterLevel, typeEau, waterDensity, coteRef):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param presenceEau: Is the water pressure taken into account in the calculation (True or False)
        :type type: bool
        :param waterLevel: Water level for calculations
        :type niveau_eau: float
        :param typeEau: Type "EE", "EH", "EB"
        :param waterDensity: value of the water density (in kN/m3)
        :type precaution: float
        :return: A dictionary representing the caracteristics 
        :rtype: dict
        """

        # Check the type of the 'presenceEau' variable (should be a bool). Otherwise, set it up to False
        if not isinstance(presenceEau, bool):
            presenceEau = False

        # The 'waterLevel' should be a float or a int
        if not isinstance(waterLevel, (float, int)):
            raise ValueError("Récupération des Données - La valeur du niveau d'eau est incorrecte")
        else:
            waterLevel = round(abs(waterLevel - coteRef), 2)
        
        # The 'waterDensity' should be a float or a int. Otherwise, take the value 0.010 MN/m3
        if not isinstance(waterDensity, (float, int)):
            waterDensity = 0.01
        else : 
            waterDensity = waterDensity * 10**(-3)

        # The 'typeEau' variable can only take four values: "EE", "EH", "EB" or "EC"
        if typeEau not in ["EE", "EH", "EB", "EC"]:
            typeEau = None

        self.caracteristics = {"Eau": presenceEau,
                               "Niveau": waterLevel,
                               "Type": typeEau,
                               "Densité": waterDensity,
                               }
       
        # dict to be used in the Sol>sol class for calculations
        self.eau_sol = {"Eau": False,
                        "Niveau": None,
                        "Type": None,
                        "Densité": waterDensity,
                        }