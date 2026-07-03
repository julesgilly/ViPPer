# ViPPer — Phase 1 : Finalisation Engine de Calcul

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructurer le code de calcul Python existant en architecture `domain/application/infrastructure`, implémenter la traçabilité `ValeurTracee`, et établir une base de tests solide (pytest + hypothesis + cas de référence).

**Architecture:** Séparation stricte en 3 couches. Le `domain/` contient des fonctions pures typées sans I/O. L'`application/` orchestre. L'`infrastructure/` gère FastAPI, Supabase, PDF. Aucun code du domaine ne connaît FastAPI ou Supabase.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic v2, pytest, hypothesis, mypy --strict, ruff

---

## Scope

Ce plan couvre la Phase 1 uniquement : restructuration architecture + `ValeurTracee` + tests. **Pas de déploiement, pas de frontend.** Le code tourne en local et via l'API FastAPI locale.

---

## File Structure cible

```
backend/
├── domain/                          ← calculs purs, zéro I/O, zéro framework
│   ├── __init__.py
│   ├── types.py                     # ValeurTracee, dataclasses communes
│   ├── sol/
│   │   ├── __init__.py
│   │   ├── caracteristiques.py      # Ka, Kp, cohésion, angle frottement
│   │   ├── poussee.py               # poussée/butée des terres
│   │   ├── surcharges.py            # surcharges en surface
│   │   └── eau.py                   # pression hydrostatique
│   ├── chargement/
│   │   ├── __init__.py
│   │   ├── combinaisons.py          # ELU1, ELU2, ELS QP, Acc
│   │   └── chargement.py            # assemblage des charges sur le voile
│   ├── sollicitations/
│   │   ├── __init__.py
│   │   ├── beam_fem.py              # BeamFEM (solveur éléments finis poutre)
│   │   └── output.py                # diagrammes M, V, déformée
│   ├── beton/
│   │   ├── __init__.py
│   │   └── proprietes.py            # fcm, fctm, Ecm, Eps_cu1… (avec lru_cache)
│   └── armatures/
│       ├── __init__.py
│       ├── flexion.py               # ferraillage flexion simple/composée
│       └── cisaillement.py          # ferraillage effort tranchant
│
├── application/
│   ├── __init__.py
│   └── calcul_vpp.py                # orchestre domain/ pour un projet VPP complet
│
└── tests/
    ├── conftest.py                      # PYTHONPATH setup, fixtures partagées
│
├── infrastructure/
│   ├── __init__.py
│   ├── api/
│   │   ├── main.py                  # app FastAPI
│   │   ├── config.py                # Settings Pydantic (env vars)
│   │   ├── dependencies.py          # get_current_user (JWT Supabase)
│   │   └── routers/
│   │       ├── calculations.py      # POST /calculate
│   │       └── projects.py          # CRUD /projects
│   └── schemas/
│       ├── calculation.py           # Pydantic : CalculationInput, CalculationOutput
│       └── project.py               # Pydantic : ProjectCreate, ProjectOut
│
└── tests/
    ├── conftest.py
    ├── domain/
    │   ├── test_types.py            # Tests ValeurTracee
    │   ├── sol/
    │   │   ├── test_caracteristiques.py
    │   │   ├── test_poussee.py
    │   │   └── test_surcharges.py
    │   ├── chargement/
    │   │   └── test_combinaisons.py
    │   ├── sollicitations/
    │   │   └── test_beam_fem.py
    │   ├── beton/
    │   │   └── test_proprietes.py
    │   └── armatures/
    │       └── test_flexion.py
    ├── application/
    │   └── test_calcul_vpp.py
    └── reference-cases/
        ├── README.md                # Comment ajouter un cas de référence
        ├── runner.py                # Exécute tous les cas, alerte si écart > 0.5%
        └── cas-001/
            ├── inputs.json
            └── outputs_expected.json
```

---

## Task 1 : Setup environnement et outils qualité

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/pyproject.toml`
- Create: `backend/.env.example`

- [ ] **Step 1.1 : Créer la structure de dossiers et les `__init__.py`**

```bash
mkdir -p backend/domain/sol backend/domain/chargement backend/domain/sollicitations backend/domain/beton backend/domain/armatures
mkdir -p backend/application
mkdir -p backend/infrastructure/api/routers backend/infrastructure/schemas
mkdir -p backend/tests/domain/sol backend/tests/domain/chargement backend/tests/domain/sollicitations backend/tests/domain/beton backend/tests/domain/armatures
mkdir -p backend/tests/application backend/tests/reference-cases/cas-001

