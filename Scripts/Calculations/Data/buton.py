# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""

class Buton:
    def __init__(self, listeButon, listeSemButon, coteRef):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param listeButon: ensemble des informations sur les butons avec la forme suivante
                    listeButon = [[lit i, niveauButon i, entraxeButon i, entraxeGaucheButon i, entraxeDroiteButon i, fonctionnementButon i, inclinaisonButon i, distanceButon i,
                                    longueurButon i, materiauButon i, typeButon i, accrochageButon i], ...]
                    avec : lit: le numéro du lit (numéro indicatif en fonction de l'ordre de remplissage par l'utilisateur)
                    niveauButon: le niveau du buton
                    entraxeButon: l'entraxe courant des butons (en m)
                    entraxeGaucheButon: distance entre le premier buton et l'extrémité gauche du VPP (en m)
                    entraxeDroiteButon: distance entre le dernier buton et l'extrémité droite du VPP (en m)
                    fonctionnementButon: fonctionnement du buton "Incliné", "Horizontal"
                    inclinaisonButon: inclinaison du buton (en degrés)
                    distanceButon: distance au voile du pied de buton (en m)
                    longueurButon: longueur du buton (en m)
                    materiauButon: matériau du buton "Métal", "Bois"
                    typeButon: type de buton 
                    accrochageButon: accrochage du buton "Corbeau béton"
        :type listeButon: liste
        :param listeSemButon: ensemble des informations sur les semelles des butons avec la forme suivante
                    listeSemButon = [[listeAppuiButon, largeurSemButon, longueurSemButon, hauteurSemButon], ...]
                    avec : listeAppuiButon: ensemble des numéros des lits de buton s'appuyant sur la semelle
                    largeurSemButon: largeur de la semelle (en m)
                    longueurSemButon: longueur de la semelle (en m)
                    hauteurSemButon: hauteur de la semelle (en m)
        :type listeSemButon: liste
        :param coteRef: la cote de référence pour les calcul
        :type coteRef: float

        :return: A dictionary representing the caracteristics 
                 caracteristics_buton = { 1: {"Numéro": lit 1, "Niveau": niveauButon 1, "Entraxe": entraxeButon 1, "Entraxe G": entraxeGaucheButon 1, "Entraxe D": entraxeDroiteButon 1, "Fonctionnement": fonctionnementButon 1,
                                        "Inclinaison": inclinaisonButon, "Distance au voile": distanceButon 1, "Longueur": longueurButon 1, "Matériau": materiauButon 1, "Type": typeButon 1,
                                        "Accrochage": accrochageButon 1}
                                          2 : {...}}
        :rtype: dict
        :return: A dictionary representing the caracteristics 
                 caracteristics_semButon = { 1: {"Liste Buton": listeAppuiButon 1, "Largeur": largeurSemButon 1, "Longueur": longueurSemButon 1, "Hauteur": hauteurSemButon 1}
                                             2 : {...}}
        :rtype: dict
        """
        # import libraries
        import math as m
        import re

        # Tirer la liste pour faire correspondre les numéro de lit de butons avec l'ordre dans le dictionnaire
        listeButon.sort(key = lambda x: int(x[0]))

        # initialiser le dictionnaire
        self.caracteristics_buton = {}

        # Itérer à travers la liste et construire le dictionnaire
        for i, item in enumerate(listeButon, start = 1):
            
            # Check if 'lit' is an int. Otherwise (e.g: a str, a float), raise an error
            if not isinstance(item[0], int):
                raise ValueError("Récupération des Données - Le numéro du lit de butons n'est pas acceptable")
            else:
                numero = item[0]
            
            # Check if 'niveau' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[1], (int, float)):
                raise ValueError("Récupération des Données - La valeur du niveau du lit de butons n'est pas acceptable")
            else:
                niveauButon = round(abs(item[1] - coteRef), 2)
            
            # Check if 'entraxeButon' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[2], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de l'entraxe des butons n'est pas acceptable")
            else:
                entraxeButon = item[2]
            
            # Check if 'entraxeGaucheButon' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[3], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de l'entraxe gauche des butons n'est pas acceptable")
            else:
                entraxeGaucheButon = item[3]
            
            # Check if 'entraxeDroiteButon' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[4], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de l'entraxe droite des butons n'est pas acceptable")
            else:
                entraxeDroiteButon = item[4]
            
            # Check if 'fonctionnementButon' is an str. Otherwise, raise an error
            if item[5].lower() not in ["incliné", "horizontal"]:
                raise ValueError("Récupération des Données - Le mode de fonctionnement des butons n'est pas acceptable")
            else:
                # Dans le cas où le mode de fonctionnement est 'incliné'
                if item[5].lower() == "incliné":
                    
                    # Set the value of the variable 'fonctionnementButon'
                    fonctionnementButon = item[5]

                    # Set the value of the angle 
                    inclinaisonButon = item[6]

                    # If the value is not between 40 and 90, raise an error
                    if inclinaisonButon < 40 or inclinaisonButon >= 90:
                        raise ValueError("Récupération des Données - L'inclinaison des butons n'est pas comprise entre 40° et 90°")

                    # Set the value of the variable 'distanceButon'
                    distanceButon = item[7]

                    # if the value is not positive, raise an error
                    if distanceButon <= 0:
                        raise ValueError("Récupération des Données - La distance au VPP au pied des butons n'est pas correcte")

                    #Compute the value of the length 
                    longueurButon = round(distanceButon / m.sin(m.radians(inclinaisonButon)), 2)
                
                else:
                    # Set the value of the variable 'fonctionnementButon'
                    fonctionnementButon = item[5]

                    # Set the value of the angle 
                    inclinaisonButon = 90

                    # Set the value of the variable 'distanceButon'
                    distanceButon = None

                    #Set the value of the length 
                    longueurButon = item[8]

                    # if the value is not positive, raise an error
                    if longueurButon <= 0:
                        raise ValueError("Récupération des Données - La longueur des butons n'est pas correcte")
            
            # Check if 'materiauButon' is an str. Otherwise, raise an error
            if item[9].lower() not in ["bois", "acier - tube", "acier - ipe", "acier - he"]:
                raise ValueError("Récupération des Données - Le matériau des butons n'est pas acceptable")
            else:
                materiauButon = item[9]
            
            # Check if 'typeButon' is an str. Otherwise (e.g: a int, a float), raise an error
            if not isinstance(item[10], str):
                raise ValueError("Récupération des Données - Le type de butons n'est pas acceptable")
            else:
                if materiauButon.lower() == "bois":
                    #Check the format of the typeButon variable
                    pattern = r"Diamètre:\s*(\d+)cm"
                    match = re.match(pattern, item[10])
                    # Dans le cas de butons bois, la variable 'typeButon' prend la valeur du diamètre du buton en m
                    if match:
                        typeButon = float(match.group(1)) * 10**(-2)
                else: 
                    raise ValueError("Récupération des Données - Le matériau choisi n'est pas encore pris en compte dans cette version")
            
            # Check if 'accorchageButon' is an str. Otherwise, raise an error
            if item[11].lower() not in ["corbeau béton", "platine"]:
                raise ValueError("Récupération des Données - Le mode d'accrochage des butons n'est pas acceptable")
            else:
                accrochageButon = item[11]


            self.caracteristics_buton[i] =  {"Numéro": numero,
                                             "Niveau": niveauButon,
                                             "Entraxe": entraxeButon,
                                             "Entraxe G": entraxeGaucheButon,
                                             "Entraxe D": entraxeDroiteButon,
                                             "Fonctionnement": fonctionnementButon,
                                             "Inclinaison": inclinaisonButon,
                                             "Distance au voile": distanceButon,
                                             "Longueur": longueurButon,
                                             "Matériau": materiauButon,
                                             "Type": typeButon,
                                             "Accrochage": accrochageButon
                                            }
            

        # initialiser le dictionnaire
        self.caracteristics_semButon = {}

        # Itérer à travers la liste et construire le dictionnaire
        for i, item in enumerate(listeSemButon, start = 1):
            
            #Check if the 'listeAppuiButon' is a list. otherwise, raise an error
            if not isinstance(item[0], list):
                raise ValueError("Récupération des Données - La liste contenant les numéros des lits de butons n'est pas acceptable")
            else:
                #Check if the 'listeAppuiButon' is not empty. Otherwise, raise an error
                if len(item[0]) == 0:
                    raise ValueError("Récupération des Données - La semelle ne supporte aucun buton")
                else:
                    #Check if all elements in 'listeAppuiButon' are int. Otherwise, raise an error
                    if not all(isinstance(x, int) for x in item[0]):
                        raise ValueError("Récupération des Données - Le format des numéros des lits de buton n'est pas acceptables")
                    else:
                        listeAppuiButon = item[0]

                    # Vérify if the variable 'fonctionnementButon' is set to 'Horizontal' for a specific value of 'Numéro'
                    for num in range(len(item[0])):
                        number_to_match = item[0][num]
                        # Loop through the dictionary items
                        for key, value in self.caracteristics_buton.items():
                            # Check if the "Numéro" matches the specified number
                            if value["Numéro"] == number_to_match:
                                #Get the value of the "Fonctionnement" key
                                if value.get("Fonctionnement", None) == "Horizontal":
                                    raise ValueError("Récupération des Données - La semelle supporte un buton horizontal")

            # Check if 'largeurSemButon' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[1], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de la largeur des semelles de buton n'est pas acceptable")
            else:
                largeurSemButon = item[1]
            
            # Check if 'longueurSemButon' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[2], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de la longueur des semelles de buton n'est pas acceptable")
            else:
                longueurSemButon = item[2]
            
             # Check if 'hauteurSemButon' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[3], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de la hauteur des semelles de buton n'est pas acceptable")
            else:
                hauteurSemButon = item[3]

            self.caracteristics_semButon[i] =  {"Liste Buton": listeAppuiButon,
                                                "Largeur": largeurSemButon,
                                                "Longueur": longueurSemButon,
                                                "Hauteur": hauteurSemButon,
                                                }