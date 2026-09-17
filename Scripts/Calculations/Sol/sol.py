# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2022 for a personal use
This file forms the class Sol which computes the action of the soil on the retaining wall

Input: 
    - sol: Nested dictionaries containing for each layer: the name of the layer, the upper level, the lower level, c, phi and gamma
            sol= { 1: {'Nom de la couche': ,
                        'Cote supérieure': ,
                        'Cote inférieure': ,
                        'Cohésion': ,
                        'Angle de frottement': ,
                        'Masse volumique': 
                        'Liste abscisses':
                }
            }
    - eau: {'Eau': False,
            'Niveau': None,
            'Densité': 10 kN/m3 
        }
Dans le script principal, il sera nécessaire de créer un dict spécifique pour l'eau car dans cette classe la prise en compte de l'eau ne permet pas de réaliser les combinaisons
du DTU 14.1. Il faudra utiliser les fonctions de la classe EAU. 

Output: 
    - data: Nested dictionary (keys: type of loads, positions (xmin and xmax), values (pmin and pmax)) containing an horizontal distributed load for each layer
             dloads = { 1: {'Type': type1, 'xmin': xmin1, 'xmax': xmax1, 'pmin': pmin1, 'pmax': pmax1},
                        2: {'Type': type2, 'xmin': xmin2, 'xmax': xmax2, 'pmin': pmin2, 'pmax': pmax2}, And so on }
             where the type is "Linear"

Warning!: Convention - use of relative coordinates
Note that the first layer in the 'sol' dictionary corresponds to the first real ground layer. So that means that the 'top' (i.e: xmin) of the wall is the part of the wall closest to the surface

   surface           -------------------------------------------------------      ground
                    /_\                                                   /_\  
                     0                                                 wallLength
