# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""
import re

class Lierne:
    def __init__(self, listeLierne):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param listeLierne: ensemble des informations sur les liernes avec la forme suivante
                    listeLierne = [[numéro lit i, typeLierne i, enrobageLierne i, largeurLierne i, hauteurSurEpLierne i], ...]
                    avec : numéro lit : le numéro du lit de butons lié au dict des butons
                           typeLierne : le type de lierne parmi "Béton dans l'épaisseur", "Béton en sur-épaisseur extérieure", "Béton en sur-épaisseur intérieure"
                           enrobageLierne: l'enrobage dans les liernes (en cm)
                           largeurLierne : la largeur de la lierne (en cm)
                           hauteurSurEpLierne : la hauteur de la sur-épaisseur de la lierne (en cm)
        :type critereFleche: liste
        :return: A dictionary representing the caracteristics 
                 caractéristics = { 1: {"Numéro": numéro lit 1, "Type": typeLierne 1, "Enrobage": enrobageLierne 1, "Largeur": largeurLierne 1, "Hauteur Sur-épaisseur": hauteurSurEpLierne 1}, 
                                    2 : {...}}
        :rtype: dict
        """
        
        # Tirer la liste pour faire correspondre les numéro de lit de butons avec l'ordre dans le dictionnaire
        listeLierne.sort(key = lambda x: int(x[0]))

        # initialiser le dictionnaire
        self.caracteristics = {}

        # Itérer à travers la liste et construire le dictionnaire
        for i, item in enumerate(listeLierne, start = 1):
            # Ajouter le numéro du lit
            numero = item[0]

            # Vérifier que le type de lierne est dans la liste autorisée
            if item[1].lower() not in ["béton dans l'épaisseur", "béton en sur-épaisseur extérieure", "béton en sur-épaisseur intérieure"]:
                raise ValueError("Récupération des Données - Le type de lierne n'est pas correct")
            else:
                type = item[1]
            
            # Check if 'enrobageLierne' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[2], (int, float)):
                raise ValueError("Récupération des Données - La valeur de l'enrobage de la lierne n'est pas acceptable")
            else:
                enrobage = item[2] * 10**(-2)

            # Check if 'largeurLierne' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[3], (int, float)):
                raise ValueError("Récupération des Données - La valeur de la largeur de la lierne n'est pas acceptable")
            else:
                largeur = item[3] * 10**(-2)

            #Si pas de sur-épaisseur, la hauteur de la sur-épaisseur prennent les valeurs None
            if item[1] == "Béton dans l'épaisseur":
                hauteur = None
            else:
                # Check if 'hauteurSurEpLierne' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[4], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la hauteur de la sur-épaisseur de la lierne n'est pas acceptable")
                else:
                    hauteur = item[4] * 10**(-2)

            self.caracteristics[i] =  { "Numéro": numero,
                                   "Type": type,
                                   "Enrobage": enrobage,
                                   "Largeur": largeur,
                                   "Hauteur Sur-épaisseur": hauteur
                                 }