# __init__.py domain
touch backend/domain/__init__.py backend/domain/sol/__init__.py backend/domain/chargement/__init__.py
touch backend/domain/sollicitations/__init__.py backend/domain/beton/__init__.py backend/domain/armatures/__init__.py

# __init__.py application + infrastructure
touch backend/application/__init__.py
touch backend/infrastructure/__init__.py backend/infrastructure/api/__init__.py
touch backend/infrastructure/api/routers/__init__.py  # ← indispensable pour les imports
touch backend/infrastructure/schemas/__init__.py

# __init__.py tests
touch backend/tests/__init__.py backend/tests/domain/__init__.py
touch backend/tests/domain/sol/__init__.py backend/tests/domain/beton/__init__.py
touch backend/tests/domain/chargement/__init__.py backend/tests/domain/sollicitations/__init__.py
touch backend/tests/domain/armatures/__init__.py backend/tests/application/__init__.py
```

- [ ] **Step 1.2 : Créer tests/conftest.py (PYTHONPATH)**

Sans ce fichier, `from domain.xxx import` échoue dans tous les tests.

`backend/tests/conftest.py` :
```python
import sys
from pathlib import Path

# Ajoute backend/ au PYTHONPATH pour que les imports domain.xxx fonctionnent
sys.path.insert(0, str(Path(__file__).parent.parent))
```

- [ ] **Step 1.3 : Créer requirements.txt**

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic==2.7.0
pydantic-settings==2.2.1
numpy>=1.26.0
scipy>=1.13.0
pytest==8.2.0
pytest-asyncio==0.23.6
hypothesis==6.100.0
mypy==1.10.0
ruff==0.4.4
httpx==0.27.0
sentry-sdk[fastapi]==2.3.0
weasyprint==62.3
```

- [ ] **Step 1.4 : Créer pyproject.toml**

```toml
[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

- [ ] **Step 1.5 : Installer les dépendances**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

- [ ] **Step 1.6 : Vérifier que ruff et mypy tournent**

```bash
ruff check domain/      # Attendu : no errors (dossier vide)
mypy domain/            # Attendu : Success: no issues found
```

- [ ] **Step 1.7 : Commit**

```bash
git add backend/
git commit -m "chore: initialiser structure backend domain/application/infrastructure"
```

---

## Task 2 : `ValeurTracee` — dataclass de traçabilité

**Files:**
- Create: `backend/domain/types.py`
- Create: `backend/tests/domain/test_types.py`

- [ ] **Step 2.1 : Écrire les tests**

`backend/tests/domain/test_types.py` :
```python
from domain.types import ValeurTracee, ResultatCalcul

def test_valeur_tracee_creation():
    v = ValeurTracee(
        valeur=0.333,
        unite="—",
        formule="Ka = tan²(π/4 - φ/2)",
        reference="CFMS 2023 §3.2.1",
        inputs_utilises={"phi_deg": 30.0},
    )
    assert v.valeur == 0.333
    assert "CFMS" in v.reference

def test_valeur_tracee_immutable():
    """ValeurTracee est une dataclass frozen — les valeurs ne doivent pas changer."""
    v = ValeurTracee(valeur=1.0, unite="kPa", formule="", reference="", inputs_utilises={})
    try:
        v.valeur = 2.0  # type: ignore
        assert False, "Doit lever FrozenInstanceError"
    except Exception:
        pass  # attendu

def test_resultat_calcul_contient_tracees():
    from dataclasses import fields
    from domain.types import ResultatCalcul
    field_names = [f.name for f in fields(ResultatCalcul)]
    assert "valeurs" in field_names
    assert "messages" in field_names
