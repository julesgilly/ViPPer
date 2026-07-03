# ViPPer SaaS — Phase 1 MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformer l'engine de calcul ViPPer Python/Qt en application web fonctionnelle (FastAPI backend + React frontend + auth Supabase), accessible par des beta-testeurs.

**Architecture:** FastAPI expose l'engine de calcul Python existant via une API REST. React (Vite + TypeScript) fournit l'interface avec trois zones : schéma SVG central dynamique, onglets de saisie à droite, console en bas. Supabase gère l'authentification (JWT) et la base de données (profiles + projects).

**Tech Stack:** Python 3.11+, FastAPI, Pydantic v2, pytest · React 18, TypeScript, Vite, @supabase/supabase-js · Supabase (PostgreSQL + Auth) · Vercel (frontend) · Railway (backend)

---

## Scope Check

Ce plan couvre uniquement la Phase 1 (MVP). Les paiements Stripe sont hors-scope (Phase 2). L'export PDF est hors-scope (Phase 3).

---

## File Structure

```
vipper-saas/                         ← nouveau dossier racine du projet SaaS
├── backend/
│   ├── main.py                      # App FastAPI, CORS, montage des routers
│   ├── config.py                    # Settings Pydantic (env vars : SUPABASE_URL, etc.)
│   ├── dependencies.py              # Dependency get_current_user (vérif JWT Supabase)
│   ├── routers/
│   │   ├── calculations.py          # POST /calculate
│   │   └── projects.py              # GET/POST/PUT/DELETE /projects
│   ├── schemas/
│   │   ├── calculation.py           # Pydantic : CalculationInput, CalculationOutput
│   │   └── project.py               # Pydantic : ProjectCreate, ProjectUpdate, ProjectOut
│   ├── engine/                      # Copie du dossier Scripts/ existant (sans Qt)
│   │   ├── Calculations/
│   │   │   ├── Data/
│   │   │   ├── Sol/
│   │   │   ├── Chargement/
│   │   │   ├── Combinaisons/
│   │   │   ├── Sollicitations/
│   │   │   ├── Armatures/
│   │   │   └── Concrete/
│   │   └── __init__.py
│   ├── tests/
│   │   ├── conftest.py              # Client FastAPI de test, fixtures
│   │   ├── test_health.py           # Test GET /health
│   │   ├── test_schemas.py          # Tests validation Pydantic
│   │   ├── test_calculations.py     # Tests endpoint /calculate
│   │   └── test_projects.py         # Tests CRUD /projects
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx                  # Router React (react-router-dom)
│   │   ├── lib/
│   │   │   ├── supabase.ts          # Client Supabase singleton
│   │   │   └── api.ts               # Fetch wrapper vers le backend FastAPI
│   │   ├── pages/
│   │   │   ├── Auth/
│   │   │   │   └── LoginPage.tsx    # Formulaire login/signup Supabase
│   │   │   └── Calculator/
│   │   │       └── CalculatorPage.tsx  # Page principale (assemble les 3 zones)
│   │   ├── components/
│   │   │   ├── SchemaViewer/
│   │   │   │   ├── index.tsx        # Conteneur SVG + sélecteur de vue
│   │   │   │   └── renderers/
│   │   │   │       └── GeoRenderer.tsx  # Rendu schéma géotechnique (Phase 1)
│   │   │   ├── InputPanel/
│   │   │   │   ├── index.tsx        # Conteneur onglets + nav Précédent/Suivant
│   │   │   │   └── tabs/
│   │   │   │       ├── ProjetTab.tsx
│   │   │   │       ├── SolTab.tsx
│   │   │   │       ├── ChargementTab.tsx
│   │   │   │       ├── BetonTab.tsx
│   │   │   │       └── VPPTab.tsx
│   │   │   └── AppConsole/
│   │   │       └── index.tsx        # Console bas (messages horodatés)
│   │   ├── hooks/
│   │   │   ├── useCalculation.ts    # Appel POST /calculate + état résultats
│   │   │   └── useProject.ts        # Auto-save (Phase 1) + stub CRUD (Phase 2)
│   │   └── types/
│   │       └── vipper.ts            # Types TypeScript partagés (CalculationInput, etc.)
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── supabase/
│   └── migrations/
│       ├── 001_profiles.sql         # Table profiles + trigger auto-création
│       └── 002_projects.sql         # Table projects + RLS policies
│
└── README.md
```

---

## Task 1 : Initialisation du monorepo

**Files:**
- Create: `vipper-saas/backend/requirements.txt`
- Create: `vipper-saas/backend/.env.example`
- Create: `vipper-saas/frontend/package.json` (via Vite CLI)

- [ ] **Step 1.1 : Créer la structure de dossiers**

```bash
mkdir -p vipper-saas/backend/routers vipper-saas/backend/schemas vipper-saas/backend/engine vipper-saas/backend/tests
mkdir -p vipper-saas/frontend vipper-saas/supabase/migrations
```

- [ ] **Step 1.2 : Créer le projet React avec Vite**

```bash
cd vipper-saas/frontend
npm create vite@latest . -- --template react-ts
npm install
npm install @supabase/supabase-js react-router-dom
```

