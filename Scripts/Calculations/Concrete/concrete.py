# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2022 for a personal use
This file forms the class which compute the caracteristic of the concrete according to Eurocode 2
"""

class _concrete:

    @classmethod
    def f_cm(cls, fck):
        """ Compute the 'resistance moyenne à la compression du béton' 
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is the 'resistance moyenne à la compression du béton' 
        :rtype: float
        """
        return fck + 8

    @classmethod
    def f_cd(cls, fck, alpha_cc = 1, gammaC = 1.5):
        """ Compute the 'resistance de calcul à la compression' 
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :param alpha_cc: Eurocode 2 coefficient
        :type alpha_cc: float
        :param gammaC: Eurocode 2 coefficient - security
        :type gammaC: float
        :raise TypeError: If arguments are not floats
        :return: A float that is the 'resistance de calcul à la compression' 
        :rtype: float
        """

        return alpha_cc * fck / gammaC

    @classmethod
    def f_ctm(cls, fck):
        """ Compute the 'resistance moyenne à la traction du béton'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is the 'resistance moyenne à la traction du béton'
        :rtype: float
        """

        import math as m
        if fck <= 50:
            fctm = 0.3 * (fck**(2/3))
        else:
            fctm = 2.12  *m.ln(1 + (fck + 8) / 10)
        return fctm

    @classmethod
    def f_ctk_005(cls, fck):
        """ Compute the 'resistance caractéristiques à la traction du béton (fractile 5%)'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is the 'resistance caractéristiques à la traction du béton (fractile 5%)'
        :rtype: float
        """

        fctm = cls.f_ctm(fck)
        return 0.7 * fctm

    @classmethod
    def f_ctk_095(cls, fck):
        """ Compute the 'resistance caractéristiques à la traction du béton (fractile 95%)'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is the 'resistance caractéristiques à la traction du béton (fractile 95%)'
        :rtype: float
        """

        fctm = cls.f_ctm(fck)
        return 1.3 * fctm

    @classmethod
    def f_ctd(cls, fck, alpha_ct = 1, gammaC = 1.5):
        """ Compute the 'resistance de calcul à la traction du béton'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :param alpha_ct: Eurocode 2 coefficient
        :type alpha_cc: float
        :param gammaC: Eurocode 2 coefficient - security
        :type gammaC: float
        :raise TypeError: If arguments are not floats
        :return: A float that is the 'resistance de calcul à la traction du béton'
        :rtype: float
        """

        fctk005 = cls.f_ctk_005(fck)
        return alpha_ct * fctk005 / gammaC

    @classmethod
    def E_cm(cls, fck):
        """ Compute the 'Module d'élasticité sécant du béton'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is the 'Module d'élasticité sécant du béton'
        :rtype: float
        """

        fcm = cls.f_cm(fck)
        return 22000 * (fcm/10)**0.3
    
    @classmethod
    def Eps_c1(cls, fck):
        """ Compute the 'déformation atteinte au pic de contrainte de la relation contrainte-deformation pour l'analyse structurale'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is eps_c1
        :rtype: float
        """

        fcm = cls.f_cm(fck)
        return min(0.7 * fcm**0.31, 2.8)/1000

    @classmethod
    def Eps_cu1(cls, fck):
        """ Compute the 'valeur nominale de la déforamtion ultime de la relation contrainte-deformation pour l'analyse structurale'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is eps_cu1
        :rtype: float
        """

        if fck <= 50:
            return 3.5/1000 # pour mille
        else:
            fcm = cls.f_cm(fck)
            return (2.8 + 27*((98 - fcm) / 100)**4)/1000

    @classmethod
    def Eps_c2(cls, fck):
        """ Compute the 'déformation atteinte pour la contrainte maximale pour un diagramme parabole rectangle'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is eps_c2
        :rtype: float
        """

        if fck <= 50:
            return 2/1000 # pour mille
        else:
            return (2 + 0.085*(fck - 50)**0.53)/1000
    
    @classmethod
    def Eps_cu2(cls, fck):
        """ Compute the 'déformation ultime pour un diagramme parabole rectangle'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is eps_cu2
        :rtype: float
        """

        if fck <= 50:
            return 3.5/1000 # pour mille
        else:
            return (2 + 35*((90 - fck) / 100)**4)/1000

    @classmethod
    def n(cls, fck):
        """ Compute the 'exposant dans la relation contrainte-déformation'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is n
        :rtype: float
        """

        if fck <= 50:
            return 2/1000
        else:
            return (1.4 + 23.4*((90 - fck) / 100)**4)/1000

    @classmethod
    def Eps_c3(cls, fck):
        """ Compute the 'déformation atteinte pour la contrainte maximale pour un diagramme bilinéaire'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is eps_c3
        :rtype: float
        """

        if fck <= 50:
            return 1.75/1000 # pour mille
        else:
            return (1.75 + 0.55*(fck - 50)/40)/1000

    @classmethod
    def Eps_cu3(cls, fck):
        """ Compute the 'déformation ultime pour un diagramme bilinéaire'
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is eps_cu3
        :rtype: float
        """

        if fck <= 50:
            return 3.5/1000 # pour mille
        else:
            return (2.6 + 35*((90 - fck) / 100)**4)/1000

    @classmethod
    def fct_eff(cls, fck):
        """ Compute the 'valeur moyenne de la résistance en traction du béton au moment où les premières fissures sont supposées apparaitre'
        fct_eff = f_ctm(t) si les fissures sont supposées apparaître avant 28 jours
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :raise TypeError: If fck is not a float
        :return: A float that is fct_eff
        :rtype: float
        """

        return cls.f_ctm(fck)


    @classmethod
    def enrobage_mini(cls, fck, classe_exposition):
        """ Compute the coating minimal value in concrete

        This method is to be used in the VPP calculation algorithm ONLY because of the hypothesis that are made. For this function to be used in any cases, it is needed to add more arguments

        Hypothesis for the calculations:
            - Structure usage type: 'Structures de bâtiments courants'. Duration of projet is then 50 years and structure category is S4
            - Quality of the reinforcement installation: 'Pas de plan de qualité'. C_dev = 10 mm
            - We consider a concrete 'sans cendres volantes'
            - Aggregates biggest diameter: 15 - 16 mm
            - Control of the quality of concrete production: Common (i.e: not particular)
            - Diameter of reinforcement: < 10 mm. In common TS (welded mesh, e.g: treillis soudé), the biggest diameter is 9 mm
        
        :param fck: 'Résistance caractéristique béton en compression'
        :type fck: float
        :param classe_exposition: 'classe d'exposition du béton'
        :type classe_exposition: str
        :raise TypeError: If fck is not a float
        :return: A float that is the minimum coating
        :rtype: float
        """
        
        # The coating minimal value, called cnom, is defined as follows: cnom = max(cmin_b, cmin, 10) + C_dev

        # Quality of the reinforcement installation: 'Pas de plan de qualité'. C_dev = 10 mm
        cdev=0.01 # in meters

        # cmin,b = max(diameter of reinforcement + 5 if aggregate diameter is > 32 mm, 10) = 10 mm because of hypothesis describe above
        cmin_b = 0.01 # in meters

        # Check the possibility of reduction of structure category by 1. Recall that category is S4
        match classe_exposition:
            case "X0" | "XC1" | "XC2" | "XC3" if fck >= 30:
                R1 = 1
            case "XC4" | "XF1" if fck >= 35:
                R1 = 1
            case "XD1" | "XS1" | "XA2" | "XF2" | "XF3" | "XD2" | "XS2" | "XA2" | "XF4" if fck >= 40:
                R1 = 1
            case "XD3" | "XS3" | "XA3" if fck >= 45:
                R1 = 1
            case _: 
                R1 = 0
        
        # Check the possibility of reduction of structure category by 2. Recall that category is S4
        match classe_exposition:
            case "X0" | "XC1" if fck >= 50:
                R1 = 0
                R2 = 1
            case "XC2" | "XC3" if fck >= 55:
                R1 = 0
                R2 = 1
            case "XC4" | "XF1" | "XD1" | "XS1" | "XA1" | "XF2" | "XF3" | "XD2" | "XS2" | "XA2" | "XF4" if fck >= 60:
                R1 = 0
                R2 = 1
            case "XD3" | "XS3" | "XA3" if fck >= 70:
                R1 = 0
                R2 = 1
            case _: 
                R2 = 0
        
        # Control of the quality of concrete production: with these hypothesis
        Rqualite = 0

        # Is the element similar to a slab ? For VPP, yes. therefore, we can reduce the structure category by 1
        Rdalle = 1

        # Is the concrete made with 'cendres volantes'. We consider a concrete 'sans cendres volantes'
        RCEM1 = 0

        # Compute the new structure category 
        classe=max(1, 4 - (R1 + 2 * R2) - Rqualite - Rdalle - RCEM1)

        # Get the value of cmin based of the computated structure class and the 'classe d'exposition'
        if classe == 1:
            match classe_exposition:
                case "X0" | "XC1" | "XC2" | "XC3":
                    cmin = 0.01
                case "XC4" | "XF1":
                    cmin = 0.015
                case "XD1" | "XS1" | "XA1" | "XF2" | "XF3":
                    cmin = 0.02
                case "XD2" | "XS2" | "XA2" | "XF4":
                    cmin = 0.025
                case _:
                    cmin = 0.03

        elif classe == 2:
            match classe_exposition:
                case "X0" | "XC1":
                    cmin = 0.01
                case "XC2" | "XC3":
                    cmin = 0.015
                case "XC4" | "XF1":
                    cmin = 0.02
                case "XD1" | "XS1" | "XA1" | "XF2" | "XF3":
                    cmin = 0.025
                case "XD2" | "XS2" | "XA2" | "XF4":
                    cmin = 0.03
                case _:
                    cmin = 0.035

        elif classe == 3:
            match classe_exposition:
                case "X0" | "XC1":
                    cmin = 0.01
                case "XC2" | "XC3":
                    cmin = 0.02
                case "XC4" | "XF1":
                    cmin = 0.025
                case "XD1" | "XS1" | "XA1" | "XF2" | "XF3":
                    cmin = 0.03
                case "XD2" | "XS2" | "XA2" | "XF4":
                    cmin = 0.035
                case _:
                    cmin = 0.04

        elif classe == 4:
            match classe_exposition:
                case "X0":
                    cmin = 0.01
                case "XC1":
                    cmin = 0.015
                case "XC2" | "XC3":
                    cmin = 0.025
                case "XC4" | "XF1":
                    cmin = 0.03
                case "XD1" | "XS1" | "XA1" | "XF2" | "XF3":
                    cmin = 0.035
                case "XD2" | "XS2" | "XA2" | "XF4":
                    cmin = 0.04
                case _:
                    cmin = 0.045

        elif classe == 5:
            match classe_exposition:
                case "X0":
                    cmin = 0.015
                case "XC1":
                    cmin = 0.02
                case "XC2" | "XC3":
                    cmin = 0.03
                case "XC4" | "XF1":
                    cmin = 0.035
                case "XD1" | "XS1" | "XA1" | "XF2" | "XF3":
                    cmin = 0.04
                case "XD2" | "XS2" | "XA2" | "XF4":
                    cmin = 0.045
                case _:
                    cmin = 0.05

        elif classe == 6:
            match classe_exposition:
                case "X0":
                    cmin = 0.02
                case "XC1":
                    cmin = 0.025
                case "XC2" | "XC3":
                    cmin = 0.035
                case "XC4" | "XF1":
                    cmin = 0.04
                case "XD1" | "XS1" | "XA1" | "XF2" | "XF3":
                    cmin = 0.045
                case "XD2" | "XS2" | "XA2" | "XF4":
                    cmin = 0.05
                case _:
                    cmin = 0.055
        
        # Compute the value of cnom
        cnom = round(max(cmin_b, cmin, 0.01) + cdev, 3)

        return cnom