"""
# Import modules
import numpy as np
import math as m

class _sol(object):

    @classmethod
    def average_density(cls, sol):
        """ This function computes the average density of the ground weighted by the thickness of the layers
        
        :raise error: If 'sol' is not given as expected (see above)
        :return: A single value which is the average density
        :rtype: float
        """

        # Define miscellaneous variables
        res, somme = 0, 0

        # Loop over the number of layers
        for sol_id, sol_info in sol.items():

            res += sol_info['Masse volumique'] * (sol_info['Cote supérieure'] - sol_info['Cote inférieure'])
            somme += (sol_info['Cote supérieure'] - sol_info['Cote inférieure'])

        # Compute the average angle weighted by the thickness of the layers
        averageDensity = res / somme

        return averageDensity
        

    @classmethod
    def K_a(cls, sol):
        """ This function computes the 'Coefficient de poussée du sol' defined as: Ka = tan²(pi/4 - phi/2)
        
        :raise error: If 'sol' is not given as expected (see above)
        :return: A dictionary of the values of Ka for each ground layer
        :rtype: dict
        """
        
        # Create an empty dictionary to store the values of Ka for each layer of soil
        Dict_Ka={}
        
        # Loop over the number of layers
        for sol_id, sol_info in sol.items():

            # Append to the list the computed value of Ka using the formula above
            Dict_Ka[sol_id] = {'Ka': (m.tan(m.pi / 4 - sol_info['Angle de frottement'] * m.pi / 180 / 2))**2}

        return Dict_Ka
    

    @classmethod
    def K_p(cls, sol):
        """ This function computes the 'Coefficient de butée du sol' defined as: Kp = 1/Ka
        
        :raise error: If 'sol' is not given as expected (see above)
        :return: A dictionary of the values of Kp for each ground layer
        :rtype: dict
        """
        
        # Create an empty dictionary to store the values of Ka for each layer of soil
        Dict_Kp={}
        
        # Loop over the number of layers
        for sol_id, sol_info in sol.items():

            # Append to the list the computed value of Ka using the formula above
            Dict_Kp[sol_id] = {'Kp': 1 / (m.tan(m.pi / 4 - sol_info['Angle de frottement'] * m.pi / 180 / 2))**2}

        return Dict_Kp


    @classmethod
    def sigma_verticale_tot(cls, sol):
        """ This function computes the 'Contraintes verticales totales' defined as: sigmaV = Gamma * hi
        
        :raise error: If 'sol' is not given as expected (see above)
        :return: A dictionary of the values of the total vertical stresses
        :rtype: dict
        """

        # Create an empty dictionary to store the values of sigmaV for each layer of soil 
        sigma={}

        # Loop over the number of layers
        for sol_id, sol_info in sol.items():

            # Create an empty sub-list to store the values of sigmaV at x for one layer
            Liste_i=[]

            # For the first layer
            if sol_id == 1:
                # Loop over the x list for the first layer 
                for j in range(len(sol_info['Liste abscisses'])):
                    # Append to the sublist the value of sigmaV using the formula above
                    Liste_i.append(sol_info['Masse volumique'] * abs(sol_info['Liste abscisses'][0] - sol_info['Liste abscisses'][j]))

            # For the other layers        
            else:
                # Loop over the x list for the layer 
                for j in range(len(sol_info['Liste abscisses'])):
                    # Append to the sublist the value of sigmaV using the formula above and adding the last value of the previous layer
                    Liste_i.append(sigma[sol_id - 1]['Contraintes verticales totales'][-1] + sol_info['Masse volumique'] * abs(sol_info['Liste abscisses'][0] - sol_info['Liste abscisses'][j]))

            # Append sublist to the list 
            sigma[sol_id] = {'Contraintes verticales totales': np.array(Liste_i)}

        return sigma


    @classmethod
    def pression_hydrostatique(cls, sol, eau):
        """ This function computes the 'Pression hydrostatique' defined as: sigmaV = Gamma_eau * hi
        
        :raise error: If 'sol' and 'eau' are not given as expected (see above)
        :return: A dictionary of the values of the hydrostatic pressure
        :rtype: dict
        """

        # Create an empty dictionary to store the values of u for each layer of soil 
        u={}

        # Loop over the number of layers
        for sol_id, sol_info in sol.items():

            # Create an empty sub-list to store the values of u at x for one layer
            u_i=[]

            # Loop over the x list of the layer 
            for j in range(len(sol_info['Liste abscisses'])):

                # Check the presence of water and upper level of water greater than x 
                if eau['Eau'] == True and sol_info['Liste abscisses'][j] >= eau['Niveau']:
                    # In this case, compute u
                    u_i.append(eau['Densité'] * abs(eau['Niveau'] - sol_info['Liste abscisses'][j]))

                # In every other cases
                else:
                    # Add 0 to the sublist
                    u_i.append(0)
            
            # Append sublist to the list 
            u[sol_id] = {'Pression hydrostatique': np.array(u_i)}

        return u


    @classmethod
    def sigma_verticale(cls, sigma_v_tot, u):
        """ This function computes the 'Contraintes verticales effectives' defined as: sigmaV' = sigmaV - u
        
        :param sigma_v_tot: total vertical stresses from 'sigma_verticale_tot' function
        :type sigma_v_tot: dict
        :param u: hydrostatic pressure from 'pression_hydrostatique' function 
        :type u: dict
        :return: A dictionary of the values of the effective vertical stresses
        :rtype: dict
        """
        # This function computes the 'Contraintes verticales effectives' defined as: sigmaV' = sigmaV - u

        # Create an empty dictionary to store the values of sigmaV' for each layer of soil 
        sigma={}

        # Loop over the number of layers
        for sigma_id, sigma_info in sigma_v_tot.items():

            # Create an empty sub-list to store the values of sigmaV' at x for one layer
            Liste_i=[]

            # Loop over the values of sigmaV for one layer
            for j in range(len(sigma_info['Contraintes verticales totales'])):

                # Subtract u to sigmaV and append the value to the sub-list
                Liste_i.append(sigma_info['Contraintes verticales totales'][j] - u[sigma_id]['Pression hydrostatique'][j])

            # Append sublist to the list 
            sigma[sigma_id] = {'Contraintes verticales effectives': np.array(Liste_i)}

        return sigma


    @classmethod
    def sigma_horizontale(cls, sol, sigma_v, K):
        """ This function computes the 'Contraintes horizontales effectives' defined as: sigmaH' = Ka * sigmaV' - 2 * c * srqt(Ka)
        
        :param sigma_v: effective vertical stresses from 'sigma_verticale' function
        :type sigma_v: dict
        :param K: Ka (or Kp) values
        :type K: dict
        :raise error: If 'sol' is not given as expected (see above)
        :return: A dictionary of the values of the effective horizontal stresses
        :rtype: dict
        """

        # Create an empty dictionary to store the values of sigmaH' for each layer of soil 
        sigma={}

        # Loop over the number of layers
        for sol_id, sol_info in sol.items():

            # Create an empty sub-list to store the values of sigmaH' at x for one layer
            Liste_i=[]

            # Loop over the x list of the layer 
            for j in range(len(sol_info['Liste abscisses'])):

                # Compute sigmaH' using the formula above and append the value to the sub-list
                val, = K[sol_id].values()
                Liste_i.append(val * sigma_v[sol_id]['Contraintes verticales effectives'][j] - 2  * sol_info['Cohésion'] * (val)**0.5)

            # Append sublist to the list    
            sigma[sol_id] = {'Contraintes horizontales effectives': np.array(Liste_i)}

        return sigma


    @classmethod
    def sigma_horizontale_tot(cls, sigma_h, u):
        """ This function computes the 'Contraintes horizontales totales' defined as: sigmaH = sigmaH' + u
        
        :param sigma_h: effective horizontal stresses from 'sigma_horizontale' function
        :type sigma_h: dict
        :param u: hydrostatic pressure from 'pression_hydrostatique' function 
        :type u: dict
        :return: A dictionary of the values of the total horizontal stresses
        :rtype: dict
        """

        # Create an empty dictionary to store the values of sigmaH for each layer of soil 
        sigma={}

        # Loop over the number of layers
        for sigma_id, sigma_info in sigma_h.items():

            # Create an empty sub-list to store the values of sigmaH at x for one layer
            Liste_i=[]

            # Loop over the values of sigmaH' for one layer
            for j in range(len(sigma_info['Contraintes horizontales effectives'])):

                # Check if sigmaH' + u < 0, in this case: append 0 to the sub-list because no negative values for sigmaH
                if sigma_info['Contraintes horizontales effectives'][j] + u[sigma_id]['Pression hydrostatique'][j] < 0:
                    Liste_i.append(0)
                
                # If positive, then add to the sub-list the computed value 
                else:
                    Liste_i.append(sigma_info['Contraintes horizontales effectives'][j] + u[sigma_id]['Pression hydrostatique'][j])

            # Append sublist to the list       
            sigma[sigma_id] = {'Contraintes horizontales totales': np.array(Liste_i)}

        return sigma


    @classmethod
    def contraintes_sol(cls, sol, eau):
        """ Main function computing the 'Contraintes horizontales totales' using every functions above 
        (function to call when using this class)
        
        :raise error: If 'sol' and 'eau' are not given as expected (see above)
        :return: A dictionary of the values of the total horizontal stresses
        :rtype: dict
        """

        Liste_Ka=cls.K_a(sol)
        sigma_v_tot=cls.sigma_verticale_tot(sol)
        u=cls.pression_hydrostatique(sol, eau)
        sigma_v=cls.sigma_verticale(sigma_v_tot, u)
        sigma_h=cls.sigma_horizontale(sol, sigma_v, Liste_Ka)
        sigma_h_tot=cls.sigma_horizontale_tot(sigma_h, u)
            
        return sigma_h_tot


    @classmethod
    # A reprendre !!!
    def butee(cls, sol, eau):
        """ This function computes the 'Contraintes horizontales en butée' using the same formula as for the 'Contraintes horizontales totales'
         (but Ka is replaced by Kp defined as: Kp = 1/Ka)
        
        :raise error: If 'sol' and 'eau' are not given as expected (see above)
        :return: A dictionary of the values of the total horizontal stresses
        :rtype: dict
        """
        # This function computes the 'Contraintes horizontales en butée' using the same formula as for the 'Contraintes horizontales totales'
        # But Ka is replaced by Kp defined as: Kp = 1/Ka
        Liste_Kp=cls.K_p(sol)
        sigma_v_tot=cls.sigma_verticale_tot(sol)
        u=cls.pression_hydrostatique(sol, eau)
        sigma_v=cls.sigma_verticale(sigma_v_tot, u)
        sigma_h=cls.sigma_horizontale(sol, sigma_v, Liste_Kp)
        sigma_h_tot=cls.sigma_horizontale_tot(sigma_h, u)
        
        # The resulting force is sigma_max*h/2
        return sigma_h_tot[len(sol)]['Contraintes horizontales totales'][-1]/2


    @classmethod
    def endData(cls, sol, sigma_h_tot):
        """ This function transforms the data from the computed list of values to a dictionary as expected in the 'Sollicitations' class
        
        :param sigma_h_tot: total horizontal stresses from 'sigma_horizontale_tot' function
        :type sigma_h_tot: dict
        :raise error: If 'sol' and 'eau' are not given as expected (see above)
        :return: A dictionary of the values of the total horizontal stresses with the correct data form
        :rtype: dict
        """

        # Create an empty dictionary to store the final values
        data = {}

        # Loop over the number of layer
        for id, info in sol.items():

            # Find the first and last index for which the 'Contraintes horizontales' is not zero
            index = np.nonzero(sigma_h_tot[id]['Contraintes horizontales totales'])

            # Check for errors, i.e: every value is 0
            try:
                index_min, index_max = index[0][0], index[0][-1]
            except IndexError:
                # In case of an error, put arbitrary values for the indices (doesn't really matter since pmin and pmax are 0)
                index_min, index_max = 0, len(info['Liste abscisses']) - 1
            else:
                # If no error, (just for perfection concerns) if there is at least one 0 we should take it into account as the beggining point of the distributed load. Same for a 0 at the end. 
                # So readjust the indices in the case a 0 is encountered
                if index_min != 0:
                    index_min -= 1
                if index_max != len(info['Liste abscisses']) - 1:
                    index_max += 1

            # Get xmin and xmax using the indices and the 'Liste abscisses'
            x_min, x_max = info['Liste abscisses'][index_min], info['Liste abscisses'][index_max]

            # Get pmin and pmax using the indices and the 'Contraintes horizontales totales'
            p_min, p_max = sigma_h_tot[id]['Contraintes horizontales totales'][index_min], sigma_h_tot[id]['Contraintes horizontales totales'][index_max]
            
            # Store all the values in the data dictionary with the correct syntax
            data[id] = {'Type': 'linear', "Charge": "Permanente", 'xmin': x_min, 'xmax': x_max, 'pmin': p_min, 'pmax': p_max}

        return data 


