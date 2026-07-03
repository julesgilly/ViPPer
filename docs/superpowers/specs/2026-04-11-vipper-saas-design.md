# ViPPer SaaS — Design Specification
Date: 2026-04-12 (révisé)
Auteur: Jules GILLY (avec Claude)

---

## Contexte

ViPPer est un outil de **pré-dimensionnement** des écrans de soutènement de type Voiles Par Passes alternées (VPP), développé en Python. Il s'adresse aux ingénieurs BET structure (2-15 ans d'expérience) travaillant en réhabilitation urbaine.

**Positionnement strict** : outil d'avant-projet, pas de calcul EXE. Il ne remplace pas le jugement de l'ingénieur ni les calculs d'interaction sol-structure (MISS, Plaxis). Ce positionnement est reflété dans l'UI, les CGV, et toutes les notes PDF générées.

**Référentiel normatif** : Recommandations CFMS 2023 · NF P94-282 · Eurocodes 2 et 7.

**Marché cible** : 200-500 BETs / entreprises spécialisées en France traitant les VPP. Petit marché identifiable et joignable directement.

**Contrainte principale** : développeur solo avec ~5-10h/semaine disponibles. L'architecture doit rester la plus simple possible.

---

## Décisions clés

| Décision | Choix | Raison |
|----------|-------|--------|
| Positionnement | Pré-dimensionnement uniquement | Responsabilité limitée, marché bien délimité |
| Scope | VPP uniquement (12 premiers mois) | Focus stratégique, pas de dilution |
| Backend | FastAPI (Python) | Réutilise l'engine Python, API auto-documentée |
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui | SSR, SEO, routing intégré, composants prêts |
| Base de données | Supabase (PostgreSQL + Auth) | Auth intégrée, RLS, free tier généreux |
| Hébergement backend | Fly.io + Docker | Process persistant, free tier, plus flexible que Railway |
| Hébergement frontend | Vercel | Déploiement Next.js natif, gratuit |
| Paiements | Stripe | Standard SaaS, Checkout hébergé, webhooks |
| Emails transactionnels | Resend | Simple, 3 000 emails/mois gratuits |
| Monitoring | Sentry | Free tier, alertes d'erreurs en production |
| Génération PDF | WeasyPrint (HTML → PDF côté serveur) | En Python, pas de dépendance Node |
| Facturation | Par utilisateur (mensuel / annuel) | Modèle le plus simple avec Stripe |
| Files d'attente | Aucune pour le MVP | YAGNI — mesurer d'abord avec cProfile |

---

## Architecture globale

```
Vercel (Next.js 14)
      ↕ HTTPS / REST API
Fly.io (FastAPI + engine ViPPer)
      ↕
Supabase (PostgreSQL + Auth)  +  Stripe (abonnements)
                              +  Resend (emails)
                              +  Sentry (monitoring)
```

### Séparation en 3 couches (obligatoire)

```
backend/
├── domain/          ← calculs purs. Fonctions typées, sans I/O, sans framework.
│   ├── sol/         ← poussée des terres, caractéristiques sol, eau
│   ├── chargement/  ← surcharges, combinaisons ELU/ELS
│   ├── sollicitations/ ← BeamFEM, moments, efforts tranchants
│   ├── beton/       ← propriétés béton (Ec, fcm, fctm…)
│   └── armatures/   ← ferraillage flexion, cisaillement, cuvelage
├── application/     ← orchestration. Reçoit une requête, assemble le domaine.
│   └── calcul_vpp.py
└── infrastructure/  ← FastAPI, Supabase, PDF, emails, auth
    ├── api/
    ├── database/
    └── pdf/
```

**Règle** : le code dans `domain/` ne connaît pas FastAPI, Supabase, ni même `httpx`. Il prend des nombres typés, retourne des nombres typés. Testable en isolation totale.

---

## Traçabilité des résultats

Chaque valeur calculée porte sa justification normative via une dataclass commune :

```python
from dataclasses import dataclass

@dataclass
class ValeurTracee:
    valeur: float
    unite: str
    formule: str        # ex: "Ka = tan²(π/4 - φ/2)"
    reference: str      # ex: "CFMS 2023 §3.2.1"
    inputs_utilises: dict
```

