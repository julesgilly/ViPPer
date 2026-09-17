# import libraries
import Combinaisons
import Chargement
import Concrete
import Sollicitations
import Data
import Sol
import Schema_Statique
import Armatures
import numpy as np

import Sollicitations.Element

###############################################################################
#                 HARNAIS DE VERIFICATION PAS-A-PAS                           #
###############################################################################
# Principe :
#   - Chaque étape du calcul est suivie d'un bloc de vérifications.
#   - Renseigner les valeurs calculées à la main dans le dictionnaire
#     REFERENCES ci-dessous (remplacer None par la valeur manuelle).
#   - Pour chaque grandeur, le script affiche : valeur logiciel, valeur de
#     référence et écart en pourcentage. Tant que la référence vaut None,
#     la ligne est marquée "A REMPLIR" et affiche la valeur logiciel
#     (pratique pour savoir quoi calculer à la main).
#   - Unités : celles utilisées en interne par le logiciel (identiques à
#     celles affichées par ce script). Renseigner les références dans les
#     mêmes unités.
#   - Nota : les moments et tranchants de l'étape 7 sont des VALEURS
#     ABSOLUES (cf. BeamFEM.end_Data qui applique abs() aux min/max).

TOLERANCE_PCT = 5.0   # écart admissible (en %) entre logiciel et calcul manuel

