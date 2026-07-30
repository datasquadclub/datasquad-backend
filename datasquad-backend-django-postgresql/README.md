# Data Squad — Backend de suivi des visites (Django + PostgreSQL)

Guide pas-à-pas pour quelqu'un qui n'a jamais déployé de backend. Aucune
commande dans un terminal n'est nécessaire pour la mise en ligne : tout se
fait dans des interfaces web (GitHub, Railway, Netlify).

Deux morceaux à héberger séparément :
- **le site statique** (le zip du site) → hébergé sur **Netlify** (gratuit)
- **ce backend Django + PostgreSQL** → hébergé sur **Railway** (quelques $/mois,
  offre d'essai gratuite au départ)

## Étape 1 — Mettre ce dossier sur GitHub

1. Créez un compte sur https://github.com si vous n'en avez pas.
2. Cliquez sur "New repository" (bouton vert). Nom: `datasquad-backend`.
   Laissez "Public" ou "Private" selon votre préférence. Ne cochez rien
   d'autre. Cliquez "Create repository".
3. Sur la page qui suit, cliquez le lien "uploading an existing file".
4. Glissez-déposez TOUT le contenu de ce dossier `backend/` (pas le dossier
   lui-même, son contenu : `config/`, `tracking/`, `Dockerfile`, `manage.py`,
   `requirements.txt`, etc.) dans la zone de dépôt.
5. Cliquez "Commit changes".

## Étape 2 — Créer le backend sur Railway

1. Allez sur https://railway.app et créez un compte (le plus simple:
   "Sign in with GitHub").
2. Cliquez "New Project" → "Deploy from GitHub repo" → choisissez
   `datasquad-backend`. Railway détecte automatiquement le `Dockerfile` et
   lance la construction.
3. Ajoutez la base de données : dans votre projet Railway, cliquez "New" →
   "Database" → "Add PostgreSQL". Un service Postgres apparaît à côté de
   votre service web.
