# Graph Report - .  (2026-04-11)

## Corpus Check
- 62 files · ~361,303 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 525 nodes · 685 edges · 100 communities detected
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 29 edges (avg confidence: 0.87)
- Token cost: 13,300 input · 6,400 output

## God Nodes (most connected - your core abstractions)
1. `BeamFEM` - 21 edges
2. `creation_liste_abscisse()` - 15 edges
3. `ViPPer 2.0.0 - Retaining Wall Dimensioning Software` - 13 edges
4. `creation_liste_vide()` - 10 edges
5. `methode_3moments()` - 9 edges
6. `chargement_surcharges()` - 9 edges
7. `contraintes_sol()` - 8 edges
8. `butee()` - 8 edges
9. `diagramme_interaction()` - 8 edges
10. `torseur_inf_semelle()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Graphify Knowledge Graph Integration` --conceptually_related_to--> `ViPPer 2.0.0 - Retaining Wall Dimensioning Software`  [EXTRACTED]
  CLAUDE.md → graphify-out/converted/Description fichiers_25a88a91.md
- `ViPPer 2.0.0 - Retaining Wall Dimensioning Software` --references--> `Data: Projet`  [EXTRACTED]
  graphify-out/converted/Description fichiers_25a88a91.md → graphify-out/converted/Liste data_f67361fe.md
- `ViPPer 2.0.0 - Retaining Wall Dimensioning Software` --references--> `Output: Note de Calcul`  [EXTRACTED]
  graphify-out/converted/Description fichiers_25a88a91.md → graphify-out/converted/Liste data_f67361fe.md
- `ViPPer 2.0.0 - Retaining Wall Dimensioning Software` --references--> `Output: Ratios`  [EXTRACTED]
  graphify-out/converted/Description fichiers_25a88a91.md → graphify-out/converted/Liste data_f67361fe.md
- `ViPPer 2.0.0 - Retaining Wall Dimensioning Software` --references--> `Output: Prix VPP`  [EXTRACTED]
  graphify-out/converted/Description fichiers_25a88a91.md → graphify-out/converted/Liste data_f67361fe.md

## Hyperedges (group relationships)
- **Pipeline de Calcul Structurel** — submodule_combinaisons, submodule_beton, submodule_sol, submodule_sollicitations [INFERRED 0.85]

## Communities

### Community 0 - "Moteur Calcul Principal"
Cohesion: 0.03
Nodes (100): butee(), caquot(), console_droite(), console_gauche(), contrainte_acier(), contraintes_sol(), copie_inverse_liste(), copie_liste_double() (+92 more)

### Community 1 - "Modules Data Centraux"
Cohesion: 0.07
Nodes (30): Chargement, Take the user's inputs from software as arguments and transform into a dict to b, _combinaisons, _concrete, Data: Acier, Data: Béton, Data: Chargement, Data: Combinaison (+22 more)

### Community 2 - "Caractéristiques Sol"
Cohesion: 0.08
Nodes (12): caracteristiques, Developed by Jules GILLY in November 2022 for a personal use This file forms th, _eau, Take the user's inputs from software as arguments and transform into a dict to b, element, Developed by Jules GILLY in November 2022 for a personal use This file forms th, object, Output (+4 more)

### Community 3 - "Solveur FEM BeamFEM"
Cohesion: 0.1
Nodes (12): BeamFEM, Compute the shape functions vector for a beam element         DOFs are: vertica, Compute the B-matrix, i.e: the derivatives of the shape functions vector, Compute the derivatives of the B-matrix, Compute the flexural part of the element Stiffness matrix, Compute the axial part of the element stiffness matrix, In general, an element of a curved beam can be in any orientation             T, Create an array for the load used for the integration of the element load vector (+4 more)

### Community 4 - "Propriétés Béton"
Cohesion: 0.1
Nodes (15): E_cm(), Eps_c1(), Eps_cu1(), f_cm(), f_ctd(), f_ctk_005(), f_ctk_095(), f_ctm() (+7 more)

### Community 5 - "Pipeline Chargement"
Cohesion: 0.15
Nodes (12): butee(), contraintes_sol(), K_a(), K_p(), pression_hydrostatique(), Take the user's inputs from software as arguments and transform into a dict to b, sigma_horizontale(), sigma_horizontale_tot() (+4 more)

