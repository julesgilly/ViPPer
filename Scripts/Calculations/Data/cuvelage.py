# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in December 2022 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""


class Cuvelage:
    def __init__(self, type, face, precaution, wOuvFiss,dureeOuvFiss):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param type: type of 'cuvelage': "Imperméabilisation", "Etanchéité", "Etanche"
        :type type: str
        :param precaution: 'précaution nécessaire en vue de limiter les phénomènes de variation dimensionnelle contraire (retrait, température, etc...': True or False
        :type precaution: bool
        : param face: "Face Intérieure" ou "Face Extérieure" - face d'application du cuvelage
        :return: A dictionary representing the caracteristics of the 'cuvelage'
        :rtype: dict
        """

        # The 'type' variable can only take three values: "Imperméabilisation", "Etanchéité" and "Etanche"
        # If 'None', no 'cuvelage' planned for the project
        if type != None:
            if type.lower() not in ["revêtement par imperméabilisation", "revêtement par etanchéité", "structure relativement etanche"]:   
                type = None
            else:
                type = type.split()[-1]

        # If 'None', no 'cuvelage' planned for the project
        if type != None:
            if face.lower() not in ["face extérieure", "face intérieure"]:   
                raise ValueError("Récupération des Donénes - Face du cuvelage non valide")
            else:
                face = face.split()[-1]


        # Check the type of the 'precaution' variable (should be a bool). Otherwise, set it up to False
        if not isinstance(precaution, bool):
            precaution = False

        # The 'wOuvFiss' should be a float or a int
        if not isinstance(wOuvFiss, (float, int)) or wOuvFiss < 0:
            raise ValueError("Récupération des Données - La valeur limie de l'ouverture des fissures est incorrecte")
        
        #Get the value for the load's duration in th computation
        if "Longue durée" in dureeOuvFiss:
            dureeOuvFiss = "Longue"
        elif "Courte durée" in dureeOuvFiss:
            dureeOuvFiss = "Courte"
        else:
            raise ValueError("Récupération des Données - La valeur de la durée de l'ouverture des fissures est incorrect")

        self.caracteristics = {"Type de cuvelage": type,
                               "Precaution": precaution,
                               "Face": face
                               }
        
        self.fissures = {"Limite": wOuvFiss * 10**(-3),
                        "Charges": dureeOuvFiss
                        }