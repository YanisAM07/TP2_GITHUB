import unittest
import requests

class TestCorrelationAPI(unittest.TestCase):
    """Classe de test pour le service 3, route correlation"""

    URL = "http://localhost:5003/db/stats/correlation"

    def test_correlation_valide(self):
        """Teste si les champs du json sont cohérent"""
        response = requests.get(
            self.URL,
            params={
                "serie_x": "serie_A",
                "serie_y": "serie_B"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["source"], "mysql")

        self.assertIn("series", data)
        self.assertIn("resultat", data)

        resultat = data["resultat"]

        self.assertIn("r", resultat)
        self.assertIn("p_value", resultat)
        self.assertIn("significatif", resultat)

        self.assertGreaterEqual(resultat["r"], -1)
        self.assertLessEqual(resultat["r"], 1)

    def test_parametres_manquants(self):
        """Verifie qu'il n'y a pas d'erreur html"""
        response = requests.get(self.URL)

        self.assertEqual(response.status_code, 400)

        data = response.json()

        self.assertEqual(
            data["erreur"],
            "Paramètres serie_x et serie_y requis"
        )

    def test_serie_inexistante(self):
        """Vérifie que des données soit bien envoyé"""
        response = requests.get(
            self.URL,
            params={
                "serie_x": "inconnue",
                "serie_y": "serie_B"
            }
        )

        self.assertEqual(response.status_code, 404)

        data = response.json()

        self.assertIn("erreur", data)


if __name__ == "__main__":
    unittest.main()