"""
app.py

Service REST Flask permettant d'exposer les fonctions statistiques
implémentées dans une bibliothèque C.

Les calculs sont réalisés dans une DLL chargée dynamiquement grâce
au module ctypes via le module c_bridge.py.

"""

from flask import Flask, request, jsonify
import c_bridge as C

# Création de l'application Flask

app = Flask(__name__)

def validate_list(data, key, min_len=1):
    """
    Vérifie qu'une clé du JSON contient une liste valide.

    ```
    Paramètres
    ----------
    data : dict
        Corps de la requête JSON.
    key : str
        Nom de la clé à vérifier.
    min_len : int
        Nombre minimum d'éléments attendus.

    Retour
    ------
    list[float]
        Liste convertie en nombres flottants.

    Exceptions
    ----------
    ValueError
        Levée si la clé est absente ou si la liste est invalide.
    """

    # Vérifie la présence de la clé dans le JSON
    if key not in data:
        raise ValueError(f"Clé '{key}' manquante dans la requête")

    values = data[key]

    # Vérifie que la valeur est bien une liste
    # et qu'elle contient suffisamment d'éléments
    if not isinstance(values, list) or len(values) < min_len:
        raise ValueError(
            f"'{key}' doit être une liste d'au moins {min_len} valeur(s)"
        )

    # Conversion des valeurs en flottants
    return [float(v) for v in values]

@app.route('/c/stats/describe', methods=['POST'])
def c_describe():
    """
    Retourne un ensemble complet de statistiques descriptives.

    ```
    Calculs effectués :
    - moyenne
    - médiane
    - variance
    - écart-type
    - minimum
    - maximum
    """

    data = request.get_json()

    try:
        values = validate_list(data, 'data', min_len=2)

        result = {
            'n': len(values),
            'moyenne': C.moyenne(values),
            'mediane': C.mediane(values),
            'ecart_type': C.ecart_type(values),
            'variance': C.variance(values),
            'minimum': C.minimum(values),
            'maximum': C.maximum(values)
        }

        return jsonify({
            'moteur': 'C/ctypes',
            'operation': 'description',
            'resultat': result
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400

@app.route('/c/stats/mean', methods=['POST'])
def c_mean():
    """
    Calcule la moyenne arithmétique d'une série de données.
    """
    data = request.get_json()

    try:
        values = validate_list(data, 'data')

        return jsonify({
            'moteur': 'C/ctypes',
            'operation': 'moyenne',
            'resultat': C.moyenne(values)
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400

@app.route('/c/stats/stddev', methods=['POST'])
def c_stddev():
    """
    Calcule l'écart-type d'une série statistique.
    """

    data = request.get_json()

    try:
        values = validate_list(data, 'data', min_len=2)

        return jsonify({
            'moteur': 'C/ctypes',
            'operation': 'ecart_type',
            'resultat': C.ecart_type(values)
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400

@app.route('/c/stats/median', methods=['POST'])
def c_median():
    """
    Calcule la médiane d'une série de données.
    """

    data = request.get_json()

    try:
        values = validate_list(data, 'data')

        return jsonify({
            'moteur': 'C/ctypes',
            'operation': 'mediane',
            'resultat': C.mediane(values)
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400

@app.route('/c/stats/dot', methods=['POST'])
def c_dot():
    """
    Calcule le produit scalaire de deux vecteurs.

    Les deux vecteurs doivent posséder la même dimension.
    """

    data = request.get_json()

    try:
        v1 = validate_list(data, 'v1')
        v2 = validate_list(data, 'v2')

        # Vérification de la compatibilité des dimensions
        if len(v1) != len(v2):
            return jsonify({
                'erreur': 'v1 et v2 doivent avoir la même longueur'
            }), 400

        return jsonify({
            'moteur': 'C/ctypes',
            'operation': 'produit_scalaire',
            'resultat': C.dot_product(v1, v2)
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400
    
@app.route('/c/health', methods=['GET'])
def health():
    """
    Endpoint de supervision du service.

    Permet de vérifier que l'API est démarrée et de connaître
    les principales informations de configuration.
    """

    return jsonify({
        'statut': 'ok',
        'service': 'Service 5 — C/Python Bridge',
        'port': 5005,
        'bibliotheque': 'lib/stats.dll',
        'routes': [
            'POST /c/stats/describe',
            'POST /c/stats/mean',
            'POST /c/stats/stddev',
            'POST /c/stats/median',
            'POST /c/stats/dot'
        ]
    })

if __name__ == '__main__':
# Démarrage du serveur Flask en mode développement
    app.run(debug=True, port=5005)
