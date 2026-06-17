# TP2_GITHUB

## Service 1 — Calculs Matriciels

### Description API REST Flask pour effectuer des calculs sur des matrices

### Installation

```bash
cd service1_matrices python -m venv venv && source
venv/bin/activate
pip install -r requirements.txt 
python app.py 
```

### Paquets externes

```python
flask
numpy
```

### Routes disponibles

#### POST /matrices/add

##### Additionne deux matrices de mêmes dimensions

**Corps de la requête (JSON) :**

```json
{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]} 
```

**Réponse (200 OK) :**

```json
{"operation": "addition", "resultat": [[6.0,8.0],[10.0,12.0]]} 
```

**Erreurs possibles :** 400 si dimensions incompatibles.

#### POST /matrices/multiply

##### Multiplie deux matrices de dimensions compatibles

**Corps de la requête (JSON) :**

```json
{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]} 
```

**Réponse (200 OK) :**

```json
{"operation": "multiplication", "resultat": [[19.0,22.0],[43.0,50.0]]} 
```

**Erreurs possibles :** 400 si dimensions incompatibles.

#### POST /matrices/transpose

##### Transpose une matrice

**Corps de la requête (JSON) :**

```json
{"A": [[1,2],[3,4]]} 
```

**Réponse (200 OK) :**

```json
{"operation": "transposee", "resultat": [[1.0,3.0],[2.0,4.0]]} 
```

**Erreurs possibles :** Aucune erreurs (sauf saisie ou autre).

#### POST /matrices/determinant

##### Calcule le determinant une matrice

**Corps de la requête (JSON) :**

```json
{"A": [[1,2],[3,4]]} 
```

**Réponse (200 OK) :**

```json
{"operation": "determinant", "resultat": -2} 
```

**Erreurs possibles :** 400 si la matrice n'est pas carrée.

#### POST /matrices/inverse

##### Calcule l'inverse d'une matrice

**Corps de la requête (JSON) :**

```json
{"A": [[1,2],[3,4]]} 
```

**Réponse (200 OK) :**

```json
{"operation": "determinant", "resultat": [[-1.999,0.999],[1.499,-0.499]]} 
```

**Erreurs possibles :** 400 si la matrice n'est pas inversible.