- [ ] **Step 1.3 : Créer requirements.txt backend**

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic-settings==2.2.1
pydantic==2.7.0
python-jose[cryptography]==3.3.0
httpx==0.27.0
pytest==8.2.0
pytest-asyncio==0.23.6
numpy>=1.26.0
```

- [ ] **Step 1.4 : Créer .env.example**

```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_JWT_SECRET=your-jwt-secret-from-supabase-dashboard
ALLOWED_ORIGINS=http://localhost:5173
```

- [ ] **Step 1.5 : Copier l'engine de calcul**

```bash
cp -r "Scripts/Calculations" vipper-saas/backend/engine/
cp -r "Scripts/__init__.py" vipper-saas/backend/engine/
# NE PAS copier Scripts/Windows/ ni Scripts/Drawings/ (dépendances Qt non nécessaires)
```

- [ ] **Step 1.6 : Installer les dépendances backend**

```bash
cd vipper-saas/backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

- [ ] **Step 1.7 : Commit**

```bash
git add vipper-saas/
git commit -m "chore: initialiser monorepo ViPPer SaaS (backend FastAPI + frontend React)"
```

---

## Task 2 : Supabase — tables et sécurité

**Files:**
- Create: `vipper-saas/supabase/migrations/001_profiles.sql`
- Create: `vipper-saas/supabase/migrations/002_projects.sql`

Prérequis : créer un projet sur [supabase.com](https://supabase.com), récupérer l'URL et les clés dans Settings → API.

- [ ] **Step 2.1 : Créer 001_profiles.sql**

```sql
-- Table profiles (extension de auth.users)
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  company TEXT,
  phone TEXT,
  stripe_customer_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Création automatique du profil à l'inscription
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id)
  VALUES (NEW.id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "users can view own profile"
  ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "users can update own profile"
  ON profiles FOR UPDATE USING (auth.uid() = id);
```

- [ ] **Step 2.2 : Créer 002_projects.sql**

```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  client TEXT,
  data JSONB DEFAULT '{}',
  results JSONB DEFAULT '{}',
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Mise à jour auto de updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON projects
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- RLS : chaque utilisateur ne voit que ses projets
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
CREATE POLICY "users see own projects"
  ON projects FOR ALL USING (auth.uid() = user_id);
```

- [ ] **Step 2.3 : Exécuter les migrations**

Dans le dashboard Supabase → SQL Editor, coller et exécuter chaque fichier dans l'ordre.

- [ ] **Step 2.4 : Vérifier dans Table Editor**

Les tables `profiles` et `projects` doivent apparaître avec RLS activé (icône cadenas).

- [ ] **Step 2.5 : Récupérer le JWT secret**

Dans Supabase → Settings → API → JWT Secret. Copier dans `.env` local :
```
SUPABASE_JWT_SECRET=<valeur>
SUPABASE_URL=https://<ref>.supabase.co
```

- [ ] **Step 2.6 : Commit**

```bash
git add vipper-saas/supabase/
git commit -m "feat(db): ajouter tables profiles et projects avec RLS Supabase"
```

---

## Task 3 : Backend FastAPI — config et auth

**Files:**
- Create: `vipper-saas/backend/config.py`
- Create: `vipper-saas/backend/dependencies.py`
- Create: `vipper-saas/backend/main.py`
- Create: `vipper-saas/backend/tests/conftest.py`

- [ ] **Step 3.1 : Écrire le test de sanité**

`vipper-saas/backend/tests/conftest.py` :
```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)
```

`vipper-saas/backend/tests/test_health.py` :
```python
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 3.2 : Vérifier que le test échoue**

```bash
cd vipper-saas/backend
pytest tests/test_health.py -v
```
Attendu : `FAILED` — `ModuleNotFoundError: No module named 'main'`

- [ ] **Step 3.3 : Créer config.py**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_jwt_secret: str
    allowed_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()
```

- [ ] **Step 3.4 : Créer dependencies.py**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config import settings

bearer = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
        )
```

- [ ] **Step 3.5 : Créer main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

app = FastAPI(title="ViPPer API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 3.6 : Vérifier que le test passe**

```bash
pytest tests/test_health.py -v
```
Attendu : `PASSED`

- [ ] **Step 3.7 : Commit**

```bash
git add vipper-saas/backend/
git commit -m "feat(backend): initialiser FastAPI avec config Pydantic et auth JWT Supabase"
```

---

## Task 4 : Schemas Pydantic pour les calculs

**Files:**
- Create: `vipper-saas/backend/schemas/calculation.py`
- Create: `vipper-saas/backend/tests/test_schemas.py`

L'objectif est de définir la forme exacte des données qui entrent dans l'engine. Partir du dictionnaire utilisé dans `Scripts/Calculations/main_calculation.py` comme référence.

- [ ] **Step 4.1 : Écrire les tests de validation**

`vipper-saas/backend/tests/test_schemas.py` :
```python
from schemas.calculation import SolCouche, CalculationInput
import pytest

def test_sol_couche_valid():
    couche = SolCouche(
        nom="Limons",
        cote_sup=0.0,
        cote_inf=3.0,
        type_sol="Limons",
        cohesion_court_terme=0.0,
        cohesion_long_terme=0.0,
        angle_frottement_ct=30.0,
        angle_frottement_lt=30.0,
        masse_volumique=22.0,
        pression_limite=1.0,
        module_pressiometrique=1.0,
        coefficient_rheologique=1.0,
    )
    assert couche.angle_frottement_ct == 30.0

def test_sol_couche_angle_hors_borne():
    with pytest.raises(ValueError):
        SolCouche(
            nom="X", cote_sup=0, cote_inf=1, type_sol="Argiles",
            cohesion_court_terme=0, cohesion_long_terme=0,
            angle_frottement_ct=50,  # > 45 → invalide
            angle_frottement_lt=30, masse_volumique=22,
            pression_limite=1, module_pressiometrique=1,
            coefficient_rheologique=1,
        )

