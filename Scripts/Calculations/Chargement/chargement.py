# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################
"""
Developed by Jules GILLY in November 2024 for a personal use
This file forms the class which get the loading from the different classes and return a single dictionnary to use in the computation of the sollicitations

Inputs : 

pointLoads = { 1: {'Type': ("Vertical", "Horizontal", "Moment"), "Charge": ("Permanente", "Exploitation"), 'Position': x1, 'P': P1},
               2: {'Type': ("Vertical", "Horizontal", "Moment"), "Charge": ("Permanente", "Exploitation"), 'Position': x2, 'P': P2}, And so on }

distributedloads = { 1: {'Type': ("Linear", "Uniform", "Trapezoidal"), "Charge": ("Permanente", "Exploitation", "EE", "EH", "EB", "EC"), 'xmin': xmin1, 'xmax': xmax1, 'pmin': pmin1, 'pmax': pmax1},
                     2: {'Type': ("Linear", "Uniform", "Trapezoidal"), "Charge": ("Permanente", "Exploitation", "EE", "EH", "EB", "EC"), 'xmin': xmin2, 'xmax': xmax2, 'pmin': pmin2, 'pmax': pmax2}, And so on }
"""

class _chargement:

    @classmethod
    def get_chargement_Voile(cls, surcharges, eau, sol, plancher):

        # Liste des dictionnaires à assembler
        dictionaries = [surcharges, eau, sol, plancher]

        # Initialize the dictionaries to be returned
        dict_chargement_voile = {}
        dict_distributedLoads, dict_pointLoads = {}, {}

        # Compteur pour les clés numériques
        counter = 1

        # Assemblage des dictionnaires
        for d in dictionaries:

            for value in d.values():
                # Vérifier si la valeur est un sous-dictionnaire
                if isinstance(value, dict):
                    # Vérifier si 'Type' n'est pas 'Vertical'
                    if value['Type'] != "Vertical":
                        dict_chargement_voile[counter] = value  # Utiliser le compteur comme clé
                        counter += 1  # Incrémenter le compteur
                else:
                    # Vérifier si 'Type' n'est pas 'Vertical'
                    if d['Type'] != "Vertical":
                        dict_chargement_voile[counter] = d  # Utiliser le compteur comme clé
                        counter += 1  # Incrémenter le compteur
                    break
                
        for key, value in dict_chargement_voile.items():
            if value['Type'].lower() in ["uniform", "linear", "trapezoidal"]:
                dict_distributedLoads[key] = value
            else:
                dict_pointLoads[key] = value

        return dict_distributedLoads, dict_pointLoads
    
    @classmethod
    def get_chargement_Fondations(cls, surcharges, plancher):

        # Liste des dictionnaires à assembler
        dictionaries = [surcharges, plancher]

        # Initialize the dictionaries to be returned
        dict_chargement_fondations = {}
        dict_distributedLoads, dict_pointLoads = {}, {}

        # Compteur pour les clés numériques
        counter = 1

        # Assemblage des dictionnaires
        for d in dictionaries:
            
            for value in d.values():
                # Vérifier si la valeur est un sous-dictionnaire
                if isinstance(value, dict):
                    # Vérifier si 'Type' n'est pas 'Vertical'
                    if value['Type'] == "Vertical":
                        dict_chargement_fondations[counter] = value  # Utiliser le compteur comme clé
                        counter += 1  # Incrémenter le compteur
                else:
                    break
        
        for key, value in dict_chargement_fondations.items():
            if value['Type'].lower() in ["uniform", "linear", "trapezoidal"]:
                dict_distributedLoads[key] = value
            else:
                dict_pointLoads[key] = value

        return dict_distributedLoads, dict_pointLoads