# Service 5 — Bridge C/Python pour calculs statistiques

## Présentation

Ce service expose une API REST développée avec Flask permettant d'effectuer différents calculs statistiques. Les calculs sont réalisés dans une bibliothèque écrite en C puis appelés depuis Python grâce au module `ctypes`.

L'objectif est de démontrer l'intégration d'un code natif C dans une application Python afin d'améliorer les performances sur certains traitements numériques.

## Fonctionnalités

Le service permet de calculer :

* Moyenne
* Variance
* Écart-type
* Médiane
* Minimum
* Maximum
* Produit scalaire de deux vecteurs

## Structure du projet

```text
service5_c_python/
│
├── app.py
├── c_bridge.py
├── benchmark.py
├── requirements.txt
│
├── src/
│   └── stats.c
│
├── lib/
│   └── stats.dll
│
├── compile.sh
└── compile.ps1
```

## Installation

### Création de l'environnement virtuel

```bash
python -m venv venv
```

### Activation

Windows :

```bash
venv\Scripts\activate
```

Linux / macOS :

```bash
source venv/bin/activate
```

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## Compilation de la bibliothèque C

### Windows

```powershell
.\compile.ps1
```

La compilation génère :

```text
lib/stats.dll
```

### Linux / macOS

```bash
chmod +x compile.sh
./compile.sh
```

La compilation génère :

```text
lib/stats.so
```

## Lancement du service

```bash
python app.py
```

Le service est accessible sur :

```text
http://127.0.0.1:5005
```

## Endpoints

### Vérification du service

```http
GET /c/health
```

### Moyenne

```http
POST /c/stats/mean
```

Exemple :

```json
{
    "data": [1, 2, 3, 4, 5]
}
```

### Médiane

```http
POST /c/stats/median
```

### Écart-type

```http
POST /c/stats/stddev
```

### Description complète

```http
POST /c/stats/describe
```

Exemple de réponse :

```json
{
    "moteur": "C/ctypes",
    "operation": "description",
    "resultat": {
        "n": 5,
        "moyenne": 3.0,
        "mediane": 3.0,
        "variance": 2.5,
        "ecart_type": 1.581139,
        "minimum": 1.0,
        "maximum": 5.0
    }
}
```

### Produit scalaire

```http
POST /c/stats/dot
```

Exemple :

```json
{
    "v1": [1, 2, 3],
    "v2": [4, 5, 6]
}
```

Réponse :

```json
{
    "moteur": "C/ctypes",
    "operation": "produit_scalaire",
    "resultat": 32.0
}
```

## Tests

Lancement du benchmark :

```bash
python benchmark.py
```

Ce script compare les performances des calculs effectués en Python et via la bibliothèque C.

## Technologies utilisées

* Python 3
* Flask
* ctypes
* Langage C
* GCC / MinGW-w64

## Auteurs
**Clément Gonet--Petit**

Projet réalisé dans le cadre de R2.10 GPO