REFERENCES = {
    # ------------------- ETAPE 1 : géométrie et caractéristiques du sol ----
    "1.1 Hauteur voile PROV (m)":                       3.7,
    "1.2 Hauteur voile DEF (m)":                        3.7,
    "1.3 Ka couche 1 (phase DEF)":                      0.49,
    "1.4 Ka couche 2 (phase DEF)":                      0.33,

    # ------------------- ETAPE 2 : contraintes du sol sur le voile ---------
    "2.1 Contrainte horiz. totale pied couche 1 DEF":   0.00882523,
    "2.2 Contrainte horiz. totale pied du voile DEF":   0.0231,
    "2.3 xmax charge sol derniere couche DEF (m)":      3.7,
    "2.4 Contrainte horiz. totale pied du voile PROV":  0.0231,

    # ------------------- ETAPE 3 : pression hydrostatique ------------------
    "3.1 Niveau d'eau relatif xmin (m)":                2.2,
    "3.2 Pression hydrostatique en pied pmax":          0.015,

    # ------------------- ETAPE 4 : surcharges ------------------------------
    "4.1 pmax surcharges PROV (Exploitation)":          0.0049,
    "4.2 pmax surcharges DEF (Exploitation)":           0.0049,

    # ------------------- ETAPE 5 : combinaisons (réparties, phase DEF) -----
    "5.1 ELU1 DEF - pmax charges Permanente":           0.031185,
    "5.2 ELU1 DEF - pmax charge EE (eau)":              0,
    "5.3 ELU2 DEF - pmax charges Exploitation":         0.005145,
    "5.4 ELSQPE DEF - pmax charge EE (eau)":            0.015,
    "5.5 Acc DEF - pmax charges Exploitation":          0.00147,
    "5.6 ELSQP DEF - pmax charges Permanente":          0.0231,

    # ------------------- ETAPE 6 : schéma statique -------------------------
    "6.1 Longueur poutre PROV (m)":                     3.7,
    "6.2 Longueur poutre DEF (m)":                      3.7,
    "6.3 Nombre d'appuis PROV":                         2,
    "6.4 Nombre d'appuis DEF":                          2,
    "6.5 Position appui 1 PROV (m)":                    0.75,
    "6.6 Position appui 1 DEF (m)":                     0.1,

    # ------------------- ETAPE 7 : sollicitations (valeurs absolues) -------
    "7 ELU1_PROV - Moment MAX (abs)":                   0,
    "7 ELU1_PROV - Moment MIN (abs)":                   0.013,
    "7 ELU1_PROV - Tranchant MAX (abs)":                0,
    "7 ELU1_PROV - Tranchant MIN (abs)":                0.033,
    "7 ELU1_PROV - Somme reactions verticales":         0.075,

    "7 ELU2_PROV - Moment MAX (abs)":                   None,
    "7 ELU2_PROV - Moment MIN (abs)":                   None,
    "7 ELU2_PROV - Tranchant MAX (abs)":                None,
    "7 ELU2_PROV - Tranchant MIN (abs)":                None,
    "7 ELU2_PROV - Somme reactions verticales":         None,

    "7 Acc_PROV - Moment MAX (abs)":                    None,
    "7 Acc_PROV - Moment MIN (abs)":                    None,
    "7 Acc_PROV - Tranchant MAX (abs)":                 None,
    "7 Acc_PROV - Tranchant MIN (abs)":                 None,
    "7 Acc_PROV - Somme reactions verticales":          None,

    "7 ELSQP_PROV - Moment MAX (abs)":                  None,
    "7 ELSQP_PROV - Moment MIN (abs)":                  None,
    "7 ELSQP_PROV - Tranchant MAX (abs)":               None,
    "7 ELSQP_PROV - Tranchant MIN (abs)":               None,
    "7 ELSQP_PROV - Somme reactions verticales":        None,

    "7 ELU1_DEF - Moment MAX (abs)":                    None,
    "7 ELU1_DEF - Moment MIN (abs)":                    None,
    "7 ELU1_DEF - Tranchant MAX (abs)":                 None,
    "7 ELU1_DEF - Tranchant MIN (abs)":                 None,
    "7 ELU1_DEF - Somme reactions verticales":          None,

    "7 ELU2_DEF - Moment MAX (abs)":                    None,
    "7 ELU2_DEF - Moment MIN (abs)":                    None,
    "7 ELU2_DEF - Tranchant MAX (abs)":                 None,
    "7 ELU2_DEF - Tranchant MIN (abs)":                 None,
    "7 ELU2_DEF - Somme reactions verticales":          None,

    "7 Acc_DEF - Moment MAX (abs)":                     None,
    "7 Acc_DEF - Moment MIN (abs)":                     None,
    "7 Acc_DEF - Tranchant MAX (abs)":                  None,
    "7 Acc_DEF - Tranchant MIN (abs)":                  None,
    "7 Acc_DEF - Somme reactions verticales":           None,

    "7 ELSQP_DEF - Moment MAX (abs)":                   None,
    "7 ELSQP_DEF - Moment MIN (abs)":                   None,
    "7 ELSQP_DEF - Tranchant MAX (abs)":                None,
    "7 ELSQP_DEF - Tranchant MIN (abs)":                None,
    "7 ELSQP_DEF - Somme reactions verticales":         None,

    "7 ELSQPE_DEF - Moment MAX (abs)":                  None,
    "7 ELSQPE_DEF - Moment MIN (abs)":                  None,
    "7 ELSQPE_DEF - Tranchant MAX (abs)":               None,
    "7 ELSQPE_DEF - Tranchant MIN (abs)":               None,
    "7 ELSQPE_DEF - Somme reactions verticales":        None,

    # ------------------- ETAPE 8 : enveloppes et chargement BN -------------
    "8 PROV face INT - Moment ELS":                     None,
    "8 PROV face INT - Moment ELU":                     None,
    "8 PROV face INT - Tranchant ELS":                  None,
    "8 PROV face INT - Tranchant ELU":                  None,
    "8 PROV face INT - Normal ELS":                     None,
    "8 PROV face INT - Normal ELU":                     None,

    "8 PROV face EXT - Moment ELS":                     None,
    "8 PROV face EXT - Moment ELU":                     None,
    "8 PROV face EXT - Tranchant ELS":                  None,
    "8 PROV face EXT - Tranchant ELU":                  None,
    "8 PROV face EXT - Normal ELS":                     None,
    "8 PROV face EXT - Normal ELU":                     None,

    "8 DEF face INT - Moment ELS":                      None,
    "8 DEF face INT - Moment ELU":                      None,
    "8 DEF face INT - Tranchant ELS":                   None,
    "8 DEF face INT - Tranchant ELU":                   None,
    "8 DEF face INT - Normal ELS":                      None,
    "8 DEF face INT - Normal ELU":                      None,

    "8 DEF face EXT - Moment ELS":                      None,
    "8 DEF face EXT - Moment ELU":                      None,
    "8 DEF face EXT - Tranchant ELS":                   None,
    "8 DEF face EXT - Tranchant ELU":                   None,
    "8 DEF face EXT - Normal ELS":                      None,
    "8 DEF face EXT - Normal ELU":                      None,

    "8 Chargement BN ELS - buton 1":                    None,
    "8 Chargement BN ELS - buton 2":                    None,
    "8 Chargement BN ELU - buton 1":                    None,
    "8 Chargement BN ELU - buton 2":                    None,
}

_resultats_tests = []


def titre(texte):
    """Affiche un en-tête de section de vérification."""
    print("\n" + "=" * 79)
    print(texte)
    print("=" * 79)


