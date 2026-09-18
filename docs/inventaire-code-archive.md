# Inventaire du code archivé

Fichiers retirés de `main` lors de la phase 0 (septembre 2026) :

- `Scripts/Calculations/Calculs8.py` — version 1 procédurale, non exécutable (importe `classes_projet`, absent).
- `Scripts/Calculations/main_calculation.py` — script d'essais, plante (`NameError: wallLength`).
- `Scripts/Calculations/Sollicitations/sollicitations_old.py` — solveur EF avant les corrections de juillet 2026.

Ils restent consultables sur le tag `v2.0.0-audit-2026-09` et la branche `archive/v1` :

```
git show v2.0.0-audit-2026-09:Scripts/Calculations/Calculs8.py > Calculs8_archive.py
```

## Fonctions de `Calculs8.py` à relire avant d'écrire les modules suivants

Relire, jamais copier sans test : ce code n'a jamais été vérifié.

| Ligne | Fonction | Utile pour la tâche |
|---|---|---|
| 392 | `methode_3moments` | 3.6 — cas de référence CR-02 (poutre continue) |
| 1114 | `verification_flambement` | 4.1 — flambement du voile |
| 1132 | `flexion_composee_voile` | 4.1 — flexion composée |
| 1183 | `etat_section` | 4.1 — état de la section |
| 1228 | `flexion_partiellement_` | 4.1 |
| 1303 | `flexion_totalement_tendue` | 4.1 |
| 1347 | `verification_contrainte_partiellement_` | 4.2 — contraintes ELS |
| 1365 | `diagramme_interaction` | 4.1 — diagramme M-N |
| 1404 à 1653 | `pivot_A`, `pivot_A_B`, `pivot_B`, `pivot_B_C`, `pivot_C` | 4.1 |
| 1713 | `verif_section_diagramme_interaction` | 4.1 |
| 1767, 1779 | `inertie_fissuree`, `inertie_homogene` | 4.2 |
| 1868 | `ouverture_fissure` | 4.2 — fissuration |
| 1900, 1945 | `methode_forfaitaire_simplifiee`, `methode_forfaitaire` | 3.6 — recoupement des sollicitations |
| 2414, 2425 | `verification_portance_butons`, `verification_glissement_butons` | 5.2 — semelles de butons |
| 2467, 2491 | `verification_portance`, `verification_glissement` | 5.1 — semelle du VPP |
| 2912 | `verification_portance1` | 5.1 |