def test_masse_volumique_hors_borne():
    with pytest.raises(ValueError):
        SolCouche(
            nom="X", cote_sup=0, cote_inf=1, type_sol="Argiles",
            cohesion_court_terme=0, cohesion_long_terme=0,
            angle_frottement_ct=30, angle_frottement_lt=30,
            masse_volumique=5,  # < 10 → invalide
            pression_limite=1, module_pressiometrique=1,
            coefficient_rheologique=1,
        )
```

- [ ] **Step 4.2 : Vérifier que les tests échouent**

```bash
pytest tests/test_schemas.py -v
```
Attendu : `FAILED` — `ModuleNotFoundError: No module named 'schemas'`

- [ ] **Step 4.3 : Créer schemas/calculation.py**

```python
from pydantic import BaseModel, Field
from typing import Optional

class SolCouche(BaseModel):
    nom: str
    cote_sup: float
    cote_inf: float
    type_sol: str
    cohesion_court_terme: float = Field(ge=0)
    cohesion_long_terme: float = Field(ge=0)
    angle_frottement_ct: float = Field(ge=0, le=45)
    angle_frottement_lt: float = Field(ge=0, le=45)
    masse_volumique: float = Field(ge=10, le=30)
    pression_limite: float = Field(ge=0)
    module_pressiometrique: float = Field(ge=0)
    coefficient_rheologique: float = Field(ge=0)

class ProjetInput(BaseModel):
    nom: str
    categorie: str
    ingenieur: str
    niveau_eau: int = Field(ge=0, le=2)
    seisme: int = Field(ge=0, le=1)
    pression_limite_defaut: float = Field(ge=0)

class CalculationInput(BaseModel):
    projet: ProjetInput
    sol: dict[int, SolCouche]
    # Les autres sections (chargement, beton, vpp) seront ajoutées
    # au fur et à mesure que les onglets sont implémentés

class CalculationOutput(BaseModel):
    success: bool
    messages: list[str] = []
    results: Optional[dict] = None
    error: Optional[str] = None
```

- [ ] **Step 4.4 : Vérifier que les tests passent**

```bash
pytest tests/test_schemas.py -v
```
Attendu : `3 passed`

- [ ] **Step 4.5 : Commit**

```bash
git add vipper-saas/backend/schemas/ vipper-saas/backend/tests/test_schemas.py
git commit -m "feat(backend): ajouter schemas Pydantic pour validation entrées calcul"
```

---

## Task 5 : Endpoint POST /calculate

**Files:**
- Create: `vipper-saas/backend/routers/calculations.py`
- Modify: `vipper-saas/backend/main.py`
- Create: `vipper-saas/backend/tests/test_calculations.py`

- [ ] **Step 5.1 : Écrire les tests**

`vipper-saas/backend/tests/test_calculations.py` :
```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

VALID_INPUT = {
    "projet": {
        "nom": "Test",
        "categorie": "Catégorie A: habitation, zones résidentielles",
        "ingenieur": "Test Ingenieur",
        "niveau_eau": 0,
        "seisme": 0,
        "pression_limite_defaut": 100,
    },
    "sol": {
        "1": {
            "nom": "Limons",
            "cote_sup": 0.0,
            "cote_inf": 3.0,
            "type_sol": "Limons",
            "cohesion_court_terme": 0.0,
            "cohesion_long_terme": 0.0,
            "angle_frottement_ct": 30.0,
            "angle_frottement_lt": 30.0,
            "masse_volumique": 22.0,
            "pression_limite": 1.0,
            "module_pressiometrique": 1.0,
            "coefficient_rheologique": 1.0,
        }
    }
}

def test_calculate_sans_auth_retourne_401():
    response = client.post("/calculate", json=VALID_INPUT)
    assert response.status_code == 401

def test_calculate_donnees_invalides_retourne_422():
    bad_input = {**VALID_INPUT, "sol": {"1": {"angle_frottement_ct": 99}}}
    # On mock l'auth pour tester la validation Pydantic
    with patch("routers.calculations.get_current_user", return_value={"sub": "test-user-id"}):
        response = client.post("/calculate", json=bad_input)
    assert response.status_code == 422
```

- [ ] **Step 5.2 : Vérifier que les tests échouent**

```bash
pytest tests/test_calculations.py::test_calculate_sans_auth_retourne_401 -v
```
Attendu : `FAILED` — route `/calculate` inexistante (404, pas 401)

- [ ] **Step 5.3 : Créer routers/calculations.py**

```python
from fastapi import APIRouter, Depends
from schemas.calculation import CalculationInput, CalculationOutput
from dependencies import get_current_user
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'engine'))

router = APIRouter(prefix="/calculate", tags=["calculations"])

@router.post("", response_model=CalculationOutput)
def calculate(
    data: CalculationInput,
    current_user: dict = Depends(get_current_user),
) -> CalculationOutput:
    """
    Lance le calcul ViPPer avec les données fournies.
    Retourne les résultats ou les messages d'erreur.
    """
    try:
        # Conversion du schema Pydantic vers le format dict attendu par l'engine
        # Les clés du dict sol sont déjà des int (Pydantic v2 coerce str→int automatiquement)
        sol_dict = {
            k: {
                "Nom de la couche": v.nom,
                "Cote supérieure": v.cote_sup,
                "Cote inférieure": v.cote_inf,
                "Type de sol": v.type_sol,
                "Cohésion court terme": v.cohesion_court_terme,
                "Cohésion long terme": v.cohesion_long_terme,
                "Angle de frottement court terme": v.angle_frottement_ct,
                "Angle de frottement long terme": v.angle_frottement_lt,
                "Masse volumique": v.masse_volumique,
                "Pression limite": v.pression_limite,
                "Module pressiométrique Ménard": v.module_pressiometrique,
                "Coefficient rhéologique": v.coefficient_rheologique,
            }
            for k, v in data.sol.items()
        }

        # NOTE: L'appel à l'engine sera complété au fur et à mesure
        # que les autres onglets (chargement, béton, VPP) sont intégrés.
        # Pour le MVP Phase 1, on retourne une réponse de succès partielle.
        return CalculationOutput(
            success=True,
            messages=["Données sol reçues et validées"],
            results={"sol": sol_dict},
        )

    except Exception as e:
        return CalculationOutput(success=False, error=str(e))
