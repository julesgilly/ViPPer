# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""

import re

class Bois:
    def __init__(self, classeServiceBois, dureeActionBois, Coeff_securite_Bois, classeBois, facteurRelatifBois):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param classeServiceBois: classe de service du bois
        :type classeServiceBois: str
        :param dureeActionBois: durée des actions pour les éléments bois
        :type dureeActionBois: float
        :param Coeff_securite_Bois: Coefficient de sécurité pour le bois
        :type Coeff_securite_Bois: float
        :param classeBois: Classe mécanique du bois
        :type classeBois: str
        :param facteurRelatifBois: Facteur relatif en compression
        :type facteurRelatifBois: float
        :return: A dictionary representing the caracteristics 
        :rtype: dict
        """

        # The 'classeServiceBois' should be a str
        if not isinstance(classeServiceBois, str):
            raise ValueError("Récupération des Données - Le format pour la classe de service du bois est incorrect")
        
        #Check the format of the categorie variable
        pattern = r'^Classe de service\s*([1-3])$'
        match = re.match(pattern, classeServiceBois)
        if match:
            classeServiceBois = int(match.group(1))
        else:
            raise ValueError("Récupération des Données - Le format pour la classe de service du bois est incorrect")
        
        # Check if 'dureeActionBois' is an str with the right form
        if dureeActionBois.lower() not in ["instantanée", "court terme", "moyen terme", "long terme", "permanent"]:
            raise ValueError("Récupération des Données - La valeur de la durée des actions des éléments bois n'est pas correcte")

        # Check if 'Coeff_securite' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(Coeff_securite_Bois, (int, float)):
            raise ValueError("Récupération des Données - La valeur du coefficient de sécurité du bois n'est pas acceptable")

        # The 'classeBois' should be a str
        if not isinstance(classeBois, str):
            raise ValueError("Récupération des Données - Le format pour la classe mécanique du bois est incorrect")
        
        #Check the format of the categorie variable
        pattern = r'^C([1-9][0-9])$'
        match = re.match(pattern, classeBois)
        if match:
            classeBois = int(match.group(1))
        else:
            raise ValueError("Récupération des Données - Le format pour la classe mécanique du bois est incorrect")
        
        # Check if 'Coeff_securite' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(facteurRelatifBois, (int, float)):
            raise ValueError("Récupération des Données - La valeur du facteur relatif en compression du bois n'est pas acceptable")
        
        self.caracteristics = {"Service": classeServiceBois,
                               "Action": dureeActionBois,
                               "Coefficient de sécurité": Coeff_securite_Bois,
                               "Classe": classeBois,
                               "Facteur relatif": facteurRelatifBois  
                               } # Add the caracteristics