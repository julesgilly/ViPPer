# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""
import re

class Fleche:
    def __init__(self, critereFleche, valeurFleche):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param critereFleche: critère de flèche sous la forme L/250
        :type critereFleche: str
        :param valeurFleche: valeur de la flèche admissible sur le critère n'est pas renseigné
        :type valeurFleche: float
        :return: A dictionary representing the caracteristics 
        :rtype: dict
        """
        
        pattern = r'^L/(\d+)$'
        match = re.match(pattern, critereFleche)
        if match:
            critereFleche = int(match.group(1))
            valeurFleche = None
        elif critereFleche == "Autres (Valeur à préciser)" and isinstance(valeurFleche, (float, int)):
            critereFleche = None
            valeurFleche = float(valeurFleche) * 10**(-3)
        else:
            raise ValueError("Récupération des Données - Le format pour la flèche admissible est incorrect")

        self.caracteristics = {"Critère": critereFleche,
                               "Flèche admissible": valeurFleche,
                               }