```

- [ ] **Step 2.2 : Vérifier que les tests échouent**

```bash
pytest tests/domain/test_types.py -v
```
Attendu : `FAILED` — `ModuleNotFoundError: No module named 'domain'`

- [ ] **Step 2.3 : Créer domain/types.py**

```python
"""
Types communs à tout le domaine ViPPer.
Aucune dépendance externe (pas de FastAPI, pas de Pydantic, pas de numpy).
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ValeurTracee:
    """
    Encapsule un résultat de calcul avec sa justification normative complète.
    Utilisé pour générer les notes de calcul traçables.
    """
    valeur: float
    unite: str
    formule: str         # ex: "Ka = tan²(π/4 - φ/2)"
    reference: str       # ex: "CFMS 2023 §3.2.1"
    inputs_utilises: dict


@dataclass
class ResultatCalcul:
    """Résultat d'un module de calcul du domaine."""
    valeurs: dict[str, ValeurTracee] = field(default_factory=dict)
    messages: list[str] = field(default_factory=list)
    succes: bool = True
```

- [ ] **Step 2.4 : Vérifier que les tests passent**

```bash
pytest tests/domain/test_types.py -v
```
Attendu : `3 passed`

- [ ] **Step 2.5 : Vérifier mypy**

```bash
mypy domain/types.py
```
Attendu : `Success: no issues found`

- [ ] **Step 2.6 : Commit**

```bash
git add backend/domain/types.py backend/tests/domain/test_types.py
git commit -m "feat(domain): ajouter ValeurTracee et ResultatCalcul avec tests"
```

---

## Task 3 : Migration — propriétés béton vers domain/

**Files:**
- Create: `backend/domain/beton/proprietes.py`
- Create: `backend/tests/domain/beton/test_proprietes.py`

Le code source est dans `Scripts/Calculations/Concrete/concrete.py`. On le migre en le typant strictement et en ajoutant `ValeurTracee`.

- [ ] **Step 3.1 : Écrire les tests (valeurs vérifiées sur table Eurocode 2)**

`backend/tests/domain/beton/test_proprietes.py` :
```python
import pytest
from hypothesis import given, settings
import hypothesis.strategies as st
from domain.beton.proprietes import f_cm, E_cm, f_ctm, eps_cu1

def test_f_cm_C25():
    """f_cm = fck + 8 MPa. NF EN 1992-1-1 §3.1.2 Tableau 3.1."""
    result = f_cm(fck=25.0)
    assert abs(result.valeur - 33.0) < 0.01
    assert result.unite == "MPa"
    assert "1992" in result.reference

def test_f_cm_C30():
    result = f_cm(fck=30.0)
    assert abs(result.valeur - 38.0) < 0.01

def test_E_cm_C25():
    """Ecm = 22 × ((fck+8)/10)^0.3 GPa. Tableau 3.1."""
    result = E_cm(fck=25.0)
    assert abs(result.valeur - 31476.0) < 10  # en MPa

def test_f_ctm_C25():
    result = f_ctm(fck=25.0)
    assert abs(result.valeur - 2.6) < 0.05

def test_eps_cu1_C25():
    result = eps_cu1(fck=25.0)
    assert abs(result.valeur - 3.5e-3) < 1e-5

@given(st.floats(min_value=12.0, max_value=90.0))
@settings(max_examples=50)
def test_f_cm_croissant_avec_fck(fck: float) -> None:
    """La résistance moyenne augmente toujours avec fck."""
    assert f_cm(fck=fck).valeur == pytest.approx(fck + 8.0, abs=0.01)

@given(st.floats(min_value=12.0, max_value=90.0))
@settings(max_examples=50)
def test_E_cm_croissant_avec_fck(fck: float) -> None:
    """Le module de Young augmente avec fck."""
    e1 = E_cm(fck=fck).valeur
    e2 = E_cm(fck=fck + 5.0).valeur
    assert e2 > e1
```

- [ ] **Step 3.2 : Vérifier que les tests échouent**

```bash
pytest tests/domain/beton/test_proprietes.py -v
```
Attendu : `FAILED` — module introuvable

- [ ] **Step 3.3 : Créer domain/beton/proprietes.py**

```python
"""
Propriétés mécaniques du béton selon NF EN 1992-1-1 (Eurocode 2).
Référence principale : Tableau 3.1 de NF EN 1992-1-1.

Toutes les fonctions sont pures (pas d'I/O, pas de side-effects).
Résultats mis en cache (lru_cache) car les propriétés ne dépendent
que de fck et ne changent jamais pour une nuance donnée.
"""
from functools import lru_cache
from domain.types import ValeurTracee
import math


