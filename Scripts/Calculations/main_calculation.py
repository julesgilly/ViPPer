import Combinaisons
import Chargement
import Concrete
import Sollicitations
import Data
import Sol
import Armatures
import numpy as np

# Test - combinaisons 
#print(Combinaisons._combinaisons.get_Psy2("C"))

# Test - carcatéristiques béton
#print(Concrete._concrete.n(25))


# Test - sollicitations sur voile
BeamInfo = {"length": 3, # m
            "width": 1,  # m
            "height": 0.25, # m
            "Young's Modulus": 10000, # kPa
            "supports": {1: {'Type':"simply supported", 'Position': 0}, 2: {'Type': "roller", 'Position': 3}}, # position in m
            "distributedLoads": {1: {'Type': 'uniform', 'Charge': 'Exploitation', 'xmin': 0.0, 'xmax': 1.0, 'pmin': 0.005148051263939871, 'pmax': 0.005148051263939871}, 2: {'Type': 'uniform', 'Charge': 'Exploitation', 'xmin': 1.0, 'xmax': 3.7, 'pmin': 0.0035000000000000005, 'pmax': 0.0035000000000000005}, 3: {'Type': 'linear', 'Charge': 'EE', 'xmin': 2.2, 'xmax': 3.7, 'pmin': 0, 'pmax': 0}, 4: {'Type': 'linear', 'Charge': 'Permanente', 'xmin': 0.0, 'xmax': 1.0, 'pmin': 0.0, 'pmax': 0.011914061496546563}, 5: {'Type': 'linear', 'Charge': 'Permanente', 'xmin': 1.0, 'xmax': 3.7, 'pmin': 0.008100000000000005, 'pmax': 0.03118500000000001}},
            "pointLoads": {}  # loads in kPa
}

elt = Sollicitations.element(BeamInfo, "ELU2_DEF")
elementInfo = elt.elementInfo
problemData = elt.problemData
FEData = elt.FEData
Sollicitations.BeamFEM(elementInfo, problemData, FEData)

#Tests class "projet"
projet = Data.Projet("Projet Test", "Catégorie A: habitation, zones résidentielles", "Jules GILLY", 0, 1, 100)

# Example: how to use the sol class
sol1 = { 1: {'Nom de la couche': "name1",
                        'Cote supérieure': 0,
                        'Cote inférieure': 0.9,
                        'Type de sol': "Argiles",
                        'Cohésion court terme': 0,
                        'Cohésion long terme': 0,
                        'Angle de frottement court terme': 30,
                        'Angle de frottement long terme': 30,
                        'Masse volumique': 22,
                        'Pression limite': 1,
                        'Module pressiométrique Ménard': 1,
                        'Coefficient rhéologique': 1},
                    2: { 'Nom de la couche': "name2",
                        'Cote supérieure': 0.9,
                        'Cote inférieure': 3.0,
                        'Type de sol': "Limons",
                        'Cohésion court terme': 0,
                        'Cohésion long terme': 0,
                        'Angle de frottement court terme': 30,
                        'Angle de frottement long terme': 30,
                        'Masse volumique': 22,
                        'Pression limite': 1,
                        'Module pressiométrique Ménard': 1,
                        'Coefficient rhéologique': 1}
                   }

eau = {'Présence eau': True,
       'Niveau eau': 5,
       'Masse volumique': 10}


# Test - contraintes de sol
"""
Ka = Sol._sol.K_a(sol_DEF)
sigma = Sol._sol.sigma_verticale_tot(sol_DEF)
u = Sol._sol.pression_hydrostatique(sol_DEF, eau)
sigmaV = Sol._sol.sigma_verticale(sigma, u)
sigmah = Sol._sol.sigma_horizontale(sol_DEF, sigmaV, Ka)
sigmaH = Sol._sol.sigma_horizontale_tot(sigmah, u)

print(Sol._sol.contraintes_sol(sol_DEF, eau))
print(Sol._sol.endData(sol_DEF, sigmaH))"""

# Test - surcharges
"""angleFrottementmoyen = Sol.surcharges.moyenne_angle_frottement(sol_DEF)
uniform = Sol.surcharges.pl_uniforme_d(1, 0, sol_DEF, wallLength)
lineique = Sol.surcharges.pl_lineique_d(1, 1, sol_DEF, wallLength)
limi_uniform = Sol.surcharges.pl_uniforme_limitee(1, 1, 1, sol_DEF, wallLength)
contigue_uniform = Sol.surcharges.pression_contigue(1, sol_DEF)"""
aire_uniform = Sol.surcharges.pl_uniforme_limitee(0.85, 1, 1, sol_DEF, wallLength)
"""risberme = Sol.surcharges.risberme({'height':2, 'length':1, 'inclination angle':45, 'density':25, 'c':10, 'friction angle':20}, wallLength)
talus = Sol.surcharges.talus(1, {'height': 2, 'distance': 1, 'density': 25, 'c': 15, 'friction angle': 21}, sol_DEF, wallLength)
print(talus)"""

