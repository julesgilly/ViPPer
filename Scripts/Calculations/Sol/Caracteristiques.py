"""
Developed by Jules GILLY in November 2022 for a personal use
This file forms the class to transform the data from the user
    This files works with the class 'Sol'

SolInfo (dictionary) needs to have the following form:
    - SolInfo: Nested dictionaries containing for each layer: the name of the layer, the upper level, the lower level, the type of soil, 
                                                                               cu, c*, phi_u, phi*, gamma, pl*, Em and alpha
            SolInfo = { 1: {'Nom de la couche': ,
                        'Cote supérieure': ,
                        'Cote inférieure': ,
                        'Type de sol': ,
                        'Cohésion court terme': ,
                        'Cohésion long terme': ,
                        'Angle de frottement court terme': ,
                        'Angle de frottement long terme': ,
                        'Masse volumique': ,
                        'Pression limite': ,
                        'Module pressiométrique Ménard': ,
                        'Coefficient rhéologique': }
                    2: { ... 
                   }
            }

Output: 
    - 2 dictionaries for each phase of the project (i.e: PROV and DEF) with the followinf forms:
        sol_xxxx= { 1: {'Nom de la couche': ,
                        'Cote supérieure': ,
                        'Cote inférieure': ,
                        'Cohésion': ,
                        'Angle de frottement': ,
                        'Masse volumique': ,
                        'Liste abscisses':
                }
            }
        where c and phi corresponds to the "cohésion" and "angle de frottement" to the corresponding phase (DEF or PROV)
        where 'Liste abscisses' is a list a values from 'Cote supérieure' to 'Cote inférieure' with an increment of 0.01

Nota: Always use relative coordinates - which means that 'cote supérieure' is smaller than 'cote inférieure'
"""
class caracteristiques(object):
    def __init__(self, SolInfo, AiFondation):
        self.main(SolInfo, AiFondation)

    def main(self, SolInfo, AiFondation):
        # Define miscellaneous variables
        sol_DEF, sol_PROV = {}, {}

        # Loop over the number of soil layers
        for sol_id, sol_info in SolInfo.items():
            
            # Verify if the inferior level of the layer is above the wall height
            if sol_info['Cote inférieure'] > AiFondation:
                cote_inf = AiFondation
            else:
                cote_inf = sol_info['Cote inférieure']

            # Verify that if the superior level of the layer is above the wall height, you remove the layer from the calculation
            if sol_info['Cote supérieure'] > AiFondation:
                break

            sol_DEF[sol_id] = {'Nom de la couche': sol_info['Nom de la couche'],
                               'Cote supérieure': sol_info['Cote supérieure'],
                               'Cote inférieure': cote_inf,
                               'Cohésion': sol_info['Cohésion long terme'],
                               'Angle de frottement': sol_info['Angle de frottement long terme'],
                               'Masse volumique': sol_info['Masse volumique'],
                               'Liste abscisses': caracteristiques.creation_liste_abscisse(0.01, sol_info['Cote supérieure'], cote_inf)            
            }

            sol_PROV[sol_id] = {'Nom de la couche': sol_info['Nom de la couche'],
                               'Cote supérieure': sol_info['Cote supérieure'],
                               'Cote inférieure': cote_inf,
                               'Cohésion': sol_info['Cohésion court terme'],
                               'Angle de frottement': sol_info['Angle de frottement court terme'],
                               'Masse volumique': sol_info['Masse volumique'],
                               'Liste abscisses': caracteristiques.creation_liste_abscisse(0.01, sol_info['Cote supérieure'], cote_inf)          
            }

        # Store values
        self.sol_DEF = sol_DEF
        self.sol_PROV = sol_PROV

    @staticmethod
    def creation_liste_abscisse(pas, debut, fin):
        longueur = fin - debut
        # round() et non int(): int(0.29/0.01) == 28 par erreur d'arrondi flottant
        nb_points = round(longueur / pas)
        Liste = [debut]
        for i in range(1, nb_points + 1):
            Liste.append(round(Liste[i - 1] + pas, 2))
        return Liste