@lru_cache(maxsize=64)
def f_cm(fck: float) -> ValeurTracee:
    """
    Résistance moyenne en compression du béton.

    Référence normative : NF EN 1992-1-1 §3.1.2, Tableau 3.1.
    Hypothèses : béton à 28 jours, essai cylindrique.

    Args:
        fck: résistance caractéristique en compression [MPa]

    Returns:
        ValeurTracee avec valeur en MPa
    """
    valeur = fck + 8.0
    return ValeurTracee(
        valeur=valeur,
        unite="MPa",
        formule="f_cm = f_ck + 8",
        reference="NF EN 1992-1-1 §3.1.2 Tableau 3.1",
        inputs_utilises={"fck_mpa": fck},
    )


@lru_cache(maxsize=64)
def E_cm(fck: float) -> ValeurTracee:
    """
    Module de Young sécant du béton.

    Référence normative : NF EN 1992-1-1 §3.1.3, Tableau 3.1.

    Args:
        fck: résistance caractéristique en compression [MPa]

    Returns:
        ValeurTracee avec valeur en MPa
    """
    valeur = 22_000.0 * ((fck + 8.0) / 10.0) ** 0.3
    return ValeurTracee(
        valeur=valeur,
        unite="MPa",
        formule="E_cm = 22 000 × ((f_cm / 10)^0.3)",
        reference="NF EN 1992-1-1 §3.1.3 Tableau 3.1",
        inputs_utilises={"fck_mpa": fck},
    )


@lru_cache(maxsize=64)
def f_ctm(fck: float) -> ValeurTracee:
    """
    Résistance moyenne en traction du béton.

    Référence normative : NF EN 1992-1-1 §3.1.2, Tableau 3.1.
    """
    if fck <= 50.0:
        valeur = 0.30 * fck ** (2.0 / 3.0)
        formule = "f_ctm = 0.30 × f_ck^(2/3)  [f_ck ≤ 50 MPa]"
    else:
        valeur = 2.12 * math.log(1.0 + (fck + 8.0) / 10.0)
        formule = "f_ctm = 2.12 × ln(1 + f_cm/10)  [f_ck > 50 MPa]"
    return ValeurTracee(
        valeur=valeur,
        unite="MPa",
        formule=formule,
        reference="NF EN 1992-1-1 §3.1.2 Tableau 3.1",
        inputs_utilises={"fck_mpa": fck},
    )


@lru_cache(maxsize=64)
def eps_cu1(fck: float) -> ValeurTracee:
    """
    Déformation ultime en compression (fibre extrême).

    Référence normative : NF EN 1992-1-1 §3.1.3, Tableau 3.1.
    """
    if fck <= 50.0:
        valeur = 3.5e-3
        formule = "ε_cu1 = 3.5‰  [f_ck ≤ 50 MPa]"
    else:
        valeur = (2.8 + 27.0 * ((98.0 - (fck + 8.0)) / 100.0) ** 4) * 1e-3
        formule = "ε_cu1 = (2.8 + 27×((98-f_cm)/100)⁴)‰  [f_ck > 50 MPa]"
    return ValeurTracee(
        valeur=valeur,
        unite="—",
        formule=formule,
        reference="NF EN 1992-1-1 §3.1.3 Tableau 3.1",
        inputs_utilises={"fck_mpa": fck},
    )
```

- [ ] **Step 3.4 : Vérifier que les tests passent**

```bash
pytest tests/domain/beton/test_proprietes.py -v
```
Attendu : `7 passed` (5 unitaires + 2 hypothesis)

- [ ] **Step 3.5 : Vérifier mypy**

```bash
mypy domain/beton/proprietes.py
```
Attendu : `Success: no issues found`

- [ ] **Step 3.6 : Commit**

```bash
git add backend/domain/beton/ backend/tests/domain/beton/
git commit -m "feat(domain/beton): migrer proprietes béton EC2 avec ValeurTracee et tests hypothesis"
```

---

## Task 4 : Migration — caractéristiques sol vers domain/

**Files:**
- Create: `backend/domain/sol/caracteristiques.py`
- Create: `backend/tests/domain/sol/test_caracteristiques.py`

Source : `Scripts/Calculations/Sol/Caracteristiques.py`

- [ ] **Step 4.1 : Écrire les tests**

`backend/tests/domain/sol/test_caracteristiques.py` :
```python
import math
import pytest
from hypothesis import given, settings
import hypothesis.strategies as st
from domain.sol.caracteristiques import Ka_Rankine, Kp_Rankine

