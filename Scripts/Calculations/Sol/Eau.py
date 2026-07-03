# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2022 for a personal use
This file forms the class Sol which computes the action of the water on the retaining wall

Input: 

    - eau: {'Eau': presenceEau,
            'Niveau': niveauEau,
            'Type': typeEau, # "EE", "EH", "EB", "EC"
            'Densité': 10 kN/m3 
        } 
    
        - wallLength : hauteur du mur (en m)

Output: 
    - data: Nested dictionary (keys: type of loads, positions (xmin and xmax), values (pmin and pmax)) containing an horizontal distributed load for each layer
             dloads = {'Type': type1, "Charge": "EE", "EH", "EB", 'xmin': xmin1, 'xmax': xmax1, 'pmin': pmin1, 'pmax': pmax1}
             where the type is "Linear"

Warning!: Convention - use of relative coordinates
Note that the first layer in the 'sol' dictionary corresponds to the first real ground layer. So that means that the 'top' (i.e: xmin) of the wall is the part of the wall closest to the surface

   surface           -------------------------------------------------------      ground
                    /_\                                                   /_\  
                     0                                                 wallLength
"""
import numpy as np

class _eau(object):

    @classmethod
    def pression_hydrostatique(cls, eau, wallLength):
        """ This function computes the 'Pression hydrostatique' defined as: sigmaV = Gamma_eau * hi
        
        :raise error: If 'eau' are not given as expected (see above)
        :return: A dictionary of the values of the hydrostatic pressure
        :rtype: dict
        """

        # Create the dict with the form of a distributed load
        u={"Type": "linear", 
           "Charge": eau['Type'],
           "xmin": eau['Niveau'],
           "xmax": wallLength,
           "pmin": 0,
           "pmax": (wallLength - eau['Niveau']) * eau['Densité'] }

        return u