def verifier(nom, valeur_logiciel):
    """Compare une valeur du logiciel à la référence manuelle de REFERENCES
    et affiche la différence en pourcentage :
        écart (%) = 100 * (valeur logiciel - valeur référence) / valeur référence
    """
    reference = REFERENCES.get(nom)

    # Grandeur introuvable dans les résultats du logiciel (ex: type de charge absent)
    if valeur_logiciel is None:
        print(f"[ABSENT   ] {nom:52} valeur logiciel indisponible")
        _resultats_tests.append((nom, "ABSENT", None))
        return

    valeur = float(valeur_logiciel)

    # Référence non encore saisie: on affiche la valeur logiciel pour aider le calcul manuel
    if reference is None:
        print(f"[A REMPLIR] {nom:52} logiciel = {valeur:12.6g}")
        _resultats_tests.append((nom, "A REMPLIR", None))
    # Référence nulle: l'écart en % n'est pas défini, comparaison absolue
    elif reference == 0:
        statut = "OK" if abs(valeur) <= 1e-9 else "ECART"
        print(f"[{statut:9}] {nom:52} logiciel = {valeur:12.6g}   reference = 0 (comparaison absolue)")
        _resultats_tests.append((nom, statut, None))
    else:
        ecart = 100.0 * (valeur - reference) / reference
        statut = "OK" if abs(ecart) <= TOLERANCE_PCT else "ECART"
        print(f"[{statut:9}] {nom:52} logiciel = {valeur:12.6g}   reference = {reference:12.6g}   ecart = {ecart:+8.2f} %")
        _resultats_tests.append((nom, statut, ecart))


def pmax_par_charge(dict_charges, type_charge):
    """Plus grande valeur (en valeur absolue) de pmax parmi les charges
    réparties d'un type donné ('Permanente', 'Exploitation', 'EE', ...).
    Retourne None si aucune charge de ce type n'est présente."""
    valeurs = [c["pmax"] for c in dict_charges.values()
               if isinstance(c, dict) and c.get("Charge") == type_charge and "pmax" in c]
    return max(valeurs, key=abs) if valeurs else None


def bilan_tests():
    """Récapitulatif final : nombre de OK / ECART / A REMPLIR / ABSENT
    et détail des écarts dépassant la tolérance."""
    compte = {}
    for _, statut, _ecart in _resultats_tests:
        compte[statut] = compte.get(statut, 0) + 1

    titre("BILAN DES VERIFICATIONS")
    print(f"  Tolérance : ±{TOLERANCE_PCT} %")
    for statut in ("OK", "ECART", "A REMPLIR", "ABSENT"):
        if compte.get(statut):
            print(f"  {statut:10}: {compte[statut]}")

    ecarts = [(nom, ecart) for nom, statut, ecart in _resultats_tests if statut == "ECART"]
    if ecarts:
        print("\n  Détail des écarts dépassant la tolérance :")
        for nom, ecart in ecarts:
            if ecart is None:
                print(f"   - {nom}")
            else:
                print(f"   - {nom}: {ecart:+.2f} %")

###############################################################################
#                        FIN DU HARNAIS DE VERIFICATION                       #
###############################################################################

# Data project
nameProj = "ISLE ADAM"
categorie = "Catégorie A: habitation, zones résidentielles"
nameIng = "Jules GILLY"
largeurPasse = 3 # m
hauteurPasse = 2 # m
refCote = 29.80 # NGF

fck = "C25/30"
classe_exposition = "XC2"
enrobage = 4 # cm
density = 25 # kN/m3
Module_DEF = 10000 # MPa
Module_PROV = 20000 # MPa
coeff_securite_beton = 1.5
Coeff_equivalence = 15

fyk = 500 # MPa
palier = "Horizontal"
classe = "B"
coeff_securite_acier = 1.15
Module = 200000 # MPa

typeCuvelage = "Revêtement par Imperméabilisation"
faceCuvelage = "Face Intérieure"
PrecautionCuvelage = True
wOuvFiss = 0.2 # mm
dureeOuvFiss = "Longue durée"

presenceEau = True
waterLevel = 27.60 # NGF
typeEau = "EE"
waterDensity = 10 # kN/m3

listeSol = [["Remblais", 29.80, 28.80, "Sables", 0, 0, 20, 20, 18, None, None, None], ["Alluvions anciennes", 28.80, 20.80, "Sables", 0, 0, 30, 30, 19, None, None, None]]
computeTassement = False
typeInterface = "Interface Frottante"
tauxSolELS = 0.55 # MPa
tauxSemButELS = 0.3 # MPa

classeServiceBois = "Classe de service 3"
dureeActionBois = "Moyen Terme"
Coeff_securite_bois = 1.3
classeBois = "C18"
facteurRelatifBois = 0.2