def test_Ka_sol_sableux_30deg():
    """Ka = tan²(π/4 - φ/2). Pour φ=30°, Ka ≈ 0.333."""
    result = Ka_Rankine(phi_deg=30.0, cohesion_kpa=0.0)
    assert abs(result.valeur - 0.333) < 0.002
    assert "Rankine" in result.formule
    assert "CFMS" in result.reference

def test_Ka_augmente_quand_phi_diminue():
    """Plus le sol est mauvais (φ faible), plus la poussée est grande."""
    Ka_20 = Ka_Rankine(phi_deg=20.0, cohesion_kpa=0.0).valeur
    Ka_30 = Ka_Rankine(phi_deg=30.0, cohesion_kpa=0.0).valeur
    assert Ka_20 > Ka_30

def test_Kp_superieur_a_1():
    """La butée est toujours supérieure à la poussée active."""
    Kp = Kp_Rankine(phi_deg=30.0, cohesion_kpa=0.0).valeur
    Ka = Ka_Rankine(phi_deg=30.0, cohesion_kpa=0.0).valeur
    assert Kp > 1.0
    assert Kp > Ka

@given(st.floats(min_value=5.0, max_value=44.0))
@settings(max_examples=100)
def test_Ka_toujours_positif(phi: float) -> None:
    assert Ka_Rankine(phi_deg=phi, cohesion_kpa=0.0).valeur > 0

@given(st.floats(min_value=5.0, max_value=44.0))
@settings(max_examples=100)
def test_Ka_Kp_reciproques(phi: float) -> None:
    Ka = Ka_Rankine(phi_deg=phi, cohesion_kpa=0.0).valeur
    Kp = Kp_Rankine(phi_deg=phi, cohesion_kpa=0.0).valeur
    assert abs(Ka * Kp - 1.0) < 0.001  # Ka × Kp ≈ 1 (Rankine)
```

- [ ] **Step 4.2 : Vérifier que les tests échouent**

```bash
pytest tests/domain/sol/test_caracteristiques.py -v
```
Attendu : `FAILED`

- [ ] **Step 4.3 : Créer domain/sol/caracteristiques.py**

```python
"""
Coefficients de poussée et de butée des terres.

Référence principale : CFMS 2023 §3.2 + NF P94-282.
Méthode Rankine (hypothèse sol pulvérulent, paroi lisse).
"""
import math
from functools import lru_cache
from domain.types import ValeurTracee


@lru_cache(maxsize=256)
def Ka_Rankine(phi_deg: float, cohesion_kpa: float) -> ValeurTracee:
    """
    Coefficient de poussée active des terres (Rankine).

    Référence normative : CFMS 2023 §3.2.1, NF P94-282 §A.1.
    Hypothèses : paroi lisse (δ = 0), remblai horizontal (β = 0).

    Args:
        phi_deg: angle de frottement interne [degrés]
        cohesion_kpa: cohésion non drainée [kPa]

    Returns:
        ValeurTracee avec Ka sans dimension
    """
    phi_rad = math.radians(phi_deg)
    Ka = math.tan(math.pi / 4.0 - phi_rad / 2.0) ** 2
    return ValeurTracee(
        valeur=Ka,
        unite="—",
        formule="Ka = tan²(π/4 - φ/2)  [Rankine, paroi lisse]",
        reference="CFMS 2023 §3.2.1",
        inputs_utilises={"phi_deg": phi_deg, "cohesion_kpa": cohesion_kpa},
    )


