# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""
import re

class Projet:
    def __init__(self, nameProj, categorie, nameIng, largeurPasse, hauteurPasse, refCote):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param nameProj: Project's name
        :type nameProj: str
        :param categorie: Building's category
        :type categorie: str
        :param nameIng: Engineer's name
        :type nameIng: str
        :param largeurPasse: width of the passes
        :type largeurPasse: float
        :param hauteurPasse: height of the passes 
        :type hauteurPasse: float
        :param refCote: reference level for the project
        :type refCote: float
        :return: A dictionary representing the caracteristics of the project
        :rtype: dict
        """

        # The 'nameProj' should be a str
        if not isinstance(nameProj, str):
            raise ValueError("Récupération des Données - Le format pour le nom du projet est incorrect")

        # The 'categorie' should be a str
        if not isinstance(categorie, str):
            raise ValueError("Récupération des Données - Le format pour la catégorie du bâtiment est incorrect")
        #Check the format of the categorie variable
        pattern = r"^Catégorie ([A-H]).*"
        match = re.match(pattern, categorie)
        if match:
            categorie = match.group(1)
        else:
            raise ValueError("Récupération des Données - Le format pour la catégorie du bâtiment est incorrect")
        
        # The 'nameIng' should be a str
        if not isinstance(nameIng, str):
            raise ValueError("Récupération des Données - Le format pour le nom de l'ingénieur est incorrect")
        
        # The 'largeurPasse' should be a float or a int
        if not isinstance(largeurPasse, (float, int)) or largeurPasse < 0 :
            raise ValueError("Récupération des Données - La valeur de la largeur de passes est incorrecte")
        
        # The 'hauteurPasse' should be a float or a int
        if not isinstance(hauteurPasse, (float, int)) or hauteurPasse < 0:
            raise ValueError("Récupération des Données - La valeur de la hauteur de passes est incorrecte")
        
        # The 'refCote' should be a float or a int
        if not isinstance(refCote, (float, int)):
            raise ValueError("Récupération des Données - La valeur de la cote de reference est incorrecte")
        
        self.caracteristics = {"Projet": nameProj,
                               "Catégorie": categorie,
                               "Ingénieur": nameIng,
                               "Largeur de passes": largeurPasse,
                               "Hauteur de passes": hauteurPasse,
                               "Cote de référence": refCote
                               }