```

- [ ] **Step 5.4 : Enregistrer le router dans main.py**

Ajouter dans `main.py` :
```python
from routers import calculations, projects
app.include_router(calculations.router)
app.include_router(projects.router)
```

- [ ] **Step 5.5 : Vérifier que les tests passent**

```bash
pytest tests/test_calculations.py -v
```
Attendu : `2 passed`

- [ ] **Step 5.6 : Tester manuellement**

```bash
uvicorn main:app --reload
# Ouvrir http://localhost:8000/docs → tester POST /calculate
```

- [ ] **Step 5.7 : Commit**

```bash
git add vipper-saas/backend/routers/calculations.py vipper-saas/backend/main.py vipper-saas/backend/tests/test_calculations.py
git commit -m "feat(backend): ajouter endpoint POST /calculate avec auth JWT"
```

---

## Task 6 : Endpoint CRUD /projects

**Files:**
- Create: `vipper-saas/backend/routers/projects.py`
- Create: `vipper-saas/backend/schemas/project.py`
- Create: `vipper-saas/backend/tests/test_projects.py`

- [ ] **Step 6.1 : Ajouter supabase_anon_key dans config.py**

Ajouter le champ dans `config.py` (avant de créer le router qui l'utilise) :
```python
supabase_anon_key: str  # clé "anon" publique depuis Supabase → Settings → API
```

Et dans `.env` local et `.env.example` :
```
SUPABASE_ANON_KEY=your-anon-key
```

- [ ] **Step 6.2 : Écrire les tests (TDD)**

`vipper-saas/backend/tests/test_projects.py` :
```python
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

def test_list_projects_sans_auth_retourne_401():
    response = client.get("/projects")
    assert response.status_code == 401

def test_create_project_sans_auth_retourne_401():
    response = client.post("/projects", json={"name": "Test"})
    assert response.status_code == 401
```

- [ ] **Step 6.3 : Créer schemas/project.py**

```python
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    client: Optional[str] = None
    data: dict = {}

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    client: Optional[str] = None
    data: Optional[dict] = None
    results: Optional[dict] = None

class ProjectOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    client: Optional[str]
    data: dict
    results: dict
    updated_at: datetime
```

- [ ] **Step 6.4 : Vérifier que les tests échouent**

```bash
pytest tests/test_projects.py -v
```
Attendu : `FAILED` (404 — router pas encore monté)

- [ ] **Step 6.5 : Créer routers/projects.py**

```python
from fastapi import APIRouter, Depends, HTTPException
from schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from dependencies import get_current_user
import httpx
from config import settings
import uuid

router = APIRouter(prefix="/projects", tags=["projects"])

def supabase_headers(token: str) -> dict:
    """Headers pour les requêtes directes à l'API REST Supabase."""
    return {
        "apikey": settings.supabase_anon_key,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

# NOTE : Pour le MVP Phase 1, les opérations CRUD passent par l'API REST
# Supabase (pas de client Python officiel requis). En Phase 2 on pourra
# utiliser supabase-py si nécessaire.

@router.get("", response_model=list[ProjectOut])
async def list_projects(current_user: dict = Depends(get_current_user)):
    async with httpx.AsyncClient() as http:
        response = await http.get(
            f"{settings.supabase_url}/rest/v1/projects",
            headers=supabase_headers(current_user["_raw_token"]),
            params={"select": "*", "order": "updated_at.desc"},
        )
    response.raise_for_status()
    return response.json()

@router.post("", response_model=ProjectOut, status_code=201)
async def create_project(
    project: ProjectCreate,
    current_user: dict = Depends(get_current_user),
):
    payload = {
        "user_id": current_user["sub"],
        "name": project.name,
        "client": project.client,
        "data": project.data,
    }
    async with httpx.AsyncClient() as http:
        response = await http.post(
            f"{settings.supabase_url}/rest/v1/projects",
            headers=supabase_headers(current_user["_raw_token"]),
            json=payload,
        )
    response.raise_for_status()
    return response.json()[0]

@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: uuid.UUID,
    project: ProjectUpdate,
    current_user: dict = Depends(get_current_user),
):
    payload = project.model_dump(exclude_none=True)
    async with httpx.AsyncClient() as http:
        response = await http.patch(
            f"{settings.supabase_url}/rest/v1/projects",
            headers=supabase_headers(current_user["_raw_token"]),
            params={"id": f"eq.{project_id}"},
            json=payload,
        )
    response.raise_for_status()
    data = response.json()
    if not data:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    return data[0]

@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
):
    async with httpx.AsyncClient() as http:
        response = await http.delete(
            f"{settings.supabase_url}/rest/v1/projects",
            headers=supabase_headers(current_user["_raw_token"]),
            params={"id": f"eq.{project_id}"},
        )
    response.raise_for_status()
