# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in December 2022 for a personal use
This file forms the class which implement the DTU 14.1 about coating

Inputs:
        - beton: dict obtained from the Data folder containing the caracteristics of concrete used for the element considered
                beton = {"Masse volumique": ...,
                         "fck": ...,
                         "Classe exposition": ...,
                         "Enrobage": ...,
                         "Coefficient sécurité": ...,
                         "Module élasticité DEF": ..., 
                         "Module élasticité PROV": ...,
                         "Coefficient equivalence": ...
                          }

        - acier: dict obtained from the Data folder containing the caracteristics of reinforcement used in the concrete for the element considered
                acier = {"fyk": ...,
                         "Palier": ...,
                         "Classe": ...,
                         "Coefficient sécurité": ...,
                         "Module élasticité": ...
                          }

        - section: dict obtained from the Data folder containing the caracteristics of the element's section 
                section = {"Largeur": ...,
                           "Hauteur": ...,
                           "d": ..., 
                           "Calcul en T": ...,
                           "Largeur de la table": ...,
                           "Hauteur de la table": ...
                            }

        - cuvelage: dict obtained from the Data folder containing the caracteristics of the 'cuvelage'
                cuvelage = {"Type de cuvelage": ...,
                            "Precaution": ...,
                            "Face": ...
                             }
        
        - eau: dict obtained from the Data folder containing the caracteristics from the water 
                eau = {"Eau": ...,
                       "Niveau": ...,
                       "Type": ...,
                       "Densité": ...
                       }
        
        - sollicitations: dict containing the loads on the element (units: MN, MN.m)
                sollicitations: {"Moment ELS": ...,
                                 "Moment ELU": ...,
                                 "Tranchant ELS": ...,
                                 "Tranchant ELU": ...,
                                 "Normal ELS": ...,
                                 "Normal ELU": ...
                                 }
        
        - armatures: dict containing the reinforcement section in the concrete element (units: m²) - Verify units
                armatures: {"mu_lim": ...,
                            "mu_lu": ...,
                            "alpha_u": ...,
                            "z": ...,
                            "sigma": ...,
                            "As,min": ...,
                            "As,max": ...,
                            "As1": ...,
                            "As2": ...,
                            "Diametre": {"1": [n1, phi1], # number of steel bars in the first row and diameter 
                                         "2": ...}
                            }

        - fissures: dict containing the parameters necessary to the computation of the crack openings
                fissures = {"Limite": ...,   # Limit value of the crack openings
                            "Charges": ...,  # Type of loads (Longue durée ou Courte durée)
                             }                     

Units: m, cm², MN, MN.m, MPa