coeffThermique = 0.000010 # K-1
deltaTemperature = 20 # °C

critereFleche = "L/250"
valeurFleche = None

coeffG = 1.35
coeffQ = 1.5

longueurVoile = 9 # m
epaisseurVoile = 0.25 # m
coteSupVoile_DEF = 29.80 # NGF
coteSupVoile_PROV = 29.80 # NGF
listePlancher = [["Plancher", 29.70, 0.25, True], ["Plancher", 26.45, 0.3, True]]

torseurCharges = [["Permanente", 29.80, "Vertical", 270], ["Exploitation", 29.80, "Vertical", 30]]
listeSurcharges = [["Pression uniforme infinie contigüe à l'écran", "Phase définitive ET provisoire", 10, None, None, None, None, None, None, None, None, None]]

modeFondation = "Fondations superficielles (semelle excentrée)"
AiFondation = 26.10 # NGF
largeurFondation = 0.6 # m
hauteurFondation = 0.5 # m
debordFondation = 0 # m
enrobageFondation = 4 # cm
typeFondation = "Coulée pleine fouille"
isButeeFondation = False
portanceELU = 1.4
glissementELU = 1.1
portanceELS = 2.3
modelePortance = 1.2
modeleGlissement = 1.1

listeButon = [[1, 29.05, 3, 3, 3, "Incliné", 45, 3.20, None, "Bois", "Diamètre: 25cm", "Corbeau béton"], [2, 27.10, 3, 3, 3, "Incliné", 62, 3.20, None, "Bois", "Diamètre: 25cm", "Corbeau béton"]]
listeSemButon = [[[1,2], 1.20, 1.20, 0.25]]

listeLierne = [[1, "Béton dans l'épaisseur", 5, 0, 0], [2, "Béton dans l'épaisseur", 5, 0, 0]]

# Test
# import modules
import time
t1 = time.time()

#IMPORT DATA
projet = Data.Projet(nameProj, categorie, nameIng, largeurPasse, hauteurPasse, refCote)
acier = Data.Acier(fyk, palier, classe, coeff_securite_acier, Module)
beton = Data.Beton(density, fck, classe_exposition, enrobage, coeff_securite_beton, Module_DEF, Module_PROV, Coeff_equivalence)
cuvelage = Data.Cuvelage(typeCuvelage, faceCuvelage, PrecautionCuvelage, wOuvFiss, dureeOuvFiss)
eau = Data.Eau(presenceEau, waterLevel, typeEau, waterDensity, refCote)
bois = Data.Bois(classeServiceBois, dureeActionBois, Coeff_securite_bois, classeBois, facteurRelatifBois)
fleche = Data.Fleche(critereFleche, valeurFleche)
lierne = Data.Lierne(listeLierne)
combinaison = Data.Combinaison(coeffG, coeffQ)
plancher = Data.Plancher(listePlancher, refCote, longueurVoile, epaisseurVoile, coteSupVoile_DEF, coteSupVoile_PROV)
chargement = Data.Chargement(torseurCharges, refCote)
fondation = Data.Fondation(modeFondation, AiFondation, largeurFondation, hauteurFondation, debordFondation, enrobageFondation, typeFondation, isButeeFondation, portanceELU, glissementELU, portanceELS, modelePortance, modeleGlissement, refCote)
surcharges = Data.Surcharges(listeSurcharges)
butons = Data.Buton(listeButon, listeSemButon, refCote)
sol = Data.SolInfo(listeSol, computeTassement, typeInterface, tauxSolELS, tauxSemButELS, refCote)

wallLength_PROV = fondation.caracteristics['Arase inférieure'] - plancher.caracteristics['Cote PROV']
wallLength_DEF = fondation.caracteristics['Arase inférieure'] - plancher.caracteristics['Cote DEF']

# Chargement SOL
solPROV = Sol.caracteristiques(sol.SolInfo, fondation.caracteristics['Arase inférieure']).sol_PROV
solDEF = Sol.caracteristiques(sol.SolInfo, fondation.caracteristics['Arase inférieure']).sol_DEF
eau_sol = eau.eau_sol

###############################################################################
# VERIFICATION - ETAPE 1 : géométrie et caractéristiques du sol
titre("ETAPE 1 - GEOMETRIE ET CARACTERISTIQUES DU SOL")
verifier("1.1 Hauteur voile PROV (m)", wallLength_PROV)
verifier("1.2 Hauteur voile DEF (m)", wallLength_DEF)
Ka_DEF = Sol._sol.K_a(solDEF)
verifier("1.3 Ka couche 1 (phase DEF)", Ka_DEF.get(1, {}).get("Ka"))
verifier("1.4 Ka couche 2 (phase DEF)", Ka_DEF.get(2, {}).get("Ka"))
###############################################################################

