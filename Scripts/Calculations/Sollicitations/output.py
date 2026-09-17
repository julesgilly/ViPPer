"""
Developed by Jules GILLY in December 2024 for a personal use
This file forms the class to get the sollicitations on each sides of the VPP to compute the reinforcement section with the "Armatures" classes. This class also create a dict with the loads on the BN. 

Inputs:
- sollicitations_ELS_PROV: a list containing dicts of the max and min sollicitations for every combinations at ELS for the PROV phase
 The dicts must have the following form : 
 self.endDict = {"Moment MIN": minMoment,
                   "Moment MAX": maxMoment,
                   "Tranchant MIN": minShear,
                   "Tranchant MAX": maxShear,
                   "Reactions": self.verticalreaction}   

- sollicitations_ELU_PROV: a list containing dicts of the max and min sollicitations for every combinations at ELU for the PROV phase
 The dicts must have the following form : 
 self.endDict = {"Moment MIN": minMoment,
                   "Moment MAX": maxMoment,
                   "Tranchant MIN": minShear,
                   "Tranchant MAX": maxShear,
                   "Reactions": self.verticalreaction}

- sollicitations_ELS_DEF: a list containing dicts of the max and min sollicitations for every combinations at ELS for the DEF phase
 The dicts must have the following form : 
 self.endDict = {"Moment MIN": minMoment,
                   "Moment MAX": maxMoment,
                   "Tranchant MIN": minShear,
                   "Tranchant MAX": maxShear,
                   "Reactions": self.verticalreaction}

- sollicitations_ELU_DEF: a list containing dicts of the max and min sollicitations for every combinations at ELU for the DEF phase
 The dicts must have the following form : 
 self.endDict = {"Moment MIN": minMoment,
                   "Moment MAX": maxMoment,
                   "Tranchant MIN": minShear,
                   "Tranchant MAX": maxShear,
                   "Reactions": self.verticalreaction}

- chargementFondationsGLOBAL_P_PROV : the vertical loading on the VPP for the PROV phase
The dicts must have the following form:
ploads = { 1: {'Type': type1, 'Position': x1, 'P': P1},
           2: {'Type': type2, 'Position': x2, 'P': P2}, And so on }

- chargementFondationsGLOBAL_P_DEF : the vertical loading on the VPP for the DEF phase
The dicts must have the following form:
ploads = { 1: {'Type': type1, 'Position': x1, 'P': P1},
           2: {'Type': type2, 'Position': x2, 'P': P2}, And so on }

- combinaisons : a dict with the values of the coefficient for the combinations 
combinaisons = {"G": coeffG,
                "Q": coeffQ}

Output: 
- sollicitationsVoiles_PROV_faceINT : a dict with the sollicitations on the INT side of the VPP for the PROV phase
The dict must have the following form : 
sollicitations: {"Moment ELS": ...,
                 "Moment ELU": ...,
                 "Tranchant ELS": ...,
                 "Tranchant ELU": ...,
                 "Normal ELS": ...,
                 "Normal ELU": ...
                  }

- sollicitationsVoiles_PROV_faceEXT : a dict with the sollicitations on the EXT side of the VPP for the PROV phase
The dict must have the following form : 
sollicitations: {"Moment ELS": ...,
                 "Moment ELU": ...,
                 "Tranchant ELS": ...,
                 "Tranchant ELU": ...,
                 "Normal ELS": ...,
                 "Normal ELU": ...
                  }

- sollicitationsVoiles_DEF_faceINT : a dict with the sollicitations on the INT side of the VPP for the DEF phase
The dict must have the following form : 
sollicitations: {"Moment ELS": ...,
                 "Moment ELU": ...,
                 "Tranchant ELS": ...,
                 "Tranchant ELU": ...,
                 "Normal ELS": ...,
                 "Normal ELU": ...
                  }

- sollicitationsVoiles_DEF_faceEXT : a dict with the sollicitations on the EXT side of the VPP for the DEF phase
The dict must have the following form : 
sollicitations: {"Moment ELS": ...,
                 "Moment ELU": ...,
                 "Tranchant ELS": ...,
                 "Tranchant ELU": ...,
                 "Normal ELS": ...,
                 "Normal ELU": ...
                  }

- chargementLierne_ELS : the loading on the BN linked with the number corresponding to the butons with no coefficient (ELS)
distributedloads = { 1: {'Type': "Linear"", "Charge": None, 'xmin': xmin1, 'xmax': xmax1, 'pmin': pmin1, 'pmax': pmax1},
                     2: {'Type': "Linear"", "Charge": None, 'xmin': xmin2, 'xmax': xmax2, 'pmin': pmin2, 'pmax': pmax2}, And so on }

- chargementLierne_ELU : the loading on the BN linked with the number corresponding to the butons with coefficients (ELU)
distributedloads = { 1: {'Type': "Linear"", "Charge": None, 'xmin': xmin1, 'xmax': xmax1, 'pmin': pmin1, 'pmax': pmax1},
                     2: {'Type': "Linear"", "Charge": None, 'xmin': xmin2, 'xmax': xmax2, 'pmin': pmin2, 'pmax': pmax2}, And so on }

Nota: Always use relative coordinates - which means that 'cote supérieure' is smaller than 'cote inférieure'
"""

