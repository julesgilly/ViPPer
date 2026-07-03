# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in December 2022 for a personal use
This file forms the class which transform the data retrieved from the user's inputs into a usable form for the calculations
"""
import re

class Beton:
    def __init__(self, density, fck, classe_exposition, enrobage, Coeff_securite, Module_DEF, Module_PROV, Coeff_equivalence):
        """ Take the user's inputs from software as arguments and transform into a dict to be used for calculations 
        
        :param density:density of concrete (units: kN/m3)
        :type density: float
        :param fck: 'Résistance caractéristique à la compression du béton' (units: MPa)
        :type fck: str
        :param classe_exposition: 'Classe d'exposition' du béton
        :type classe_exposition: str
        :param enrobage: coating for reinforcement (units: cm)
        :type enrobage: float or int
        :param Coeff_securite: steel security coefficient per Eurocode (units: None)
        :type Coeff_securite: float
        :param Module_DEF: concrete Young's modulus for phase 'DEF' (units: MPa)
        :type Module_DEF: float or int
        :param Module_PROV: concrete Young's modulus for phase 'PROV' (units: MPa)
        :type Module_PROV: float or int
        :param Coeff_equivalence: 'Coefficient d'équivalence acier/béton pour les sections homogènes' (units: None)
        :type Coeff_equivalence: int or float 
        :raise ValueError: If density, fck, enorbage, Coeff_securite, Module_DEF, Module_PROV or Coeff_equivalence are not a float/int
        :return: A dictionary representing the caracteristics of concrete
        :rtype: dict
        """

        # Check if 'density' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(density, (int, float)):
            raise ValueError("Récupération des Données - La valeur de la masse volumique n'est pas acceptable")

        # Check if 'fck' is an int or a float. Otherwise (e.g: a str), raise an error
        match = re.match(r'^C(\d{2})/(\d{2})$', fck)
        if not match:
            raise ValueError("Récupération des Données - La valeur de fck n'est pas acceptable")
        
        # The 'classe_exposition' variable can only the following values: "X0", "Xc1" to "XC4", "XD1" to "XD3", "XS1" to "XS3", "XF1" to "XF4" or "XA1" to "XA3"
        if classe_exposition not in ["X0", "XC1", "XC2", "XC3", "XC4", "XD1", "XD2", "XD3", "XS1", "XS2", "XS3", "XF1", "XF2", "XF3", "XF4", "XA1", "XA2", "XA3"]:
            raise ValueError("Récupération des Données - La classe d'exposition n'est pas reconnu")

        # Check if 'enrobage' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(enrobage, (int, float)):
            raise ValueError("Récupération des Données - La valeur de l'enrobage n'est pas acceptable")

        # Check if 'Coeff_securite' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(Coeff_securite, (int, float)):
            raise ValueError("Récupération des Données - La valeur du coefficient de sécurité du béton n'est pas acceptable")

        # Check if 'Module_DEF' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(Module_DEF, (int, float)):
            raise ValueError("Récupération des Données - La valeur du module d'élasticité du béton en phase DEF n'est pas acceptable")
        
        # Check if 'Module_PROV' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(Module_PROV, (int, float)):
            raise ValueError("Récupération des Données - La valeur du module d'élasticité du béton en phase PROV n'est pas acceptable")

        # Check if 'Coeff_equivalence' is an int or a float. Otherwise (e.g: a str), raise an error
        if not isinstance(Coeff_equivalence, (int, float)):
            raise ValueError("Récupération des Données - La valeur du coefficient d'équivalence aciers/béton pour les sections homogènes n'est pas acceptable")

        self.caracteristics = {"Masse volumique": density * 10**(-3),
                               "fck": int(match.group(1)),
                               "Classe exposition": classe_exposition,
                               "Enrobage": enrobage * 10**(-2),
                               "Coefficient sécurité": Coeff_securite,
                               "Module élasticité DEF": Module_DEF, 
                               "Module élasticité PROV": Module_PROV,
                               "Coefficient equivalence": Coeff_equivalence
                               }