**Toute fonction du domaine retourne des `ValeurTracee`** — ou une dataclass qui en contient. Les notes PDF sont générées à partir de ces objets : chaque ligne de résultat est automatiquement justifiée.

---

## Versioning des algorithmes

Chaque projet stocke `algo_version: "x.y.z"`. Les versions antérieures restent déployées (branche git + tag Docker) pour garantir la reproductibilité. Un calcul fait aujourd'hui doit donner exactement le même résultat dans 3 ans, même après évolution de l'engine.

Format : `MAJOR.MINOR.PATCH`
- MAJOR : changement de méthode de calcul (résultats différents)
- MINOR : ajout de vérification ou de sortie (rétrocompatible)
- PATCH : correction de bug (résultats corrigés, anciens projets doivent être recalculés)

---

## Base de données (Supabase)

### Tables

**`auth.users`** — gérée par Supabase Auth

**`profiles`** — informations complémentaires
- `id` uuid → auth.users.id
- `full_name` text
- `company` text
- `stripe_customer_id` text
- `created_at` timestamptz

**`subscriptions`** — synchronisée via webhooks Stripe
- `id` uuid PRIMARY KEY
- `user_id` uuid → profiles.id
- `stripe_subscription_id` text
- `plan` text — `'monthly'` | `'annual'`
- `status` text — `'active'` | `'canceled'` | `'past_due'`
- `algo_version` text — version de l'engine au moment de la souscription
- `current_period_end` timestamptz

**`projects`** — projets de pré-dimensionnement
- `id` uuid PRIMARY KEY
- `user_id` uuid → profiles.id
- `name` text
- `client` text
- `algo_version` text — version utilisée pour ce projet
- `data` jsonb — données saisies (sol, charges, béton, VPP…)
- `results` jsonb — résultats avec ValeurTracee sérialisés
- `updated_at` timestamptz

### Sécurité

Row Level Security (RLS) sur toutes les tables :
```sql
CREATE POLICY "users see own projects"
ON projects FOR ALL USING (auth.uid() = user_id);
```

---

## Paiements (Stripe)

### Flux d'abonnement

1. Inscription (Supabase Auth)
2. Choix du plan → FastAPI crée une Stripe Checkout Session
3. Paiement sur page Stripe hébergée
4. Webhook `checkout.session.completed` → FastAPI met à jour `subscriptions`
5. Accès débloqué

### Webhooks à gérer

| Événement | Action |
|-----------|--------|
| `checkout.session.completed` | Créer l'abonnement en BDD |
| `customer.subscription.updated` | Mettre à jour plan / renouvellement |
| `customer.subscription.deleted` | Révoquer l'accès |
| `invoice.payment_failed` | Email Resend de relance + accès suspendu |

### Sécurité des webhooks
```python
stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
```

### Période de grâce `past_due`

7 jours après `current_period_end` avant révocation. Route protection : `status IN ('active', 'past_due') AND current_period_end + 7 days > NOW()`.

### Portail client

`POST /billing/portal` → URL Stripe Customer Portal (changement de plan, annulation, factures, CB).

### Tarification

- **Mensuel** : 49,99 €/mois
- **Annuel** : 39,99 €/mois (468 €/an — 2,5 mois offerts)

---

## UX/UI — Layout principal (Phase 4)

L'interface de calcul est organisée en trois zones :

### Centre — Schéma dynamique SVG
- S'actualise en temps réel à chaque modification
- Sélecteur de vue : **Schéma géo.** / **M.F. ELU** / **E.T. ELU** / **Déformée** / **Ratios**
- Rendu SVG côté client (React dans Next.js)

### Droite — Onglets de saisie
Onglets : **Projet** / **Sol** / **Charges** / **Béton** / **VPP**
- Navigation Précédent / Suivant
- Validation en temps réel → messages → console

### Bas — Console
- Horodatage · code couleur (vert/orange/rouge) · bouton Effacer

### Toolbar
- Statut auto-save (debounce 2s, données partielles sauvegardées telles quelles)
- Bouton "Note de calcul PDF" (Phase 4)
- Identité utilisateur

---

## Stratégie de tests

### Tests unitaires (pytest)
Un fichier de test par module `domain/`. Chaque fonction testée avec ≥5 cas connus (valeurs calculées à la main ou issues de la littérature).

