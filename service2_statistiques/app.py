from flask import Flask, request, jsonify 
import numpy as np 
from scipy import stats 

app = Flask(__name__) 

def validate_data(data, key='data'):     
    """
    Vérifie la présence et la validité d'une liste de valeurs numériques
    dans les données JSON reçues.

    Paramètres
    ----------
    data : dict
        Dictionnaire issu du corps JSON de la requête HTTP.

    key : str, optionnel
        Nom de la clé contenant les données à valider.
        Par défaut : 'data'.

    Retour
    -------
    numpy.ndarray
        Tableau NumPy contenant les valeurs converties en flottants.

    Exceptions
    ----------
    ValueError
        Levée si la clé est absente ou si moins de deux valeurs sont fournies.

    TypeError
        Levée si les données ne peuvent pas être converties en nombres.
    """    
    if key not in data:         
        raise ValueError(f"Clé '{key}' manquante dans la requête")     
    values = data[key]     
    if not isinstance(values, list) or len(values) < 2: 
        raise ValueError("'data' doit être une liste d'au moins 2 valeurs")     
    return np.array(values, dtype=float) 

@app.route("/stats/describe", methods=["POST"])
def describe():
    """
    Calcule les principales statistiques descriptives d'un échantillon.

    Cette route reçoit une liste de valeurs numériques et retourne
    plusieurs indicateurs permettant de résumer la distribution :

    - Effectif total (n)
    - Moyenne
    - Médiane
    - Variance
    - Écart-type
    - Minimum
    - Maximum
    - Premier quartile (Q1)
    - Troisième quartile (Q3)
    - Étendue

    Requête attendue
    ----------------
    {
        "data": [10, 20, 30, 40, 50]
    }

    Retour
    -------
    JSON
        Objet contenant l'ensemble des statistiques calculées.

    Codes HTTP
    ----------
    200 : calcul effectué avec succès
    400 : données invalides ou mal formatées
    """
    data = request.get_json()
    try:
        values = validate_data(data)
        result = {
            "n": int(len(values)),
            "moyenne": round(float(np.mean(values)), 4),
            "medianne": round(float(np.median(values)), 4),
            "ecart_type": round(float(np.std(values, ddof=1)), 4),
            "variance": round(float(np.var(values, ddof=1)), 4),
            "minimum": round(float(np.min(values)), 4),
            "maximum": round(float(np.max(values)), 4),
            'q1' : round(float(np.percentile(values, 25)), 4),
            'q3' : round(float(np.percentile(values, 75)), 4),
            'etendue': round(float(np.ptp(values)), 4)
        }
        return jsonify({"operation": "description", "resultat": result})
    except (ValueError, TypeError) as e:
        return jsonify({"erreur": str(e)}), 400

@app.route('/stats/correlation', methods=['POST'])
def correlation():
    """
    Calcule le coefficient de corrélation linéaire de Pearson entre
    deux variables numériques.

    Le test de Pearson mesure la force et la direction de la relation
    linéaire entre deux séries de valeurs.

    Le coefficient r est compris entre -1 et 1 :

    - r proche de 1  : forte corrélation positive
    - r proche de -1 : forte corrélation négative
    - r proche de 0  : absence de corrélation linéaire

    Une p-value est également calculée afin de déterminer si la
    corrélation observée est statistiquement significative.

    Requête attendue
    ----------------
    {
        "x": [1, 2, 3, 4, 5],
        "y": [2, 4, 6, 8, 10]
    }

    Retour
    -------
    JSON
        - coefficient de corrélation (r)
        - p-value
        - interprétation qualitative
        - significativité statistique

    Codes HTTP
    ----------
    200 : calcul effectué avec succès
    400 : données invalides ou longueurs incompatibles
    """
    data = request.get_json()     
    try: 
        x = validate_data(data, 'x')         
        y = validate_data(data, 'y')         
        if len(x) != len(y): 
            return jsonify({'erreur': 'x et y doivent avoir la même longueur'}), 400         
        r,p_value = stats.pearsonr(x, y)
        interpretation = ('forte' if abs(r) > 0.7 else 'modérée' if abs(r) > 0.4 else 'faible')         
        return jsonify({             'operation': 'correlation_pearson', 
            'resultat': { 
                'r': round(r, 4), 
                'p_value': round(p_value, 6), 
                'interpretation': interpretation, 
                'significatif': bool(p_value < 0.05) 
            }})     
    except (ValueError, TypeError) as e: 
        return jsonify({'erreur': str(e)}), 400 

@app.route('/stats/test_normalite', methods=['POST'])
def test_normalite():
    """
    Vérifie si un échantillon suit une distribution normale
    à l'aide du test de Shapiro-Wilk.

    Le test compare la distribution observée à une loi normale.

    Hypothèses :
    - H0 : les données suivent une distribution normale
    - H1 : les données ne suivent pas une distribution normale

    Interprétation :
    - p-value > 0.05  : normalité non rejetée
    - p-value <= 0.05 : normalité rejetée

    Limitation :
    Le test de Shapiro-Wilk est limité à 5000 observations.

    Requête attendue
    ----------------
    {
        "data": [10, 11, 12, 13, 14]
    }

    Retour
    -------
    JSON
        - statistique du test
        - p-value
        - résultat du test
        - interprétation textuelle

    Codes HTTP
    ----------
    200 : test réalisé avec succès
    400 : données invalides ou taille excessive
    """
    data = request.get_json()
    try:
        values = validate_data(data)
        if len(values) > 5000:
            return jsonify({"erreur":"shapiro-Wilk limité à 5000 valeurs"}), 400
        stat, p_value = stats.shapiro(values)
        return jsonify({
            "operation": "test_normalite_shapiro_wilk",
            "resultats": {
                "statistique": round(float(stat), 6),
                "p_value": round(float(p_value), 6),
                "est_normalite": bool(p_value > 0.05),
                "interpretation" : (
                    "Distribution normale (p > 0.05)" if p_value > 0.05 else 
                    "Distribution non normale (p <= 0.05)"
                )
            }
        })
    except (ValueError, TimeoutError) as e:
        return jsonify({"erreur": str(e)}), 400

@app.route('/stats/test_student', methods=['POST']) 
def test_student():
    """
    Compare les moyennes de deux échantillons indépendants
    à l'aide du test t de Student.

    Ce test permet de déterminer si la différence observée
    entre deux groupes est statistiquement significative.

    Hypothèses :
    - H0 : les deux groupes ont la même moyenne
    - H1 : les moyennes sont différentes

    Interprétation :
    - p-value < 0.05  : différence significative
    - p-value >= 0.05 : différence non significative

    Requête attendue
    ----------------
    {
        "groupe1": [10, 11, 12, 13],
        "groupe2": [20, 21, 22, 23]
    }

    Retour
    -------
    JSON
        - statistique t
        - p-value
        - indication de significativité

    Codes HTTP
    ----------
    200 : test réalisé avec succès
    400 : données invalides ou incomplètes
    """
    data = request.get_json()     
    try:
        groupe1 = validate_data(data, 'groupe1')         
        groupe2 = validate_data(data, 'groupe2')         
        t_stat, p_value = stats.ttest_ind(groupe1, groupe2)         
        return jsonify({             'operation': 'test_t_student',
            'resultat': {
                't_statistique': round(float(t_stat), 4),
                'p_value': round(float(p_value), 6),
                'difference_significative': bool(p_value < 0.05)
            }         })     
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


if __name__ == '__main__': 
    app.run(debug=True, port=5002) 