contraintes_solPROV = Sol._sol.contraintes_sol(solPROV, eau_sol)
chargementSOL_PROV = Sol._sol.endData(solPROV, contraintes_solPROV)

contraintes_solDEF = Sol._sol.contraintes_sol(solDEF, eau_sol)
chargementSOL_DEF = Sol._sol.endData(solDEF, contraintes_solDEF)

###############################################################################
# VERIFICATION - ETAPE 2 : contraintes du sol sur le voile
titre("ETAPE 2 - CONTRAINTES DU SOL SUR LE VOILE")
derniere_couche_DEF = max(contraintes_solDEF)
derniere_couche_PROV = max(contraintes_solPROV)
verifier("2.1 Contrainte horiz. totale pied couche 1 DEF",
         contraintes_solDEF[1]["Contraintes horizontales totales"][-1])
verifier("2.2 Contrainte horiz. totale pied du voile DEF",
         contraintes_solDEF[derniere_couche_DEF]["Contraintes horizontales totales"][-1])
verifier("2.3 xmax charge sol derniere couche DEF (m)",
         chargementSOL_DEF[derniere_couche_DEF]["xmax"])
verifier("2.4 Contrainte horiz. totale pied du voile PROV",
         contraintes_solPROV[derniere_couche_PROV]["Contraintes horizontales totales"][-1])
###############################################################################

# Chargement EAU
chargementEAU = Sol._eau.pression_hydrostatique(eau.caracteristics, wallLength_DEF)

###############################################################################
# VERIFICATION - ETAPE 3 : pression hydrostatique
titre("ETAPE 3 - PRESSION HYDROSTATIQUE")
verifier("3.1 Niveau d'eau relatif xmin (m)", chargementEAU["xmin"])
verifier("3.2 Pression hydrostatique en pied pmax", chargementEAU["pmax"])
###############################################################################

# Chargement AVOISINANT
chargementAVOISINANT = chargement.caracteristics

chargementSURCHARGES_PROV, chargementSURCHARGES_DEF = Sol.surcharges.chargement_surcharges(surcharges.caracteristics, solPROV, solDEF, wallLength_PROV, wallLength_DEF)

###############################################################################
# VERIFICATION - ETAPE 4 : surcharges
titre("ETAPE 4 - SURCHARGES")
verifier("4.1 pmax surcharges PROV (Exploitation)", pmax_par_charge(chargementSURCHARGES_PROV, "Exploitation"))
verifier("4.2 pmax surcharges DEF (Exploitation)", pmax_par_charge(chargementSURCHARGES_DEF, "Exploitation"))
###############################################################################

# CHARGEMENT GLOBAL VPP PROV
chargementGLOBAL_p_PROV, chargementGLOBAL_P_PROV = Chargement._chargement.get_chargement_Voile(chargementSURCHARGES_PROV, {}, chargementSOL_PROV, chargementAVOISINANT)

# CHARGEMENT GLOBAL VPP DEF
chargementGLOBAL_p_DEF, chargementGLOBAL_P_DEF = Chargement._chargement.get_chargement_Voile(chargementSURCHARGES_DEF, chargementEAU, chargementSOL_DEF, chargementAVOISINANT)

# CHARGEMENT GLOBAL FONDATIONS VPP PROV
chargementFondationsGLOBAL_p_PROV, chargementFondationsGLOBAL_P_PROV = Chargement._chargement.get_chargement_Fondations(chargementSURCHARGES_PROV, chargementAVOISINANT)

# CHARGEMENT GLOBAL FONDATIONS VPP DEF
chargementFondationsGLOBAL_p_DEF, chargementFondationsGLOBAL_P_DEF = Chargement._chargement.get_chargement_Fondations(chargementSURCHARGES_PROV, chargementAVOISINANT)

# COMBINAISONS VPP PHASE PROV
#DISTRIBUTED LOADS
ELU1_p_PROV = Combinaisons._combinaisons.ELU1_voile(chargementGLOBAL_p_PROV, combinaison.caracteristics["G"], combinaison.caracteristics["Q"])
ELU2_p_PROV = Combinaisons._combinaisons.ELU2_voile(chargementGLOBAL_p_PROV, combinaison.caracteristics["G"], combinaison.caracteristics["Q"], projet.caracteristics["Catégorie"])
Acc_p_PROV = Combinaisons._combinaisons.Acc_voile(chargementGLOBAL_p_PROV, projet.caracteristics["Catégorie"])
ELSQP_p_PROV = Combinaisons._combinaisons.ELS_QP_voile(chargementGLOBAL_p_PROV)