@lru_cache(maxsize=256)
def Kp_Rankine(phi_deg: float, cohesion_kpa: float) -> ValeurTracee:
    """
    Coefficient de butée passive des terres (Rankine).

    Référence normative : CFMS 2023 §3.2.2, NF P94-282 §A.2.
    Hypothèses : paroi lisse (δ = 0), remblai horizontal.

    Args:
        phi_deg: angle de frottement interne [degrés]
        cohesion_kpa: cohésion non drainée [kPa]

    Returns:
        ValeurTracee avec Kp sans dimension
    """
    phi_rad = math.radians(phi_deg)
    Kp = math.tan(math.pi / 4.0 + phi_rad / 2.0) ** 2
    return ValeurTracee(
        valeur=Kp,
        unite="—",
        formule="Kp = tan²(π/4 + φ/2)  [Rankine, paroi lisse]",
        reference="CFMS 2023 §3.2.2",
        inputs_utilises={"phi_deg": phi_deg, "cohesion_kpa": cohesion_kpa},
    )
```

- [ ] **Step 4.4 : Vérifier que les tests passent**

```bash
pytest tests/domain/sol/test_caracteristiques.py -v
```
Attendu : `7 passed`

- [ ] **Step 4.5 : Vérifier mypy**

```bash
mypy domain/sol/caracteristiques.py
```
Attendu : `Success: no issues found`

- [ ] **Step 4.6 : Commit**

```bash
git add backend/domain/sol/caracteristiques.py backend/tests/domain/sol/
git commit -m "feat(domain/sol): migrer Ka/Kp Rankine avec ValeurTracee et tests hypothesis"
```

---

## Task 5 : Premier cas de référence

**Files:**
- Create: `backend/tests/reference-cases/README.md`
- Create: `backend/tests/reference-cases/runner.py`
- Create: `backend/tests/reference-cases/cas-001/inputs.json`
- Create: `backend/tests/reference-cases/cas-001/outputs_expected.json`

- [ ] **Step 5.1 : Créer README.md des cas de référence**

`backend/tests/reference-cases/README.md` :
```markdown
# Cas de référence ViPPer

## Objectif
Chaque dossier `cas-NNN/` contient un cas de calcul vérifié manuellement
ou issu d'un calcul de référence (tableur, note de calcul validée).

Le runner compare les sorties de l'engine avec les valeurs attendues.
Une alerte est levée si l'écart dépasse 0.5% sur une valeur numérique.

## Structure d'un cas
- `inputs.json` : données d'entrée du projet
- `outputs_expected.json` : résultats attendus (calculés à la main ou via référence)
- `notes.md` (optionnel) : contexte, source, hypothèses

## Ajouter un cas
1. Créer un dossier `cas-NNN/`
2. Remplir `inputs.json` selon le schéma CalculationInput
3. Calculer les valeurs attendues (à la main ou avec le code actuel avant modification)
4. Les mettre dans `outputs_expected.json`
5. Lancer `python runner.py` pour valider
```

- [ ] **Step 5.2 : Créer inputs.json du cas-001**

`backend/tests/reference-cases/cas-001/inputs.json` :
```json
{
  "description": "Voile VPP simple, sol bicouche, sans nappe, sans buton",
  "algo_version": "1.0.0",
  "sol": {
    "1": {
      "nom": "Remblai limoneux",
      "cote_sup_m": 0.0,
      "cote_inf_m": 3.5,
      "phi_deg": 30.0,
      "cohesion_kpa": 0.0,
      "gamma_kn_m3": 18.0
    }
  },
  "chargement": {
    "surcharge_exploitation_kpa": 10.0,
    "categorie": "A"
  },
  "vpp": {
    "longueur_totale_m": 3.5,
    "largeur_m": 1.0,
    "epaisseur_m": 0.25,
    "fck_mpa": 25.0
  }
}
```

- [ ] **Step 5.3 : Créer outputs_expected.json du cas-001**

Valeurs calculées à la main :
- Ka pour φ=30° : `tan²(π/4 - 30°/2) = tan²(30°) ≈ 0.3333`
- Kp pour φ=30° : `tan²(π/4 + 30°/2) = tan²(60°) = 3.0000`

`backend/tests/reference-cases/cas-001/outputs_expected.json` :
```json
{
  "description": "Valeurs calculées à la main — Rankine sol pulvérulent φ=30°",
  "sol": {
    "1": {
      "Ka": 0.3333,
      "Kp": 3.0000
    }
  }
}
```

- [ ] **Step 5.4 : Créer runner.py**

`backend/tests/reference-cases/runner.py` :
```python
"""
Runner de non-régression pour les cas de référence ViPPer.
Lance : python tests/reference-cases/runner.py
Alerte si un écart dépasse TOLERANCE (0.5%).
"""
import json
import sys
from pathlib import Path