### Community 6 - "Module Dessin"
Cohesion: 0.12
Nodes (8): _drawViPPer, Nouvelle version du logiciel ViPPer   Date: Août 2022  Améliorations: (Prévi, _MainWindow, Nouvelle version du logiciel ViPPer   Date: Août 2022  Améliorations: (Prévi, Afficher le nom du fichier dans la titlebar, Définir les polices d'écriture, la taille de la police et l'associer à la fenetr, Initialise the menus and toolbar., Fixer la taille initiale de la fenetre et la Size policy

### Community 7 - "Surcharges"
Cohesion: 0.27
Nodes (12): chargement_surcharges(), moyenne_angle_frottement(), pl_lineique_d(), pl_uniforme_aire(), pl_uniforme_d(), pl_uniforme_limitee(), pression_contigue(), pression_contigue_limitee() (+4 more)

### Community 8 - "Combinaisons de Charges"
Cohesion: 0.19
Nodes (6): Acc_voile(), ELS_QP_fondations(), ELS_QPE_voile(), ELU2_voile(), get_Psy0(), get_Psy2()

### Community 9 - "Calcul en Flexion"
Cohesion: 0.27
Nodes (11): centerOfGravity(), contrainte_aciers_tendus(), Flexion, flexion_simple_rect(), flexion_simple_T(), necessite_tranchant(), section_min(), section_min_flexion() (+3 more)

### Community 10 - "Résultats ELS QPE Définitif"
Cohesion: 0.27
Nodes (10): Bending Moment Diagram, Deflection Minimum: -0.002m at x=1.760m, Deformed Shape (Deflection Curve), Sollicitations ELS QPE - Structural Diagrams, ELS QPE (Serviceability Limit State - Quasi-Permanent), Bending Moment Maximum: ~0.018 kN.m at x=1.810m, Shear Force Diagram, Shear Force Max: ~0.025 kN at x=3.500m (+2 more)

### Community 11 - "Résultats ELU1 Définitif"
Cohesion: 0.27
Nodes (10): ELU1 Load Combination (Ultimate Limit State 1), VPP Beam (Longueur du VPP), Bending Moment (ELU1 DEF), Deflection Min: (1.750, -0.003), Deformed Shape (ELU1 DEF), Bending Moment Max: (1.896, 0.035 kN.m), Shear Force (ELU1 DEF), Shear Force Max: (3.500, 0.040 kN) (+2 more)

### Community 12 - "Résultats ELU1 Provisoire"
Cohesion: 0.27
Nodes (10): Bending Moment (ELU1 PROV, kN.m/m), Deflection Max: (2.152, 0.0002m), Deformed Shape (ELU1 PROV), ELU1 Load Combination (Ultimate Limit State 1), Solicitations ELU1 Provisional Figure, Bending Moment Max: (1.406, 0.002 kN.m/m), Provisional Condition (PROV), Shear Force (ELU1 PROV, kN/m) (+2 more)

### Community 13 - "Résultats ELU2 Définitif"
Cohesion: 0.27
Nodes (10): Bending Moment (ELU2 DEF, kN.m), Deflection Min: ~-0.005m at x=1.75m, Deformed Shape (ELU2 DEF), ELU2 Load Combination (Ultimate Limit State 2), Solicitations ELU2 Definitive Figure, Bending Moment Max: ~0.034 kN.m at x=1.875m, Shear Force (ELU2 DEF, kN), Shear Force Max: ~0.317 kN at x=3.4m (+2 more)

### Community 14 - "Résultats ELU2 Provisoire"
Cohesion: 0.27
Nodes (10): Bending Moment (ELU2 PROV, kN.m/m), Deflection Max at x=2.188m, Deformed Shape (ELU2 PROV), ELU2 Load Case (Ultimate Limit State 2), Solicitations ELU2 Provisional Figure, Bending Moment Min: -0.316 kN.m/m at x=2.750m, Provisional Load Combination (PROV), Shear Force (ELU2 PROV, kN/m) (+2 more)

### Community 15 - "Module 15"
Cohesion: 0.28
Nodes (9): Bending Moment (ELS QP DEF, kN.m), Deflection Min: ~-0.002m mid-span, Deformed Shape (ELS QP DEF), ELS QP Load Case (Quasi-Permanent SLS), Sollicitations ELS QP DEF Structural Diagrams, Bending Moment Max: ~0.015 kN.m, Shear Force (ELS QP DEF, kN), Shear Force Min: ~-0.13 kN (+1 more)

### Community 16 - "Module 16"
Cohesion: 0.48
Nodes (7): Accidental Load Case (Acc), Bending Moment (Acc PROV, kN.m), Deformed Shape (Acc PROV), Solicitations Accidental Provisional Figure, Provisional Condition (PROV), Shear Force (Acc PROV, kN), VPP Element (Longueur du VPP)

### Community 17 - "Module 17"
Cohesion: 0.52
Nodes (7): Bending Moment (Moment Fléchissant), Deformed Shape (Flèche), ELS QP Limit State (Quasi-Permanent Serviceability), Solicitations ELS QP Provisional Figure, Provisional Load Condition (PROV), Shear Force (Effort Tranchant), VPP Element (Voile Préfabriqué Provisoire)

### Community 18 - "Module 18"
Cohesion: 0.6
Nodes (6): Accidental Load Case (ACC), Bending Moment Diagram, Deformed Shape Diagram, Solicitations Accidental Deformation Figure, Shear Force Diagram, VPP Structural Member Length

### Community 19 - "Module 19"
Cohesion: 0.5
Nodes (2): Acier, Take the user's inputs from software as arguments and transform into a dict to b

### Community 20 - "Module 20"
Cohesion: 0.5
Nodes (2): Beton, Take the user's inputs from software as arguments and transform into a dict to b

### Community 21 - "Module 21"
Cohesion: 0.5
Nodes (2): Bois, Take the user's inputs from software as arguments and transform into a dict to b

### Community 22 - "Module 22"
Cohesion: 0.5
Nodes (2): Buton, Take the user's inputs from software as arguments and transform into a dict to b

### Community 23 - "Module 23"
Cohesion: 0.5
Nodes (2): Combinaison, Take the user's inputs from software as arguments and transform into a dict to b

### Community 24 - "Module 24"
Cohesion: 0.5
Nodes (2): Fleche, Take the user's inputs from software as arguments and transform into a dict to b

### Community 25 - "Module 25"
Cohesion: 0.5
Nodes (2): Fondation, Take the user's inputs from software as arguments and transform into a dict to b

### Community 26 - "Module 26"
Cohesion: 0.5
Nodes (2): Lierne, Take the user's inputs from software as arguments and transform into a dict to b

### Community 27 - "Module 27"
Cohesion: 0.5
Nodes (2): Plancher, Take the user's inputs from software as arguments and transform into a dict to b

### Community 28 - "Module 28"
Cohesion: 0.5
Nodes (2): Projet, Take the user's inputs from software as arguments and transform into a dict to b

### Community 29 - "Module 29"
Cohesion: 0.5
Nodes (2): Take the user's inputs from software as arguments and transform into a dict to b, Section

### Community 30 - "Module 30"
Cohesion: 0.5
Nodes (2): Take the user's inputs from software as arguments and transform into a dict to b, Temperature

### Community 31 - "Module 31"
Cohesion: 1.0
Nodes (1): Verify that the thickness of the wall respects the criteria of minimum thickness

### Community 32 - "Module 32"
Cohesion: 1.0
Nodes (1): Compute the crack openings of a concrete section              :raise ValueErro

### Community 33 - "Module 33"
Cohesion: 1.0
Nodes (1): Compute the inertia of a homogeneous section              :raise ValueError: I

### Community 34 - "Module 34"
Cohesion: 1.0
Nodes (1): Compute the inertia of a cracked section              :raise ValueError: If ar

### Community 35 - "Module 35"
Cohesion: 1.0
Nodes (1): Compute the reinforcement stresses              :raise ValueError: If argument

### Community 36 - "Module 36"
Cohesion: 1.0
Nodes (1): Compute the reinforcement stresses                   :param alpha_u: coefficie

### Community 37 - "Module 37"
Cohesion: 1.0
Nodes (1): Compute the minimal section of reinforcements for a concrete element in bending

### Community 38 - "Module 38"
Cohesion: 1.0
Nodes (1): Compute the minimal section of reinforcements for a concrete element in bending

### Community 39 - "Module 39"
Cohesion: 1.0
Nodes (1): Compute the minimal thickness or height of the element. Per Eurocodes, it must r

### Community 40 - "Module 40"
Cohesion: 1.0
Nodes (1): Compute the section of reinforcements needed for a rectangular section for a con

### Community 41 - "Module 41"
Cohesion: 1.0
Nodes (1): Compute the section of reinforcements needed for a section shaped in T for a con

### Community 42 - "Module 42"
Cohesion: 1.0
Nodes (1): Verify if transverse reinforcements are needed. Per Eurocode 2:             - i

### Community 43 - "Module 43"
Cohesion: 1.0
Nodes (1): Compute the center of gravity of a section from the bottom                  :r

### Community 44 - "Module 44"
Cohesion: 1.0
Nodes (1): Determine the state of the section: 'Partiellement tendue', 'Partiellement compr

### Community 45 - "Module 45"
Cohesion: 1.0
Nodes (1): Check if the compression of the connecting rods is verified                  :

### Community 46 - "Module 46"
Cohesion: 1.0
Nodes (1): Compute the section of transverse reinforcement for the element

### Community 47 - "Module 47"
Cohesion: 1.0
Nodes (1): POUR LE VOILE         Compute the load combination at ELU 1: 1.35*G + 1.5*Q + 0

### Community 48 - "Module 48"
Cohesion: 1.0
Nodes (1): POUR LE VOILE         Compute the load combination at ELU 2: 1.35*G + 1.5*psy0*

### Community 49 - "Module 49"
Cohesion: 1.0
Nodes (1): POUR LE VOILE         Compute the load combination at ELU Acc: G + EE + psy_2*Q

### Community 50 - "Module 50"
Cohesion: 1.0
Nodes (1): POUR LE VOILE         Compute the load combination at 'ELS Quasi-Permanent' = G

### Community 51 - "Module 51"
Cohesion: 1.0
Nodes (1): POUR LE VOILE         Compute the load combination at 'ELS Quasi-Permanent' = G

### Community 52 - "Module 52"
Cohesion: 1.0
Nodes (1): POUR LES FONDATIONS DU VPP         Compute the load combination at ELU 1: 1.35*

### Community 53 - "Module 53"
Cohesion: 1.0
Nodes (1): POUR LES FONDATIONS DU VPP         Compute the load combination at 'ELS Quasi-P

### Community 54 - "Module 54"
Cohesion: 1.0
Nodes (1): POUR LES FONDATIONS DU VPP         Compute the load combination at 'ELS caracte

### Community 55 - "Module 55"
Cohesion: 1.0
Nodes (1): POUR LES FONDATIONS DU VPP         Compute the load combination for the verific

### Community 56 - "Module 56"
Cohesion: 1.0
Nodes (1): POUR LES FONDATIONS DU VPP         Compute the load combination for the vertica

### Community 57 - "Module 57"
Cohesion: 1.0
Nodes (1): POUR LES FONDATIONS DU VPP         Compute the load combination for the horizon

### Community 58 - "Module 58"
Cohesion: 1.0
Nodes (1): Get the psy_0 coefficient from table in Eurocode 0                  :param cat

### Community 59 - "Module 59"
Cohesion: 1.0
Nodes (1): Get the psy_2 coefficient from table in Eurocode 0                  :param cat

### Community 60 - "Module 60"
Cohesion: 1.0
Nodes (1): Compute the 'resistance moyenne à la compression du béton'                   :

### Community 61 - "Module 61"
Cohesion: 1.0
Nodes (1): Compute the 'resistance de calcul à la compression'                   :param f

### Community 62 - "Module 62"
Cohesion: 1.0
Nodes (1): Compute the 'resistance moyenne à la traction du béton'                  :para

### Community 63 - "Module 63"
Cohesion: 1.0
Nodes (1): Compute the 'resistance caractéristiques à la traction du béton (fractile 5%)'

### Community 64 - "Module 64"
Cohesion: 1.0
Nodes (1): Compute the 'resistance caractéristiques à la traction du béton (fractile 95%)'

### Community 65 - "Module 65"
Cohesion: 1.0
Nodes (1): Compute the 'resistance de calcul à la traction du béton'                  :pa

### Community 66 - "Module 66"
Cohesion: 1.0
Nodes (1): Compute the 'Module d'élasticité sécant du béton'                  :param fck:

### Community 67 - "Module 67"
Cohesion: 1.0
Nodes (1): Compute the 'déformation atteinte au pic de contrainte de la relation contrainte

### Community 68 - "Module 68"
Cohesion: 1.0
Nodes (1): Compute the 'valeur nominale de la déforamtion ultime de la relation contrainte-

### Community 69 - "Module 69"
Cohesion: 1.0
Nodes (1): Compute the 'déformation atteinte pour la contrainte maximale pour un diagramme

### Community 70 - "Module 70"
Cohesion: 1.0
Nodes (1): Compute the 'déformation ultime pour un diagramme parabole rectangle'

### Community 71 - "Module 71"
Cohesion: 1.0
Nodes (1): Compute the 'exposant dans la relation contrainte-déformation'

### Community 72 - "Module 72"
Cohesion: 1.0
Nodes (1): Compute the 'déformation atteinte pour la contrainte maximale pour un diagramme

### Community 73 - "Module 73"
Cohesion: 1.0
Nodes (1): Compute the 'déformation ultime pour un diagramme bilinéaire'

### Community 74 - "Module 74"
Cohesion: 1.0
Nodes (1): Compute the 'valeur moyenne de la résistance en traction du béton au moment où l

### Community 75 - "Module 75"
Cohesion: 1.0
Nodes (1): Compute the coating minimal value in concrete          This method is to be us

### Community 76 - "Module 76"
Cohesion: 1.0
Nodes (1): This function computes the 'Pression hydrostatique' defined as: sigmaV = Gamma_e

### Community 77 - "Module 77"
Cohesion: 1.0
Nodes (1): This function computes the average density of the ground weighted by the thickne

### Community 78 - "Module 78"
Cohesion: 1.0
Nodes (1): This function computes the 'Coefficient de poussée du sol' defined as: Ka = tan²

### Community 79 - "Module 79"
Cohesion: 1.0
Nodes (1): This function computes the 'Coefficient de butée du sol' defined as: Kp = 1/Ka

### Community 80 - "Module 80"
Cohesion: 1.0
Nodes (1): This function computes the 'Contraintes verticales totales' defined as: sigmaV =

### Community 81 - "Module 81"
Cohesion: 1.0
Nodes (1): This function computes the 'Pression hydrostatique' defined as: sigmaV = Gamma_e

### Community 82 - "Module 82"
Cohesion: 1.0
Nodes (1): This function computes the 'Contraintes verticales effectives' defined as: sigma

### Community 83 - "Module 83"
Cohesion: 1.0
Nodes (1): This function computes the 'Contraintes horizontales effectives' defined as: sig

### Community 84 - "Module 84"
Cohesion: 1.0
Nodes (1): This function computes the 'Contraintes horizontales totales' defined as: sigmaH

### Community 85 - "Module 85"
Cohesion: 1.0
Nodes (1): Main function computing the 'Contraintes horizontales totales' using every funct

### Community 86 - "Module 86"
Cohesion: 1.0
Nodes (1): This function computes the 'Contraintes horizontales en butée' using the same fo

### Community 87 - "Module 87"
Cohesion: 1.0
Nodes (1): This function transforms the data from the computed list of values to a dictiona

### Community 88 - "Module 88"
Cohesion: 1.0
Nodes (1): In the case of a multilayer soil, we have the choice between two possibilities:

### Community 89 - "Module 89"
Cohesion: 1.0
Nodes (1): This method computes the horizontal loads for a uniform pressure applied from a

### Community 90 - "Module 90"
Cohesion: 1.0
Nodes (1): This method computes the horizontal loads for a vertical line load applied on a

### Community 91 - "Module 91"
Cohesion: 1.0
Nodes (1): This method computes the horizontal loads for a uniform pressure applied from a

### Community 92 - "Module 92"
Cohesion: 1.0
Nodes (1): This method computes the horizontal loads for a uniform pressure applied against

### Community 93 - "Module 93"
Cohesion: 1.0
Nodes (1): This method computes the horizontal loads for a uniform pressure applied against

### Community 94 - "Module 94"
Cohesion: 1.0
Nodes (1): This method computes the horizontal loads for a uniform load applied at a distan

### Community 95 - "Module 95"
Cohesion: 1.0
Nodes (1): This method computes the horizontal loads for a line load applied at a distance

### Community 96 - "Module 96"
Cohesion: 1.0
Nodes (1): This method computes the horizontal loads for a risberme

### Community 97 - "Module 97"
Cohesion: 1.0
Nodes (1): This method computes the horizontal overloads for a talus

### Community 98 - "Module 98"
Cohesion: 1.0
Nodes (1): This method returns a dict with all the computed overloads applied to the wall

### Community 99 - "Module 99"
Cohesion: 1.0
Nodes (1): TODO: Cuvelage Face Checkbox

## Knowledge Gaps
- **151 isolated node(s):** `Verify that the thickness of the wall respects the criteria of minimum thickness`, `Compute the crack openings of a concrete section              :raise ValueErro`, `Compute the inertia of a homogeneous section              :raise ValueError: I`, `Compute the inertia of a cracked section              :raise ValueError: If ar`, `Compute the reinforcement stresses              :raise ValueError: If argument` (+146 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Module 31`** (1 nodes): `Verify that the thickness of the wall respects the criteria of minimum thickness`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 32`** (1 nodes): `Compute the crack openings of a concrete section              :raise ValueErro`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 33`** (1 nodes): `Compute the inertia of a homogeneous section              :raise ValueError: I`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 34`** (1 nodes): `Compute the inertia of a cracked section              :raise ValueError: If ar`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 35`** (1 nodes): `Compute the reinforcement stresses              :raise ValueError: If argument`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 36`** (1 nodes): `Compute the reinforcement stresses                   :param alpha_u: coefficie`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 37`** (1 nodes): `Compute the minimal section of reinforcements for a concrete element in bending`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 38`** (1 nodes): `Compute the minimal section of reinforcements for a concrete element in bending`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 39`** (1 nodes): `Compute the minimal thickness or height of the element. Per Eurocodes, it must r`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 40`** (1 nodes): `Compute the section of reinforcements needed for a rectangular section for a con`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 41`** (1 nodes): `Compute the section of reinforcements needed for a section shaped in T for a con`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 42`** (1 nodes): `Verify if transverse reinforcements are needed. Per Eurocode 2:             - i`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 43`** (1 nodes): `Compute the center of gravity of a section from the bottom                  :r`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 44`** (1 nodes): `Determine the state of the section: 'Partiellement tendue', 'Partiellement compr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 45`** (1 nodes): `Check if the compression of the connecting rods is verified                  :`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 46`** (1 nodes): `Compute the section of transverse reinforcement for the element`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 47`** (1 nodes): `POUR LE VOILE         Compute the load combination at ELU 1: 1.35*G + 1.5*Q + 0`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 48`** (1 nodes): `POUR LE VOILE         Compute the load combination at ELU 2: 1.35*G + 1.5*psy0*`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 49`** (1 nodes): `POUR LE VOILE         Compute the load combination at ELU Acc: G + EE + psy_2*Q`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 50`** (1 nodes): `POUR LE VOILE         Compute the load combination at 'ELS Quasi-Permanent' = G`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 51`** (1 nodes): `POUR LE VOILE         Compute the load combination at 'ELS Quasi-Permanent' = G`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 52`** (1 nodes): `POUR LES FONDATIONS DU VPP         Compute the load combination at ELU 1: 1.35*`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 53`** (1 nodes): `POUR LES FONDATIONS DU VPP         Compute the load combination at 'ELS Quasi-P`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 54`** (1 nodes): `POUR LES FONDATIONS DU VPP         Compute the load combination at 'ELS caracte`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 55`** (1 nodes): `POUR LES FONDATIONS DU VPP         Compute the load combination for the verific`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 56`** (1 nodes): `POUR LES FONDATIONS DU VPP         Compute the load combination for the vertica`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 57`** (1 nodes): `POUR LES FONDATIONS DU VPP         Compute the load combination for the horizon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 58`** (1 nodes): `Get the psy_0 coefficient from table in Eurocode 0                  :param cat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 59`** (1 nodes): `Get the psy_2 coefficient from table in Eurocode 0                  :param cat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 60`** (1 nodes): `Compute the 'resistance moyenne à la compression du béton'                   :`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 61`** (1 nodes): `Compute the 'resistance de calcul à la compression'                   :param f`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 62`** (1 nodes): `Compute the 'resistance moyenne à la traction du béton'                  :para`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 63`** (1 nodes): `Compute the 'resistance caractéristiques à la traction du béton (fractile 5%)'`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 64`** (1 nodes): `Compute the 'resistance caractéristiques à la traction du béton (fractile 95%)'`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 65`** (1 nodes): `Compute the 'resistance de calcul à la traction du béton'                  :pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 66`** (1 nodes): `Compute the 'Module d'élasticité sécant du béton'                  :param fck:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 67`** (1 nodes): `Compute the 'déformation atteinte au pic de contrainte de la relation contrainte`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 68`** (1 nodes): `Compute the 'valeur nominale de la déforamtion ultime de la relation contrainte-`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 69`** (1 nodes): `Compute the 'déformation atteinte pour la contrainte maximale pour un diagramme`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 70`** (1 nodes): `Compute the 'déformation ultime pour un diagramme parabole rectangle'`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 71`** (1 nodes): `Compute the 'exposant dans la relation contrainte-déformation'`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 72`** (1 nodes): `Compute the 'déformation atteinte pour la contrainte maximale pour un diagramme`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 73`** (1 nodes): `Compute the 'déformation ultime pour un diagramme bilinéaire'`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 74`** (1 nodes): `Compute the 'valeur moyenne de la résistance en traction du béton au moment où l`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 75`** (1 nodes): `Compute the coating minimal value in concrete          This method is to be us`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 76`** (1 nodes): `This function computes the 'Pression hydrostatique' defined as: sigmaV = Gamma_e`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 77`** (1 nodes): `This function computes the average density of the ground weighted by the thickne`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 78`** (1 nodes): `This function computes the 'Coefficient de poussée du sol' defined as: Ka = tan²`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 79`** (1 nodes): `This function computes the 'Coefficient de butée du sol' defined as: Kp = 1/Ka`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 80`** (1 nodes): `This function computes the 'Contraintes verticales totales' defined as: sigmaV =`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 81`** (1 nodes): `This function computes the 'Pression hydrostatique' defined as: sigmaV = Gamma_e`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 82`** (1 nodes): `This function computes the 'Contraintes verticales effectives' defined as: sigma`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 83`** (1 nodes): `This function computes the 'Contraintes horizontales effectives' defined as: sig`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 84`** (1 nodes): `This function computes the 'Contraintes horizontales totales' defined as: sigmaH`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 85`** (1 nodes): `Main function computing the 'Contraintes horizontales totales' using every funct`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 86`** (1 nodes): `This function computes the 'Contraintes horizontales en butée' using the same fo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 87`** (1 nodes): `This function transforms the data from the computed list of values to a dictiona`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 88`** (1 nodes): `In the case of a multilayer soil, we have the choice between two possibilities:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 89`** (1 nodes): `This method computes the horizontal loads for a uniform pressure applied from a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 90`** (1 nodes): `This method computes the horizontal loads for a vertical line load applied on a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 91`** (1 nodes): `This method computes the horizontal loads for a uniform pressure applied from a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 92`** (1 nodes): `This method computes the horizontal loads for a uniform pressure applied against`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 93`** (1 nodes): `This method computes the horizontal loads for a uniform pressure applied against`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 94`** (1 nodes): `This method computes the horizontal loads for a uniform load applied at a distan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 95`** (1 nodes): `This method computes the horizontal loads for a line load applied at a distance`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 96`** (1 nodes): `This method computes the horizontal loads for a risberme`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 97`** (1 nodes): `This method computes the horizontal overloads for a talus`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 98`** (1 nodes): `This method returns a dict with all the computed overloads applied to the wall`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module 99`** (1 nodes): `TODO: Cuvelage Face Checkbox`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BeamFEM` connect `Solveur FEM BeamFEM` to `Caractéristiques Sol`, `Pipeline Chargement`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `_sol` connect `Caractéristiques Sol` to `Modules Data Centraux`, `Pipeline Chargement`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `_concrete` connect `Modules Data Centraux` to `Propriétés Béton`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **What connects `Verify that the thickness of the wall respects the criteria of minimum thickness`, `Compute the crack openings of a concrete section              :raise ValueErro`, `Compute the inertia of a homogeneous section              :raise ValueError: I` to the rest of the system?**
  _151 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Moteur Calcul Principal` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._
- **Should `Modules Data Centraux` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._
- **Should `Caractéristiques Sol` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._