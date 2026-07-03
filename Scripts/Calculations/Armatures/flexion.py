# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in December 2022 for a personal use
This file forms the class which compute the reinforcement section for an element in bending

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

Units: m, cm², MN, MN.m, MPa

"""
# Import classes 
import Concrete 
import Armatures

class Flexion: 

    @classmethod
    def contrainte_aciers_tendus(cls, beton, acier, cuvelage, eau, alpha_u):
        """ Compute the reinforcement stresses 
        
        :param alpha_u: coefficient defined as: alpha_u = 1/lambda * (1 - sqrt(1 - 2 * mu_u))
        :type alpha_u: float
        :raise ValueError: If arguments are not dictionaries with the correct keys as define above
        :return: The value of the stress: sigma_s1
        :rtype: float
        """

        # If statement to determine if there is a 'cuvelage' planned in the project. If not: compute sigma_s1 as described in the Eurocodes
        if cuvelage['Type de cuvelage'] == None:
            
            # First compute the 'Allongement des aciers tendus: eps_s1
            eps_cu2 = Concrete._concrete.Eps_cu2(beton['fck'])
            eps_s1 = eps_cu2 * (1 - alpha_u) / alpha_u

            # If statement to determine which type of 'palier' is used, i.e: 'Horizontal' or 'Incliné'
            if acier['Palier'] == "Horizontal":

                    # Branche montante du diagramme 
                    if eps_s1 <= acier['fyk'] / (acier['Coefficient sécurité'] * acier['Module élasticité']):
                        
                        # Compute the value of sigma_s1
                        sigma_s1 = acier['Module élasticité'] * eps_s1

                    else: # Palier horizontal du diagramme

                        # Compute the value of sigma_s1
                        sigma_s1 = acier['fyk'] / acier['Coefficient sécurité']
            
            else: # Palier 'Incliné'

                # Branche montante du diagramme
                if eps_s1 <= acier['fyk'] / (acier['Coefficient sécurité'] * acier['Module élasticité']):

                    # Compute the value of sigma_s1
                    sigma_s1 = acier['Module élasticité'] * eps_s1

                else: # Palier incliné du diragramme

                    # Compute the value of sigma_s1 function of the steel class
                    if acier['Classe'] == "A":

                        sigma_s1 = min(432.37 + 952.38 * eps_s1, 454)

                    elif acier['Classe'] == "B":

                        sigma_s1 = min(433.2 + 727.27 * eps_s1, 466)

                    else:

                        sigma_s1 = min(432.84 + 895.52 * eps_s1, 494)
        
         
        else: # In the case of a 'cuvelage', used the DTU 14.1 part 1.1 to compute the value of sigma_s1

            sigma_s1 = Armatures.Cuvelage.contrainte_acier_cuvelage(acier, cuvelage, eau)

        return sigma_s1



    @classmethod
    def section_min_flexion(cls, beton, acier, section):
        """ Compute the minimal section of reinforcements for a concrete element in bending
        
        :raise ValueError: If arguments are not dictionaries with the correct keys as define above
        :return: The value of the minimal section: As_min (units: cm²)
        :rtype: float
        """
        # import modules 
        import math as m

        # Compute the value of fctm
        fctm = Concrete._concrete.f_ctm(beton['fck'])

        # Compute the value of the minimal section per Eurocodes
        As_min= round(max(0.26 * fctm * section['Largeur'] * section['d'] / acier['fyk'], 0.0013 * section['Largeur'] * section['d']) * m.pow(10, 4), 3)

        return As_min



    @classmethod
    def section_min(cls, beton, acier, section, cuvelage, sollicitations):
        """ Compute the minimal section of reinforcements for a concrete element in bending taking into account of the possible 'cuvelage'
        
        :raise ValueError: If arguments are not dictionaries with the correct keys as define above
        :return: The value of the minimal section: As_min (units: cm²)
        :rtype: float
        """
        # import modules 
        import math as m

        # The section depends on the type of 'cuvelage' used
        match cuvelage['Type de cuvelage']:

            # In the case where there is no 'cuvelage' or the type of 'cuvelage' is 'Etanchéité', then apply the 'Condition de non-fragilité' per Eurocodes 
            case None | "Etanchéité": # Section necessary to limit crack opening w < wmax
                As_min = cls.section_min_flexion(beton, acier, section)

            # If coating is "Imperméabilisation"
            case "Imperméabilisation":
                # When the element is cast with the necessary precautions, take the max of 0.1% of the element's cross section (but no greater than 4.00 cm²) and the minimal section in bending per DTU 14.1
                if cuvelage['Precaution'] == True:
                    As_min = max(round(min(1/1000 * section['Largeur'] * section['Hauteur'] * m.pow(10, 4), 4.0), 3), cls.section_min_flexion(beton, acier, section))
                
                # No precaution: take the max of 0.25% of the element's cross section and the minimal section in bending per DTU 14.1
                else:
                    As_min = max(round(2.5/1000 * section['Largeur'] * section['Hauteur'] * m.pow(10, 4), 3), cls.section_min_flexion(beton, acier, section))
            
            # If coating is "Etanche"
            case "Etanche":

                # "Etanche" in cases of simple traction or compound bending with traction, when the eccentricity is at most equal to half the thickness
                if (sollicitations["Normal ELU"] < 0 and sollicitations["Moment ELU"] == 0) or \
                   (sollicitations["Moment ELU"] != 0 and sollicitations["Normal ELU"] < 0 and abs(sollicitations["Moment ELU"] / sollicitations["Normal ELU"]) <= section["Hauteur"] * 0.5):

                    # When the element is cast with the necessary precautions, take the max of 0.1% of the element's cross section (but no greater than 4.00 cm²) and the minimal section in bending per DTU 14.1
                    if cuvelage['Precaution'] == True:
                        As_min = max(round(min(1/1000 * section['Largeur'] * section['Hauteur'] * m.pow(10, 4), 4.0), 3), cls.section_min_flexion(beton, acier, section))
                    
                    # No precaution: take the max of 0.25% of the element's cross section and the minimal section in bending per DTU 14.1
                    else:
                        As_min = max(round(2.5/1000 * section['Largeur'] * section['Hauteur'] * m.pow(10, 4), 3), cls.section_min_flexion(beton, acier, section))
                
                else: # Section necessary to limit crack opening w < wmax
                    As_min = cls.section_min_flexion(beton, acier, section)

        return As_min



    @classmethod
    def ep_mini_flexion(cls, beton, section, sollicitations):
        """ Compute the minimal thickness or height of the element. Per Eurocodes, it must respect the condition of no 'armatures supérieures comprimées de calcul' while being in the pivot B
        
        :raise ValueError: If arguments are not dictionaries with the correct keys as define above
        :return: The value of the minimal height: h (units: m)
        :rtype: float
        """

        # import modules 
        import math as m

        d = m.sqrt(sollicitations['Moment ELU'] / (0.372 * Concrete._concrete.f_cd(beton['fck']) * section['Largeur']))

        return round(d + beton['Enrobage'], 2)



    @classmethod
    def flexion_simple_rect(cls, beton, acier, section, cuvelage, sollicitations):
        """ Compute the section of reinforcements needed for a rectangular section for a concrete beam. 
        See the document that details the calculations to read about the methods used and the definition of the variables. 
        
        :raise ValueError: If arguments are not dictionaries with the correct keys as define above
        :return: A dictionary with the computed variables used in the calculation of the reinforcement section
        :rtype: dict
        """

        # import modules
        import math as m 


        # 1 - Compute the value of mu_lim per Eurocode 2

            # Coefficient alpha_e, defined in Eurocode 2 as a constant value of 15
        alpha_e = 15

            # Coefficient gamma, defined in Eurocode 2 as: gamma = M_elu / M_els
        gamma = sollicitations["Moment ELU"] / sollicitations["Moment ELS"]

            # If statement to determine which formula of Eurocode 2 to use
        match beton['Classe exposition'].strip()[0:2]:

            # If the 'Classe d'exposition' is either XD, XS or XF
            case "XD" | "XS" | "XF":

                # If the value of fck is lower than 30 MPa
                if beton['fck'] <= 30:
                    if acier['Palier'] == "Horizontal":
                        mu_lim = (2740 * gamma + 60 * beton['fck'] - 3100) * m.pow(10, -4)
                    else:
                        mu_lim = (2800 * gamma + 37 * beton['fck'] - 2605) * m.pow(10, -4)
                
                else: # If fck > 30 MPa
                    if acier['Palier'] == "Horizontal":
                        A = 71.2 * beton['fck'] + 108
                        B = - 5.2 * beton['fck'] + 874.4
                        C = 0.03 * beton['fck'] - 12.5
                        K = (A + B * alpha_e + C * (alpha_e**2)) * m.pow(10, -4)
                        mu_lim = (beton['fck'] * K) / ((4.69 - 1.70 * gamma) * beton['fck'] + (159.90 - 76.20 * gamma))
                    
                    else: # if acier['Palier'] == "Incliné""
                        A = 75.3 * beton['fck'] - 189.8
                        B = - 5.6 * beton['fck'] + 874.5
                        C = 0.04 * beton['fck'] - 13
                        K = (A + B * alpha_e + C * (alpha_e**2)) * m.pow(10, -4)
                        mu_lim = (beton['fck'] * K) / ((4.62 - 1.66 * gamma) * beton['fck'] + (165.69 - 79.62 * gamma))
            
            # If the 'Classe d'exposition' is NOT XD, XS or XF
            case _:
                mu_lim = 0.372
        

        # 2 - Compute the value of mu_lu defined as: mu_lu = Melu / bw.d².fcd
        fcd = Concrete._concrete.f_cd(beton['fck'], gammaC = beton['Coefficient sécurité'])
        mu_lu = abs(sollicitations["Moment ELU"]) / (section['Largeur'] * m.pow(section['d'], 2) * fcd)
        

        # 3 - Compute the value of As1 (inf.) and As2 (sup.)
        
            # Compute the coefficient delta, defined as: delta = enrobage / (h - enrobage)
        delta = beton['Enrobage'] / section['d']
        
            # Compute the value of lambda, defined in Eurocode 2
        if beton['fck'] <= 50:
            lambda_ = 0.8
        elif beton['fck'] > 50 and beton['fck'] < 90:
            lambda_ = 0.8 - (beton['fck'] - 50) / 400
        else:
            raise ValueError('La valeur de fck est trop grande (> 90 MPa)')
        
            # Compute As1 and As2 accordingly to the values of mu_lu and mu_lim
        if mu_lu <= mu_lim:

            # As1
            alpha_u = (1 / lambda_) * (1 - m.sqrt(1 - 2 * mu_lu))
            z = section['d'] * (1 - 0.5 * lambda_ * alpha_u)
            sigma_s1 = cls.contrainte_aciers_tendus(beton, acier, cuvelage, alpha_u)
            As1 = abs(sollicitations["Moment ELU"]) / (z * sigma_s1)
            
            # In this case, there is no reinforcement at the top of the section
            As2 = 0
            
        else: # if mu_lu > mu_lim

            # As1 and As2
            alpha_u = (1 / lambda_) * (1 - m.sqrt(1 - 2 * mu_lim))
            z = section['d'] * (1 - 0.5 * lambda_ * alpha_u)
            sigma_s1 = cls.contrainte_aciers_tendus(beton, acier, cuvelage, alpha_u)

            M_lu = mu_lim * section['Largeur'] * m.pow(section['d'], 2) * fcd

            if acier['Palier'] == "Horizontal":
                A = 0.5 / alpha_e + 13
                B = 6517 / alpha_e + 1
            else:
                A = - 5 / alpha_e + 13
                B = 6855 / alpha_e - 9

            sigma_s2e = 0.6 * alpha_e * gamma * beton['fck'] - delta * (A * beton['fck'] + B)
            sigma_s1e = (A * beton['fck'] + B) - 0.6 * alpha_e * gamma * beton['fck']
            As2 = (abs(sollicitations["Moment ELU"]) - M_lu) / ((section['d'] - beton['Enrobage']) * sigma_s2e)
            As1 = M_lu / (z * sigma_s1) + As2 * sigma_s2e / sigma_s1e
        

        # 4 - Compute As,min and check that the value of As1 is greater than As,min
        As_min = cls.section_min(beton, acier, section, cuvelage, sollicitations)
        As_retenu = max(As1 * m.pow(10, 4), As_min)


        # 5 - Compute As,max per Eurocode 2
        As_max = round(0.04 * section['Largeur'] * section['Hauteur'] * m.pow(10, 4), 3)

        
        # Return dictionary
        armatures = {
            "mu_lim": round(mu_lim, 3),
            "mu_lu": round(mu_lu, 3),
            "alpha_u": round(alpha_u, 3),
            "z": round(z, 3),
            "sigma": round(sigma_s1,3),
            "As,min": As_min,
            "As,max": As_max,
            "As1": round(As_retenu, 3),
            "As2": round(As2 * m.pow(10, 4), 3),
            "Diametre": {}
        }

        return armatures



    @classmethod
    def flexion_simple_T(cls, beton, acier, section, cuvelage, sollicitations):
        """ Compute the section of reinforcements needed for a section shaped in T for a concrete beam. 
        See the document that details the calculations to read about the methods used and the definition of the variables. 
        
        :raise ValueError: If arguments are not dictionaries with the correct keys as define above
        :return: A dictionary with the computed variables used in the calculation of the reinforcement section
        :rtype: dict
        """

        # import modules
        import math as m 

        # Is the "Calcul en T" enabled ? If not: used the function for a rect. section
        if section['Calcul en T'] == False:
            return cls.flexion_simple_rect(beton, acier, section, cuvelage, sollicitations)

        # Compute miscellaneous variables
            # Fcd = Fck / gammaC
        fcd = Concrete._concrete.f_cd(beton['fck'], gammaC = beton['Coefficient sécurité'])
            # Coefficient alpha_e, defined in Eurocode 2 as a constant value of 15
        alpha_e = 15
            # Coefficient gamma, defined in Eurocode 2 as: gamma = M_elu / M_els
        gamma = sollicitations["Moment ELU"] / sollicitations["Moment ELS"]

        # Compute the reference moment Mtu with respect to the gravity center of tensioned reinforcements
        M_tu = (section['Largeur de la table'] * section['Hauteur de la table'] * fcd) * (section['d'] - section['Hauteur de la table'] / 2)
        
        # IF the table alone is able to balance a moment greater than the soliciting moment: the neutral axis is in the table and one uses the function for a rect. section with the width changed to beff 
        if M_tu >= abs(sollicitations["Moment ELU"]):

            # Create a copy of the dictionary 'section' and change the value of 'Largeur' 
            section_ = section.copy()
            section_['Largeur'] = section['Largeur de la table']

            # Compute as a rect. section using the new 'section_' dictionary
            armatures = cls.flexion_simple_rect(beton, acier, section_, cuvelage, sollicitations)

            # Change the value of As,min and As,max which are supposed to be computed with the width of the rect. section and not beff
            armatures['As,min'] = cls.section_min(beton, acier, section, cuvelage, sollicitations)
            armatures['As,max'] = round(0.04 * section['Largeur'] * section['Hauteur'] * m.pow(10, 4), 3)

            return armatures
        
        # IF the concrete of the table alone is not able to balance the soliciting moment: the neutral axis is in the rect. sect
        else: 
            # M2 is the solliciting moment in the section constituted by the table
            M_2 = ((section['Largeur de la table'] - section['Largeur']) * section['Hauteur de la table'] * fcd) * (section['d'] - section['Hauteur de la table'] / 2)

            # M1 is the solliciting moment in the rib (rib = 'nervure')
            M_1 = abs(sollicitations["Moment ELU"]) - M_2

            
            # Compute As2 using M1

            # Compue mu_lu using M1 
            mu_lu = abs(M_1) / (section['Largeur'] * m.pow(section['d'], 2) * fcd)

            # Compute mu_lim similarly to a rect. sect
            match beton['Classe exposition'].strip()[0:2]:

                # If the 'Classe d'exposition' is either XD, XS or XF
                case "XD" | "XS" | "XF":

                    # If the value of fck is lower than 30 MPa
                    if beton['fck'] <= 30:
                        if acier['Palier'] == "Horizontal":
                            mu_lim = (2740 * gamma + 60 * beton['fck'] - 3100) * m.pow(10, -4)
                        else:
                            mu_lim = (2800 * gamma + 37 * beton['fck'] - 2605) * m.pow(10, -4)
                    
                    else: # If fck > 30 MPa
                        if acier['Palier'] == "Horizontal":
                            A = 71.2 * beton['fck'] + 108
                            B = - 5.2 * beton['fck'] + 874.4
                            C = 0.03 * beton['fck'] - 12.5
                            K = (A + B * alpha_e + C * (alpha_e**2)) * m.pow(10, -4)
                            mu_lim = (beton['fck'] * K) / ((4.69 - 1.70 * gamma) * beton['fck'] + (159.90 - 76.20 * gamma))
                        
                        else: # if acier['Palier'] == "Incliné""
                            A = 75.3 * beton['fck'] - 189.8
                            B = - 5.6 * beton['fck'] + 874.5
                            C = 0.04 * beton['fck'] - 13
                            K = (A + B * alpha_e + C * (alpha_e**2)) * m.pow(10, -4)
                            mu_lim = (beton['fck'] * K) / ((4.62 - 1.66 * gamma) * beton['fck'] + (165.69 - 79.62 * gamma))
                
                # If the 'Classe d'exposition' is NOT XD, XS or XF
                case _:
                    mu_lim = 0.372

            # Compute the value of lambda, defined in Eurocode 2
            if beton['fck'] <= 50:
                lambda_ = 0.8
            elif beton['fck'] > 50 and beton['fck'] < 90:
                lambda_ = 0.8 - (beton['fck'] - 50) / 400
            else:
                raise ValueError('La valeur de fck est trop grande (> 90 MPa)')
            
            # Compute As2 if the section is totally compressed (i.e: mu_lu > mu_lim)
            if mu_lu <= mu_lim:
                alpha_u=(1 / lambda_) * (1 - m.sqrt(1 - 2 * mu_lu))
                z = section['d'] * (1 - 0.5 * lambda_ * alpha_u)
                sigma_s1 = cls.contrainte_aciers_tendus(beton, acier, cuvelage, alpha_u)
                As2 = 0
            else:
                # Question: Do you should use mu_lim or mu_lu to compute alpha_u and then z ? There is a small difference if you use mu_lu 
                alpha_u=(1 / lambda_) * (1 - m.sqrt(1 - 2 * mu_lim))
                z = section['d'] * (1 - 0.5 * lambda_ * alpha_u)
                sigma_s1 = cls.contrainte_aciers_tendus(beton, acier, cuvelage, alpha_u)
                
                # Per 'Traité de béton armé selon l'Eurocode 2' by Jean Perchat page 371
                As2 = (mu_lu - mu_lim) / (section['Largeur'] * m.pow(section['d'], 2) * fcd * (section['d'] - beton['Enrobage']) * acier['fyk'] / acier['Coefficient sécurité']) * m.pow(10, 4)
            
            
            # Compute As1

            # As1 = A1 + A2
            # A1: Reinforcement section in balance with the concrete of the rib 
            # A2: Reinforcement section in balance with the concrete of the table 
            As1 = (abs(M_1) / (z * sigma_s1) + (section['Largeur de la table'] - section['Largeur']) * section['Hauteur de la table'] * fcd / sigma_s1) * m.pow(10, 4)

        # Compute As,min and check that the value of As1 is greater than As,min
        As_min = cls.section_min(beton, acier, section, cuvelage, sollicitations)
        As_retenu = max(As1, As_min)


        # Compute As,max per Eurocode 2
        As_max = round(0.04 * section['Largeur'] * section['Hauteur'] * m.pow(10, 4), 3)

        # Return dictionary
        armatures = {
            "mu_lim": round(mu_lim, 3),
            "mu_lu": round(mu_lu, 3),
            "alpha_u": round(alpha_u, 3),
            "z": round(z, 3),
            "sigma": round(sigma_s1,3),
            "As,min": As_min,
            "As,max": As_max,
            "As1": round(As_retenu, 3),
            "As2": round(As2, 3),
            "Diametre": {}
        }

        return armatures



    @classmethod
    def necessite_tranchant(cls, beton, section, sollicitations, armatures, elementType):
        """ Verify if transverse reinforcements are needed. Per Eurocode 2:
            - if |Velu| < Vrd,c: Asw = Asw,min
            - if |Velu| >= Vrd,c: Transerve reinforcements are needed
        
        :param armatures: Dictionary containing all info of element's section of reinforcement. It must contain a key called 'As1' which is the main section of reinforcement.
                          For a beam subjected to bending: As1 is the section of reinforcement in the lower part of the beam (units: cm²)
        :type armatures: dict
        :param elementType: Variable which value is either "Poutre" or "Plaque" and characterizes the type of element. By default, the element considered is a type-Beam element. 
        :type elementType: str
        :raise ValueError: If arguments are not dictionaries with the correct keys as define above
        :return: True/False if transverse reinforcements are/aren't needed
        :rtype: bool
        """

        # Import modules
        import math as m

        # Deal with possible errors
        if elementType.lower().strip() not in ["plaque", "poutre"]:
            raise ValueError("Le type d'élément n'est pas correct dans la vérification de la nécessité d'armatures d'effort tranchant")

        if "As1" not in armatures:
            raise ValueError("L'argument 'armatures' n'est pas correctement renseigné dans la vérification de la nécessité d'armatures d'effort tranchant")
        
        # Define coefficient
            # Crd,c: 0.18/gammaC
        Crd_c = 0.18 / beton["Coefficient sécurité"]

            # k: mini(1 + sqrt(200/d), 2) where d is in millimeters
        k = min(1 + m.sqrt(200 / (section['d'] * 1000)), 2)

            # p: called 'pourcentage d'armatures longitudinales' 
        rho = min(armatures['As1'] * m.pow(10, -4) / section['Largeur'] / section['d'], 0.02)

            # k1: 0.15 per Eurocode 2 and NA
        k1 = 0.15

            # sigma,cp: stresses due to normal load
        fcd = Concrete._concrete.f_cd(beton['fck'], gammaC = beton['Coefficient sécurité'])
        sigma = min(0.2 * fcd, sollicitations["Normal ELU"] / section['Largeur'] / section['Hauteur'])

            # nu,min: depends on the element type
        match elementType:
            case "Plaque":
                nu_min = 0.23 * m.sqrt(beton['fck'])
            case "Poutre":
                nu_min = 0.035 * m.pow(k, 3/2) * m.sqrt(beton['fck'])
        
        # Compute Vrd,c
        Vrd_c = max((nu_min + k1 * sigma) * section['Largeur'] * section['d'], (Crd_c * k * m.pow(100 * rho * beton['fck'], 1/3) + k1 * sigma) * section['Largeur'] * section['d'])
        
        
        # Return the boolean after doing the check
        if abs(sollicitations["Tranchant ELU"]) <= Vrd_c:
            return True
        else:
            return False
    
    @classmethod
    def centerOfGravity(cls, section):
        """ Compute the center of gravity of a section from the bottom
        
        :return G: return the y-coordinates of the center of gravity from the bottom of the section
        :rtype G: float
        """

        # Import modules
        import math as m

        # Check if the section is rectangular or T-shaped
        if section["Calcul en T"] == False:
            G = section["Hauteur"] / 2
        else:
            num = (section["Hauteur"] - section["Hauteur de la table"])**2 / 2 * section["Largeur"] + section["Largeur de la table"] * section["Hauteur de la table"] * (section["Hauteur"] - section["Hauteur de la table"] / 2)
            denom = (section["Hauteur"] - section["Hauteur de la table"]) * section["Largeur"] + section["Largeur de la table"] * section["Hauteur de la table"]
            G = num / denom

        return G
    
    @classmethod
    def sectionState(cls, section, sollicitations):
        """ Determine the state of the section: 'Partiellement tendue', 'Partiellement comprimée', 'Totalement tendue', 'Totalement comprimée'
        
        :return state: the state of the section among the four possible states listed above
        :rtype state: str
        :return eA: the distance between the application point of the vertical load and the center of gravity of the tensioned reinforcement
        :rtype eA: float
        """


        # Deal with possible errors
        if sollicitations["Normal ELS"] == 0 or sollicitations["Normal ELU"] == 0:
            raise ValueError("La valeur de l'effort normal est nulle - Erreur dans le calcul de l'excentrement de la section")
        
        # Compute the position of the center of gravity of the section
        G = cls.centerOfGravity(section)

        # Compute the value of the eccentricity: e0 = Mu / Nu
        e0 = sollicitations["Moment ELU"] / sollicitations["Normal ELU"]

        # Compute eA depending on the signs of Mu et Nu
        if sollicitations["Normal ELU"] > 0:
            if sollicitations["Moment ELU"] > 0:
                eA = abs(e0) - (section["Hauteur"] - G) + section["d"]
            else:
                eA = abs(e0) - G + section["d"]

        elif sollicitations["Normal ELU"] < 0:
            if sollicitations["Moment ELU"] > 0:
                eA = abs(e0) + (section["Hauteur"] - G) - section["d"]
            else:
                eA = abs(e0) + G - section["d"]

        # Determine the state of the secton based on the value of eA and Nu
        if sollicitations["Normal ELU"] > 0:
            if abs(e0) > G - (section["Hauteur"] - section["d"]):
                state = 'Partiellement comprimée'
            else:
                state = 'Totalement comprimée'

        if sollicitations["Normal ELU"] < 0:
            if abs(e0) > G - (section["Hauteur"] - section["d"]):
                state = 'Partiellement tendue'
            else:
                state = 'Totalement tendue'
        
        return state, eA
        


    @classmethod
    def verification_tranchant(cls, beton, acier, section, sollicitations, theta, alpha):
        """ Check if the compression of the connecting rods is verified
        
        :param theta: 'angle des bielles'
        :type theta: int
        :param alpha: 'angles des cadres transversaux'
        :type alpha: int
        :raise ValueError: If arguments are not dictionaries with the correct keys as define above
        :return verif: True/False if 'la compression des bielles est/n'est pas vérifiée'
        :rtype verif: bool
        :return As_max: maximum section for transverse reinforcements
        """

        # Import modules
        import math as m

        # Deal with possible errors
            # The variable theta should be a number between 0 and 90°. So first check the type and then the value
        if not isinstance(theta, (int, float)):
            raise TypeError("La valeur de l'angle d'inclinaison des bielles n'a pas le bon format")

        if not 0 <= theta <= 90:
            raise ValueError("La valeur de l'angle d'inclinaison des bielles n'est pas correct dans la vérification de l'effort tranchant")

            # The variable alpha should be a number between 0 and 90°. So first check the type and then the value
        if not isinstance(alpha, (int, float)):
            raise TypeError("La valeur de l'angle des cadres transversaux n'a pas le bon format")

        if not 0 <= alpha <= 90:
            raise ValueError("La valeur de l'angle des cadres transversaux n'est pas correct dans la vérification de l'effort tranchant")
        
        # Define coefficient
        fcd = Concrete._concrete.f_cd(beton['fck'], gammaC = beton['Coefficient sécurité'])

            # Alpha,cw: its value depends on the loads applied called 'Coefficient tenant compte de l'état de contrainte dans la membrure comprimée'
        if sollicitations["Moment ELU"] != None:
            # No axial load (i.e: pure bending)
            if sollicitations["Normal ELU"] == None or sollicitations["Normal ELU"] == 0:
                alpha_cw = 1
            
            # Bending + positive axial loads (i.e: compression)
            elif sollicitations["Normal ELU"] > 0:
                sigma_cp = sollicitations["Normal ELU"] / (section['Largeur'] * section['Hauteur'])
                if 0 <= sigma_cp <= 0.25 * fcd:
                    alpha_cw = 1 + sigma_cp / fcd
                elif 0.25 * fcd <= sigma_cp <= 0.5 * fcd:
                    alpha_cw = 1.25
                elif 0.5 * fcd <= sigma_cp <= fcd:
                    alpha_cw = 2.5 * (1 - sigma_cp / fcd)
            
            # Bending + negative axial loads (i.e: tension) and only in the case of a 'membrure comprimée'
            # flexion composée avec traction avec membrure comprimée = section partiellement tendue avec une zone comprimée
            # Les cas à exclure en traction sont donc les sections totalement tendue et les cas ou |sigma_ct| >= fctm
            # Attention: la condition de membrure comprimée n'est pas codée ici. 
            elif sollicitations["Normal ELU"] < 0:
                sigma_cp = sollicitations["Normal ELU"] / (section['Largeur'] * section['Hauteur'])
                fctm = Concrete._concrete.f_ctm(beton['fck'])
                alpha_cw = 1 + sigma_cp / fctm

            else:
                raise ValueError("Vérification de l'effort tranchant: cas non traité par l'Eurocode")
        else:
            raise ValueError("Vérification de l'effort tranchant: l'élément n'est pas en flexion")

        
            # z = 0.9 * d
        z = 0.9 * section['d']

            # nu1: called 'Coefficient de réduction de la résistance du béton fissuré à l'effort tranchant
        nu1 = 0.6 * (1 - beton['fck'] / 250)

        # Compute Vrd,max: 'effort tranchant résistant max'
        Vrd_max = alpha_cw * section['Largeur'] * z * nu1 * fcd * (1 / m.tan(alpha * m.pi / 180) + 1 / m.tan(theta * m.pi / 180)) / (1 + m.pow(1 / m.tan(theta * m.pi / 180), 2))

        # Return the boolean after doing the check
        if abs(sollicitations["Tranchant ELU"]) <= Vrd_max:
            verification = True
        else:
            verification = False
        
        # Compute the maximum value of the reinforcement section
        fyd = acier['fyk'] / acier['Coefficient sécurité']
        Asw_max = 0.5 * alpha_cw * section['Largeur'] * nu1 * fcd / fyd / m.sin(alpha * m.pi / 180) * m.pow(10, 4)
        
        return verification, Asw_max



    @classmethod
    def section_tranchant(cls, beton, acier, section, sollicitations, armatures, theta = 45, alpha = 90, elementType = "Poutre"):
        """ Compute the section of transverse reinforcement for the element
        
        :param theta: 'angle des bielles' (units: degrees)
        :type theta: int
        :param alpha: 'angles des cadres transversaux' (units: degrees)
        :type alpha: int
        :param armatures: Dictionary containing all info of element's section of reinforcement. It must contain a key called 'As1' which is the main section of reinforcement.
                          For a beam subjected to bending: As1 is the section of reinforcement in the lower part of the beam (units: cm²)
        :type armatures: dict
        :param elementType: Variable which value is either "Poutre" or "Plaque" and characterizes the type of element. By default, the element considered is a type-Beam element. 
        :type elementType: str
        :raise ValueError: If arguments are not dictionaries with the correct keys as define above
        :return: A dictionary with the computed variables used in the calculation of the reinforcement section: Asw,min; Asw,max; Asw (units: cm²/ml)
        :rtype: dict
        """

        # Import modules
        import math as m
        
        # Verify if transverse reinforcements are needed and the compression of the connecting rods by calling functions above
        necessite = cls.necessite_tranchant(beton, section, sollicitations, armatures, elementType)
        verif, As_max = cls.verification_tranchant(beton, acier, section, sollicitations, theta, alpha)

        # Compute miscellaneous variables
        Z = 0.9 * section['d']
        fyd = acier['fyk'] / acier['Coefficient sécurité']

        # 'Armatures transversales de calcul'
        Asw_s = abs(sollicitations["Tranchant ELU"]) / (Z * fyd * (m.tan(alpha * m.pi / 180) + m.tan(theta * m.pi / 180)) * m.sin(alpha * m.pi / 180))

        # 'Armatures transversales minimale'
        Asw_s_min = 0.08 * section['Largeur'] * m.sin(alpha * m.pi / 180) * beton['fck'] / acier['fyk']

        # 'Armatures transversales maximales'
        Asw_s_max = As_max

        # Affect the value to the selected section

        # If |Velu| < Vrd,c: Asw = As,min
        if necessite == True:
            Asw_s_retenu = Asw_s_min

        # If |Velu| >= Vrd,c and |Velu| <= Vrd,max
        elif necessite == False and verif == True:
            # If the calculated section of reinforcement is NOT greater than the maximum valeu Asw_s_max
            if Asw_s <= Asw_s_max:
                Asw_s_retenu = Asw_s
            else:
                raise ValueError("La section d'armatures transversales de calcul est supérieure à la section maximale: redimensionner l'élément !")

        # If If |Velu| >= Vrd,c and |Velu| > Vrd,max: redesign element
        elif necessite == False and verif == False:
            raise ValueError("La compression des bielles n'est pas vérifiée: redimensionner l'élément !")
        
        # Create dictionary to be returned
        armatures = {
            "As,min": Asw_s_min,
            "As,max": Asw_s_max,
            "Asw": Asw_s_retenu
        }

        return armatures
    
    # Methods: 
    # - Verifier fonctions tranchant + membrure comprimée dans vérif tranchant
    # - Flexion composée: vérif flambement, pivot, etc...
    # - Ouverture de fissures
