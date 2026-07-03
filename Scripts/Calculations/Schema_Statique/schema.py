"""
Developed by Jules GILLY in November 2022 for a personal use
This file forms the class to transform the data from the user

Inputs:
 - fondations.caracteristics = {"Mode": modeFondation,
                               "Arase inférieure": AiFondation,
                               "Largeur": largeurFondation,
                               "Hauteur": hauteurFondation,
                               "Débord": debordFondation,
                               "Enrobage": enrobageFondation,
                               "Type": typeFondation,
                               "Butee": isButeeFondation,
                               "Portance ELU": portanceELU,
                               "Glissement ELU": glissementELU,
                               "Portance ELS": portanceELS,
                               "Modele Portance": modelePortance,
                               "Modele Glissement": modeleGlissement
                               }
 - planchers.caracteristics = {"Longueur VPP": longueurVoile, 
                               "Epaisseur VPP": epaisseurVoile,
                               "Cote DEF": coteSupVoile_DEF,
                               "Cote PROV": coteSupVoile_PROV}
 - planchers.dictPlancher = { 1 : { "Type": type,
                                    "Niveau": niveau,
                                    "Epaisseur": epaisseur,
                                    "Appui" : appui
                                    }
 - beton.caracteristics = {"Masse volumique": density,
                           "fck": fck,
                           "Classe exposition": classe_exposition,
                           "Enrobage": enrobage,
                           "Coefficient sécurité": Coeff_securite,
                           "Module élasticité DEF": Module_DEF, 
                           "Module élasticité PROV": Module_PROV,
                           "Coefficient equivalence": Coeff_equivalence
                            }
 -  butons.caracteristics_buton = {1: {"Numéro": numero,
                                       "Niveau": niveauButon,
                                       "Entraxe": entraxeButon,
                                       "Entraxe G": entraxeGaucheButon,
                                       "Entraxe D": entraxeDroiteButon,
                                       "Fonctionnement": fonctionnementButon,
                                       "Inclinaison": inclinaisonButon,
                                       "Distance au voile": distanceButon,
                                       "Longueur": longueurButon,
                                       "Matériau": materiauButon,
                                       "Type": typeButon,
                                       "Accrochage": accrochageButon
                                        }}
 - chargement_Voile = {"distributed PROV": chargementGLOBAL_p_PROV,
                       "point PROV": chargementGLOBAL_P_PROV,
                       "distributed DEF": chargementGLOBAL_p_DEF,
                       "point DEF":  chargementGLOBAL_P_DEF
                       }

Output: 2 dictionaries for both phases PROV and DEF
    - L: length of the beam
    - b: width of the beam
    - h: height of the beam
    - E: Young's modulus  
    - supports: Dictionary (keys: type and position)
                supports = { 1: {'Type': type1, 'Position': x1},
                             2: {'Type': type2, 'Position': x2}, And so on }
                where the type is one of the following: "Simply supported", "Roller", "Free", "Fixed"
    - distributedLoads: Dictionary (keys: type of loads, positions (xmin and xmax), values (pmin and pmax))
             dloads = { 1: {'Type': type1, 'xmin': xmin1, 'xmax': xmax1, 'pmin': pmin1, 'pmax': pmax1},
                        2: {'Type': type2, 'xmin': xmin2, 'xmax': xmax2, 'pmin': pmin2, 'pmax': pmax2}, And so on }
             where the type is one of the following: "Uniform", "Linear", "Trapezoidal"
    - pointLoads: Dictionary (keys: type of loads, position and value)
             ploads = { 1: {'Type': type1, 'Position': x1, 'P': P1},
                        2: {'Type': type2, 'Position': x2, 'P': P2}, And so on }
             where the type is one of the following: "Horizontal", "Vertical", "Moment"

Nota: Always use relative coordinates - which means that 'cote supérieure' is smaller than 'cote inférieure'
"""
import numpy as np