class Output(object):

    def __init__(self, sollicitations_ELS_PROV, sollicitations_ELU_PROV, sollicitations_ELS_DEF, sollicitations_ELU_DEF, chargementFondationsGLOBAL_P_PROV, chargementFondationsGLOBAL_P_DEF, combinaisons):
        self.main(sollicitations_ELS_PROV, sollicitations_ELU_PROV, sollicitations_ELS_DEF, sollicitations_ELU_DEF, chargementFondationsGLOBAL_P_PROV, chargementFondationsGLOBAL_P_DEF, combinaisons)

    def main(self, sollicitations_ELS_PROV, sollicitations_ELU_PROV, sollicitations_ELS_DEF, sollicitations_ELU_DEF, chargementFondationsGLOBAL_P_PROV, chargementFondationsGLOBAL_P_DEF, combinaisons):
        
        # Compute the value of the vertical effort for both phases at ELS and ELU
        # Intialize the values for later use
        V_PROV_ELS, V_PROV_ELU, V_DEF_ELS, V_DEF_ELU = 0, 0, 0, 0
        
        # Loop over the dictionnaries
        for key, value in chargementFondationsGLOBAL_P_PROV.items():
            if value["Charge"] == "Permanente":
                V_PROV_ELS += value["P"]
                V_PROV_ELU += combinaisons["G"] * value["P"]
            elif value["Charge"] == "Exploitation":
                V_PROV_ELS += value["P"]
                V_PROV_ELU += combinaisons["Q"] * value["P"]
        
        for key, value in chargementFondationsGLOBAL_P_DEF.items():
            if value["Charge"] == "Permanente":
                V_DEF_ELS += value["P"]
                V_DEF_ELU += combinaisons["G"] * value["P"]
            elif value["Charge"] == "Exploitation":
                V_DEF_ELS += value["P"]
                V_DEF_ELU += combinaisons["Q"] * value["P"]

        # Create the output dict
        def enveloppe(liste_els, liste_elu, cle_moment, cle_tranchant, n_els, n_elu):
            """Enveloppe des sollicitations sur une face (max sur toutes les combinaisons)."""
            return {"Moment ELS":    max(d[cle_moment]    for d in liste_els),
                    "Moment ELU":    max(d[cle_moment]    for d in liste_elu),
                    "Tranchant ELS": max(d[cle_tranchant] for d in liste_els),
                    "Tranchant ELU": max(d[cle_tranchant] for d in liste_elu),
                    "Normal ELS":    n_els,
                    "Normal ELU":    n_elu}

        self.sollicitationsVoiles_PROV_faceINT = enveloppe(sollicitations_ELS_PROV, sollicitations_ELU_PROV,
                                                           "Moment MAX", "Tranchant MAX", V_PROV_ELS, V_PROV_ELU)
        self.sollicitationsVoiles_PROV_faceEXT = enveloppe(sollicitations_ELS_PROV, sollicitations_ELU_PROV,
                                                           "Moment MIN", "Tranchant MIN", V_PROV_ELS, V_PROV_ELU)
        self.sollicitationsVoiles_DEF_faceINT  = enveloppe(sollicitations_ELS_DEF, sollicitations_ELU_DEF,
                                                           "Moment MAX", "Tranchant MAX", V_DEF_ELS, V_DEF_ELU)
        self.sollicitationsVoiles_DEF_faceEXT  = enveloppe(sollicitations_ELS_DEF, sollicitations_ELU_DEF,
                                                           "Moment MIN", "Tranchant MIN", V_DEF_ELS, V_DEF_ELU)
        
        # get the laoding on the BN
        # First, create a list with the vertical reaction 
        # intialize lists that will contain the values
        list_reaction_ELS, list_reaction_ELU = [], []

        # Search in the dictionaries and add the reactions
        for d in sollicitations_ELS_PROV:
            list_reaction_ELS.append(d["Reactions"])
        for d in sollicitations_ELU_PROV:
            list_reaction_ELU.append(d["Reactions"])
        
        # get the maximum values at each position
        list_reaction_ELS = [max(elements) for elements in zip(*list_reaction_ELS)]
        list_reaction_ELU = [max(elements) for elements in zip(*list_reaction_ELU)]

        # Create the output dict
        self.chargementBN_ELS = {(valeur + 1): {'Type': "Linear",
                                          'Charge': None,
                                          'xmin': None,
                                          'xmax': None,
                                          'pmin': float(list_reaction_ELS[valeur].item()),
                                          'pmax': float(list_reaction_ELS[valeur].item())}
                                    for valeur in range(len(list_reaction_ELS))}
        
        self.chargementBN_ELU = {(valeur + 1): {'Type': "Linear",
                                          'Charge': None,
                                          'xmin': None,
                                          'xmax': None,
                                          'pmin': float(list_reaction_ELU[valeur].item()),
                                          'pmax': float(list_reaction_ELU[valeur].item())}
                                    for valeur in range(len(list_reaction_ELU))}