# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2022 for a personal use
This file forms the class 'Surcharges' which computes the action of the overloads on the retaining wall
This file is to be used with the document that describe the calculations of the overloads on the wall 

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
    - wallLength is the length of the retaining wall from top to bottom

Output: 
    - data: Nested dictionary (keys: type of loads, positions (xmin and xmax), values (pmin and pmax)) containing horizontal distributed loads for each overloads
             overloads = { 1: {'Type': type1, 'xmin': xmin1, 'xmax': xmax1, 'pmin': pmin1, 'pmax': pmax1},
                           2: {'Type': type2, 'xmin': xmin2, 'xmax': xmax2, 'pmin': pmin2, 'pmax': pmax2}, And so on }
             where the type is "Linear"

Nota:
    - Methods that start with 'pl_' are based on the plasticity theory
    - Methods that start with 'el_' are based on the elasticity theory
"""
import numpy as np
import math as m

class surcharges:

    @classmethod
    def moyenne_angle_frottement(cls, sol):
        """ In the case of a multilayer soil, we have the choice between two possibilities:
               - We take into account the change of layers by changing the angles at the interface but keeping the continuity
               - We compute an average of the internal friction angles weighted by the thickness of the layers
        In this program we have chosen to consider the latter approach """
        
        # Define miscellaneous variables
        res, somme = 0, 0

        # Loop over the number of layers
        for sol_id, sol_info in sol.items():

            res += sol_info['Angle de frottement'] * (sol_info['Cote supérieure'] - sol_info['Cote inférieure'])
            somme += (sol_info['Cote supérieure'] - sol_info['Cote inférieure'])

        # Compute the average angle weighted by the thickness of the layers
        moyenneAngleFrottement = res / somme

        return moyenneAngleFrottement


    @classmethod
    def pl_uniforme_d(cls, pression, distance, sol, wallLength):
        """ This method computes the horizontal loads for a uniform pressure applied from a distance "d" from the retaining wall 
        
        :param pression: Value of the uniform pressure applied on the ground
        :type pression: float
        :param distance: distance from the retaining wall from where the pressure is applied
        :type distance: float
        :raise TypeError: If pression or distance are not floats or ints
        :return: A dictionary of the horizontal loads 
        :rtype: dict
        """

        # Import modules 
        import math as m

        # Create an empty dictionary to store the values of sigma
        sigma={}

        # Get the average of the internal friction angles
        meanInternalFrictionAngle = cls.moyenne_angle_frottement(sol)

        # Compute the value of 'Coefficient de poussée du sol' defined as: Ka = tan²(pi/4 - phi/2)
        Ka = (m.tan(m.pi / 4 - meanInternalFrictionAngle * m.pi / 180 /2))**2

        # Compute z1 and z2 as defined by the plasticity theory (e.g: NF P94-282 Annexe D)
        z_1 = distance * m.tan(meanInternalFrictionAngle * m.pi / 180)
        z_2 = distance * m.tan(m.pi / 4 + meanInternalFrictionAngle * m.pi /180 /2)
        
        # Affect the horizontal laods due to the uniform pressure to the dictionary to be returned
        if z_1 >= wallLength:
            # if z_1 is lower than the bottom of the wall, then no loads are applied to the retaining wall
            sigma = {}
        elif z_2 >= wallLength >= z_1:
            # if z_2 is lower than the botton of the wall, then the only load applied is the linear one 
            sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': wallLength, 'pmin': 0, 'pmax': pression * Ka * (wallLength - z_1) / (z_2 - z_1)}
        else:
            # if both z_1 and z_2 are above the bottom of the wall, then both the linear and the uniform loads are applied
            sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_2, 'pmin': 0, 'pmax': pression * Ka}
            sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_2, 'xmax': wallLength, 'pmin': pression * Ka, 'pmax': pression * Ka}

        return sigma


    @classmethod
    def pl_lineique_d(cls, lineLoad, distance, sol, wallLength):
        """ This method computes the horizontal loads for a vertical line load applied on a horizontal ground at a distance "d" of the retaining wall 
        
        :param lineLoad: Value of the vertical line load applied on the ground
        :type lineLoad: float
        :param distance: distance from the retaining wall from where the pressure is applied
        :type distance: float
        :raise TypeError: If pression or distance are not floats or ints
        :return: A dictionary of the horizontal loads 
        :rtype: dict
        """

        # Import modules 
        import math as m

        # Create an empty dictionary to store the values of sigma
        sigma={}

        # Get the average of the internal friction angles
        meanInternalFrictionAngle = cls.moyenne_angle_frottement(sol)

        # Compute the value of 'Coefficient de poussée du sol' defined as: Ka = tan²(pi/4 - phi/2)
        Ka = (m.tan(m.pi / 4 - meanInternalFrictionAngle * m.pi / 180 /2))**2

        # Compute z1 and z2 as defined by the plasticity theory (e.g: NF P94-282 Annexe D)
        z_1 = distance * m.tan(meanInternalFrictionAngle * m.pi / 180)
        z_2 = distance * m.tan(m.pi / 4 + meanInternalFrictionAngle * m.pi /180 /2)

        # Compute the maximum value of the horizontal load 
        p_max = 2 * lineLoad * (Ka)**0.5 / (z_2 - z_1) 

        # Affect the horizontal laods due to the vertical line load to the dictionary to be returned
        if z_1 >= wallLength:
            # if z_1 is lower than the bottom of the wall, then no loads are applied to the retaining wall
            sigma = {}
        elif z_2 >= wallLength >= z_1:
            # if z_2 is lower than the botton of the wall, then the only load applied is the linear one 
            sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': wallLength, 'pmin': p_max, 'pmax': p_max * (z_2 - wallLength) / (z_2 - z_1)}
        else:
            # if both z_1 and z_2 are above the bottom of the wall, then both the linear and the uniform loads are applied
            sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_2, 'pmin': p_max, 'pmax': 0}

        return sigma

    
    @classmethod
    def pl_uniforme_limitee(cls, pression, distance, width, sol, wallLength):
        """ This method computes the horizontal loads for a uniform pressure applied from a distance "d" from the retaining wall and over a limited width 
        
        :param pression: Value of the uniform pressure applied on the ground
        :type pression: float
        :param distance: distance from the retaining wall from where the pressure is applied
        :type distance: float
        :param width: width of the uniform pressure 
        :type width: float
        :raise TypeError: If pression, distance or width are not floats or ints
        :return: A dictionary of the horizontal loads 
        :rtype: dict
        """

        # Import modules 
        import math as m

        # Create an empty dictionary to store the values of sigma
        sigma={}

        # Get the average of the internal friction angles
        meanInternalFrictionAngle = cls.moyenne_angle_frottement(sol)

        # Compute the value of 'Coefficient de poussée du sol' defined as: Ka = tan²(pi/4 - phi/2)
        Ka = (m.tan(m.pi / 4 - meanInternalFrictionAngle * m.pi / 180 /2))**2

        # Compute z1, z2, z3 and z4 as defined by the plasticity theory (e.g: NF P94-282 Annexe D)
        z_1 = distance * m.tan(meanInternalFrictionAngle * m.pi / 180)
        z_2 = distance * m.tan(m.pi / 4 + meanInternalFrictionAngle * m.pi /180 /2)
        z_3 = (width + distance) * m.tan(meanInternalFrictionAngle * m.pi / 180)
        z_4 = (width + distance) * m.tan(m.pi / 4 + meanInternalFrictionAngle * m.pi /180 /2)

        # Define a limit stress which cannot be exceeded 
        sigma_lim = pression * Ka

        # if z_2 < z_3, the distribution of stresses is trapezoidal, otherwise it is triangular
        # Compute the maximum stress depending on the distribution
        if z_2 < z_3:
            distributionType = "Trapezoidal"
            sigma_max = 2 * width * pression * m.tan(m.pi / 4 + meanInternalFrictionAngle * m.pi /180 /2) / ((z_3 + z_4) - (z_1 + z_2))
        else:
            distributionType = "Triangular"
            sigma_max = 2 * width * pression * m.tan(m.pi / 4 + meanInternalFrictionAngle * m.pi /180 /2) / (z_4 - z_1)

        # If sigma_lim is exceeded, it is necessary to limit the stress and enlarge the range where the stress is constant from z_3 to a new value z_3'
        stressType = "Limited"
        if sigma_max > sigma_lim:

            stressType = "Maximum"
            # Set sigma_max = sigma_lim
            sigma_max = sigma_lim

            if z_2 < z_3:
                z_3_prime = 2 * width / Ka * m.tan(m.pi / 4 - meanInternalFrictionAngle * m.pi /180 /2) + z_1 + z_3 - z_4
            else: # Condition: z_2 > z_3
                z_3_prime = 2 * width / Ka * m.tan(m.pi / 4 - meanInternalFrictionAngle * m.pi /180 /2) + z_1 + z_2 - z_4

        # Affect the horizontal laods due to the uniform pressure to the dictionary to be returned
        # If statement: determine which case it is - case 1: z_2 < z_3 and sigma_max < sigma_lim
        if distributionType == "Trapezoidal" and stressType == "Limited":
            if z_1 >= wallLength:
                # if z_1 is lower than the bottom of the wall, then no loads are applied to the retaining wall
                sigma = {}
            elif z_2 >= wallLength >= z_1:
                # if z_2 is lower than the botton of the wall, then the only load applied is the linear one 
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': wallLength, 'pmin': 0, 'pmax': sigma_max * (wallLength - z_1) / (z_2 - z_1)}
            elif z_3 >= wallLength >= z_2:
                # if z_3 is lower than the botton of the wall
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_2, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_2, 'xmax': wallLength, 'pmin': sigma_max, 'pmax': sigma_max}
            elif z_4 >= wallLength >= z_3:
                # if z_4 is lower than the botton of the wall
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_2, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_2, 'xmax': z_3, 'pmin': sigma_max, 'pmax': sigma_max}
                sigma[3] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_3, 'xmax': wallLength, 'pmin': sigma_max, 'pmax': sigma_max * (z_4 - wallLength) / (z_4 - z_3)}
            else:
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_2, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_2, 'xmax': z_3, 'pmin': sigma_max, 'pmax': sigma_max}
                sigma[3] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_3, 'xmax': z_4, 'pmin': sigma_max, 'pmax': 0}


        # Case 2: z_2 < z_3 and sigma_max > sigma_lim
        elif distributionType == "Trapezoidal" and stressType == "Maximum":
            if z_1 >= wallLength:
                # if z_1 is lower than the bottom of the wall, then no loads are applied to the retaining wall
                sigma = {}
            elif z_2 >= wallLength >= z_1:
                # if z_2 is lower than the botton of the wall, then the only load applied is the linear one 
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': wallLength, 'pmin': 0, 'pmax': sigma_max * (wallLength - z_1) / (z_2 - z_1)}
            elif z_3_prime >= wallLength >= z_2:
                # if z_3 is lower than the botton of the wall
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_2, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_2, 'xmax': wallLength, 'pmin': sigma_max, 'pmax': sigma_max}
            elif z_4 >= wallLength >= z_3_prime:
                # if z_4 is lower than the botton of the wall
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_2, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_2, 'xmax': z_3_prime, 'pmin': sigma_max, 'pmax': sigma_max}
                sigma[3] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_3_prime, 'xmax': wallLength, 'pmin': sigma_max, 'pmax': sigma_max * (z_4 - wallLength) / (z_4 - z_3_prime)}
            else:
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_2, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_2, 'xmax': z_3_prime, 'pmin': sigma_max, 'pmax': sigma_max}
                sigma[3] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_3_prime, 'xmax': z_4, 'pmin': sigma_max, 'pmax': 0}
        
 
        # Case 3: z_2 > z_3 and sigma_max < sigma_lim
        if distributionType == "Triangular" and stressType == "Limited":
            if z_1 >= wallLength:
                # if z_1 is lower than the bottom of the wall, then no loads are applied to the retaining wall
                sigma = {}
            elif z_3 >= wallLength >= z_1:
                # if z_2 is lower than the botton of the wall, then the only load applied is the linear one 
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': wallLength, 'pmin': 0, 'pmax': sigma_max * (wallLength - z_1) / (z_3 - z_1)}
            elif z_4 >= wallLength >= z_3:
                # if z_3 is lower than the botton of the wall
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_3, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_3, 'xmax': wallLength, 'pmin': sigma_max, 'pmax': sigma_max * (z_4 - wallLength) / (z_4 - z_3)}
            else:
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_3, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_3, 'xmax': z_4, 'pmin': sigma_max, 'pmax': 0}


        # Case 4: z_2 > z_3 and sigma_max > sigma_lim
        elif distributionType == "Triangular" and stressType == "Maximum":
            if z_1 >= wallLength:
                # if z_1 is lower than the bottom of the wall, then no loads are applied to the retaining wall
                sigma = {}
            elif z_3 >= wallLength >= z_1:
                # if z_2 is lower than the botton of the wall, then the only load applied is the linear one 
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': wallLength, 'pmin': 0, 'pmax': sigma_max * (wallLength - z_1) / (z_3 - z_1)}
            elif z_3_prime >= wallLength >= z_3:
                # if z_3 is lower than the botton of the wall
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_3, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_3, 'xmax': wallLength, 'pmin': sigma_max, 'pmax': sigma_max}
            elif z_4 >= wallLength >= z_3_prime:
                # if z_4 is lower than the botton of the wall
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_3, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_3, 'xmax': z_3_prime, 'pmin': sigma_max, 'pmax': sigma_max}
                sigma[3] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_3_prime, 'xmax': wallLength, 'pmin': sigma_max, 'pmax': sigma_max * (z_4 - wallLength) / (z_4 - z_3_prime)}
            else:
                sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_3, 'pmin': 0, 'pmax': sigma_max}
                sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_3, 'xmax': z_3_prime, 'pmin': sigma_max, 'pmax': sigma_max}
                sigma[3] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_3_prime, 'xmax': z_4, 'pmin': sigma_max, 'pmax': 0}


        return sigma


    @classmethod
    def pression_contigue(cls, pression, sol):
        """ This method computes the horizontal loads for a uniform pressure applied against the retaining wall
        Using the following approach: 'We take into account the change of layers by changing the angle at the interface'
            
            :param pression: Value of the uniform pressure applied on the ground
            :type pression: float
            :raise TypeError: If 'pression' is not a float or if 'sol' isn't given as defined (see above)
            :return: A dictionary of the horizontal loads 
            :rtype: dict
        """

        # Import modules 
        import math as m

        # Create an empty dictionary to store the values of sigma
        sigma={}

        # Loop over the number of layers
        for sol_id, sol_info in sol.items():

            # Compute the value of Ka for the layer using the corresponding internal friction angle
            Ka = (m.tan(m.pi / 4 - sol_info['Angle de frottement'] * m.pi / 180 /2))**2

            # Affect loads to the dictionary
            sigma[sol_id] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': sol_info['Cote supérieure'], 'xmax': sol_info['Cote inférieure'], 'pmin': pression * Ka, 'pmax': pression * Ka}

        return sigma

    
    @classmethod
    def pression_contigue_limitee(cls, pression, width, sol, wallLength):
        """ This method computes the horizontal loads for a uniform pressure applied against the retaining wall and over a limited width 
            
            :param pression: Value of the uniform pressure applied on the ground
            :type pression: float
            :param width: width of the uniform pressure 
            :type width: float
            :raise TypeError: If pression or width are not floats or ints
            :return: A dictionary of the horizontal loads 
            :rtype: dict
            """
    
        # Import modules 
        import math as m

        # Create an empty dictionary to store the values of sigma
        sigma={}

        # Get the average of the internal friction angles
        meanInternalFrictionAngle = cls.moyenne_angle_frottement(sol)

        # Compute the value of 'Coefficient de poussée du sol' defined as: Ka = tan²(pi/4 - phi/2)
        Ka = (m.tan(m.pi / 4 - meanInternalFrictionAngle * m.pi / 180 /2))**2

        # Compute z1 and z2 as defined by the plasticity theory (e.g: NF P94-282 Annexe D)
        z_1 = width * m.tan(meanInternalFrictionAngle * m.pi / 180)
        
        # Affect the horizontal laods due to the uniform pressure to the dictionary to be returned
        if z_1 >= wallLength:
            # if z_1 is lower than the bottom of the wall, then the loads are applied to the whole length of the retaining wall
            sigma[1] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': 0, 'xmax': wallLength, 'pmin': pression * Ka, 'pmax': pression * Ka}
        else:
            # if both z_1 and z_2 are above the bottom of the wall, then the uniform loads is applied
            sigma[1] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': 0, 'xmax': z_1, 'pmin': pression * Ka, 'pmax': pression * Ka}

        return sigma


    @classmethod
    def pl_uniforme_aire(cls, pression, distance, width, length, sol, wallLength):
        """ This method computes the horizontal loads for a uniform load applied at a distance "d" from the retaining wall and with a limited length and width 
            (using the elasticity theory)
            
            :param pression: Value of the uniform pressure applied on the ground
            :type pression: float
            :param distance: distance from the retaining wall from where the pressure is applied 
            :type distance: float
            :param width: width of the uniform pressure 
            :type width: float
            :param length: length of the uniform pressure (nota: is equal to the diameter in the case of a circular loading)
            :type length: float  
            :return: A dictionary of the horizontal loads 
            :rtype: dict
            """

        # Define the lenght of application on the retaining wall
        L_p  = length + distance

        # Define a multiplying factor
        K_p = L_p / (L_p + distance)

        # Compute sigma similarly to the case of a uniform pressure applied from a distance "d" from the retaining wall and over a limited width 
        sigma=cls.pl_uniforme_limitee(K_p * pression, distance, width, sol, wallLength)

        return sigma


    @classmethod
    def el_lineique(cls, z, lineLoad, distance, angle, sol, wallLength):
        """ This method computes the horizontal loads for a line load applied at a distance "d" from the retaining wall and with an angle 
            (using the elasticity theory)
            
            :param z: depth at which the horizontal load is computed
            :type z: float
            :param lineLoad: Value of the vertical line load applied on the ground
            :type lineLoad: float
            :param distance: distance from the retaining wall from where the pressure is applied 
            :type distance: float
            :param angle: angle of the load with respect to the axis perpendicular with the ground (in degrees)
            :type angle: float 
            :return: A single value of the horizontal load at z
            :rtype: float
            """
    
        # Import modules 
        import math as m

        # Define a multiplying factor - In theory, one should use lambda = (d + 2)/(d + 1) but one can use: lambda = 1.5
        multiplyingFactor = 1.5

        # Compute the horizontal load
        sigma = multiplyingFactor * 2 * lineLoad / m.pi *(z * m.cos(angle * m.pi / 180) - distance * m.sin(angle * m.pi /180)) * distance.pow(2) / (distance.pow(2) + z.pow(2))

        return sigma

    
    @classmethod
    def risberme(cls, risbermeCaracteristics, wallLength):
        """ This method computes the horizontal loads for a risberme
            
            :param risbermeCaracteristics: contains the dimensions (height, length - at least 2.00m - and the inclination angle - usually 45°) of the risberme and the soil caracteristics (density, soil cohesiveness and friction angle)
            :form risbermeCaracteristics: _risberme = {'height': ..., 'length': ..., 'inclination angle': ..., 'density': ..., 'c': ..., 'friction angle': ...}
            :type risbermeCaracteristics: dict
            :return: A dict containing the single value of the horizontal load and the application point
            :rtype: dict
            """

        # Import modules 
        import math as m

        # Create an empty dictionary to store the values of sigma
        sigma={}

        # Total length of risberme: length + inclined part
        L_r = risbermeCaracteristics['length'] + risbermeCaracteristics['height'] / m.tan(risbermeCaracteristics['inclination angle'] * m.pi / 180)
        
        # Weight of the risberme
        W = (L_r + risbermeCaracteristics['length']) * risbermeCaracteristics['height'] * risbermeCaracteristics['density'] / 2

        # Horizontal load and position
        B_max = W * m.tan(risbermeCaracteristics['friction angle'] * m.pi /180) + risbermeCaracteristics['c'] * L_r
        pos = wallLength - risbermeCaracteristics['height']/3

        # Affect values to sigma
        sigma = {"Type": "Horizontal", "Charge": "Exploitation", "Position": pos, "P": B_max}

        return sigma


    @classmethod 
    def talus(cls, distance, talusCaracteristics, sol, wallLength):
        """ This method computes the horizontal overloads for a talus
            
            :param distance: distance from the base of the inclied part of the talus to the wall
            :type distance: float
            :param talusCaracteristics: contains the dimensions (height, length - at least 2.00m - and the inclination angle - usually 45°) of the risberme and the soil caracteristics (density, soil cohesiveness and friction angle)
            :form talusCaracteristics: talusCaracteristics = {'height': ..., 'distance': ..., 'density': ..., 'c': ..., 'friction angle': ...} where 'distance' is the length of the inclined part
            :type talusCaracteristics: dict
            :return: A dict containing the horizontal overloads 
            :rtype: dict
            """

        # Import modules 
        import math as m

        # Create an empty dictionary to store the values of sigma
        sigma={}

        # Get the average of the internal friction angles
        meanInternalFrictionAngle = cls.moyenne_angle_frottement(sol)

        # Compute the value of 'Coefficient de poussée du sol' defined as: Ka = tan²(pi/4 - phi/2)
        Ka = (m.tan(m.pi / 4 - meanInternalFrictionAngle * m.pi / 180 /2))**2

        # Compute z1 and z2 as defined by the plasticity theory (e.g: NF P94-282 Annexe D)
        z_1 = distance * m.tan(meanInternalFrictionAngle * m.pi / 180)
        z_2 = distance * m.tan(m.pi / 4 + meanInternalFrictionAngle * m.pi /180 /2) + talusCaracteristics['distance'] * m.tan(meanInternalFrictionAngle * m.pi / 180)

        # Compute sigma_max according to the theory
        sigma_max = Ka * talusCaracteristics['density'] * talusCaracteristics['height']

        # Affect the horizontal laods due to the vertical line load to the dictionary to be returned
        if z_1 >= wallLength:
            # if z_1 is lower than the bottom of the wall, then no loads are applied to the retaining wall
            sigma = {}
        elif z_2 >= wallLength >= z_1:
            # if z_2 is lower than the botton of the wall, then the only load applied is the linear one 
            sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': wallLength, 'pmin': 0, 'pmax': sigma_max * (z_2 - wallLength) / (z_2 - z_1)}
        else:
            # if both z_1 and z_2 are above the bottom of the wall, then both the linear and the uniform loads are applied
            sigma[1] = {'Type': 'linear', "Charge": "Exploitation", 'xmin': z_1, 'xmax': z_2, 'pmin': 0, 'pmax': sigma_max}
            sigma[2] = {'Type': 'uniform', "Charge": "Exploitation", 'xmin': z_2, 'xmax': wallLength, 'pmin': sigma_max, 'pmax': sigma_max}

        return sigma

    @classmethod 
    def chargement_surcharges(cls, dict_surcharges, sol_PROV, sol_DEF, wallLength_PROV, wallLength_DEF):
        """ This method returns a dict with all the computed overloads applied to the wall
            
            :param dict_surcharges: list with all the caracteristics of the overloads (from the Data > surcharges)
            :type dict_surcharges: dict
            :param sol8PROV, sol_DEF: Nested dictionaries containing for each layer: the name of the layer, the upper level, the lower level, c, phi and gamma for both phase
            sol= { 1: {'Nom de la couche': ,
                        'Cote supérieure': ,
                        'Cote inférieure': ,
                        'Cohésion': ,
                        'Angle de frottement': ,
                        'Masse volumique': 
                        'Liste abscisses':
                } and so on}
            :type sol_PROV, sol_DEF: dict
            :param wallLength: wallLength is the length of the retaining wall from top to bottom (en m)
            :type wallLength: float
            :return: A dict containing the horizontal overloads 
            :rtype: dict
        """

        # Initialize the dicts to be returned - one for the PROV phase and one for the DEF phase 
        final_surcharges_PROV = {}
        final_surcharges_DEF = {}

        # Loop over the dict_surcharges dictionary
        for key, overload in dict_surcharges.items():
            
            # Determine the type of the overload - Type 1 : "Pression uniforme appliquée à distance de l'écran"
            if overload['Type'] == "Pression uniforme appliquée à distance de l'écran":

                if overload['Phase'].lower() in ["phase définitive uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pl_uniforme_d(overload['q'], overload['d'], sol_DEF, wallLength_DEF)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_DEF[key] = computed_overloads
                
                if overload['Phase'].lower() in ["phase provisoire uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pl_uniforme_d(overload['q'], overload['d'], sol_PROV, wallLength_PROV)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_PROV[key] = computed_overloads
            
            # Determine the type of the overload - Type 2 : "Pression uniforme avec largeur limitée"
            elif overload['Type'] == "Pression uniforme avec largeur limitée":

                if overload['Phase'].lower() in ["phase définitive uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pl_uniforme_limitee(overload['q'], overload['d'], overload['B'], sol_DEF, wallLength_DEF)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_DEF[key] = computed_overloads
                
                if overload['Phase'].lower() in ["phase provisoire uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pl_uniforme_limitee(overload['q'], overload['d'], overload['B'], sol_PROV, wallLength_PROV)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_PROV[key] = computed_overloads
            
            # Determine the type of the overload - Type 3 : "Pression uniforme contigüe à l'écran avec largeur limitée"
            elif overload['Type'] == "Pression uniforme contigüe à l'écran avec largeur limitée":

                if overload['Phase'].lower() in ["phase définitive uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pression_contigue_limitee(overload['q'], overload['B'], sol_DEF, wallLength_DEF)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_DEF[key] = computed_overloads
                
                if overload['Phase'].lower() in ["phase provisoire uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pression_contigue_limitee(overload['q'], overload['B'], sol_PROV, wallLength_PROV)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_PROV[key] = computed_overloads

            # Determine the type of the overload - Type 4 : "Pression uniforme infinie contigüe à l'écran"
            elif overload['Type'] == "Pression uniforme infinie contigüe à l'écran":

                if overload['Phase'].lower() in ["phase définitive uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pression_contigue(overload['q'], sol_DEF)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_DEF[key] = computed_overloads
                
                if overload['Phase'].lower() in ["phase provisoire uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pression_contigue(overload['q'], sol_PROV)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_PROV[key] = computed_overloads

            # Determine the type of the overload - Type 5 : "Pression uniforme appliquée sur une aire"
            elif overload['Type'] == "Pression uniforme appliquée sur une aire":

                if overload['Phase'].lower() in ["phase définitive uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pl_uniforme_aire(overload['q'], overload['d'], overload['B'], overload['L'], sol_DEF, wallLength_DEF)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_DEF[key] = computed_overloads
                
                if overload['Phase'].lower() in ["phase provisoire uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pl_uniforme_aire(overload['q'], overload['d'], overload['B'], overload['L'], sol_PROV, wallLength_PROV)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_PROV[key] = computed_overloads

            # Determine the type of the overload - Type 6 : "Charge linéique verticale"
            elif overload['Type'] == "Charge linéique verticale":

                if overload['Phase'].lower() in ["phase définitive uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pl_lineique_d(overload['q'], overload['d'], sol_DEF, wallLength_DEF)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_DEF[key] = computed_overloads
                
                if overload['Phase'].lower() in ["phase provisoire uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.pl_lineique_d(overload['q'], overload['d'], sol_PROV, wallLength_PROV)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_PROV[key] = computed_overloads


            # Determine the type of the overload - Type 7 : "Talus"
            elif overload['Type'] == "Talus":

                if overload['Phase'].lower() in ["phase définitive uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.talus(overload['d'], {'height': overload['h Talus'], 'distance': overload['h Talus'] / m.tan(m.radians(overload['Angle Talus'])), 'density': overload['Poids Talus'], 'c':overload['c Talus'], 'friction angle': overload['phi Talus']}, sol_DEF, wallLength_DEF)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_DEF[key] = computed_overloads
                
                if overload['Phase'].lower() in ["phase provisoire uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.talus(overload['d'], {'height': overload['h Talus'], 'distance': overload['h Talus'] / m.tan(m.radians(overload['Angle Talus'])), 'density': overload['Poids Talus'], 'c':overload['c Talus'], 'friction angle': overload['phi Talus']}, sol_PROV, wallLength_PROV)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_PROV[key] = computed_overloads

            # Determine the type of the overload - Type 8 : "Risberme"
            elif overload['Type'] == "Risberme":

                if overload['Phase'].lower() in ["phase définitive uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.risberme({'height': overload['h Talus'], 'length': overload['L Risberme'], 'inclination angle': overload['Angle Talus'],'density': overload['Poids Talus'], 'c': overload['c Talus'], 'friction angle': overload['phi Talus']}, wallLength_DEF)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_DEF[key] = computed_overloads
                
                if overload['Phase'].lower() in ["phase provisoire uniquement", "phase définitive et provisoire"]:
                    # In this case, get the dict after computation using the function in the class
                    computed_overloads = cls.risberme({'height': overload['h Talus'], 'length': overload['L Risberme'], 'inclination angle': overload['Angle Talus'],'density': overload['Poids Talus'], 'c': overload['c Talus'], 'friction angle': overload['phi Talus']}, wallLength_PROV)
                    # Add the dict in the right final_dict regarding the phase
                    final_surcharges_PROV[key] = computed_overloads
        
        # Créer un nouveau dictionnaire
        DEF_sorted, PROV_sorted = {}, {}

        # Compteur pour générer des clés uniques
        counter_DEF, counter_PROV = 1, 1

        # PHASE DEF
        # Parcours du dictionnaire d'origine 
        for key, value in final_surcharges_DEF.items():
            if isinstance(value, dict):
                # Pour chaque sous-dictionnaire, on ajoute ses éléments directement au dictionnaire de résultats
                for sub_value in value.values():
                    if isinstance(sub_value, dict):
                        # On utilise un compteur pour générer une clé unique
                        DEF_sorted[counter_DEF] = sub_value
                        counter_DEF += 1
                    else:
                        # On utilise un compteur pour générer une clé unique
                        DEF_sorted[counter_DEF] = sub_value
                        counter_DEF += 1

        # PHASE PROV
        # Parcours du dictionnaire d'origine 
        for key, value in final_surcharges_PROV.items():
            if isinstance(value, dict):
                # Pour chaque sous-dictionnaire, on ajoute ses éléments directement au dictionnaire de résultats
                for sub_value in value.values():
                    if isinstance(sub_value, dict):
                        # On utilise un compteur pour générer une clé unique
                        PROV_sorted[counter_PROV] = sub_value
                        counter_PROV += 1
                    else:
                        # On utilise un compteur pour générer une clé unique
                        PROV_sorted[counter_PROV] = sub_value
                        counter_PROV += 1
        
        return PROV_sorted, DEF_sorted