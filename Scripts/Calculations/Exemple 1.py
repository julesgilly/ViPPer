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

contraintes_solPROV = Sol._sol.contraintes_sol(solPROV, eau_sol)
chargementSOL_PROV = Sol._sol.endData(solPROV, contraintes_solPROV)

contraintes_solDEF = Sol._sol.contraintes_sol(solDEF, eau_sol)
chargementSOL_DEF = Sol._sol.endData(solDEF, contraintes_solDEF)

# Chargement EAU
chargementEAU = Sol._eau.pression_hydrostatique(eau.caracteristics, wallLength_DEF)

# Chargement AVOISINANT
chargementAVOISINANT = chargement.caracteristics

chargementSURCHARGES_PROV, chargementSURCHARGES_DEF = Sol.surcharges.chargement_surcharges(surcharges.caracteristics, solPROV, solDEF, wallLength_PROV, wallLength_DEF)

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

# Transform the sollicitations for the computation
sollicitations_VPP = Sollicitations.Output(sollicitations_ELS_PROV, sollicitations_ELU_PROV, sollicitations_ELS_DEF, sollicitations_ELU_DEF, chargementFondationsGLOBAL_P_PROV, chargementFondationsGLOBAL_P_DEF, combinaison.caracteristics)

print(sollicitations_VPP.sollicitationsVoiles_PROV_faceINT, sollicitations_VPP.chargementBN_ELU)
# Compute time
t2 = time.time()
print(f"The computation took: {t2 - t1: .2f} seconds")   