# Faire le calcul des sections min comme fait maintenant. Puis calculer l'ouverture de fissure. Ajouter une phrase à la fin si l'ouverture de fissure n'est pas respecté. 
"""

# Import classes 
import Concrete 

class Cuvelage:

    @classmethod
    def VerificationEpaisseurMini(cls, beton, section, sollicitations, armatures):
        """ Verify that the thickness of the wall respects the criteria of minimum thickness from DTU 14.1

            :raise ValueError: If arguments are not dictionaries with the correct keys as define above
            :return: A boolean that indicates if the criteria is satisfied or not
            :rtype: boolean
            """

        # Compute the value of theta
        # Case 1: tension
        if sollicitations["Normal ELU"] < 0 and sollicitations["Moment ELU"] == 0:
            theta = 1

        # Case 2: compound bending with traction where M/T <= h/2
        elif sollicitations["Moment ELU"] !=0 and sollicitations["Normal ELU"] < 0:
            if sollicitations["Moment ELU"] / sollicitations["Normal ELU"] <= section["Hauteur"] / 2:
                theta = 1 + (4 * sollicitations["Moment ELU"] / sollicitations["Normal ELU"] / 3 * section["Hauteur"])

            else:
                theta = 5 / 3

        # Other cases:
        else:
            theta = 5 / 3

        # Compute values from the function in the class
        Area, Inertia, NeutralAxis = cls.InertieHomogene(beton, section, armatures)

        # Compute the value of the concrete tensile stress in homogenized section
        sigma_ct = abs(sollicitations["Normal ELU"] / Area - sollicitations["Moment ELU"] * (section["Hauteur"] - NeutralAxis) / Inertia)

        # Check the criteria and return the result
        if sigma_ct > 1.1 * (0.6 + 0.06 * beton["fck"]) * theta:
            return True

        else:
            return False

    @classmethod
    def CalculOuvertureFissures(cls, beton, acier, section, sollicitations, armatures, fissures): #Necessite le choix du ferraillage
        """ Compute the crack openings of a concrete section

            :raise ValueError: If arguments are not dictionaries with the correct keys as define above
            :return: A boolean that indicates if the criteria is satisfied or not
            :rtype: boolean
            """
        
        # Nota:
                # Mqp = Moment ELS Quasi Permanent
                # phi = diamètre du treillis (6-9 mm)

        # Import modules
        import math as m
        
        # Names:
        Mqp = sollicitations["Moment ELS"]

        # Compute the parameters of the cracked section: 
        NeutralAxis, Inertia = cls.InertieFissuree(beton, section, armatures)

        # Compute the stresses in the tensed reinforcement
        Sigma_s = beton["Coefficient equivalence"] * abs(Mqp) * (section["d"] - NeutralAxis) / Inertia

        # Compute the different parameters for the verification

        # kt: coefficient depending on the duration of the loading
        if fissures["Charges"] == "Longue":
            kt = 0.4
        else:
            kt = 0.6
        
        # hc_ef: height of the concrete section around the tensed reinforcement
        hc_ef = min(2.5 * (section["Hauteur"] - section["d"]), (section["Hauteur"] - NeutralAxis) / 3, section["Hauteur"] / 2)
        
        # Ac_eff: Effective area of concrete around the tensed reinforcement
        Ac_eff = section["Largeur"] * hc_ef

        # rho_eff: percentage of tensed reinforcement
        rho_eff = armatures["As1"] * m.pow(10, -4) / Ac_eff

        alpha_e = acier["Module élasticité"] / Concrete._concrete.E_cm(beton["fck"])

        fct_eff = Concrete._concrete.fct_eff(beton["fck"])
        
        # Compute the value of eps = eps_sm - eps_cm
        eps = max(0.6  *Sigma_s / acier["Module élasticité"], (Sigma_s - kt * fct_eff / rho_eff * (1 + alpha_e * rho_eff)) / acier["Module élasticité"])

        # Compute the parameters for the computation of sr_max: the maximum spacing of the cracks

        k1 = 0.8 # fot high-adhesion bars

        if sollicitations["Moment ELU"] != 0:
            k2 = 0.5
        elif sollicitations["Moment ELU"] == 0 and sollicitations["Normal ELU"] < 0:
            k2 = 1.0
        
        # Based on the hypothesis that there is the same amount of every type of bars
        enrobageLongitudinal = beton["Enrobage"]

        if armatures["Diametre"]:
            num, denom = 0, 0
            for value in armatures["Diametre"].values():
                num += int(value[1])**2
                denom += int(value[1])
            phi = num / denom * m.pow(10, -3)
            espacementArmatures = (section["Largeur"] - 2 * enrobageLongitudinal - 1.2 * armatures["Diametre"]["1"][1] * m.pow(10, -3)) / (armatures["Diametre"]["1"][0] -1)
        else:
            # If the Diametre dictionary is empty, take the assumption that the diameter of the reinforcement is 9mm
            phi = 0.009
            espacementArmatures = 0.1

        if enrobageLongitudinal > 0.025:
            k3 = 3.4 * (25 / enrobageLongitudinal / m.pow(10, 3))**(2/3)
        else:
            k3 = 3.4

        k4 = 0.425

        # Compute the maximum spacing of the cracks
        if espacementArmatures > 5 * (enrobageLongitudinal + phi / 2):
            sr_max = max(k3 * beton["Enrobage"] + k1 * k2 * k4 * phi / rho_eff, 1.3 * (section["d"] - NeutralAxis))
        else:
            sr_max = k3 * beton["Enrobage"] + k1 * k2 * k4 * phi / rho_eff

        # Compute the cracks opening
        wk = sr_max * eps
        
        if wk <= fissures["Limite"]:
            return True
        else:
            return False

    @classmethod
    def InertieHomogene(cls, beton, section, armatures):
        """ Compute the inertia of a homogeneous section

            :raise ValueError: If arguments are not dictionaries with the correct keys as define above
            :return Area: the value of the homogeneous area
            :rtype Area: float
            :return inertie: tha value of the inertia
            :rtype inertia: float
            :return AxeNeutre: tha position of the neutral axis
            :rtype AxeNeutre: float
            """
        # Import modules
        import math as m

        # parameters needed for the computation
        enrobageSup = section["Hauteur"] - section["d"]
        
        # Concrete parameters
        InertieBeton = section["Largeur"] * section["Hauteur"] ** 3 /12
        AxeNeutreBeton = section["Hauteur"] / 2
        AireBeton = section["Largeur"] * section["Hauteur"]
        S_c = AireBeton * AxeNeutreBeton

        # reinforcement parameters
        AxeNeutre_As1 = section["d"]
        AxeNeutre_As2  = enrobageSup
        Ss1 = armatures["As1"] * m.pow(10, -4) * AxeNeutre_As1
        Ss2 = armatures["As2"] * m.pow(10, -4) * AxeNeutre_As2
        
        # Compute the homogeneous inertia
        # Homogeneous area
        A = AireBeton + beton["Coefficient equivalence"] * (armatures["As1"] + armatures["As2"]) * m.pow(10, -4)

        # Homogenous section
        S = S_c + beton["Coefficient equivalence"] * (Ss1 + Ss2)

        # Position of the neutral axis
        NeutralAxis = S / A
        
        # Homogenous inertia
        Inertie = InertieBeton + (AxeNeutreBeton - NeutralAxis)**2 * AireBeton + beton["Coefficient equivalence"] * (AxeNeutre_As1 - NeutralAxis)**2 * armatures["As1"] * m.pow(10, -4) + beton["Coefficient equivalence"] * (AxeNeutre_As2 - NeutralAxis)**2 * armatures["As2"] * m.pow(10, -4)

        return A, Inertie, NeutralAxis

    @classmethod
    def InertieFissuree(cls, beton, section, armatures):
        """ Compute the inertia of a cracked section

            :raise ValueError: If arguments are not dictionaries with the correct keys as define above
            :return inertie: tha value of the inertia
            :rtype inertia: float
            :return AxeNeutre: tha position of the neutral axis
            :rtype AxeNeutre: float
        """
        
        # Import modules
        import math as m
        import numpy as np

        # parameters needed for the computation
        enrobageSup = section["Hauteur"] - section["d"]
        
        # Put the reinforcement sections in m² (from cm²)
        As_1 = armatures["As1"] * m.pow(10,-4)
        As_2 = armatures["As2"] * m.pow(10,-4)

        # resolve the polynomial equation
        poly = np.polynomial.polynomial.Polynomial([-beton["Coefficient equivalence"] * As_1 * section["d"] - beton["Coefficient equivalence"] * As_2 * enrobageSup, beton["Coefficient equivalence"] * As_1 + beton["Coefficient equivalence"] * As_2, section["Largeur"] / 2])
        
        # Put the roots in a list
        res = poly.roots()

        # Find the positive roots (2nd degrees polynomial)
        for i in range(len(res)):
            if res[i] >= 0:
                neutralAxis = res[i]
        
        # Compute the inertia
        inertie = section["Largeur"] / 3 * neutralAxis**3 + beton["Coefficient equivalence"] * As_1 * (section["d"] - neutralAxis)**2 + beton["Coefficient equivalence"] * As_2 * (enrobageSup - neutralAxis)**2

        # return the values 
        return neutralAxis, inertie
    
    @classmethod
    def contrainte_acier_cuvelage(cls, acier, cuvelage, eau):
        """ Compute the reinforcement stresses

            :raise ValueError: If arguments are not dictionaries with the correct keys as define above
            :return sigma: tha value of sigma (MPa)
            :rtype sigma: float
        """    

         # If statement to determine which type of 'cuvelage' is used
        if cuvelage['Type de cuvelage'] == "Imperméabilisation" and cuvelage["Face"] == "Intérieure":
                
                # Compute the value of sigma depending on the water level
                sigma = min(2/3 * acier['fyk'], 240)

        # Type of 'cuvelage': other than 'Imperméabilisation'
        elif cuvelage['Type de cuvelage'] == "Etanche" or cuvelage['Type de cuvelage'] == "Etanchéité" or (cuvelage['Type de cuvelage'] == "Imperméabilisation" and cuvelage["Face"] == "Extérieure"):

            # If statement to deterline the water level used for calculations
            if eau['Type'] == "EB":

                # Compute the value of sigma_s1
                sigma = min(2/3 * acier['fyk'], 200)

            elif eau['Type'] == "EH":

                # Compute the value of sigma_s1
                sigma = min(2/3 * acier['fyk'], 300)

            elif eau['Type'] == "EE":

                # Compute the value of sigma_s1
                sigma = min(2/3 * acier['fyk'], 400)  

            else: # If water level is "EC" for "Eaux chantier", raise an error. 
                raise ValueError("Le niveau EC n'est pas encore pris en compte dans le logiciel") 
        
        return sigma