#POINT LOADS
ELU1_P_PROV = Combinaisons._combinaisons.ELU1_voile(chargementGLOBAL_P_PROV, combinaison.caracteristics["G"], combinaison.caracteristics["Q"])
ELU2_P_PROV = Combinaisons._combinaisons.ELU2_voile(chargementGLOBAL_P_PROV, combinaison.caracteristics["G"], combinaison.caracteristics["Q"], projet.caracteristics["Catégorie"])
Acc_P_PROV = Combinaisons._combinaisons.Acc_voile(chargementGLOBAL_P_PROV, projet.caracteristics["Catégorie"])
ELSQP_P_PROV = Combinaisons._combinaisons.ELS_QP_voile(chargementGLOBAL_P_PROV)

# COMBINAISONS VPP PHASE DEF
#DISTRIBUTED LOADS
ELU1_p_DEF = Combinaisons._combinaisons.ELU1_voile(chargementGLOBAL_p_DEF, combinaison.caracteristics["G"], combinaison.caracteristics["Q"])
ELU2_p_DEF = Combinaisons._combinaisons.ELU2_voile(chargementGLOBAL_p_DEF, combinaison.caracteristics["G"], combinaison.caracteristics["Q"], projet.caracteristics["Catégorie"])
Acc_p_DEF = Combinaisons._combinaisons.Acc_voile(chargementGLOBAL_p_DEF, projet.caracteristics["Catégorie"])
ELSQPE_p_DEF = Combinaisons._combinaisons.ELS_QPE_voile(chargementGLOBAL_p_DEF, projet.caracteristics["Catégorie"])
ELSQP_p_DEF = Combinaisons._combinaisons.ELS_QP_voile(chargementGLOBAL_p_DEF)

#POINT LOADS
ELU1_P_DEF = Combinaisons._combinaisons.ELU1_voile(chargementGLOBAL_P_DEF, combinaison.caracteristics["G"], combinaison.caracteristics["Q"])
ELU2_P_DEF = Combinaisons._combinaisons.ELU2_voile(chargementGLOBAL_P_DEF, combinaison.caracteristics["G"], combinaison.caracteristics["Q"], projet.caracteristics["Catégorie"])
Acc_P_DEF = Combinaisons._combinaisons.Acc_voile(chargementGLOBAL_P_DEF, projet.caracteristics["Catégorie"])
ELSQPE_P_DEF = Combinaisons._combinaisons.ELS_QPE_voile(chargementGLOBAL_P_DEF, projet.caracteristics["Catégorie"])
ELSQP_P_DEF = Combinaisons._combinaisons.ELS_QP_voile(chargementGLOBAL_P_DEF)

###############################################################################
# VERIFICATION - ETAPE 5 : combinaisons (charges réparties, phase DEF)
# Chaque test compare le pmax le plus grand (en valeur absolue) parmi les
# charges d'un type donné, après application des coefficients de combinaison.
titre("ETAPE 5 - COMBINAISONS (charges reparties, phase DEF)")
verifier("5.1 ELU1 DEF - pmax charges Permanente", pmax_par_charge(ELU1_p_DEF, "Permanente"))
verifier("5.2 ELU1 DEF - pmax charge EE (eau)", pmax_par_charge(ELU1_p_DEF, "EE"))
verifier("5.3 ELU2 DEF - pmax charges Exploitation", pmax_par_charge(ELU2_p_DEF, "Exploitation"))
verifier("5.4 ELSQPE DEF - pmax charge EE (eau)", pmax_par_charge(ELSQPE_p_DEF, "EE"))
verifier("5.5 Acc DEF - pmax charges Exploitation", pmax_par_charge(Acc_p_DEF, "Exploitation"))
verifier("5.6 ELSQP DEF - pmax charges Permanente", pmax_par_charge(ELSQP_p_DEF, "Permanente"))
###############################################################################

# CHARGEMENT VPP
# ELU 1
chargement_Voile_ELU1 = {"distributed PROV": ELU1_p_PROV,
                         "point PROV": ELU1_P_PROV,
                         "distributed DEF": ELU1_p_DEF,
                         "point DEF":  ELU1_P_DEF}
schema_statique_ELU1_PROV = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_ELU1).schema_statique_PROV
schema_statique_ELU1_DEF = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_ELU1).schema_statique_DEF