```

> **Note :** `current_user["_raw_token"]` nécessite de stocker le token brut dans la dépendance. Modifier `dependencies.py` pour ajouter `payload["_raw_token"] = token` avant le return.

- [ ] **Step 6.6 : Modifier dependencies.py pour passer le token brut**

```python
# Dans get_current_user, avant return payload :
payload["_raw_token"] = token
return payload
```

- [ ] **Step 6.7 : Vérifier que les tests passent**

```bash
pytest tests/test_projects.py -v
```
Attendu : `2 passed`

- [ ] **Step 6.8 : Commit**

```bash
git add vipper-saas/backend/routers/projects.py vipper-saas/backend/schemas/project.py vipper-saas/backend/tests/test_projects.py vipper-saas/backend/dependencies.py vipper-saas/backend/config.py
git commit -m "feat(backend): ajouter CRUD projets via API REST Supabase"
```

---

## Task 7 : Frontend — Setup et auth Supabase

**Files:**
- Create: `vipper-saas/frontend/src/lib/supabase.ts`
- Create: `vipper-saas/frontend/src/App.tsx`
- Create: `vipper-saas/frontend/src/pages/Auth/LoginPage.tsx`

- [ ] **Step 7.1 : Créer lib/supabase.ts**

```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

- [ ] **Step 7.2 : Créer .env.local dans frontend/**

```
VITE_SUPABASE_URL=https://<ref>.supabase.co
VITE_SUPABASE_ANON_KEY=<ta-clé-anon>
VITE_API_URL=http://localhost:8000
```

- [ ] **Step 7.3 : Créer pages/Auth/LoginPage.tsx**

```tsx
import { useState } from 'react'
import { supabase } from '../../lib/supabase'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSignup, setIsSignup] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (isSignup) {
      const { error } = await supabase.auth.signUp({ email, password })
      if (error) setMessage(error.message)
      else setMessage('Compte créé — vérifiez votre email.')
    } else {
      const { error } = await supabase.auth.signInWithPassword({ email, password })
      if (error) setMessage(error.message)
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: '4rem auto', padding: '2rem' }}>
      <h1>ViPPer</h1>
      <h2>{isSignup ? 'Créer un compte' : 'Connexion'}</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" value={email} onChange={e => setEmail(e.target.value)}
          placeholder="Email" required style={{ display: 'block', width: '100%', marginBottom: '1rem' }} />
        <input type="password" value={password} onChange={e => setPassword(e.target.value)}
          placeholder="Mot de passe" required style={{ display: 'block', width: '100%', marginBottom: '1rem' }} />
        <button type="submit" style={{ width: '100%' }}>
          {isSignup ? 'Créer le compte' : 'Se connecter'}
        </button>
      </form>
      {message && <p>{message}</p>}
      <button onClick={() => setIsSignup(!isSignup)} style={{ marginTop: '1rem', background: 'none', border: 'none', cursor: 'pointer', textDecoration: 'underline' }}>
        {isSignup ? 'Déjà un compte ? Se connecter' : 'Pas de compte ? S\'inscrire'}
      </button>
    </div>
  )
}
```

- [ ] **Step 7.4 : Créer App.tsx avec routing**

```tsx
import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Session } from '@supabase/supabase-js'
import { supabase } from './lib/supabase'
import LoginPage from './pages/Auth/LoginPage'
import CalculatorPage from './pages/Calculator/CalculatorPage'

export default function App() {
  const [session, setSession] = useState<Session | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setLoading(false)
    })
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })
    return () => subscription.unsubscribe()
  }, [])

  if (loading) return <div>Chargement…</div>

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={!session ? <LoginPage /> : <Navigate to="/" />} />
        <Route path="/" element={session ? <CalculatorPage /> : <Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  )
}
```

- [ ] **Step 7.5 : Créer CalculatorPage.tsx (placeholder)**

```tsx
import { supabase } from '../../lib/supabase'

export default function CalculatorPage() {
  return (
    <div>
      <h1>ViPPer — Calcul</h1>
      <button onClick={() => supabase.auth.signOut()}>Se déconnecter</button>
      {/* Les composants SchemaViewer, InputPanel, AppConsole seront ajoutés en Task 8 */}
    </div>
  )
}
```

- [ ] **Step 7.6 : Tester manuellement**

```bash
cd vipper-saas/frontend
npm run dev
# Ouvrir http://localhost:5173
# Tester : inscription → vérifier email → connexion → page Calculator
```

- [ ] **Step 7.7 : Commit**

```bash
git add vipper-saas/frontend/src/
git commit -m "feat(frontend): ajouter auth Supabase (login/signup) et routing React"
```

---

## Task 8 : Frontend — Layout principal (3 zones)

**Files:**
- Create: `vipper-saas/frontend/src/pages/Calculator/CalculatorPage.tsx`
- Create: `vipper-saas/frontend/src/components/AppConsole/index.tsx`
- Create: `vipper-saas/frontend/src/components/InputPanel/index.tsx`
- Create: `vipper-saas/frontend/src/components/SchemaViewer/index.tsx`

- [ ] **Step 8.1 : Créer AppConsole/index.tsx**

```tsx
export type ConsoleMessage = {
  id: number
  timestamp: string
  level: 'success' | 'warning' | 'error' | 'info'
  text: string
}

type Props = { messages: ConsoleMessage[]; onClear: () => void }

const levelColors = {
  success: '#34d399',
  warning: '#fbbf24',
  error: '#f87171',
  info: '#94a3b8',
}

