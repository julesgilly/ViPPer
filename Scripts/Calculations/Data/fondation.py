# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""


class Fondation:
    def __init__(self, modeFondation, AiFondation, largeurFondation, hauteurFondation, debordFondation, enrobageFondation, typeFondation, isButeeFondation, portanceELU, glissementELU, portanceELS, modelePortance, modeleGlissement, coteRef):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param modeFondation: mode de fondation : "Fondations superficielles (semelle excentrée)" ou "Fondations profondes (pieux avec longrines de redressement)". Si Profondes, pas de vérifications donc toutes les autres variables prennent la valeur None
        :type modeFondation: str
        :param AiFondation: Niveau de l'arase inférieure de la fondation
        :type AiFondation: float
        :param largeurFondation: Largeur de la fondation (en m)
        :type largeurFondation: float
        :param hauteurFondation: Hauteur de la fondation (en m)
        :type hauteurFondation: float
        :param debordFondation: Débord extérieur de la fondation (en m)
        :type debordFondation: float
        :param enrobageFondation: Enrobage des armatures de la fondation (en cm)
        :type enrobageFondation: float
        :param typeFondation: Type de fondation : "Préfabriquée" ou "Coulée pleine fouille"
        :type typeFondation: str
        :param isButeeFondation: prise en compte de la butée dans le calcul (True/False). Prend la valeur False si typeFondation = "Préfabriquée"
        :type isButeeFondation: bool
        :param portanceELU: Coefficient de portance de l'ELU
        :type portanceELU: float
        :param glissementELU: Coefficient de glissement de l'ELU
        :type glissementELU: float
        :param portanceELS: Coefficient de portance de l'ELS
        :type portanceELS: float
        :param modelePortance: Coefficient de modèle pour la portance
        :type modelePortance: float
        :param modeleGlissement: Coefficient de modèle pour le glissement
        :type modeleGlissement: float
        :param coteRef: Cote de référence pour les calculs
        :type coteRef: float
        
        :return: A dictionary representing the caracteristics 
        :rtype: dict
        """
        # The 'modeFondations' should be a str
        if modeFondation.lower() not in ["fondations superficielles (semelle excentrée)", "fondations profondes (pieux avec longrines de redressement)"]:
            raise ValueError("Récupération des Données - Le format pour le mode de fondations est incorrect")
        
        # Si le mode de fondations est "Profondes", alors toutes les autres variables prennent la valeur None
        if modeFondation.lower() == "fondations profondes (pieux avec longrines de redressement)":
            AiFondation = None
            largeurFondation = None
            hauteurFondation = None
            debordFondation = None
            enrobageFondation = None
            typeFondation = None
            isButeeFondation = False
            portanceELU = None
            glissementELU = None
            portanceELS = None
            modelePortance = None
            modeleGlissement = None
        else:
            # Check if 'AiFondation' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(AiFondation, (int, float)):
                raise ValueError("Récupération des Données - La valeur du niveau de l'arase inférieure de la fondation du VPP n'est pas acceptable")
            else:
                AiFondation = round(abs(AiFondation - coteRef), 2)
            
            # Check if 'largeurFondation' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(largeurFondation, (int, float)):
                raise ValueError("Récupération des Données - La valeur de la largeur de la fondation du VPP n'est pas acceptable")

            # Check if 'hauteurFondation' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(hauteurFondation, (int, float)):
                raise ValueError("Récupération des Données - La valeur de la hauteur de la fondation du VPP n'est pas acceptable")
            
            # Check if 'debordFondation' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(debordFondation, (int, float)):
                raise ValueError("Récupération des Données - La valeur du débord de la fondation du VPP n'est pas acceptable")

            # Check if 'enrobageFondation' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(enrobageFondation, (int, float)):
                raise ValueError("Récupération des Données - La valeur de l'enrobage de la fondation du VPP n'est pas acceptable")
            else:
                enrobageFondation = enrobageFondation * 10**(-2)
            
            # The 'typeFondation' should be a str
            if typeFondation.lower() not in ["préfabriquée", "coulée pleine fouille"]:
                raise ValueError("Récupération des Données - Le format pour le type de fondations est incorrect")
        
            # Check if 'isButeeFondation' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(isButeeFondation, bool):
                raise ValueError("Récupération des Données - La butée est-elle prise en compte ? ")
            
            #Si la fondation est préfabriquée, alors isButeeFondation est False
            if typeFondation.lower() == "préfabriquée":
                isButeeFondation = False
                            
            # Check if 'portanceELU' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(portanceELU, (int, float)):
                raise ValueError("Récupération des Données - La valeur du coefficient de portance ELU n'est pas acceptable")
            
            # Check if 'glissementELU' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(glissementELU, (int, float)):
                raise ValueError("Récupération des Données - La valeur du coefficient de glissement ELU n'est pas acceptable")
            
            # Check if 'portanceELS' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(portanceELS, (int, float)):
                raise ValueError("Récupération des Données - La valeur du coefficient de portance ELS n'est pas acceptable")
            
            # Check if 'modelePortance' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(modelePortance, (int, float)):
                raise ValueError("Récupération des Données - La valeur du coefficient de modele pour la portance n'est pas acceptable")
            
            # Check if 'modeleGlissement' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(modeleGlissement, (int, float)):
                raise ValueError("Récupération des Données - La valeur du coefficient de modele pour le glissement n'est pas acceptable")
            
        self.caracteristics = {"Mode": modeFondation,
                               "Arase inférieure": AiFondation,
                               "Largeur": largeurFondation,
                               "Hauteur": hauteurFondation,
                               "Débord": debordFondation,
                               "Enrobage": enrobageFondation,
                               "Type": typeFondation,
                               "Butee": isButeeFondation,
                               "Portance ELU": portanceELU,
                               "Glissement ELU": glissementELU,
                               "Portance ELS": portanceELS,
                               "Modele Portance": modelePortance,
                               "Modele Glissement": modeleGlissement
                               }