class _schema(object):
    def __init__(self, fondations, plancher, beton, butons, chargement):
        self.main(fondations, plancher, beton, butons, chargement)

    def main(self, fondations, plancher, beton, butons, chargement):
        
        # Get the support dict
        support_PROV, support_DEF = self.get_support(fondations, plancher, butons)

        # Verify loading
        chargement = self.verify_loading(fondations, plancher, chargement)

        self.schema_statique_PROV = {"length": fondations.caracteristics["Arase inférieure"] - plancher.caracteristics["Cote PROV"],
                                     "width": 1.0,
                                     "height": plancher.caracteristics["Epaisseur VPP"],
                                     "Young's Modulus": beton.caracteristics["Module élasticité PROV"],
                                     "supports": support_PROV,
                                     "distributedLoads": chargement["distributed PROV"],
                                     "pointLoads": chargement["point PROV"] }
        
        self.schema_statique_DEF = {"length": fondations.caracteristics["Arase inférieure"] - plancher.caracteristics["Cote DEF"],
                                     "width": 1.0,
                                     "height": plancher.caracteristics["Epaisseur VPP"],
                                     "Young's Modulus": beton.caracteristics["Module élasticité DEF"],
                                     "supports": support_DEF,
                                     "distributedLoads": chargement["distributed DEF"],
                                     "pointLoads": chargement["point DEF"] }


    def get_support(self, fondations, plancher, butons):
        
        # Define miscellaneous variables
        support_PROV, support_DEF = {}, {}

        # Loop over the element in the dictionary
        for key, value in butons.caracteristics_buton.items():

            # Add a support for every buton at the right level
            support_PROV[key] = {"Type": "Simply supported", "Position": value["Niveau"]}

        # Loop over the element in the dictionary
        for key, value in plancher.dictPlancher.items():

            # Check if the element is a support 
            if value["Appui"] == True :

                # Add a support for the corresponding plancher at the right level
                support_DEF[key] = {"Type": "Simply supported", "Position": value["Niveau"]}

        # Check if the foundations are a support in the DEF Phase 
        if fondations.caracteristics["Butee"] == True :

            # Add a support if this is the case
            support_DEF[len(support_DEF) + 1] = {"Type": "Simply supported", "Position": fondations.caracteristics["Arase inférieure"]}

        # If there are under 2 supports, raise an error
        if len(support_PROV) < 2:
            raise ValueError("Le schéma statique en phase PROVISOIRE ne comporte pas deux appuis")
        
        # If there are under 2 supports, raise an error
        if len(support_DEF) < 2:
            raise ValueError("Le schéma statique en phase DÉFINITIVE ne comporte pas deux appuis")
        
        # Trier le dictionnaire en fonction de la valeur "Niveau" 
        support_PROV = {i: d for i, d in enumerate(sorted(support_PROV.values(), key=lambda item: item["Position"]), start=1)}
        support_DEF = {i: d for i, d in enumerate(sorted(support_DEF.values(), key=lambda item: item["Position"]), start=1)}
        
        return support_PROV, support_DEF
    

    def verify_loading(self, fondations, plancher, chargement):
        # Vérifier que le chargement s'applique bien sur le voile
        # Les positions des charges ne peuvent pas être en dehors des limites du voile

        # Loop over the dictionary
        for key, value in chargement["distributed PROV"].items():

            # Si la valeur de départ de la charge est avant le début du voile, on recale le départ au début du voile
            if value["xmin"] < plancher.caracteristics["Cote PROV"]:
                value["xmin"] = plancher.caracteristics["Cote PROV"]
            
            # Si la valeur de fin de la charge est après l'Ai de la fondation, on recale la fin de la charge
            if value["xmax"] > fondations.caracteristics["Arase inférieure"]:
                value["xmax"] = fondations.caracteristics["Arase inférieure"]
        
        # Loop over the dictionary
        for key, value in chargement["distributed DEF"].items():

            # Si la valeur de départ de la charge est avant le début du voile, on recale le départ au début du voile
            if value["xmin"] < plancher.caracteristics["Cote DEF"]:
                value["xmin"] = plancher.caracteristics["Cote DEF"]
            
            # Si la valeur de fin de la charge est après l'Ai de la fondation, on recale la fin de la charge
            if value["xmax"] > fondations.caracteristics["Arase inférieure"]:
                value["xmax"] = fondations.caracteristics["Arase inférieure"]
        
        # POINT LOADS
        # Create empty list to store the keys to remove
        lst_PROV, lst_DEF = [], []

        # Loop over the dictionary
        for key, value in chargement["point PROV"].items():
            if value["Position"] > fondations.caracteristics["Arase inférieure"] or value["Position"] < plancher.caracteristics["Cote PROV"]:
                lst_PROV.append(key)
        # Remove the element of the dictionary with the keys in the list
        for i in range(len(lst_PROV)):
            chargement["point PROV"].pop(lst_PROV[i], None)

        # Loop over the dictionary
        for key, value in chargement["point DEF"].items():
            if value["Position"] > fondations.caracteristics["Arase inférieure"] or value["Position"] < plancher.caracteristics["Cote DEF"]:
                lst_DEF.append(key)
        # Remove the element of the dictionary with the keys in the list
        for i in range(len(lst_DEF)):  
            chargement["point DEF"].pop(key, None)
        
        return chargement