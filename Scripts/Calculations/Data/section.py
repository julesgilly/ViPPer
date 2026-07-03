# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in December 2022 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""


class Section:
    def __init__(self, width, height, enrobage, Calcul_en_T, table_width, table_height):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param width: section's width (units: meters)
        :type width: float or int
        :param height: section's height (units: meters). In the case of a section shaped in T, this is the total height 
        :type height: float or int
        :param enrobage: coating for reinforcement (units: meters)
        :type enrobage: float or int
        :param Calcul_en_T: Is the section in T ? 
        :type Calcul_en_T: bool
        :param table_width: if section in T, table's width (units: meters)
        :type table_width: float or int
        :param table_height: if section in T, table's height (units: meters)
        :type table_height: float or int
        :raise ValueError: If width, height, enrobage, table_width, table_height are not a float/int
        :return: A dictionary representing the caracteristics of section
        :rtype: dict
        """

        # Check if 'width' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(width, (int, float)):
            raise ValueError("Récupération des Données - La valeur de la largeur de la section n'est pas acceptable")

        # Check if 'height' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(height, (int, float)):
            raise ValueError("Récupération des Données - La valeur de la hauteur de la section n'est pas acceptable")

        # Check if 'enrobage' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(enrobage, (int, float)):
            raise ValueError("Récupération des Données - La valeur de l'enrobage n'est pas acceptable")

        # Check the type of the 'Calcul_en_T' variable (should be a bool). Otherwise, set it up to False
        if not isinstance(Calcul_en_T, bool):
            Calcul_en_T = False

        if Calcul_en_T == True:
            # Check if 'table_width' is an int or a float. Otherwise (e.g: a str or None), raise an error
            if not isinstance(table_width, (int, float)):
                raise ValueError("Récupération des Données - La valeur de la largeur de la table de la section n'est pas acceptable")

            # Check if 'table_height' is an int or a float. Otherwise (e.g: a str or None), raise an error
            if not isinstance(table_height, (int, float)):
                raise ValueError("Récupération des Données - La valeur de la hauteur de la table de la section n'est pas acceptable")

        else:
            table_width, table_height = None, None



        self.caracteristics = {"Largeur": width,
                               "Hauteur": height,
                               "d": height - enrobage, 
                               "Calcul en T": Calcul_en_T,
                               "Largeur de la table": table_width,
                               "Hauteur de la table": table_height
                               }