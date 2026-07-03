# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""

class Chargement:
    def __init__(self, torseurCharges, coteRef):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param torseurCharges: ensemble des informations sur les charges avec la forme suivante
                    torseurCharges = [[charge i, niveau i, type i, value i], ...]
                    avec : charge : le type de charge : "Permanente", "Exploitation"
                           niveau : le niveau de la charge
                           type: charge "Vertical", "Horizontal", "Moment"
                           value : la valeur de la composante de la charge (en kN ou kN.m)
        :type torseurCharges: liste
        :param coteRef: la cote de référence pour les calcul
        :type coteRef: float

        :return: A dictionary representing the caracteristics 
                 caractéristics = { 1: {'Type': type1, "Charge": charge1, 'Position': x1, 'P': P1},
                                    2: {'Type': type2, "Charge": charge2, 'Position': x2, 'P': P2}, And so on }
        :rtype: dict
        """

        # initialiser le dictionnaire
        self.caracteristics = {}

        # Itérer à travers la liste et construire le dictionnaire
        for i, item in enumerate(torseurCharges, start = 1):

            # Vérifier que le type de charge est dans la liste autorisée
            if item[0].lower() not in ["permanente", "exploitation"]:
                raise ValueError("Récupération des Données - Le type de charge n'est pas correct")
            else:
                charge = item[0]
            
            # Check if 'Niveau' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[1], (int, float)):
                raise ValueError("Récupération des Données - La valeur du niveau de la charge n'est pas acceptable")
            else:
                niveau = round(abs(item[1] - coteRef), 2)
            
            # Vérifier que le "type" de charge est dans la liste autorisée
            if item[2].lower() not in ["vertical", "horizontal", "moment"]:
                raise ValueError("Récupération des Données - La charge n'est pas correct")
            else:
                type = item[2]

            # Check if 'value' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[3], (int, float)):
                raise ValueError("Récupération des Données - La valeur de la composante de la charge n'est pas acceptable")
            else:
                value = item[3] * 10**(-3)

            self.caracteristics[i] =  { "Type": type,
                                   "Charge": charge,
                                   "Position": niveau,
                                   "P": value,
                                 }