# ELU 2
chargement_Voile_ELU2 = {"distributed PROV": ELU2_p_PROV,
                         "point PROV": ELU2_P_PROV,
                         "distributed DEF": ELU2_p_DEF,
                         "point DEF":  ELU2_P_DEF}
schema_statique_ELU2_PROV = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_ELU2).schema_statique_PROV
schema_statique_ELU2_DEF = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_ELU2).schema_statique_DEF

# ACC
chargement_Voile_Acc = {"distributed PROV": Acc_p_PROV,
                         "point PROV": Acc_P_PROV,
                         "distributed DEF": Acc_p_DEF,
                         "point DEF":  Acc_P_DEF}
schema_statique_Acc_PROV = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_Acc).schema_statique_PROV
schema_statique_Acc_DEF = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_Acc).schema_statique_DEF

# ELSQP
chargement_Voile_ELSQP = {"distributed PROV": ELSQP_p_PROV,
                         "point PROV": ELSQP_P_PROV,
                         "distributed DEF": ELSQP_p_DEF,
                         "point DEF":  ELSQP_P_DEF}
schema_statique_ELSQP_PROV = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_ELSQP).schema_statique_PROV
schema_statique_ELSQP_DEF = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_ELSQP).schema_statique_DEF

# ELSQPE
chargement_Voile_ELSQPE = {"distributed PROV": {},
                           "point PROV": {},
                           "distributed DEF": ELSQPE_p_DEF,
                           "point DEF":  ELSQPE_P_DEF}
schema_statique_ELSQPE_PROV = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_ELSQPE).schema_statique_PROV
schema_statique_ELSQPE_DEF = Schema_Statique._schema(fondation, plancher, beton, butons, chargement_Voile_ELSQPE).schema_statique_DEF

###############################################################################
# VERIFICATION - ETAPE 6 : schéma statique
titre("ETAPE 6 - SCHEMA STATIQUE")
verifier("6.1 Longueur poutre PROV (m)", schema_statique_ELU1_PROV["length"])
verifier("6.2 Longueur poutre DEF (m)", schema_statique_ELU1_DEF["length"])
verifier("6.3 Nombre d'appuis PROV", len(schema_statique_ELU1_PROV["supports"]))
verifier("6.4 Nombre d'appuis DEF", len(schema_statique_ELU1_DEF["supports"]))
verifier("6.5 Position appui 1 PROV (m)", schema_statique_ELU1_PROV["supports"][1]["Position"])
verifier("6.6 Position appui 1 DEF (m)", schema_statique_ELU1_DEF["supports"][1]["Position"])
###############################################################################

# SOLLICITATIONS
# PHASE PROVISOIRE
# ELU 1
elt = Sollicitations.element(schema_statique_ELU1_PROV, "ELU1_PROV")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
sollicitations_ELU1_PROV = Sollicitations.BeamFEM(elementInfo, problemData, FEData)

# ELU 2
elt = Sollicitations.element(schema_statique_ELU2_PROV, "ELU2_PROV")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
sollicitations_ELU2_PROV = Sollicitations.BeamFEM(elementInfo, problemData, FEData)

# ACC
elt = Sollicitations.element(schema_statique_Acc_PROV, "Acc_PROV")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
sollicitations_Acc_PROV = Sollicitations.BeamFEM(elementInfo, problemData, FEData)

# ELSQP
elt = Sollicitations.element(schema_statique_ELSQP_PROV, "ELSQP_PROV")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
sollicitations_ELSQP_PROV = Sollicitations.BeamFEM(elementInfo, problemData, FEData)

sollicitations_ELS_PROV = [sollicitations_ELSQP_PROV.endDict]
sollicitations_ELU_PROV = [sollicitations_ELU1_PROV.endDict, sollicitations_ELU2_PROV.endDict, sollicitations_Acc_PROV.endDict]

# PHASE DEFINITIVE
# ELU 1
elt = Sollicitations.element(schema_statique_ELU1_DEF, "ELU1_DEF")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
sollicitations_ELU1_DEF = Sollicitations.BeamFEM(elementInfo, problemData, FEData)
"""
Vérification effectué avec RDM6 pour le cas ELU1_DEF
Résultats identiques: OK
"""

# ELU 2
elt = Sollicitations.element(schema_statique_ELU2_DEF, "ELU2_DEF")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
sollicitations_ELU2_DEF = Sollicitations.BeamFEM(elementInfo, problemData, FEData)

# ACC
elt = Sollicitations.element(schema_statique_Acc_DEF, "Acc_DEF")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
sollicitations_Acc_DEF = Sollicitations.BeamFEM(elementInfo, problemData, FEData)