# Test - enrobage
#print(Concrete._concrete.enrobage_mini(50, "XC3"))

# Test classes data
acier = Data.Acier(500, "Horizontal", "B", 1.15, 200000)
beton = Data.Beton(25, "C25/30", "XC1", 4, 1.5, 10000, 20000, 15)
cuvelage = Data.Cuvelage(None, "Face Intérieure", False, 0.003, "Longue durée")
eau = Data.Eau(True, 98, "EE", 10, 100)
bois = Data.Bois("Classe de service 1", "Moyen terme", 1.30, "C24", 0.2)
fleche = Data.Fleche("Autres (Valeur à préciser)", 3)
listeLierne =[[2, "Béton dans l'épaisseur", 4, None, None], [1, "Béton en sur-épaisseur extérieure", 5, 60,20]]
lierne = Data.Lierne(listeLierne)
listePlancher = [["Dallage", 5, 0.2, True], ["Plancher", 2, 0.23, False]]
plancher = Data.Plancher(listePlancher, 0, 15, 0.25, 0, 1)
section = Data.Section(1, 1, 0.05, False, None, None)
torseurCharges = [["Permanente", 145, "Vertical", 1], ["Exploitation", 148, "Moment", 2]]
chargement = Data.Chargement(torseurCharges, 150)
fondation = Data.Fondation("Fondations superficielles (semelle excentrée)",150,0.5,0.8,0,4,"Coulée pleine fouille",True, 1, 1, 1, 1, 1, 160)
listeSurcharges = [["Talus", "Phase définitive uniquement", 2, 0.3, 4, 50, 600, 45, 800, 90, 100, 11], ["Pression uniforme avec largeur limitée", "Phase définitive et provisoire", 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
surcharges = Data.Surcharges(listeSurcharges)
listeButon = [[2, 150, 2, 0.5, 0.5, "Incliné", 60, 2, 4, "Bois", "Diamètre: 25cm", "Corbeau béton"], [1, 152, 2, 1, 1, "Incliné", 41, 2, 4, "Bois", "Diamètre: 25cm", "Corbeau béton"]]
listeSemBut = [[[2, 1], 1, 1, 1]]
butons = Data.Buton(listeButon, listeSemBut, 155)
listeSol = [["Couche 2", 80, 76.6, "Limons", 10, 10, 30, 30, 20, 1, 1, 1],["Couche 1", 80.9, 80, "Argiles", 0, 0, 30, 30, 20, 1, 1, 1]]
sol = Data.SolInfo(listeSol, True, "Interface Frottante", 0.4, 0.2, 100)
solDEF = Sol.caracteristiques(sol.SolInfo).sol_DEF
dict_surcharges = Sol.surcharges.chargement_surcharges(surcharges.caracteristics, solDEF, 5)

# Test class 'Flexion'

section = {"Largeur": 0.40,
                           "Hauteur": 0.70,
                           "d": 0.64, 
                           "Calcul en T": False,
                           "Largeur de la table": None,
                           "Hauteur de la table": None
                            }


sollicitations = {"Moment ELS": -1,
                  "Moment ELS QP": -1,
                  "Moment ELU": -1.35,
                                 "Tranchant ELS": 1,
                                 "Tranchant ELU": 1,
                                 "Normal ELS": 1,
                                 "Normal ELU": 0.653
                                 }

armatures = Armatures.Flexion.contrainte_aciers_tendus(beton.caracteristics, acier.caracteristics, cuvelage.caracteristics, eau.caracteristics, 0.12)

theta  = 45
alpha = 90

fissures = {"Limite": 0.003,  
              "Charges": "Longue" }  

armatures = {"As1": 46.24, "As2":0, "Diametre": {"1": [23, 16]}}

#print(Armatures.Cuvelage.CalculOuvertureFissures(beton, acier, section, sollicitations, armatures, fissures))

#print(Armatures.Flexion.verification_tranchant(beton, acier, section, sollicitations, theta, alpha))

#print(Armatures.Flexion.sectionState(section, sollicitations))

#print(Armatures.Cuvelage.VerificationEpaisseurMini(beton, section, sollicitations, armatures))
