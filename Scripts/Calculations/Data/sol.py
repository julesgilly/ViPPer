# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""


class SolInfo:
    def __init__(self, listeSol, computeTassement, typeInterface, tauxSolELS, tauxSemButELS, coteRef):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param listeSol: ensemble des informations sur les couches de sol avec la forme suivante
                    listeSol = [[nameCouche i, coteSupCouche i, coteInfCouche i, typeSol i, cu_couche i, c_couche i, phiu_couche i, phi_couche i,
                                    gamma_couche i, Em_couche i, pressionLimite i, alpha_couche i], ...]
                    avec : nameCouche: nom de la couche de sol
                    coteSupCouche: cote supérieur de la couche de sol
                    coteInfCouche: cote inférieur de la couche de sol
                    typeSol: type de sol "Argiles", "limons", "Sables", "Graves", "Craies", "Marnes", "Marno-calcaires", "Roches"
                    cu_couche: cohésion court terme de la couche de sol (en kPa)
                    c_couche: cohésion long terme de la couche de sol (en kPa)
                    phiu_couche: angle de frottement interne court terme de la couche de sol (en °)
                    phi_couche: angle de frottement interne long terme de la couche de sol (en °)
                    gamma_couche: masse volumique de la couche de sol (en kN/m³)
                    Em_couche: module pressiométrique de Ménard (en MPa)
                    pressionLimite: pression limite de la couche de sol (en MPa)
                    alpha_couche: Coefficient rhéologique
        :type listeSol: liste
        :param computeTassement: réalisation du calculs des tassements ?
        :type computeTassement: bool
        :param typeInterface: type d'interface "Interface Frottante", "Interface Adhérente"
        :type typeInetrface: str
        :param tauxSolELS: contrainte de sol admissible ELS en MPa
        :type tauxSolELS: float
        :param tauxSemButELS: contrainte de sol admissible ELS butons en MPa
        :type tauxSemButELS: float
        :param coteRef: Cote de référence pour les calculs
        :type coteRef: float
        
        :return: A dictionary representing the caracteristics 
            SolInfo = { 1: {'Nom de la couche': ,
                        'Cote supérieure': ,
                        'Cote inférieure': ,
                        'Type de sol': ,
                        'Cohésion court terme': ,
                        'Cohésion long terme': ,
                        'Angle de frottement court terme': ,
                        'Angle de frottement long terme': ,
                        'Masse volumique': ,
                        'Pression limite': ,
                        'Module pressiométrique Ménard': ,
                        'Coefficient rhéologique': }
                    2: { ... 
                   }
            }
        :rtype: dict
        :return: Dictionnaire avec les contraintes de sol
            contraintes = {"Type Interface": typeInterface,
                           "Taux ELS": tauxSolELS,
                           "Taux ELS Buton": tauxSemButELS
                           }
        :rtype: dict
        :return: variable qui indique si le calcul des tassements est réalisé
        :rtype: bool
        """

        # Check if 'lcomputeTassement' is a bool. Otherwise (e.g: a str, a float), raise an error
        if not isinstance(computeTassement, bool):
            raise ValueError("Récupération des Données - Calcul des tassements ?")
        else:
            self.computeTassement = computeTassement

        # Vérifier que le type de surcharges est dans la liste autorisée
        if typeInterface.lower() not in ["interface frottante", "interface adhérente"]:
            raise ValueError("Récupération des Données - Le type d'interface n'est pas correct")
                
        # Check if 'tauxSolELS' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(tauxSolELS, (float, int)):
            raise ValueError("Récupération des Données - La contrainte de sol admissible à l'ELS n'est pas acceptable")
        else:
            #La contrainte de sol admissible à l'ELS doit être positive
            if tauxSolELS <= 0:
                raise ValueError("Récupération des Données - La contrainte de sol admissible à l'ELS doit être positive")   

        # Check if 'tauxSemButELS' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(tauxSemButELS, (float, int)):
            raise ValueError("Récupération des Données - La contrainte de sol admissible à l'ELS des semelles de butons n'est pas acceptable")
        else:
            #La contrainte de sol admissible à l'ELS doit être positive
            if tauxSemButELS <= 0:
                raise ValueError("Récupération des Données - La contrainte de sol admissible à l'ELS des semelles de butons doit être positive")           

        self.contraintes = {"Type Interface": typeInterface,
                            "Taux ELS": tauxSolELS,
                            "Taux ELS Buton": tauxSemButELS
                            }       

        
        # initialiser le dictionnaire
        self.SolInfo = []

        # Itérer à travers la liste et construire le dictionnaire
        for i, item in enumerate(listeSol, start = 1):
            
            #Check if the 'nameCouche' is a string. otherwise, raise an error
            if not isinstance(item[0], str):
                raise ValueError("Récupération des Données - Le nom de la couche n'est pas acceptable")
            else:
                nameCouche = item[0]

            # Check if 'coteSupCouche' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[1], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de la cote supérieure de la couche de sol n'est pas acceptable")
            else:
                coteSupCouche = round(abs(item[1] - coteRef), 2)
            
            # Check if 'coteInfCouche' is an int or a float. Otherwise (e.g: a str), raise an error
            if not isinstance(item[2], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de la cote inférieure de la couche de sol n'est pas acceptable")
            else:
                coteInfCouche = round(abs(item[2] - coteRef), 2)
            
            # Vérifier que le type de de sol est dans la liste autorisée
            if item[3].lower() not in ["argiles", "limons", "sables", "graves", "craies", "marnes", "marno-calcaires", "roches"]:
                raise ValueError("Récupération des Données - Le type de sol n'est pas correct")
            else:
                typeSol = item[3]

            # Cohésion du sol court terme
            if not isinstance(item[4], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de la cohésion court terme de la couche de sol n'est pas acceptable")
            else:
                cu_couche = item[4] * 10**(-3)

            # Cohésion du sol long terme
            if not isinstance(item[5], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de la cohésion long terme de la couche de sol n'est pas acceptable")
            else:
                c_couche = item[5] * 10**(-3)

            # Angle de frottement interne court terme
            if not isinstance(item[6], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de l'angle de frottement interne court terme de la couche de sol n'est pas acceptable")
            else:
                phiu_couche = item[6]

            # Angle de frottement interne long terme
            if not isinstance(item[7], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de l'angle de frottement interne long terme de la couche de sol n'est pas acceptable")
            else:
                phi_couche = item[7]

            # Densité couche
            if not isinstance(item[8], (int, float)):
                raise ValueError("Récupération des Données - Le valeur de la densité de la couche de sol n'est pas acceptable")
            else:
                gamma_couche = item[8] * 10**(-3)

            # Vérifier les variables nécessaires pour le calcul du tassement
            if self.computeTassement == False:
                pressionLimite = None
                Em_couche = None
                alpha_couche = None
            else:
                # Vérifier les formats des variables
                #Pression limite
                if not isinstance(item[9], (int, float)):
                    raise ValueError("Récupération des Données - Le valeur de la pression limite de la couche de sol n'est pas acceptable")
                else:
                    pressionLimite = item[9]
                
                #Module pressiométrique de Ménard
                if not isinstance(item[10], (int, float)):
                    raise ValueError("Récupération des Données - Le valeur du module pressiométrique de Ménard de la couche de sol n'est pas acceptable")
                else:
                    Em_couche = item[10]

                #Coefficient rhéologique
                if not isinstance(item[11], (int, float)):
                    raise ValueError("Récupération des Données - Le valeur du coefficient rhéologique de la couche de sol n'est pas acceptable")
                else:
                    alpha_couche = item[11]


            sol_i =  {"Nom de la couche": nameCouche,
                      "Cote supérieure": coteSupCouche,
                      "Cote inférieure": coteInfCouche,
                      "Type de sol": typeSol,
                      "Cohésion court terme" : cu_couche,
                      "Cohésion long terme" : c_couche,
                      "Angle de frottement court terme": phiu_couche,
                      "Angle de frottement long terme": phi_couche,
                      "Masse volumique": gamma_couche,
                      "Pression limite": pressionLimite,
                      "Module pressiométrique Ménard": Em_couche,
                      "Coefficient rhéologique": alpha_couche
                        }

            # Add the dictionnary to the list
            self.SolInfo.append(sol_i)
        
        # Trier le dictionnaire en fonction de la valeur "Niveau" 
        self.SolInfo = {i: d for i, d in enumerate(sorted(self.SolInfo, key=lambda item: item["Cote supérieure"]), start=1)}


        #Vérifier les niveaux INF et SUP des couches de sol pour la cohérence
        # Initialize the value 
        previous_coteInfCouche = None

        # Itérer dans le dictionnaire
        for key, value in self.SolInfo.items():

            # Récupérer la valeur de coteInfCouche et coteSupCouche
            cote_sup = value.get("Cote supérieure")
            cote_inf = value.get("Cote inférieure")

            if previous_coteInfCouche != None and cote_sup != previous_coteInfCouche:
                value["Cote supérieure"] = previous_coteInfCouche

            if previous_coteInfCouche != None and cote_inf < previous_coteInfCouche :
                raise ValueError("Récupération des Données - La valeur de la cote inférieure de la couche de sol est supérieure à la couche de sol précédente")
            
            # Set the value to compare with the value of coteSupCouche of the next item in the list
            previous_coteInfCouche = cote_inf