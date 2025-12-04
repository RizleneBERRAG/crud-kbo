Documentation du projet CRUD KBO
1. Introduction

Ce projet a pour objectif de développer une application permettant de gérer des entreprises et leurs unités d’établissement à partir des données publiques de la Banque-Carrefour des Entreprises (BCE / KBO).
L’application met en place un ensemble complet d’opérations CRUD (Create, Read, Update, Delete) sur les entités suivantes : activités, entreprises et établissements.

Les données proviennent des fichiers CSV fournis par la plateforme Open Data de la BCE et sont importées dans une base SQLite via un script Python dédié.

L’application backend est développée en FastAPI.

2. Choix techniques
2.1 Langage et Framework

Langage : Python

Framework web : FastAPI

Serveur : Uvicorn

Justification : FastAPI permet de créer rapidement une API moderne, typée, performante, avec documentation automatique (Swagger / Redoc).

2.2 Base de données

SGBD : SQLite

ORM : SQLAlchemy

Justification :
SQLite est suffisante pour un projet scolaire et ne nécessite aucune installation.
SQLAlchemy permet une gestion propre des modèles, des relations et des migrations éventuelles.

2.3 Architecture du projet
crud-kbo/
│
├── backend/
│   ├── main.py              (app FastAPI, routes)
│   ├── models.py            (tables SQLAlchemy)
│   ├── schemas.py           (Pydantic pour validations et réponses API)
│   ├── database.py          (connexion SQLite)
│   ├── import_kbo.py        (script d'import CSV → SQLite)
│
├── data/
│   ├── activity.csv
│   ├── enterprise.csv
│   ├── establishment.csv
│   └── kbo.sqlite3          (base de données générée)
│
└── docs/
    ├── base_de_donnees.md   (documentation structure BD)
    └── documentation_projet.md (ce document)

3. Modèle de données

Le modèle repose sur trois tables principales.

3.1 Table activities

Contient les codes NACE provenant du fichier officiel KBO.

Champs importants :

id

nace_code

activity_group

nace_version

classification

Relation : une activité peut être associée à plusieurs entreprises, via companies.activity_code.

3.2 Table companies

Représente les entreprises enregistrées.

Champs importants :

id

name

legal_form

street, number, postcode, city

country

activity_code (FK vers activities.nace_code)

enterprise_number (unique)

Relation : une entreprise possède plusieurs établissements.

3.3 Table establishments

Représente les unités d’établissement d’une entreprise.

Champs importants :

id

name

street, number, postcode, city

country

establishment_number (unique si présent)

company_id (FK vers companies.id)

Relation : plusieurs établissements sont liés à une seule entreprise.

4. Importation des données KBO

Les données CSV sont importées grâce au script :

python -m backend.import_kbo


Le script exécute trois étapes :

Importer les activités (activity.csv)

Importer les entreprises (enterprise.csv)

Importer les établissements et les lier aux entreprises (establishment.csv)

Lors de l’import :

les doublons sont ignorés

les colonnes sont détectées automatiquement même si leur format varie

les liens entre entreprises et établissements sont vérifiés par numéro KBO

5. API et opérations CRUD

Toutes les routes sont disponibles dans la documentation automatique FastAPI à l’URL suivante :

http://127.0.0.1:8000/docs

5.1 Entreprises (/companies)
Créer une entreprise
POST /companies


Validation d’un code NACE obligatoire.

Lire la liste des entreprises
GET /companies

Lire une entreprise spécifique
GET /companies/{company_id}

Modifier une entreprise
PUT /companies/{company_id}

Supprimer une entreprise (+ suppression en cascade des établissements)
DELETE /companies/{company_id}

5.2 Établissements (/establishments)
Ajouter un établissement à une entreprise
POST /companies/{company_id}/establishments

Lire les établissements d’une entreprise
GET /companies/{company_id}/establishments

Lire un établissement spécifique
GET /establishments/{establishment_id}

Modifier un établissement
PUT /establishments/{establishment_id}

Supprimer un établissement
DELETE /establishments/{establishment_id}

6. Démarrage de l'application
6.1 Préparation (à faire une seule fois)

Importer les données :

python -m backend.import_kbo

6.2 Lancer le serveur FastAPI
python -m uvicorn backend.main:app --reload


L’API sera disponible sur :

http://127.0.0.1:8000/
http://127.0.0.1:8000/docs

7. Conclusion

Le projet implémente l’ensemble des fonctionnalités demandées :

importation des données KBO

base de données structurée

API CRUD complète pour entreprises et établissements

vérification des codes d’activité

documentation de la base et du fonctionnement du projet

Ce document constitue la documentation technique obligatoire du livrable.