4. Reliez les deux : cliquez sur votre service **web** (celui du backend) →
   onglet "Variables" → "New Variable" → "Add Reference" (ou "Add a
   Reference Variable") → sélectionnez le service Postgres → choisissez
   `DATABASE_URL`. Railway remplit automatiquement la connexion, vous
   n'avez rien à taper.
5. Toujours dans "Variables" de votre service web, ajoutez ces variables
   une par une (bouton "New Variable") :

   | Nom | Valeur |
   |---|---|
   | `DJANGO_SECRET_KEY` | une longue chaîne aléatoire (ex: collez 40 caractères au hasard, lettres+chiffres) |
   | `DJANGO_DEBUG` | `False` |
   | `DJANGO_SUPERUSER_USERNAME` | `admin` (ou ce que vous voulez) |
   | `DJANGO_SUPERUSER_EMAIL` | votre email |
   | `DJANGO_SUPERUSER_PASSWORD` | un mot de passe solide |

6. Générez le domaine public : onglet "Settings" du service web → section
   "Networking" → "Generate Domain". Railway vous donne une URL du type
   `https://datasquad-backend-production.up.railway.app`. **Notez-la**,
   vous en aurez besoin à l'étape 4.
7. Ajoutez encore deux variables (maintenant que vous avez l'URL) :

   | Nom | Valeur |
   |---|---|
   | `DJANGO_ALLOWED_HOSTS` | `datasquad-backend-production.up.railway.app` (votre vraie URL, sans `https://`) |
   | `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://datasquad-backend-production.up.railway.app` (avec `https://` cette fois) |

8. Railway redéploie automatiquement à chaque variable ajoutée (ou cliquez
   "Deploy" en haut à droite). Attendez que le statut passe au vert.
9. Testez : ouvrez `https://VOTRE-URL.up.railway.app/admin/` dans le
   navigateur. Vous devez voir la page de connexion Django. Connectez-vous
   avec le `DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_PASSWORD` définis
   plus haut — le compte a été créé automatiquement au démarrage.

Si `/admin/` ne s'affiche pas, cliquez sur votre service → onglet
"Deployments" → dernier déploiement → "View Logs" pour voir l'erreur.

## Étape 3 — Mettre le site en ligne sur Netlify

1. Allez sur https://app.netlify.com/drop
2. Glissez-déposez le dossier du site (celui du zip
   `datasquad-site-avec-tracking`, dézippé) directement sur la page.
3. Netlify vous donne une URL du type `https://joyful-panda-123.netlify.app`
   en quelques secondes. C'est en ligne.
4. (Optionnel) Renommez-la : "Site settings" → "Change site name" pour
   avoir quelque chose comme `datasquad.netlify.app`.

## Étape 4 — Connecter le site au backend

Les deux étant sur des domaines différents, deux réglages sont nécessaires :

**A. Autoriser le site à parler au backend (CORS)**
Sur Railway, service web → "Variables" → ajoutez :

| Nom | Valeur |
|---|---|
| `CORS_ALLOWED_ORIGINS` | `https://VOTRE-SITE.netlify.app` (l'URL exacte de l'étape 3) |

**B. Dire au site où se trouve le backend**
Sur votre ordinateur, ouvrez le fichier `assets/app.js` du site (dans un
éditeur de texte simple : Bloc-notes sur Windows, TextEdit sur Mac) et
repérez cette ligne près du début :

```js
var TRACK_URL = window.DS_TRACK_ENDPOINT || '/api/track/';
```

Remplacez `'/api/track/'` par l'URL complète de votre backend Railway,
par exemple :

```js
var TRACK_URL = window.DS_TRACK_ENDPOINT || 'https://datasquad-backend-production.up.railway.app/api/track/';
```

Enregistrez le fichier, puis re-glissez tout le dossier du site sur
https://app.netlify.com — il retrouve automatiquement votre site existant
et remplace juste les fichiers.

## Étape 5 — Vérifier que ça marche

1. Ouvrez votre site Netlify, naviguez sur 2-3 pages.
2. Allez sur `https://VOTRE-BACKEND.up.railway.app/admin/tracking/visit/`
   → vos visites doivent apparaître.
3. Allez sur `.../admin/tracking/visit/dashboard/` pour le tableau de bord.

## Gérer le contenu du site (actualités & équipe)

Une fois connecté sur `/admin/`, deux nouvelles sections apparaissent :

- **Actualités** → ajouter/modifier/dépublier les actus affichées sur la
  page "Actualités" du site (titre, date affichée en texte libre, texte,
  photo optionnelle, ordre d'affichage).
- **Équipe** → idem pour les fiches de la page "Équipe" (nom, rôle,
  description, photo, ordre).

Chaque fiche a une case **"Publié sur le site"** : décochez-la pour la
masquer sans la supprimer (brouillon). Le site relit ce contenu à chaque
chargement de page — pas besoin de redéployer le site pour publier une
actu ou modifier l'équipe, ça apparaît immédiatement.

**Important — limite actuelle** : ce contenu dynamique n'alimente que les
pages **françaises** (`actualites.html`, `equipe.html`). Les versions
anglaise et arabe restent telles quelles (statiques) pour l'instant. Si
vous voulez qu'elles soient aussi gérées depuis l'admin, il faudra ajouter
des champs de traduction — dites-le si vous en avez besoin.

**Sécurité** : si vous n'ajoutez rien dans l'admin, le contenu déjà présent
dans les pages HTML reste affiché tel quel (rien ne se vide). Le contenu de
l'admin ne remplace l'affichage que lorsqu'il y a au moins une actu / un
membre publié.

## Photos et médias — persistance sur Railway

Les photos que vous uploadez dans l'admin (actus, équipe) sont enregistrées
dans le dossier `media/` du conteneur. **Problème** : sur Railway (et la
plupart des hébergeurs par conteneurs), ce dossier est effacé à chaque
redéploiement, sauf si vous attachez un **Volume**.

Pour l'activer :
1. Sur Railway, cliquez sur votre service `datasquad-backend` → onglet
   **"Settings"** → section **"Volumes"** → **"Add Volume"**.
2. Mount path : `/app/media`
3. Sauvegardez. Railway redéploie automatiquement.

Sans ce volume, tout fonctionne quand même, mais une photo uploadée
disparaîtra au prochain déploiement du backend (le texte, lui, reste
toujours en sécurité dans PostgreSQL).



Connecté sur `/admin/` : **Authentification et autorisation → Utilisateurs
→ Ajouter un utilisateur**. Cochez "Statut équipe" pour donner accès au
panneau. Ne cochez "Statut super-utilisateur" que pour les personnes de
confiance.

## Aucune donnée personnelle sensible

On stocke : IP, user-agent, page visitée, référent, et un identifiant
aléatoire (cookie). Aucun nom, email ou mot de passe des visiteurs. Ajoutez
une courte mention "Statistiques de visite anonymes" dans vos mentions
légales.

---

## Alternative : lancer en local sur votre ordinateur (pour tester avant de déployer)

Si vous voulez d'abord voir le résultat sur votre propre machine, il faut
Docker Desktop (https://www.docker.com/products/docker-desktop) et un
terminal :

```bash
cp .env.example .env
# ouvrez .env et remplissez au moins DJANGO_SECRET_KEY et un mot de passe
docker compose up --build
```

Le backend écoute sur `http://localhost:8000`, l'admin sur
`http://localhost:8000/admin/` (le compte admin défini dans `.env` est créé
automatiquement au démarrage — aucune commande `createsuperuser` à taper).

## Structure du projet

```
backend/
├── config/            # réglages Django (settings, urls, wsgi)
├── tracking/           # app: modèle Visit, endpoint /api/track/, dashboard, création admin auto
├── content/             # app: Actualités & Équipe (CMS géré depuis /admin/), API publique
├── entrypoint.sh        # migrate + création admin + lancement serveur (utilisé par Railway/Docker)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml   # pour tester en local uniquement
└── .env.example
```