### Tests de propriétés (hypothesis)
Invariants physiques vérifiés automatiquement :
```python
@given(st.floats(min_value=0, max_value=45), st.floats(min_value=10, max_value=30))
def test_poussee_croissante_avec_hauteur(phi, gamma):
    r1 = calcul_poussee(hauteur=3.0, phi=phi, gamma=gamma)
    r2 = calcul_poussee(hauteur=4.0, phi=phi, gamma=gamma)
    assert r2.Ka_valeur > r1.Ka_valeur  # augmenter h augmente les efforts
```

### Tests de non-régression (cas de référence)
Dossier `tests/reference-cases/` : ≥30 cas JSON avec inputs + outputs attendus.
Runner exécuté à chaque release, alerte si écart > 0,5%.

### CI (GitHub Actions)
pytest + mypy --strict + ruff check à chaque push sur main.

---

## Conventions de code

**Python :**
- Python 3.11+, type hints stricts, `mypy --strict`
- `ruff format` + `ruff check`
- Docstrings style Google avec section "Référence normative" pour chaque fonction de calcul
- Unités dans les noms de variables quand ambigu : `hauteur_m`, `contrainte_kpa`

**TypeScript (frontend) :**
- TypeScript strict
- Composants serveur Next.js par défaut, `"use client"` uniquement si nécessaire
- shadcn/ui pour les composants, Tailwind pour le styling
- Routes API dans `/app/api`

**Git :**
- Commits conventionnels : `feat:`, `fix:`, `refactor:`, `test:`, `docs:`
- Branches feature pour chaque nouvelle fonction de calcul
- Pas de commit direct sur main pour le code de calcul

---

## Phases de développement

### Phase 1 — Finaliser l'engine en local *(priorité immédiate)*
1. Refactoring architecture : séparation `domain/application/infrastructure`
2. Implémentation `ValeurTracee` sur tout le code existant
3. Calcul et vérification des liernes
4. Calcul des fondations de butons
5. Calcul et vérification des butons (flambement, assemblages, phases provisoires)
6. Vérification exhaustive conformité CFMS 2023
7. Constitution de ≥30 cas de référence testés
8. Profiling ciblé (uniquement les hotspots réels)

### Phase 2 — Wrapper FastAPI
1. Validation Pydantic des inputs
2. Endpoints `POST /calculate`, CRUD `/projects`
3. Dockerfile + config Fly.io
4. Déploiement initial
5. Rate limiting + CORS + Sentry

### Phase 3 — Interface web minimale *(pour beta-testeurs)*
- Next.js — **1 seule page fonctionnelle**
- Formulaire inputs → appel API → affichage résultats
- Export PDF basique (WeasyPrint)
- **Pas d'auth, pas de paiement**
- Accès restreint par liste blanche d'emails (env var)
- Dogfooding sur projets Koncrete

### Phase 4 — Productisation
1. Auth Supabase (inscription, connexion, JWT)
2. Table `subscriptions` + webhooks Stripe
3. Stripe Checkout + Customer Portal
4. UI complète (layout 3 zones validé)
5. Dashboard multi-projets
6. PDF pro (entête, hypothèses, formules, `ValeurTracee`, visuels)
7. Landing page + tunnel de conversion
8. CGV rédigées par avocat spécialisé BTP/IT
9. RC pro informatique souscrite

### Phase 5 — Lancement
- Post LinkedIn avec histoire personnelle
- Emails ciblés aux BETs du réseau
- Articles techniques (LinkedIn long format ou revue CTB)
- Contact auteurs CFMS 2023

---

## Hors-scope (12 premiers mois)

- Calcul MISS / interaction sol-structure dynamique
- Calcul temporel ou dynamique
- Autres techniques de soutènement (berlinoises, parois moulées, clouées)
- Application mobile native
- Multi-tenant complexe (comptes cabinet) avant 20+ clients payants
- Files d'attente (Celery, Redis) tant que les calculs restent < 5s en médiane

---

## Rappels stratégiques

- **Ne jamais élargir le scope** aux autres techniques pendant 12 mois
- **Architecture simple** : un service backend, une DB, pas de micro-services
- **Calculs : review ligne par ligne obligatoire** — Claude génère, le dev review
- **UI et infra** : Claude peut être plus libre (erreurs rattrapables)
- **Optimisations** : mesurer d'abord (cProfile), optimiser seulement les hotspots réels
