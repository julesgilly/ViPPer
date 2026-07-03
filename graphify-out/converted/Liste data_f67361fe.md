<!-- converted from Liste data.xlsx -->

## Sheet: Feuil1
| Données  | Type  | Nom | Catégorie  | Forme | Utilisation | Commentaires | Statut |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nameProj | Entrée  | Nom du Projet  | Données Projet | string | string |  | Oui |  |  |  |  |  |  | Oui |
| categorie | Entrée  | Catégorie du bâtiment  | Données Projet | string  | string | Garder que la lettre  | Oui |  |  |  |  |  |  | Non |
| nameIng | Entrée  | Nom de l'ingénieur | Données Projet | string | string |  | Oui |  |  |  |  |  |  |  |
| largeurPasse | Entrée  | largeur ouverture de passe | Données Projet | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| hauteurPasse | Entrée  | largeur ouverture de passe | Données Projet | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| refCote | Entrée  | Cote de référence du projet  | Données Projet | float ou int  | float ou int  | Cote tête VPP - permet de passer en cote relative (i.e: cotes croissantes dans le sens de la profondeur) | Oui |  |  |  |  |  |  |  |
| fck | Entrée  | Résistance caractéristique du béton | Données Béton  | string | float ou int  |  | Oui |  |  |  |  |  |  |  |
| classe_exposition | Entrée  | Classe exposition du béton  | Données Béton  | string | string |  | Oui |  |  |  |  |  |  |  |
| enrobage | Entrée  | Enrobage des aciers  | Données Béton  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| density | Entrée  | Poids volumique du béton  | Données Béton  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| Module_DEF | Entrée  | Module d'Young - phase définitve  | Données Béton  | float ou int  | float ou int  | NF P94-261 §6.4.1 (8) NOTE 1 | Oui |  |  |  |  |  |  |  |
| Module_PROV | Entrée  | Module d'Young - phase provisoire | Données Béton  | float ou int  | float ou int  | NF P94-261 §6.4.1 (8) NOTE 1 | Oui |  |  |  |  |  |  |  |
| Coeff_securite_Beton | Entrée  | Coefficient de sécurité béton  | Données Béton  | float ou int  | float ou int  | EC2 1-1 §2.4.2.4 tableau 2.1N | Oui |  |  |  |  |  |  |  |
| Coeff_equivalence | Entrée  | Coefficient d'équivalence acier/béton | Données Béton  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| fyk | Entrée  | limite d'élasticité des aciers  | Données Acier  | float ou int  |  |  | Oui |  |  |  |  |  |  |  |
| palier | Entrée  | Palier d'inclinaison pour la calcul | Données Acier  | string | string | Par défaut : horizontal | Oui |  |  |  |  |  |  |  |
| classe  | Entrée  | Classe de ductilité  | Données Acier  | string | string | A, B ou C. Par défaut : B | Oui |  |  |  |  |  |  |  |
| Coeff_securite_Acier | Entrée  | Coefficient de sécurité acier | Données Acier  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| Module | Entrée  | Module d'élasticité | Données Acier  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| type | Entrée  | Type de cuvelage  | Données Cuvelage | string | string | Transformer en "Imperméabilisation", "Etanchéité", "Etanche" ou None | Oui |  |  |  |  |  |  |  |
| niveau_eau | Entrée  | Niveau d'eau de calcul | Données Cuvelage | string | string | "EE", "EH", "EB", "EC", None | Oui |  |  |  |  |  |  |  |
| precaution | Entrée  | Précaution de coulage  | Données Cuvelage | bool | bool |  | Oui |  |  |  |  |  |  |  |
| wOuvFiss | Entrée  | Valeur limite de l'ouverture des fissures | Données Cuvelage | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| dureeOuvFiss | Entrée  | Durée de chargement  | Données Cuvelage | string | string | "Longue" ou "Courte" | Oui |  |  |  |  |  |  |  |
| presenceEau | Entrée  | Présence d'eau dans le sol | Données Eau | bool | bool |  | Oui |  |  |  |  |  |  |  |
| waterlevel | Entrée  | Niveau d'eau   | Données Eau | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| waterDensity | Entrée  | Masse volumique de l'eau | Données Eau | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| nameCouche | Entrée  | Nom de la couche | Données Sol | string | string |  | Oui |  |  |  |  |  |  |  |
| coteSupCouche | Entrée  | Cote supérieure de la couche  | Données Sol | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| coteinfCouche | Entrée  | Cote inférieure de la couche | Données Sol | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| typeSol | Entrée  | Type de sol de la couche | Données Sol | string | string | "Argiles", "Limons", "Sables", "Graves", "Craies", "Marnes", "Marno-calcaires", "Roches", "Remblais" | Oui |  |  |  |  |  |  |  |
| cu_couche | Entrée  | Cohésion court terme de la couche | Données Sol | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| c_couche | Entrée  | Cohésion long terme de la couche | Données Sol | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| phiu_couche | Entrée  | Angle de frottement court terme  | Données Sol | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| phi_couche | Entrée  | Angle de frottement long terme | Données Sol | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| gamma_couche | Entrée  | Masse volumique de la couche | Données Sol | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| computeTassements | Entrée  | Calcul des tassements ?  | Données Sol | bool | bool | True or False | Oui |  | Pour calcul des tassements - Prévoir de cocher une case pour faire le calcul pour ne pas à avoir à remplir ces informations dans tous les cas  |  |  |  |  |  |
| Em_couche | Entrée  | Module pressiométrique de Ménard | Données Sol | float ou int  | float ou int  | Peut valoir None | Oui |  |  |  |  |  |  |  |
| alpha_couche | Entrée  | Coefficient rhéologique de la couche | Données Sol | float ou int  | float ou int  | Peut valoir None | Oui |  |  |  |  |  |  |  |
| isCoucheAncrage | Entrée  | Couche d'ancrage de la fondations ? | Données Sol | bool | bool |  | Non |  |  |  |  |  |  |  |
| listeSol | Entrée  | Informations pour toutes les couches | Données Sol | dict | dict |  | Oui |  |  |  |  |  |  |  |
| typeInterface | Entrée  | Type d'interface sol-fondation | Données Sol | string  | string | "Interface Frottante", "Interface Adhérente" (défaut) | Oui |  |  |  |  |  |  |  |
| tauxSemButon | Entrée  | Taux de travail de la semelle de buton | Données Sol | float ou int  | float ou int  | ELS - Taux butons = Taux fondations ELS / 2 | Oui |  |  |  |  |  |  |  |
| tauxSolELS | Entrée  | Contrainte de sol admissible ELS | Données Sol | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| classeServiceBois | Entrée  | Classe de service du bois  | Données Bois  | string | int  |  | Oui |  |  |  |  |  |  |  |
| dureeActionBois | Entrée  | Durée des actions pour les éléments BOIS | Données Bois  | string | string |  | Oui |  |  |  |  |  |  |  |
| Coeff_securite_Bois | Entrée  | Coefficient de sécurité bois | Données Bois  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| classeBois | Entrée  | Classe du bois  | Données Bois  | string | float ou int  |  | Oui |  |  |  |  |  |  |  |
| facteurRelatifBois | Entrée  | Facteur relatif en compression  | Données Bois  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| coeffThermique | Entrée  | Coefficient linéaire de dilatation thermique | Données Température  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| deltaTemperature | Entrée  | Delta de température  | Données Température  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| critereFleche | Entrée  | Flèche admissible  | Données Flèche  | string  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| valeurFleche | Entrée  | Valeur de la flèche admissible | Données Flèche  | float ou int  | float ou int  | Nulle si critereFleche à une valeur  | Oui |  |  |  |  |  |  |  |
| coeffG | Entrée  | Coefficient ELU charges permanentes  | Données Combinaison | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| coeffQ | Entrée  | Coefficient ELU charges exploitation | Données Combinaison | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| longueurVoile | Entrée  | Longueur du VPP | Données Géométrie | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| epaisseurVoile | Entrée  | Epaisseur du VPP | Données Géométrie | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| coteSupVoile_DEF | Entrée  | Cote supérieur du VPP en phase DEF | Données Géométrie | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| coteSupVoile_PROV | Entrée  | Cote supérieur du VPP en phase PROV | Données Géométrie | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| typePlancher | Entrée  | Type de plancher  | Données Géométrie | string | string | Plancher ou Dallage | Oui |  |  |  |  |  |  |  |
| niveauPlancher | Entrée  | Niveau du plancher | Données Géométrie | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| epaisseurPlancher | Entrée  | Epaisseur du plancher | Données Géométrie | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| listePlancher | Entrée  | Informations pour tous les planchers | Données Géométrie | liste | liste |  | Oui |  |  |  |  |  |  |  |
| isButonnant | Entrée  | Le plancher fait-il appui ?  | Données Géométrie | bool | bool |  | Oui |  |  |  |  |  |  |  |
| typeCharges | Entrée  | Type de charges  | Données Chargement  | string  | string | "Permanente"; "Exploitation" | Oui |  |  |  |  |  |  |  |
| niveauCharges | Entrée  | Niveau de la charge  | Données Chargement  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| chargeVert | Entrée  | Valeur de la composante Verticale | Données Chargement  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| chargeHoriz | Entrée  | Valeur de la composante Horizontale | Données Chargement  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| chargeMoment | Entrée  | Valeur de la composante Moment  | Données Chargement  | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| torseurCharges | Entrée  | Informations pour toutes les charges  | Données Chargement  | liste | liste |  | Oui |  |  |  |  |  |  |  |
| typeSurcharge | Entrée  | Types de surcharges | Données Surcharges | string | int  |  | Oui |  |  |  |  |  |  |  |
| phaseCalculSurcharge | Entrée  | Phase de calul de la surcharge | Données Surcharges | string  | string |  | Oui |  |  |  |  |  |  |  |
| qSurcharge | Entrée  | Valeur de la charge | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| dSurcharge | Entrée  | Distance à l'écran | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| B_Surcharge | Entrée  | Largeur de la charge | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| L_Surcharge | Entrée  | Longueur de la charge | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| hauteurTalusSurcharge | Entrée  | Hauteur du talus/risberme | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| angleTalusSurcharge | Entrée  | Angle inclinaison talus/risberme | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| longueurBaseRisberme | Entrée  | Longueur de la base de la risberme | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| poidsTalusSurcharge | Entrée  | poids volumique talus/risberme | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| cTalusSurcharge | Entrée  | c talus/risberme | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| phi_talusSurcharge | Entrée  | phi talus/risberme | Données Surcharges | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| listeSurcharge | Entrée  | Informations pour toutes les surcharges | Données Surcharges | disct | dict |  | Oui |  |  |  |  |  |  |  |
| modeFondation | Entrée  | Mode fondation | Données Fondations | string | string | Si profonde: ne réalise pas les vérifications | Oui |  |  |  |  |  |  |  |
| AiFondation | Entrée  | Arase inférieure de la fondation  | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| largeurFondation | Entrée  | Largeur de la fondation  | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| hauteurFondation | Entrée  | Hauteur de la fondation | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| debordFondation | Entrée  | Débord extérieur de la semelle  | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| enrobageFondation | Entrée  | Enrobage pour la fondation | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| typeFondation | Entrée  | Type de semelle  | Données Fondations | string | string | "Préfabriquée"; "Coulée pleine fouille" | Oui |  |  |  |  |  |  |  |
| isButeeFondation | Entrée  | Prise en compte de la butée ?  | Données Fondations | bool | bool |  | Oui |  |  |  |  |  |  |  |
| portanceELU | Entrée  | Facteur partiel - Portance ELU | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| glissementELU | Entrée  | Facteur partiel - Glissement ELU | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| portanceELS | Entrée  | Facteur partiel - Portance ELS | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| modelePortance | Entrée  | Coefficient de modèle - Portance | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| modeleGlissement | Entrée  | Coefficient de modèle - Glissement | Données Fondations | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| niveauButon | Entrée  | Niveau du lit de Buton | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| entraxeButon  | Entrée  | Entraxe du lit de Buton | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| entraxeGaucheButon | Entrée  | Entraxe gauche du lit de Buton | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| entraxeDroitButon | Entrée  | Entraxe droit du lit de Buton | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| fonctionnementButon | Entrée  | Fonctionnement du lit de Buton | Données Butons | string | string | Horizontal ou Vertical | Oui |  |  |  |  |  |  |  |
| inclinaisonButon | Entrée  | Inclinaison du lit de Buton | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| distanceButon | Entrée  | Distance au voile du lit de Buton | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| LongueurButon | Entrée  | Longueur du Buton | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| typeButon | Entrée  | Type de Butons | Données Butons | string | string |  | Oui |  |  |  |  |  |  |  |
| materiauButon | Entrée  | Materiau du lit de Buton | Données Butons | string | string |  | Oui |  |  |  |  |  |  |  |
| accrochageButon | Entrée  | Accrochage en tête du lit de Buton | Données Butons | string | string |  | Oui |  |  |  |  |  |  |  |
| listeButon | Entrée  | Informations pour tous les lits de Butons | Données Butons | dict | dict |  | Oui |  |  |  |  |  |  |  |
| listeAppuiButon | Entrée  | Liste des n° des lits s'appuyant sur la sem. | Données Butons | liste | liste |  | Oui |  |  |  |  |  |  |  |
| largeurSemButon | Entrée  | Largeur semelle Butons | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| LongueurSemButon | Entrée  | Longueur semelle Butons | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| hauteurSemButon | Entrée  | Hauteur semelle Butons | Données Butons | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| listeSemButon | Entrée  | informations pour toutes les sem. Butons | Données Butons | dict | dict |  | Oui |  |  |  |  |  |  |  |
| typeLierne | Entrée  | Type de lierne | Données Liernes | string | string | "Dans l'épaisseur" ou en surépaisseur int. ou ext. | Oui |  |  |  |  |  |  |  |
| enrobageLierne | Entrée  | Enrobage des aciers dans la lierne | Données Liernes | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| largeurSurEpLierne | Entrée  | Largeur de la surépaisseur  | Données Liernes | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| hauteurSurEpLierne | Entrée  | Hauteur de la surépaisseur | Données Liernes | float ou int  | float ou int  |  | Oui |  |  |  |  |  |  |  |
| listeLierne | Entrée  | Informations pour toutes les liernes | Données Liernes | liste | liste |  | Oui |  |  |  |  |  |  |  |
| verifSaisie | Calcul | Vérification de la saisie | Calcul  | bool | bool |  | Non |  |  |  |  |  |  |  |
| calcul | Calcul | Lance le calcul | Calcul |  |  |  | Non |  |  |  |  |  |  |  |
| noteDeCalcul | Sortie | Note de calcul  | Livrables |  |  |  | Non |  |  |  |  |  |  |  |
| ratios | Sortie | Donnes les ratios | Livrables |  |  | Possible que si onglet ferraillage | Non |  |  |  |  |  |  |  |
| prixVPP | Sortie | Estimation du prix  | Livrables  |  |  |  | Non |  |  |  |  |  |  |  |
| Faire un exemple cote NGF et un exemple cote relative |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Pour les cotes relatives (positives dans la profondeur), on renseignera donc une valeur sup vers le bas (ex: 4m de longueur) mais dans le dessin on prendra en négatif de la valeur absolue |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Faire une clase permettant de créer le schéma statique dans le format souhaité selon Plancher, Chargement, Fondations etc…. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Fdans cette classe on vérifiera que les niveaux des charges ne sont pas supérieurs en cotes relatives à la hauteur totale du VPP. (i.e pas un niveau > au dernier appui du schéma statique) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Modifier les fonctions suivantes |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| - Fonctions de calcul des chargements: associer une key dans le dict pour "Permanente", "Exploitation" |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| - Modifier les fonctions réalisant les combinaisons pour fonctionner avec les dict |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Les fonctions de chargement doivent avoir la forme suivante |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| distributedLoads = { 1 : {"Type": ("Uniform", "Linear", "Trapezoidal"), "Charge": ("Permanente, "Exploitation"), "xmin": xmin 1, "xmax": xmax 1, "pmin": pmin 1, "pmax": pmax 1}} |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| pointLoads = { 1 : {"Type": ("Horizontal", "Vertical", "Moment"), "Charge": ("Permanente, "Exploitation"), "Position": x 1, "P": P 1}} |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Classes dans lesquelles apporter des modifications: |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| - Chargement : dans le logiciel on devra sélectionner 1 type de charges à rentrer ("Horizontal", "Vertical", "Moment") avec menu déroulant et l'utilisateur ne pourra rentrer qu'une valeur. Il en sortira un dict de pointLoad |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| - Surcharge : en output, les dict de sorti auront une key supplémentaire avec "Charge": "Exploitation" |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| - Sol: dissocier le calcul avec la pression hydro + en sorti le dict aura une key supplémentaire "Charge":"Permanente" |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| - Eau: créer une classe Eau qui calcul la pression hydrostatique et en sorti donne un dict avec une key "Charge":"EE","EH","EB"…  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Modifier la classe combinaison pour réaliser des dict avec l'ensemble des charges dans un seul dict dont les valeurs ont été pondéré avec le bon coefficient prenant en argument les dict  Chargement, Surcharge, Sol, Eau et différenciant les phases etc… |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Il faudra également différencier les chargements horizontaux sur le voile et les chargement verticaux sur les semelles  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Vérifier le bon fonctionnement avec la classe FEM "Sollicitations" |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Créer une fonction qui récupère les réactions d'appui de la classe de calcul des sollicitations et qui les transforme en chargement sur les BN avec le format adéquat décrit ci-dessus en liant avec le lit de buton |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Prévoir une fonction demandant de remplir au moins 2 lits de buton |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Fonction pour créer le schéma statique des liernes |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Créer une fonction qui récupère les réactions d'appui de la classe de calcul des sollicitations et qui les transforme en chargement sur lesbutons avec le format adéquat décrit ci-dessus en liant avec le lit de buton |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Modifier la classe Data Cuvelage pour intégrer la face sur lequel on vient mettre le cuvelage |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Modifier la classe Cuvelage pour déterminer la contraint max dans les aciers en fonction du type de cuvelage de la face d'application du cuvelage et du niveau d'eau de calcul.  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Modifier la classe flexion pour intégrer la fonction de cuvelage |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Lister les combinaisons à réaliser dans l'ensemble des calculs |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| voile |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELU 1 | 1.35*G+1.5*Q+0.74*E |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELU 2 | 1.35*G+1.35*E+1.5*phi0*Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Acc. | G+EE+phi_2*Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELU si EE ou pas eau | 1.35*G+1.5*Q  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELS QP | G+E+phi_0*Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELS QP sans eau | G+Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Fondations |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELU | 1.35*G+1.5*Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELS QP | G + phi_2*Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELS CARA | G + Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELU STR portance | gammaG * G + gammaQ * Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELU STR glissement V | gammaG * G + gammaQ * Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ELU STR glissement H | gammaG * G + gammaQ * Q |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ajouter la largeur des BN |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Créer une fonction qui récupère les réactions d'appui de la classe de calcul des sollicitations et qui les transforme en chargement sur les BN avec le format adéquat décrit ci-dessus en liant avec le lit de buton |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Créer une fonction qui récupère les sollicitations dans le voile pour ensuite faire le calcul des sections d'acier |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Schéma statique des BN |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Sauvegarder les figures sollicitations et flèches du voile + affihcer valeur sur graph |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Vérification du critère de déformation: L/250 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |