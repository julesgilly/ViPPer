# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2022 for a personal use
This file forms the class which compute the loads combinations according to Eurocode 0

Inputs : 

pointLoads = { 1: {'Type': ("Vertical", "Horizontal", "Moment"), "Charge": ("Permanente", "Exploitation"), 'Position': x1, 'P': P1},
               2: {'Type': ("Vertical", "Horizontal", "Moment"), "Charge": ("Permanente", "Exploitation"), 'Position': x2, 'P': P2}, And so on }

distributedloads = { 1: {'Type': ("Linear", "Uniform", "Trapezoidal"), "Charge": ("Permanente", "Exploitation", "EE", "EH", "EB", "EC"), 'xmin': xmin1, 'xmax': xmax1, 'pmin': pmin1, 'pmax': pmax1},
                     2: {'Type': ("Linear", "Uniform", "Trapezoidal"), "Charge": ("Permanente", "Exploitation", "EE", "EH", "EB", "EC"), 'xmin': xmin2, 'xmax': xmax2, 'pmin': pmin2, 'pmax': pmax2}, And so on }
"""

class _combinaisons:

    @classmethod
    def ELU1_voile(cls, loads_dict, Coeff_ELU_G, Coeff_ELU_Q):
        """ 
        POUR LE VOILE
        Compute the load combination at ELU 1: 1.35*G + 1.5*Q + 0.74*E
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :param Coeff_ELU_G: coefficient used for dead loads in the ELU load combination
        :type Coeff_ELU_G: float
        :param Coeff_ELU_Q: coefficient used for live loads in the ELU load combination
        :type Coeff_ELU_Q: float

        :return: A dict that is the computed value of the load combination
        :rtype: dict
        """

        #Initialize dictionary to be returned
        dict_ELU1 = {}

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()

            # Check for the type of load
            if load['Charge'] == "Permanente":
                
                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= Coeff_ELU_G
                if "pmax" in copy_load:
                    copy_load['pmax'] *= Coeff_ELU_G
                if "P" in copy_load:
                    copy_load['P'] *= Coeff_ELU_G
            
            # if loads are "Exploitation"
            if load['Charge'] == "Exploitation" :

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= Coeff_ELU_Q
                if "pmax" in copy_load:
                    copy_load['pmax'] *= Coeff_ELU_Q
                if "P" in copy_load:
                    copy_load['P'] *= Coeff_ELU_Q
            
            # if loads are "EH" or "EB"
            if load['Charge'] == "EH" or load['Charge'] == "EB":

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= 1/1.35
                if "pmax" in copy_load:
                    copy_load['pmax'] *= 1/1.35
                if "P" in copy_load:
                    copy_load['P'] *= 1/1.35

            # if loads are "EE" - do not take the action of the water on the VPP at ELU
            if load['Charge'] == "EE":

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= 0
                if "pmax" in copy_load:
                    copy_load['pmax'] *= 0
                if "P" in copy_load:
                    copy_load['P'] *= 0

            # Add the copy_load dict to the final dict to be returned
            dict_ELU1[key] = copy_load

        return dict_ELU1
    
    @classmethod
    def ELU2_voile(cls, loads_dict, Coeff_ELU_G, Coeff_ELU_Q, categorie):
        """ 
        POUR LE VOILE
        Compute the load combination at ELU 2: 1.35*G + 1.5*psy0*Q + 1.35*E
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :param Coeff_ELU_G: coefficient used for dead loads in the ELU load combination
        :type Coeff_ELU_G: float
        :param Coeff_ELU_Q: coefficient used for live loads in the ELU load combination
        :type Coeff_ELU_Q: float
        :param categorie: category of the building
        :type categorie: str
        :return: A dict that is the computed value of the load combination
        :rtype: dict
        """

        #Initialize dictionary to be returned
        dict_ELU2 = {}

        #Compute phi0
        psy0 = cls.get_Psy0(categorie)

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()

            # Check for the type of load
            if load['Charge'] == "Permanente":
                
                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= Coeff_ELU_G
                if "pmax" in copy_load:
                    copy_load['pmax'] *= Coeff_ELU_G
                if "P" in copy_load:
                    copy_load['P'] *= Coeff_ELU_G
            
            # if loads are "Exploitation"
            if load['Charge'] == "Exploitation" :

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= psy0*Coeff_ELU_Q
                if "pmax" in copy_load:
                    copy_load['pmax'] *= psy0*Coeff_ELU_Q
                if "P" in copy_load:
                    copy_load['P'] *= psy0*Coeff_ELU_Q
            
            # if loads are "EH" or "EB"
            if load['Charge'] == "EH" or load['Charge'] == "EB":

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= 1.35
                if "pmax" in copy_load:
                    copy_load['pmax'] *= 1.35
                if "P" in copy_load:
                    copy_load['P'] *= 1.35

            # if loads are "EE" - do not take the action of the water on the VPP at ELU
            if load['Charge'] == "EE":

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= 0
                if "pmax" in copy_load:
                    copy_load['pmax'] *= 0
                if "P" in copy_load:
                    copy_load['P'] *= 0

            # Add the copy_load dict to the final dict to be returned
            dict_ELU2[key] = copy_load

        return dict_ELU2
    
    @classmethod
    def Acc_voile(cls, loads_dict, categorie):
        """ 
        POUR LE VOILE
        Compute the load combination at ELU Acc: G + EE + psy_2*Q
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :param categorie: category of the building
        :type categorie: str

        :return: A dict that is the computed value of the load combination
        :rtype: dict
        """

        #Initialize dictionary to be returned
        dict_Acc = {}

        #Compute phi0
        psy2 = cls.get_Psy2(categorie)

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()
            
            # if loads are "Exploitation"
            if load['Charge'] == "Exploitation" :

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= psy2
                if "pmax" in copy_load:
                    copy_load['pmax'] *= psy2
                if "P" in copy_load:
                    copy_load['P'] *= psy2
            
            # if loads are "EH" or "EB"
            if load['Charge'] == "EH" or load['Charge'] == "EB":

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= 0
                if "pmax" in copy_load:
                    copy_load['pmax'] *= 0
                if "P" in copy_load:
                    copy_load['P'] *= 0

            # Add the copy_load dict to the final dict to be returned
            dict_Acc[key] = copy_load

        return dict_Acc

    @classmethod
    def ELS_QPE_voile(cls, loads_dict, categorie):
        """ 
        POUR LE VOILE
        Compute the load combination at 'ELS Quasi-Permanent' = G + E + psy0*Q
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :param psy_2: value of psy_2 according to table in Eurocode 0
        :type psy_2: float
        :raise TypeError: If arguments are not floats
        :return: A float that is the computed value of the load combination
        :rtype: float
        """

        #Initialize dictionary to be returned
        dict_ELSQP1 = {}

        #Compute phi0
        psy0 = cls.get_Psy0(categorie)

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()
            
            # if loads are "Exploitation"
            if load['Charge'] == "Exploitation" :

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= psy0
                if "pmax" in copy_load:
                    copy_load['pmax'] *= psy0
                if "P" in copy_load:
                    copy_load['P'] *= psy0

            # Add the copy_load dict to the final dict to be returned
            dict_ELSQP1[key] = copy_load

        return dict_ELSQP1
    
    @classmethod
    def ELS_QP_voile(cls, loads_dict):
        """ 
        POUR LE VOILE
        Compute the load combination at 'ELS Quasi-Permanent' = G + Q
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :return: A float that is the computed value of the load combination
        :rtype: float
        """

        #Initialize dictionary to be returned
        dict_ELSQP2 = {}

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()
            
            # if loads are "Exploitation"
            if load['Charge'] in ["EH", "EB", "EE"] :

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= 0
                if "pmax" in copy_load:
                    copy_load['pmax'] *= 0
                if "P" in copy_load:
                    copy_load['P'] *= 0

            # Add the copy_load dict to the final dict to be returned
            dict_ELSQP2[key] = copy_load

        return dict_ELSQP2

    @classmethod
    def ELU_fondations(cls, loads_dict, Coeff_ELU_G, Coeff_ELU_Q):
        """ 
        POUR LES FONDATIONS DU VPP
        Compute the load combination at ELU 1: 1.35*G + 1.5*Q
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :param Coeff_ELU_G: coefficient used for dead loads in the ELU load combination
        :type Coeff_ELU_G: float
        :param Coeff_ELU_Q: coefficient used for live loads in the ELU load combination
        :type Coeff_ELU_Q: float

        :return: A dict that is the computed value of the load combination
        :rtype: dict
        """

        #Initialize dictionary to be returned
        dict_ELU = {}

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()

            # Check for the type of load
            if load['Charge'] == "Permanente":
                
                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= Coeff_ELU_G
                if "pmax" in copy_load:
                    copy_load['pmax'] *= Coeff_ELU_G
                if "P" in copy_load:
                    copy_load['P'] *= Coeff_ELU_G
            
            # if loads are "Exploitation"
            elif load['Charge'] == "Exploitation" :

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= Coeff_ELU_Q
                if "pmax" in copy_load:
                    copy_load['pmax'] *= Coeff_ELU_Q
                if "P" in copy_load:
                    copy_load['P'] *= Coeff_ELU_Q

            # Do not take the action of the water on the VPP at ELU
            else:

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= 0
                if "pmax" in copy_load:
                    copy_load['pmax'] *= 0
                if "P" in copy_load:
                    copy_load['P'] *= 0

            # Add the copy_load dict to the final dict to be returned
            dict_ELU[key] = copy_load

        return dict_ELU
    
    @classmethod
    def ELS_QP_fondations(cls, loads_dict, categorie):
        """ 
        POUR LES FONDATIONS DU VPP
        Compute the load combination at 'ELS Quasi-Permanent' = G + psy2*Q
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :param psy_2: value of psy_2 according to table in Eurocode 0
        :type psy_2: float
        :raise TypeError: If arguments are not floats
        :return: A float that is the computed value of the load combination
        :rtype: float
        """

        #Initialize dictionary to be returned
        dict_ELSQP = {}

        #Compute phi0
        psy2 = cls.get_Psy2(categorie)

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()
            
            # if loads are "Exploitation"
            if load['Charge'] == "Exploitation" :

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= psy2
                if "pmax" in copy_load:
                    copy_load['pmax'] *= psy2
                if "P" in copy_load:
                    copy_load['P'] *= psy2

            # Add the copy_load dict to the final dict to be returned
            dict_ELSQP[key] = copy_load

        return dict_ELSQP
    
    @classmethod
    def ELS_Cara_fondations(cls, loads_dict):
        """ POUR LES FONDATIONS DU VPP
        Compute the load combination at 'ELS caracteristique' = G + Q
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :return: A float that is the computed value of the load combination
        :rtype: float
        """
        #Initialize dictionary to be returned
        dict_ELS_Cara = {}

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()
            
            # if loads are "Exploitation"
            if load['Charge'] not in ["Permanente", "Exploitation"] :

                # Check if distributed or point load
                if "pmin" in copy_load:
                    copy_load['pmin'] *= 0
                if "pmax" in copy_load:
                    copy_load['pmax'] *= 0
                if "P" in copy_load:
                    copy_load['P'] *= 0

            # Add the copy_load dict to the final dict to be returned
            dict_ELS_Cara[key] = copy_load

        return dict_ELS_Cara

    @classmethod
    def ELU_STR_portance(cls, loads_dict, Coeff_ELU_G, Coeff_ELU_Q):
        """
        POUR LES FONDATIONS DU VPP
        Compute the load combination for the verification of the soil's resistance capacity at ELU STR
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :param Coeff_ELU_G: coefficient used for dead loads in the ELU load combination
        :type Coeff_ELU_G: float
        :param Coeff_ELU_Q: coefficient used for live loads in the ELU load combination
        :type Coeff_ELU_Q: float

        :return: A dict that is the computed value of the load combination
        :rtype: dict
        """

        #Si V augmente c'est défavorable donc les actions positives sont défavorables

        #Initialize dictionary to be returned
        dict_ELU_P = {}

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()
        
            # Charges permanentes
            if load['Charge'] == "Permanente" :
                    
                    # Check if distributed or point load
                    if "pmin" in copy_load and "pmax" in copy_load:

                        # Check if the load is positive by checking the positivity of the mean of pmin and pmax
                        if (load['pmin'] + load['pmax']) / 2 >= 0:

                            # If so, multiply the load by the Coeff_ELU_G coefficient
                            copy_load['pmin'] *= Coeff_ELU_G
                            copy_load['pmax'] *= Coeff_ELU_G
                    
                    if "P" in copy_load:

                        # Check if the point load is positive by checking the positivity of the value of P
                        if copy_load['P'] >= 0:

                            # If so, multiply the point load by the Coeff_ELU_G coefficient
                            copy_load['P'] *= Coeff_ELU_G
            
            # Charges d'exploitation
            if load['Charge'] == "Exploitation" :
                    
                    # Check if distributed or point load
                    if "pmin" in copy_load and "pmax" in copy_load:

                        # Check if the load is positive by checking the positivity of the mean of pmin and pmax
                        if (load['pmin'] + load['pmax']) / 2 >= 0:

                            # If so, multiply the load by the Coeff_ELU_Q coefficient
                            copy_load['pmin'] *= Coeff_ELU_Q
                            copy_load['pmax'] *= Coeff_ELU_Q

                        else:
                            # Else, the load is not taken into account bc favorable in the calculations
                            copy_load['pmin'] *= 0
                            copy_load['pmax'] *= 0
                    
                    # Check if the point load is positive by checking the positivity of the value of P
                    if "P" in copy_load:
                        if copy_load['P'] >= 0:

                            # If so, multiply the point load by the Coeff_ELU_Q coefficient
                            copy_load['P'] *= Coeff_ELU_Q
                        
                        else:
                            # Else, the load is not taken into account bc favorable in the calculations
                            copy_load['P'] *= 0
            
            # Add the copy_load dict to the final dict to be returned
            dict_ELU_P[key] = copy_load

        return dict_ELU_P

    @classmethod
    def ELU_STR_glissement_V(cls, loads_dict, Coeff_ELU_G, Coeff_ELU_Q):
        """
        POUR LES FONDATIONS DU VPP
        Compute the load combination for the vertical loads in the verification of the soil's ability to resist sliding at ELU STR
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :param Coeff_ELU_G: coefficient used for dead loads in the ELU load combination
        :type Coeff_ELU_G: float
        :param Coeff_ELU_Q: coefficient used for live loads in the ELU load combination
        :type Coeff_ELU_Q: float

        :return: A dict that is the computed value of the load combination
        :rtype: dict
        """

        #Si V augmente cela devient favorbale donc les actions positives verticales sont favorable

        #Initialize dictionary to be returned
        dict_ELU_GV = {}

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()
        
            # Charges permanentes
            if load['Charge'] == "Permanente" :
                    
                    # Check if distributed or point load
                    if "pmin" in copy_load and "pmax" in copy_load:

                        # Check if the load is negative by checking the positivity of the mean of pmin and pmax
                        if (load['pmin'] + load['pmax']) / 2 <= 0:

                            # If so, multiply the load by the Coeff_ELU_G coefficient
                            copy_load['pmin'] *= Coeff_ELU_G
                            copy_load['pmax'] *= Coeff_ELU_G
                    
                    if "P" in copy_load:

                        # Check if the point load is negative by checking the positivity of the value of P
                        if copy_load['P'] <= 0:

                            # If so, multiply the point load by the Coeff_ELU_G coefficient
                            copy_load['P'] *= Coeff_ELU_G
            
            # Charges d'exploitation
            if load['Charge'] == "Exploitation" :
                    
                    # Check if distributed or point load
                    if "pmin" in copy_load and "pmax" in copy_load:

                        # Check if the load is negative by checking the positivity of the mean of pmin and pmax
                        if (load['pmin'] + load['pmax']) / 2 <= 0:

                            # If so, multiply the load by the Coeff_ELU_Q coefficient
                            copy_load['pmin'] *= Coeff_ELU_Q
                            copy_load['pmax'] *= Coeff_ELU_Q

                        else:
                            # Else, the load is not taken into account bc favorable in the calculations
                            copy_load['pmin'] *= 0
                            copy_load['pmax'] *= 0
                    
                    # Check if the point load is negative by checking the positivity of the value of P
                    if "P" in copy_load:
                        if copy_load['P'] <= 0:

                            # If so, multiply the point load by the Coeff_ELU_Q coefficient
                            copy_load['P'] *= Coeff_ELU_Q
                        
                        else:
                            # Else, the load is not taken into account bc favorable in the calculations
                            copy_load['P'] *= 0
            
            # Add the copy_load dict to the final dict to be returned
            dict_ELU_GV[key] = copy_load

        return dict_ELU_GV

    @classmethod
    def ELU_STR_glissement_H(cls, loads_dict, Coeff_ELU_G, Coeff_ELU_Q):
        """ 
        POUR LES FONDATIONS DU VPP
        Compute the load combination for the horizontal loads in the verification of the soil's ability to resist sliding at ELU STR
        
        :param laods_dict: dict with all the loads applied to the VPP
        :type loads_dict: dict
        :param Coeff_ELU_G: coefficient used for dead loads in the ELU load combination
        :type Coeff_ELU_G: float
        :param Coeff_ELU_Q: coefficient used for live loads in the ELU load combination
        :type Coeff_ELU_Q: float

        :return: A dict that is the computed value of the load combination
        :rtype: dict
        """

        #Si H augmente c'est défavorable donc les actions positives sont défavorables

        #Initialize dictionary to be returned
        dict_ELU_GH = {}

        # Loop over the loads in the dictionary
        for key, load in loads_dict.items():

            # Create a copy of the load i dict
            copy_load = load.copy()
        
            # Charges permanentes
            if load['Charge'] == "Permanente" :
                    
                    # Check if distributed or point load
                    if "pmin" in copy_load and "pmax" in copy_load:

                        # Check if the load is positive by checking the positivity of the mean of pmin and pmax
                        if (load['pmin'] + load['pmax']) / 2 >= 0:

                            # If so, multiply the load by the Coeff_ELU_G coefficient
                            copy_load['pmin'] *= Coeff_ELU_G
                            copy_load['pmax'] *= Coeff_ELU_G
                    
                    if "P" in copy_load:

                        # Check if the point load is positive by checking the positivity of the value of P
                        if copy_load['P'] >= 0:

                            # If so, multiply the point load by the Coeff_ELU_G coefficient
                            copy_load['P'] *= Coeff_ELU_G
            
            # Charges d'exploitation
            if load['Charge'] == "Exploitation" :
                    
                    # Check if distributed or point load
                    if "pmin" in copy_load and "pmax" in copy_load:

                        # Check if the load is positive by checking the positivity of the mean of pmin and pmax
                        if (load['pmin'] + load['pmax']) / 2 >= 0:

                            # If so, multiply the load by the Coeff_ELU_Q coefficient
                            copy_load['pmin'] *= Coeff_ELU_Q
                            copy_load['pmax'] *= Coeff_ELU_Q

                        else:
                            # Else, the load is not taken into account bc favorable in the calculations
                            copy_load['pmin'] *= 0
                            copy_load['pmax'] *= 0
                    
                    # Check if the point load is positive by checking the positivity of the value of P
                    if "P" in copy_load:
                        if copy_load['P'] >= 0:

                            # If so, multiply the point load by the Coeff_ELU_Q coefficient
                            copy_load['P'] *= Coeff_ELU_Q
                        
                        else:
                            # Else, the load is not taken into account bc favorable in the calculations
                            copy_load['P'] *= 0
            
            # Add the copy_load dict to the final dict to be returned
            dict_ELU_GH[key] = copy_load

        return dict_ELU_GH

    @classmethod
    def get_Psy0(cls, categorie):
        """ Get the psy_0 coefficient from table in Eurocode 0
        
        :param categorie: usage of the structure
        :type categorie: str
        :return: A float value for psy_0 or None if the usage category is not in the table
        :rtype: float
        """
        match categorie:
            case "E":
                return 1
            case _: 
                return 0.7
            
    @classmethod
    def get_Psy2(cls, categorie):
        """ Get the psy_2 coefficient from table in Eurocode 0
        
        :param categorie: usage of the structure
        :type categorie: str
        :return: A float value for psy_2 or None if the usage category is not in the table
        :rtype: float
        """
        match categorie:
            case "A" | "B" | "G":
                return 0.3
            case "C" | "D" | "F":
                return 0.6
            case "E":
                return 0.8
            case "H":
                return 0
            case _: 
                return None
 