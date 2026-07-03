# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""
import re

class Plancher:
    def __init__(self, listePlancher, coteRef, longueurVoile, epaisseurVoile, coteSupVoile_DEF, coteSupVoile_PROV):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param listePlancher: ensemble des informations sur les planchers avec la forme suivante
                    listePlancher = [[type i, Niveau i, Epaisseur i, appui i], ...]
                    avec : type : le type de plancher: "Plancher" ou "Dallage"
                           Niveau : le niveau du plancher
                           Epaisseur: l'épaisseur du plancher (en m)
                           Appui i: le plancher est-il un appui du VPP ? (True/False)
        :type listePlancher: liste
        :param coteRef: la cote de référence pour les calcul
        :type coteRef: float
        :param longueurVoile: la longueur du voile (en m)
        :type longueurVoile: float
        :param epaisseurVoile: l'épaisseur du voile (en m)
        :type epaisseurVoile: float
        :param coteSupVoile_DEF: la cote supérieure du voile lors de la phase DEFINITIVE
        :type coteSupVoile_DEF: float
        :param coteSupVoile_PROV: la cote supérieure du voile lors de la phase PROVISOIRE
        :type coteSupVoile_PROV: float

        :return: A dictionary containing all the informations defining the 'plancher' object
                 dictPlancher = { 1: {"Type": type 1, "Niveau": Niveau en cote relative 1, "Epaisseur": Epaisseur 1, "Butonnant": Bool 1}, 
                                    2 : {...}}
        :rtype: dict
        :return: A dictionary representing the caracteristics 
                 caracteristics = {"Longueur VPP": longueur du voile, "Epaisseur VPP":Epaisseur du VPP, "Cote DEF": CoteSupVoile_DEF, "CotePROV": CoteSupVoile_PROV} 
        :rtype: dict
        """
        # Check if 'longueurVoile' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(longueurVoile, (int, float)):
            raise ValueError("Récupération des Données - La valeur de la longueur du VPP n'est pas acceptable")

        # Check if 'epaisseurVoile' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(epaisseurVoile, (int, float)):
            raise ValueError("Récupération des Données - La valeur de l'épaisseur' du VPP n'est pas acceptable")

        # Check if 'coteSupVoile_DEF' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(coteSupVoile_DEF, (int, float)):
            raise ValueError("Récupération des Données - La valeur de la cote supérieure du VPP en phase DEFINITIVE n'est pas acceptable")
        else:
            coteSupVoile_DEF = round(abs(coteSupVoile_DEF - coteRef), 2)
        
        # Check if 'coteSupVoile_PROV' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(coteSupVoile_PROV, (int, float)):
            raise ValueError("Récupération des Données - La valeur de la cote supérieure du VPP en phase PROVISOIRE n'est pas acceptable")
        else:
            coteSupVoile_PROV = round(abs(coteSupVoile_PROV - coteRef), 2)

        self.caracteristics = {"Longueur VPP": longueurVoile, 
                               "Epaisseur VPP": epaisseurVoile,
                               "Cote DEF": coteSupVoile_DEF,
                               "Cote PROV": coteSupVoile_PROV}

        # initialiser le dictionnaire en liste d'abord pour trier les éléments 
        self.dictPlancher = []

        # Itérer à travers la liste et construire le dictionnaire
        for i, item in enumerate(listePlancher, start = 1):

            # Vérifier que le type de plancher est dans la liste autorisée
            if item[0].lower() not in ["plancher", "dallage"]:
                raise ValueError("Récupération des Données - Le type de plancher n'est pas correct")
            else:
                type = item[0]
            
            # Check if 'niveau' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[1], (int, float)):
                raise ValueError("Récupération des Données - La valeur du niveau du plancher n'est pas acceptable")
            else:
                niveau = round(abs(item[1] - coteRef), 2)

            # Check if 'epaisseur' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[2], (int, float)):
                raise ValueError("Récupération des Données - La valeur de l'épaisseur du plancher n'est pas acceptable")
            else:
                epaisseur = item[2]

            # Check the 'appui' variable
            if not isinstance(item[3], bool):
                raise ValueError("Récupération des Données - Indiquer si le plancher est un appui")
            else:
                if type.lower() == "plancher":
                    appui = True
                else:
                    appui = item[3]

            dict = { "Type": type,
                                   "Niveau": niveau,
                                   "Epaisseur": epaisseur,
                                   "Appui" : appui
                                    }
            
            self.dictPlancher.append(dict)
        
        # Trier le dictionnaire en fonction de la valeur "Niveau" 
        self.dictPlancher = {i: d for i, d in enumerate(sorted(self.dictPlancher, key=lambda item: item["Niveau"]), start=1)}