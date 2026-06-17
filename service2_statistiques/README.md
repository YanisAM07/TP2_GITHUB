# Service 2 — API de Fonctions Statistiques

## Description

Ce microservice expose une API REST développée avec Flask permettant de réaliser plusieurs calculs statistiques sur des données transmises au format JSON.

Le service utilise les bibliothèques suivantes :

* Flask
* NumPy
* SciPy

Les fonctionnalités proposées sont :

* Statistiques descriptives
* Corrélation de Pearson
* Test de normalité de Shapiro-Wilk
* Test t de Student

---

# Installation

## Création de l'environnement virtuel

```bash
cd service2_statistiques

python -m venv venv
```

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## Installation des dépendances

```bash
pip install flask numpy scipy
```

## Génération du fichier requirements.txt

```bash
pip freeze > requirements.txt
```

---

# Lancement du serveur

```bash
python app.py
```

Le serveur démarre sur :

```text
http://localhost:5002
```

---

# Structure du projet

```text
service2_statistiques/
│
├── app.py
├── requirements.txt
├── tests/
│   ├── test_client.py
│   └── test_html.html
│
└── README.md
```

---

# Routes disponibles

## 1. Description statistique

### Endpoint

```http
POST /stats/describe
```

### Exemple de requête

```json
{
    "data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]
}
```

### Exemple de réponse

```json
{
    "operation": "description",
    "resultat": {
        "n": 8,
        "moyenne": 13.6875,
        "mediane": 12.85,
        "ecart_type": 4.2021,
        "variance": 17.6576,
        "minimum": 8.7,
        "maximum": 21.0,
        "q1": 10.975,
        "q3": 15.875,
        "etendue": 12.3
    }
}
```

---

## 2. Corrélation de Pearson

### Endpoint

```http
POST /stats/correlation
```

### Exemple de requête

```json
{
    "x": [1,2,3,4,5],
    "y": [2,4,6,8,10]
}
```

### Exemple de réponse

```json
{
    "operation": "correlation_pearson",
    "resultat": {
        "r": 1.0,
        "p_value": 0.0,
        "interpretation": "forte",
        "significatif": true
    }
}
```

---

## 3. Test de normalité (Shapiro-Wilk)

### Endpoint

```http
POST /stats/test_normalite
```

### Exemple de requête

```json
{
    "data": [10,12,14,11,13,15,12,11]
}
```

### Exemple de réponse

```json
{
    "operation": "test_normalite_shapiro_wilk",
    "resultat": {
        "statistique": 0.982451,
        "p_value": 0.956321,
        "est_normale": true,
        "interpretation": "Distribution normale (p > 0.05)"
    }
}
```

---

## 4. Test de test Student

### Endpoint

```http
POST /stats/test_student
```

### Exemple de requête

```json
{
    "groupe1": [12,14,15,13,16],
    "groupe2": [20,21,19,22,18]
}
```

### Exemple de réponse

```json
{
    "operation": "test_t_student",
    "resultat": {
        "t_statistique": -6.2584,
        "p_value": 0.000231,
        "difference_significative": true
    }
}
```

---

# Tests avec Postman

Les quatre routes ont été testées avec Postman :

* Vérification des réponses valides
* Vérification des formats JSON
* Vérification des codes HTTP
* Gestion des erreurs (clé manquante, données invalides, tailles incompatibles)

---

Auteur : **Clément Gonet--Petit**

Projet réalisé dans le cadre de GPO TP2.

Technologies utilisées :

* Python
* Flask
* NumPy
* SciPy
* Postman
* GitHub Projects