const levelIcons = { success: '✔', warning: '⚠', error: '✗', info: '→' }

export default function AppConsole({ messages, onClear }: Props) {
  return (
    <div style={{ height: 120, background: '#020617', borderTop: '1px solid #1e293b', display: 'flex', flexDirection: 'column' }}>
      <div style={{ padding: '0.3rem 0.8rem', background: '#0a0f1e', borderBottom: '1px solid #1e293b', display: 'flex', justifyContent: 'space-between' }}>
        <span style={{ fontSize: '0.62rem', color: '#475569', textTransform: 'uppercase', letterSpacing: 1 }}>Console</span>
        <button onClick={onClear} style={{ fontSize: '0.6rem', color: '#475569', background: 'none', border: 'none', cursor: 'pointer' }}>🗑 Effacer</button>
      </div>
      <div style={{ flex: 1, overflowY: 'auto', padding: '0.4rem 0.8rem', fontFamily: 'monospace', fontSize: '0.68rem', lineHeight: 1.8 }}>
        {messages.map(msg => (
          <div key={msg.id}>
            <span style={{ color: '#475569' }}>[{msg.timestamp}]</span>{' '}
            <span style={{ color: levelColors[msg.level] }}>{levelIcons[msg.level]}</span>{' '}
            <span style={{ color: levelColors[msg.level] }}>{msg.text}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
```

- [ ] **Step 8.2 : Créer SchemaViewer/index.tsx (placeholder Phase 1)**

```tsx
import { useState } from 'react'

type View = 'geo' | 'mf_elu' | 'et_elu' | 'deformee' | 'ratios'

type Props = { data: Record<string, unknown> }

const VIEWS: { key: View; label: string }[] = [
  { key: 'geo', label: 'Schéma géo.' },
  { key: 'mf_elu', label: 'M.F. ELU' },
  { key: 'et_elu', label: 'E.T. ELU' },
  { key: 'deformee', label: 'Déformée' },
  { key: 'ratios', label: 'Ratios' },
]

export default function SchemaViewer({ data }: Props) {
  const [activeView, setActiveView] = useState<View>('geo')

  return (
    <div style={{ flex: 1, background: '#0a0f1e', display: 'flex', flexDirection: 'column', borderRight: '1px solid #1e293b' }}>
      {/* Sélecteur de vue */}
      <div style={{ padding: '0.4rem 0.8rem', background: '#0f172a', borderBottom: '1px solid #1e293b', display: 'flex', gap: '0.5rem' }}>
        {VIEWS.map(v => (
          <button key={v.key} onClick={() => setActiveView(v.key)}
            style={{ fontSize: '0.7rem', padding: '0.15rem 0.5rem', borderRadius: 4, cursor: 'pointer',
              background: activeView === v.key ? '#1e293b' : 'transparent',
              color: activeView === v.key ? '#e2e8f0' : '#64748b',
              border: 'none' }}>
            {v.label}
          </button>
        ))}
      </div>
      {/* Zone SVG — GeoRenderer sera branché ici en Task 9 */}
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <span style={{ color: '#1e293b', fontSize: '0.75rem' }}>
          {activeView === 'geo' ? 'Schéma géotechnique (saisir les données pour afficher)' : `Vue "${activeView}" disponible après calcul`}
        </span>
      </div>
    </div>
  )
}
```

- [ ] **Step 8.3 : Créer InputPanel/index.tsx**

```tsx
import { useState } from 'react'
import ProjetTab from './tabs/ProjetTab'
import SolTab from './tabs/SolTab'
import ChargementTab from './tabs/ChargementTab'
import BetonTab from './tabs/BetonTab'
import VPPTab from './tabs/VPPTab'

const TABS = [
  { key: 'projet', label: '📋 Projet', component: ProjetTab },
  { key: 'sol', label: '🏔 Sol', component: SolTab },
  { key: 'chargement', label: '⬇️ Charges', component: ChargementTab },
  { key: 'beton', label: '🧱 Béton', component: BetonTab },
  { key: 'vpp', label: '🏗 VPP', component: VPPTab },
]

type Props = {
  data: Record<string, unknown>
  onChange: (section: string, value: unknown) => void
}

export default function InputPanel({ data, onChange }: Props) {
  const [activeTab, setActiveTab] = useState(0)
  const ActiveComponent = TABS[activeTab].component

  return (
    <div style={{ width: 280, background: '#0f172a', display: 'flex', flexDirection: 'column' }}>
      {/* Onglets */}
      <div style={{ display: 'flex', overflowX: 'auto', background: '#0a0f1e', borderBottom: '1px solid #1e293b' }}>
        {TABS.map((tab, i) => (
          <button key={tab.key} onClick={() => setActiveTab(i)}
            style={{ padding: '0.4rem 0.6rem', fontSize: '0.65rem', whiteSpace: 'nowrap',
              borderRight: '1px solid #1e293b', background: activeTab === i ? '#0f172a' : 'transparent',
              color: activeTab === i ? '#e2e8f0' : '#64748b',
              border: 'none', borderBottom: activeTab === i ? '2px solid #4f46e5' : 'none',
              cursor: 'pointer' }}>
            {tab.label}
          </button>
        ))}
      </div>
      {/* Contenu onglet */}
      <div style={{ flex: 1, padding: '0.8rem', overflowY: 'auto' }}>
        <ActiveComponent data={data} onChange={(v: unknown) => onChange(TABS[activeTab].key, v)} />
      </div>
      {/* Navigation */}
      <div style={{ padding: '0.5rem 0.8rem', borderTop: '1px solid #1e293b', display: 'flex', gap: '0.4rem' }}>
        <button onClick={() => setActiveTab(Math.max(0, activeTab - 1))} disabled={activeTab === 0}
          style={{ flex: 1, background: '#1e293b', border: '1px solid #334155', borderRadius: 4, padding: '0.3rem', fontSize: '0.68rem', color: '#94a3b8', cursor: 'pointer' }}>
          ← Précédent
        </button>
        <button onClick={() => setActiveTab(Math.min(TABS.length - 1, activeTab + 1))} disabled={activeTab === TABS.length - 1}
          style={{ flex: 1, background: '#4f46e5', border: 'none', borderRadius: 4, padding: '0.3rem', fontSize: '0.68rem', color: 'white', fontWeight: 'bold', cursor: 'pointer' }}>
          Suivant →
        </button>
      </div>
    </div>
  )
}
```

- [ ] **Step 8.4 : Créer les tabs (placeholders)**

Créer `ProjetTab.tsx`, `SolTab.tsx`, `ChargementTab.tsx`, `BetonTab.tsx`, `VPPTab.tsx` avec le même template minimal :

```tsx
// Exemple pour ProjetTab.tsx — répéter pour les autres
type Props = { data: unknown; onChange: (v: unknown) => void }

export default function ProjetTab({ data, onChange }: Props) {
  return (
    <div>
      <p style={{ color: '#64748b', fontSize: '0.75rem' }}>
        Section Projet — à compléter selon le schéma Data.Projet
      </p>
    </div>
  )
}
```

- [ ] **Step 8.5 : Assembler CalculatorPage.tsx**

```tsx
import { useState, useCallback } from 'react'
import SchemaViewer from '../../components/SchemaViewer'
import InputPanel from '../../components/InputPanel'
import AppConsole, { ConsoleMessage } from '../../components/AppConsole'
import { supabase } from '../../lib/supabase'

let msgId = 0
function makeMsg(level: ConsoleMessage['level'], text: string): ConsoleMessage {
  return { id: msgId++, timestamp: new Date().toLocaleTimeString(), level, text }
}

export default function CalculatorPage() {
  const [projectData, setProjectData] = useState<Record<string, unknown>>({})
  const [messages, setMessages] = useState<ConsoleMessage[]>([
    makeMsg('info', 'ViPPer prêt. Commencez par renseigner les données Projet.'),
  ])

  const addMessage = useCallback((level: ConsoleMessage['level'], text: string) => {
    setMessages(prev => [...prev, makeMsg(level, text)])
  }, [])

  const handleSectionChange = (section: string, value: unknown) => {
    setProjectData(prev => ({ ...prev, [section]: value }))
    addMessage('success', `Section "${section}" mise à jour — schéma actualisé`)
  }

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', background: '#0a0f1e', color: '#e2e8f0' }}>
      {/* Toolbar */}
      <div style={{ padding: '0.4rem 1rem', background: '#0f172a', borderBottom: '1px solid #1e293b', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontWeight: 'bold', color: '#818cf8' }}>⚙️ ViPPer 3.0</span>
        <div style={{ display: 'flex', gap: '1rem', fontSize: '0.75rem' }}>
          <span style={{ color: '#34d399' }}>💾 Sauvegardé</span>
          <button style={{ background: '#4f46e5', color: 'white', border: 'none', borderRadius: 4, padding: '0.15rem 0.6rem', cursor: 'pointer', opacity: 0.5 }}>
            📄 Note de calcul
          </button>
          <button onClick={() => supabase.auth.signOut()} style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', fontSize: '0.75rem' }}>
            Se déconnecter
          </button>
        </div>
      </div>

      {/* Zone principale */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        <SchemaViewer data={projectData} />
        <InputPanel data={projectData} onChange={handleSectionChange} />
      </div>

      {/* Console */}
      <AppConsole messages={messages} onClear={() => setMessages([])} />
    </div>
  )
}
```

- [ ] **Step 8.6 : Tester visuellement**

```bash
npm run dev
```
Vérifier : layout 3 zones visible, onglets cliquables, console affiche les messages.

- [ ] **Step 8.7 : Commit**

```bash
git add vipper-saas/frontend/src/
git commit -m "feat(frontend): layout principal 3 zones (schéma central, onglets saisie, console)"
```

---

## Task 9 : Frontend — Connexion API et auto-save

**Files:**
- Create: `vipper-saas/frontend/src/lib/api.ts`
- Create: `vipper-saas/frontend/src/hooks/useCalculation.ts`
- Create: `vipper-saas/frontend/src/hooks/useProject.ts`
- Modify: `vipper-saas/frontend/src/pages/Calculator/CalculatorPage.tsx`

- [ ] **Step 9.1 : Créer lib/api.ts**

```typescript
import { supabase } from './supabase'

const API_URL = import.meta.env.VITE_API_URL as string

async function getAuthHeaders(): Promise<Record<string, string>> {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) throw new Error('Non authentifié')
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${session.access_token}`,
  }
}

export async function calculateApi(data: unknown) {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/calculate`, {
    method: 'POST',
    headers,
    body: JSON.stringify(data),
  })
  if (!response.ok) throw new Error(`Erreur API: ${response.status}`)
  return response.json()
}

export async function listProjectsApi() {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/projects`, { headers })
  if (!response.ok) throw new Error(`Erreur API: ${response.status}`)
  return response.json()
}

export async function updateProjectApi(id: string, data: unknown) {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/projects/${id}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(data),
  })
  if (!response.ok) throw new Error(`Erreur API: ${response.status}`)
  return response.json()
}
```

- [ ] **Step 9.2 : Créer hooks/useProject.ts (auto-save + stub CRUD Phase 2)**

```typescript
import { useEffect, useRef } from 'react'
import { updateProjectApi } from '../lib/api'

// Auto-save — utilisé en Phase 1
export function useAutoSave(
  projectId: string | null,
  data: Record<string, unknown>,
  onSaved: () => void,
  onError: (msg: string) => void,
) {
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    if (!projectId) return
    if (timerRef.current) clearTimeout(timerRef.current)

    timerRef.current = setTimeout(async () => {
      try {
        await updateProjectApi(projectId, { data })
        onSaved()
      } catch {
        onError('Erreur sauvegarde automatique')
      }
    }, 2000) // debounce 2 secondes

    return () => {
      if (timerRef.current) clearTimeout(timerRef.current)
    }
  }, [data, projectId])
}

// Stub CRUD — sera complété en Phase 2 (dashboard projets)
export function useProject() {
  // TODO Phase 2: listProjects, createProject, deleteProject
  return {}
}
```

- [ ] **Step 9.3 : Intégrer useAutoSave dans CalculatorPage.tsx**

Dans `CalculatorPage.tsx`, ajouter `projectId` dans les états et appeler `useAutoSave` :
```tsx
import { useAutoSave } from '../../hooks/useProject'

// Dans le composant, après les useState existants :
const [projectId] = useState<string | null>(null) // null en Phase 1 — Phase 2 utilisera l'ID du projet sélectionné

useAutoSave(
  projectId,
  projectData,
  () => addMessage('info', 'Projet sauvegardé'),
  (msg) => addMessage('error', msg),
)
```

- [ ] **Step 9.4 : Tester l'appel API depuis le frontend**

```bash
# Terminal 1 : backend
cd vipper-saas/backend && uvicorn main:app --reload
# Terminal 2 : frontend
cd vipper-saas/frontend && npm run dev
```
Modifier des données dans un onglet, vérifier que la console affiche "Section mise à jour".

- [ ] **Step 9.5 : Commit**

```bash
git add vipper-saas/frontend/src/lib/api.ts vipper-saas/frontend/src/hooks/
git commit -m "feat(frontend): connexion API FastAPI + auto-save debounce 2s"
```

---

## Task 10 : Déploiement

**Files:**
- Create: `vipper-saas/backend/Procfile` (Railway)
- Create: `vipper-saas/frontend/.env.production`

- [ ] **Step 10.1 : Créer Procfile pour Railway**

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

- [ ] **Step 10.2 : Pousser sur GitHub**

Créer d'abord le dépôt sur github.com (bouton "New repository", nom : `vipper-saas`), puis :
```bash
cd vipper-saas
git remote add origin https://github.com/VOTRE_COMPTE_GITHUB/vipper-saas.git
# Remplacer VOTRE_COMPTE_GITHUB par ton nom d'utilisateur GitHub
git push -u origin main
```

- [ ] **Step 10.3 : Déployer le backend sur Railway**

1. Aller sur [railway.app](https://railway.app) → New Project → Deploy from GitHub
2. Sélectionner le repo → Root Directory : `backend`
3. Ajouter les variables d'environnement (SUPABASE_URL, SUPABASE_JWT_SECRET, SUPABASE_ANON_KEY, ALLOWED_ORIGINS)
4. Récupérer l'URL Railway générée (ex: `https://vipper-api.up.railway.app`)

- [ ] **Step 10.4 : Déployer le frontend sur Vercel**

1. Aller sur [vercel.com](https://vercel.com) → New Project → Import GitHub
2. Root Directory : `frontend`
3. Ajouter les variables d'environnement (VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY, VITE_API_URL=URL Railway)
4. Deploy

- [ ] **Step 10.5 : Mettre à jour ALLOWED_ORIGINS**

Dans Railway, mettre à jour `ALLOWED_ORIGINS` avec l'URL Vercel générée (ex: `https://vipper.vercel.app`).

- [ ] **Step 10.6 : Tester en production**

- Ouvrir l'URL Vercel
- S'inscrire avec un email (vérifier la réception de l'email Supabase)
- Se connecter → vérifier que la page Calculator s'affiche
- Vérifier que les logs Railway ne montrent pas d'erreurs CORS

- [ ] **Step 10.7 : Commit final**

```bash
git add vipper-saas/backend/Procfile
git commit -m "chore: ajouter config déploiement Railway (Procfile)"
git push
```

---

## Checklist de validation Phase 1

Avant de passer en Phase 2, vérifier :

- [ ] `pytest` passe sans erreur sur le backend
- [ ] `npm run build` passe sans erreur TypeScript
- [ ] Un utilisateur peut s'inscrire, se connecter, et accéder à la page Calculator
- [ ] Le layout 3 zones est affiché (schéma centre, onglets droite, console bas)
- [ ] L'endpoint `POST /calculate` répond avec les données sol validées
- [ ] L'application est déployée et accessible depuis un navigateur externe
- [ ] Accès restreint : seuls les utilisateurs inscrits peuvent accéder (pas de calcul anonyme)

---

## Ce qui n'est PAS dans ce plan (Phase 2 + 3)

- Stripe Checkout, webhooks, abonnements (`subscriptions` table)
- Dashboard liste des projets
- Export PDF note de calcul (WeasyPrint)
- Tests unitaires engine de calcul (pytest sur BeamFEM, butee, etc.)
- Optimisations numpy + lru_cache
- Onboarding utilisateur