# ELSQP
elt = Sollicitations.element(schema_statique_ELSQP_DEF, "ELSQP_DEF")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
sollicitations_ELSQP_DEF = Sollicitations.BeamFEM(elementInfo, problemData, FEData)

# ELSQPE
elt = Sollicitations.element(schema_statique_ELSQPE_DEF, "ELSQPE_DEF")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
sollicitations_ELSQPE_DEF = Sollicitations.BeamFEM(elementInfo, problemData, FEData)

sollicitations_ELS_DEF = [sollicitations_ELSQP_DEF.endDict, sollicitations_ELSQPE_DEF.endDict]
sollicitations_ELU_DEF = [sollicitations_ELU1_DEF.endDict, sollicitations_ELU2_DEF.endDict, sollicitations_Acc_DEF.endDict]

###############################################################################
# VERIFICATION - ETAPE 7 : sollicitations par combinaison
# Rappel: BeamFEM.end_Data applique abs() aux min/max, on compare donc des
# valeurs ABSOLUES. La somme des réactions verticales doit être égale au
# total des charges appliquées (contrôle d'équilibre global).
titre("ETAPE 7 - SOLLICITATIONS (valeurs ABSOLUES)")
_cas_fem = [("ELU1_PROV", sollicitations_ELU1_PROV),
            ("ELU2_PROV", sollicitations_ELU2_PROV),
            ("Acc_PROV", sollicitations_Acc_PROV),
            ("ELSQP_PROV", sollicitations_ELSQP_PROV),
            ("ELU1_DEF", sollicitations_ELU1_DEF),
            ("ELU2_DEF", sollicitations_ELU2_DEF),
            ("Acc_DEF", sollicitations_Acc_DEF),
            ("ELSQP_DEF", sollicitations_ELSQP_DEF),
            ("ELSQPE_DEF", sollicitations_ELSQPE_DEF)]
for _nom_cas, _fem in _cas_fem:
    verifier(f"7 {_nom_cas} - Moment MAX (abs)", _fem.endDict["Moment MAX"])
    verifier(f"7 {_nom_cas} - Moment MIN (abs)", _fem.endDict["Moment MIN"])
    verifier(f"7 {_nom_cas} - Tranchant MAX (abs)", _fem.endDict["Tranchant MAX"])
    verifier(f"7 {_nom_cas} - Tranchant MIN (abs)", _fem.endDict["Tranchant MIN"])
    verifier(f"7 {_nom_cas} - Somme reactions verticales", float(np.sum(_fem.verticalreaction)))
###############################################################################

# Transform the sollicitations for the computation
sollicitations_VPP = Sollicitations.Output(sollicitations_ELS_PROV, sollicitations_ELU_PROV, sollicitations_ELS_DEF, sollicitations_ELU_DEF, chargementFondationsGLOBAL_P_PROV, chargementFondationsGLOBAL_P_DEF, combinaison.caracteristics)

###############################################################################
# VERIFICATION - ETAPE 8 : enveloppes de sollicitations et chargement des BN
titre("ETAPE 8 - ENVELOPPES ET CHARGEMENT DES LIERNES (BN)")
_faces = [("PROV face INT", sollicitations_VPP.sollicitationsVoiles_PROV_faceINT),
          ("PROV face EXT", sollicitations_VPP.sollicitationsVoiles_PROV_faceEXT),
          ("DEF face INT", sollicitations_VPP.sollicitationsVoiles_DEF_faceINT),
          ("DEF face EXT", sollicitations_VPP.sollicitationsVoiles_DEF_faceEXT)]
for _nom_face, _enveloppe in _faces:
    for _grandeur in ("Moment ELS", "Moment ELU", "Tranchant ELS", "Tranchant ELU", "Normal ELS", "Normal ELU"):
        verifier(f"8 {_nom_face} - {_grandeur}", _enveloppe[_grandeur])

verifier("8 Chargement BN ELS - buton 1", sollicitations_VPP.chargementBN_ELS.get(1, {}).get("pmax"))
verifier("8 Chargement BN ELS - buton 2", sollicitations_VPP.chargementBN_ELS.get(2, {}).get("pmax"))
verifier("8 Chargement BN ELU - buton 1", sollicitations_VPP.chargementBN_ELU.get(1, {}).get("pmax"))
verifier("8 Chargement BN ELU - buton 2", sollicitations_VPP.chargementBN_ELU.get(2, {}).get("pmax"))

# Récapitulatif final
bilan_tests()
###############################################################################

# Compute time
t2 = time.time()
print(f"The computation took: {t2 - t1: .2f} seconds")