TOLERANCE = 0.005  # 0.5%

from domain.sol.caracteristiques import Ka_Rankine, Kp_Rankine
from domain.beton.proprietes import E_cm


def run_case(case_dir: Path) -> list[str]:
    """Retourne une liste d'erreurs (vide = succès)."""
    inputs = json.loads((case_dir / "inputs.json").read_text())
    expected = json.loads((case_dir / "outputs_expected.json").read_text())
    errors = []

    # Exemple : vérifier Ka pour chaque couche sol
    for couche_id, couche in inputs.get("sol", {}).items():
        phi = couche["phi_deg"]
        Ka_calc = Ka_Rankine(phi_deg=phi, cohesion_kpa=couche.get("cohesion_kpa", 0.0)).valeur
        Ka_exp = expected.get("sol", {}).get(couche_id, {}).get("Ka")
        if Ka_exp is not None:
            ecart = abs(Ka_calc - Ka_exp) / max(abs(Ka_exp), 1e-10)
            if ecart > TOLERANCE:
                errors.append(f"Ka couche {couche_id}: calculé={Ka_calc:.4f}, attendu={Ka_exp:.4f}, écart={ecart:.2%}")

    return errors


def main() -> None:
    cases_dir = Path(__file__).parent
    all_errors: list[str] = []

    for case_dir in sorted(cases_dir.glob("cas-*/")):
        if not (case_dir / "inputs.json").exists():
            continue
        print(f"  → {case_dir.name}", end=" ")
        errors = run_case(case_dir)
        if errors:
            print("❌ ÉCHEC")
            all_errors.extend([f"[{case_dir.name}] {e}" for e in errors])
        else:
            print("✓")

    if all_errors:
        print(f"\n{len(all_errors)} erreur(s) de non-régression :")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"\nTous les cas de référence passent.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5.5 : Vérifier que le runner passe**

```bash
cd backend
python tests/reference-cases/runner.py
```
Attendu : `✓` pour cas-001, puis `Tous les cas de référence passent.`

- [ ] **Step 5.6 : Commit**

```bash
git add backend/tests/reference-cases/
git commit -m "test: ajouter infrastructure cas de référence et premier cas (sol bicouche)"
```

---

## Task 6 : FastAPI minimal — endpoint /calculate

**Files:**
- Create: `backend/infrastructure/api/main.py`
- Create: `backend/infrastructure/api/config.py`
- Create: `backend/infrastructure/schemas/calculation.py`
- Create: `backend/infrastructure/api/routers/calculations.py`

Cette task expose le domaine via FastAPI sans toucher au code de calcul.

- [ ] **Step 6.1 : Écrire le test de sanité**

`backend/tests/test_api_health.py` :
```python
from fastapi.testclient import TestClient
from infrastructure.api.main import app

def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

- [ ] **Step 6.2 : Vérifier que le test échoue**

```bash
pytest tests/test_api_health.py -v
```
Attendu : `FAILED`

- [ ] **Step 6.3 : Créer infrastructure/schemas/calculation.py**

```python
from pydantic import BaseModel, Field
from typing import Optional

class SolCoucheInput(BaseModel):
    nom: str
    cote_sup_m: float
    cote_inf_m: float
    phi_deg: float = Field(ge=0.0, le=45.0)
    cohesion_kpa: float = Field(ge=0.0)
    gamma_kn_m3: float = Field(ge=10.0, le=30.0)

class CalculationInput(BaseModel):
    sol: dict[int, SolCoucheInput]
    algo_version: Optional[str] = None

class ValeurTraceeOut(BaseModel):
    valeur: float
    unite: str
    formule: str
    reference: str
    inputs_utilises: dict

class CalculationOutput(BaseModel):
    succes: bool
    algo_version: str
    valeurs: dict[str, ValeurTraceeOut] = {}
    messages: list[str] = []
    erreur: Optional[str] = None
```

- [ ] **Step 6.4 : Créer infrastructure/api/config.py**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    allowed_origins: str = "http://localhost:3000"
    sentry_dsn: str = ""
    algo_version: str = "1.0.0"

    class Config:
        env_file = ".env"

settings = Settings()
```

