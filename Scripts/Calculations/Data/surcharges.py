# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""

class Surcharges:
    def __init__(self, listeSurcharge):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param listeSurcharge: ensemble des informations sur les surcharges sur le sol avec la forme suivante
                    listeLierne = [[typeSurcharge i, phaseCalculSurcharge i, qSurcharge i, dSurcharge i, B_Surcharge i, L_Surcharge i, hauteurTalusSurcharge i,
                                    angleTalusSurcharge i, longueurBaseRisberme i, poidsTalusSurcharge i, cTalusSurcharge i, phi_TalusSurcharge i], ...]
                    avec : typeSurcharge : le type de surcharges : "Pression uniforme appliquée à distance de l'écran"
                                                                   "Pression uniforme avec largeur limitée"
                                                                   "Pression uniforme contigüe à l'écran avec largeur limitée"
                                                                   "Pression uniforme infinie contigüe à l'écran"
                                                                   "Pression uniforme appliquée sur une aire"
                                                                   "Charge linéique verticale"
                                                                   "Talus"
                                                                   "Risberme"
                    phaseCalculSurcharge : Phase de calcul de la surcharge
                    qSurcharge : Valeur de la surcharge (en kPa/kN)
                    dSurcharge : Distance de la surcharge par rapport à l'écran (en m)
                    B_Surcharge : Largeur de la surcharge (en m)
                    L_Surcharge : Longueur de la surcharge (en m)
                    hauteurTalusSurcharge : Hauteur du talus/risberme (en m)
                    angleTalusSurcharge : Angle inclinaison du talus/risberme (en degré)
                    longueurBaseRisberme : Longueur de la base de la risberme (en m)
                    poidsTalusSurcharge : Poids volumique du talus/risberme (en kN/m3)
                    cTalusSurcharge : Coefficient de cohésion du talus/risberme (en kPa)
                    phi_TalusSurcharge : Angle de frottement interne du talus/risberme (en °)
        :type torseurCharges: liste


        :return: A dictionary representing the caracteristics 
                 caractéristics = { 1: {"Type": typeSurcharge 1, "Phase": phaseCalculSurcharge 1, "q": qSurcharge 1, "d": dSurcharge 1, "B": B_Surcharge 1, "L": L_Surcharge 1,
                                        "h Talus": hauteurTalusSurcharge 1, "Angle Talus": angleTalusSurcharge 1, "L Risberme": longueurBaseRisberme 1, "Poids Talus": poidsTalusSurcharge 1,
                                        "c Talus": cTalusSurcharge, "phi Talus": phi_TalusSurcharge 1}
                                    2 : {...}}
        :rtype: dict
        """

        # initialiser le dictionnaire
        self.caracteristics = {}

        # Itérer à travers la liste et construire le dictionnaire
        for i, item in enumerate(listeSurcharge, start = 1):

            # Vérifier que le type de surcharges est dans la liste autorisée
            if item[0].lower() not in ["pression uniforme appliquée à distance de l'écran",
                                       "pression uniforme avec largeur limitée",
                                       "pression uniforme contigüe à l'écran avec largeur limitée",
                                       "pression uniforme infinie contigüe à l'écran",
                                       "pression uniforme appliquée sur une aire",
                                       "charge linéique verticale",
                                       "talus", "risberme"]:
                raise ValueError("Récupération des Données - Le type de surcharge n'est pas correct")
            else:
                typeSurcharge = item[0]
            
            # Vérifier que la phase de calcul est dans la liste autorisée
            if item[1].lower() not in ["phase définitive uniquement", "phase provisoire uniquement", "phase définitive et provisoire"]:
                    raise ValueError("Récupération des Données - Le format de la phase de calcul de la surcharge n'est pas correct")
            else:
                phaseCalculSurcharge = item[1]

            # 1 - Dans le cas de la "Pression uniforme appliquée à distance de l'écran":
            if typeSurcharge == "Pression uniforme appliquée à distance de l'écran":
                
                # Set the data corresponding to the type and the others to None
                
                # Check if 'qSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[2], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la surcharge n'est pas acceptable")
                else:
                    qSurcharge = item[2] * 10**(-3)
                
                # Check if 'dSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[3], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la distance à l'écran de la surcharge n'est pas acceptable")
                else:
                    dSurcharge = item[3]
                
                B_Surcharge = None
                L_Surcharge = None
                hauteurTalusSurcharge = None
                angleTalusSurcharge = None
                longueurBaseRisberme = None
                poidsTalusSurcharge = None
                cTalusSurcharge = None
                phi_TalusSurcharge = None
            
            # 2 - Dans le cas de la "Pression uniforme avec largeur limitée"
            elif typeSurcharge == "Pression uniforme avec largeur limitée":
                
                # Set the data corresponding to the type and the others to None
                
                # Check if 'qSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[2], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la surcharge n'est pas acceptable")
                else:
                    qSurcharge = item[2] * 10**(-3)
                
                # Check if 'dSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[3], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la distance à l'écran de la surcharge n'est pas acceptable")
                else:
                    dSurcharge = item[3]
                
                # Check if 'B_Surcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[4], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la largeur de la surcharge n'est pas acceptable")
                else:
                    B_Surcharge = item[4]
                
                L_Surcharge = None
                hauteurTalusSurcharge = None
                angleTalusSurcharge = None
                longueurBaseRisberme = None
                poidsTalusSurcharge = None
                cTalusSurcharge = None
                phi_TalusSurcharge = None
            
            # 3 - Dans le cas de la "Pression uniforme contigüe à l'écran avec largeur limitée"
            elif typeSurcharge == "Pression uniforme contigüe à l'écran avec largeur limitée":
                
                # Set the data corresponding to the type and the others to None
                
                # Check if 'qSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[2], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la surcharge n'est pas acceptable")
                else:
                    qSurcharge = item[2] * 10**(-3)
                
                # Check if 'B_Surcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[4], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la largeur de la surcharge n'est pas acceptable")
                else:
                    B_Surcharge = item[4]
                
                dSurcharge = None
                L_Surcharge = None
                hauteurTalusSurcharge = None
                angleTalusSurcharge = None
                longueurBaseRisberme = None
                poidsTalusSurcharge = None
                cTalusSurcharge = None
                phi_TalusSurcharge = None
            
            # 4 - Dans le cas de la "Pression uniforme infinie contigüe à l'écran"
            elif typeSurcharge == "Pression uniforme infinie contigüe à l'écran":
                
                # Set the data corresponding to the type and the others to None
                
                # Check if 'qSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[2], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la surcharge n'est pas acceptable")
                else:
                    qSurcharge = item[2] * 10**(-3)
                
                dSurcharge = None
                B_Surcharge = None
                L_Surcharge = None
                hauteurTalusSurcharge = None
                angleTalusSurcharge = None
                longueurBaseRisberme = None
                poidsTalusSurcharge = None
                cTalusSurcharge = None
                phi_TalusSurcharge = None
            
            # 5 - Dans le cas de la "Pression uniforme appliquée sur une aire"
            elif typeSurcharge == "Pression uniforme appliquée sur une aire":
                
                # Set the data corresponding to the type and the others to None
                
                # Check if 'qSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[2], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la surcharge n'est pas acceptable")
                else:
                    qSurcharge = item[2] * 10**(-3)
                
                # Check if 'dSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[3], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la distance à l'écran de la surcharge n'est pas acceptable")
                else:
                    dSurcharge = item[3]

                # Check if 'B_Surcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[4], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la largeur de la surcharge n'est pas acceptable")
                else:
                    B_Surcharge = item[4]

                # Check if 'L_Surcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[5], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la longueur de la surcharge n'est pas acceptable")
                else:
                    L_Surcharge = item[5]

                hauteurTalusSurcharge = None
                angleTalusSurcharge = None
                longueurBaseRisberme = None
                poidsTalusSurcharge = None
                cTalusSurcharge = None
                phi_TalusSurcharge = None

            # 6 - Dans le cas de la "Charge linéique verticale":
            if typeSurcharge == "Charge linéique verticale":
                
                # Set the data corresponding to the type and the others to None
                
                # Check if 'qSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[2], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la surcharge n'est pas acceptable")
                else:
                    qSurcharge = item[2] * 10**(-3)
                
                # Check if 'dSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[3], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la distance à l'écran de la surcharge n'est pas acceptable")
                else:
                    dSurcharge = item[3]
                
                B_Surcharge = None
                L_Surcharge = None
                hauteurTalusSurcharge = None
                angleTalusSurcharge = None
                longueurBaseRisberme = None
                poidsTalusSurcharge = None
                cTalusSurcharge = None
                phi_TalusSurcharge = None
            
            # 7 - Dans le cas de la "Talus":
            if typeSurcharge == "Talus":
                
                # Set the data corresponding to the type and the others to None
                
                # Check if 'dSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[3], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la distance à l'écran de la surcharge n'est pas acceptable")
                else:
                    dSurcharge = item[3]
                
                # Check if 'hauteurTalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[6], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la hauteur du talus n'est pas acceptable")
                else:
                    hauteurTalusSurcharge = item[6]
                
                # Check if 'angleTalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[7], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de l'angle d'inclinaison du talus n'est pas acceptable")
                else:
                    angleTalusSurcharge = item[7]
                
                # Check if 'poidsTalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[9], (int, float)):
                    raise ValueError("Récupération des Données - La valeur du poids volumique du talus n'est pas acceptable")
                else:
                    poidsTalusSurcharge = item[9] * 10**(-3)
                
                # Check if 'cTalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[10], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la cohésion du talus n'est pas acceptable")
                else:
                    cTalusSurcharge = item[10] * 10**(-3)

                # Check if 'phi_TalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[11], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de l'angle de frottement interne du talus n'est pas acceptable")
                else:
                    phi_TalusSurcharge = item[11]
                
                qSurcharge = None
                B_Surcharge = None
                L_Surcharge = None
                longueurBaseRisberme = None
            
            # 8 - Dans le cas de la "Risberme":
            if typeSurcharge == "Risberme":
                
                # Set the data corresponding to the type and the others to None
                
                # Check if 'hauteurTalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[6], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la hauteur du talus n'est pas acceptable")
                else:
                    hauteurTalusSurcharge = item[6]
                
                # Check if 'angleTalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[7], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de l'angle d'inclinaison du talus n'est pas acceptable")
                else:
                    angleTalusSurcharge = item[7]
                
                # Check if 'longueurBaseRisberme' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[8], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de l'angle d'inclinaison du talus n'est pas acceptable")
                else:
                    longueurBaseRisberme = item[8]
                
                # Check if 'poidsTalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[9], (int, float)):
                    raise ValueError("Récupération des Données - La valeur du poids volumique du talus n'est pas acceptable")
                else:
                    poidsTalusSurcharge = item[9] * 10**(-3)
                
                # Check if 'cTalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[10], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de la cohésion du talus n'est pas acceptable")
                else:
                    cTalusSurcharge = item[10] * 10**(-3)

                # Check if 'phi_TalusSurcharge' is an int or a float. Otherwise (e.g: a str), raise an error
                if not isinstance(item[11], (int, float)):
                    raise ValueError("Récupération des Données - La valeur de l'angle de frottement interne du talus n'est pas acceptable")
                else:
                    phi_TalusSurcharge = item[11]
                
                qSurcharge = None
                dSurcharge = None
                B_Surcharge = None
                L_Surcharge = None



            self.caracteristics[i] =  {"Type": typeSurcharge,
                                       "Phase": phaseCalculSurcharge,
                                       "q": qSurcharge,
                                       "d": dSurcharge,
                                       "B": B_Surcharge,
                                       "L": L_Surcharge,
                                       "h Talus": hauteurTalusSurcharge,
                                       "Angle Talus": angleTalusSurcharge,
                                       "L Risberme": longueurBaseRisberme,
                                       "Poids Talus": poidsTalusSurcharge,
                                       "c Talus": cTalusSurcharge,
                                       "phi Talus": phi_TalusSurcharge
                                 }