- [ ] **Step 6.5 : Créer infrastructure/api/routers/calculations.py**

```python
from fastapi import APIRouter
from infrastructure.schemas.calculation import CalculationInput, CalculationOutput, ValeurTraceeOut
from infrastructure.api.config import settings
from domain.sol.caracteristiques import Ka_Rankine, Kp_Rankine

router = APIRouter(prefix="/calculate", tags=["calculations"])

@router.post("", response_model=CalculationOutput)
def calculate(data: CalculationInput) -> CalculationOutput:
    """
    Lance les calculs ViPPer pour le projet fourni.
    Retourne les résultats avec traçabilité normative complète.
    """
    try:
        valeurs: dict[str, ValeurTraceeOut] = {}
        messages: list[str] = []

        for idx, couche in data.sol.items():
            Ka = Ka_Rankine(phi_deg=couche.phi_deg, cohesion_kpa=couche.cohesion_kpa)
            Kp = Kp_Rankine(phi_deg=couche.phi_deg, cohesion_kpa=couche.cohesion_kpa)

            valeurs[f"Ka_couche_{idx}"] = ValeurTraceeOut(
                valeur=Ka.valeur, unite=Ka.unite,
                formule=Ka.formule, reference=Ka.reference,
                inputs_utilises=Ka.inputs_utilises,
            )
            valeurs[f"Kp_couche_{idx}"] = ValeurTraceeOut(
                valeur=Kp.valeur, unite=Kp.unite,
                formule=Kp.formule, reference=Kp.reference,
                inputs_utilises=Kp.inputs_utilises,
            )
            messages.append(f"Couche {idx} ({couche.nom}) : Ka={Ka.valeur:.3f}, Kp={Kp.valeur:.3f}")

        return CalculationOutput(
            succes=True,
            algo_version=settings.algo_version,
            valeurs=valeurs,
            messages=messages,
        )

    except Exception as e:
        return CalculationOutput(succes=False, algo_version=settings.algo_version, erreur=str(e))
```

- [ ] **Step 6.6 : Créer infrastructure/api/main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.api.config import settings
from infrastructure.api.routers import calculations

app = FastAPI(
    title="ViPPer API",
    version=settings.algo_version,
    description="Pré-dimensionnement VPP — CFMS 2023",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculations.router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "algo_version": settings.algo_version}
```

- [ ] **Step 6.7 : Vérifier que les tests passent**

```bash
pytest tests/test_api_health.py -v
```
Attendu : `1 passed`

- [ ] **Step 6.8 : Tester l'API manuellement**

```bash
uvicorn infrastructure.api.main:app --reload --app-dir backend
# Ouvrir http://localhost:8000/docs
# Tester POST /calculate avec le payload du cas-001
# Vérifier que Ka_couche_1 = 0.333 avec référence "CFMS 2023 §3.2.1"
```

- [ ] **Step 6.9 : Commit**

```bash
git add backend/infrastructure/ backend/tests/test_api_health.py
git commit -m "feat(api): FastAPI endpoint /calculate et /health avec traçabilité ValeurTracee"
```

---

## Checklist de validation Phase 1

Avant de passer en Phase 2 (Fly.io + Docker) :

- [ ] `pytest backend/tests/ -v` — tous les tests passent
- [ ] `python backend/tests/reference-cases/runner.py` — tous les cas passent
- [ ] `mypy backend/domain/ --strict` — aucune erreur
- [ ] `ruff check backend/domain/` — aucune erreur
- [ ] `GET /health` répond `{"status": "ok"}`
- [ ] `POST /calculate` avec le payload cas-001 retourne Ka=0.333 avec référence CFMS 2023
- [ ] Au moins 1 cas de référence dans `tests/reference-cases/`

---

## Ce qui n'est PAS dans ce plan (Phases suivantes)

- Dockerfile + Fly.io (Phase 2)
- Frontend Next.js (Phase 3)
- Auth Supabase + Stripe (Phase 4)
- Migration complète de tous les modules (BeamFEM, chargement, combinaisons, armatures) → à faire module par module en suivant le même pattern que Tasks 3 et 4
- Calculs liernes, fondations de butons, butons → à implémenter dans domain/ en suivant le même pattern
