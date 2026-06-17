import unittest
import requests

class TestStatsDescribe(unittest.TestCase):

    URL = "http://localhost:5003/db/stats/describe"
    def test_stats_describe(self):
        """Vérifie qu'un json est renvoyé avec les bons champs"""
        # Récupére la réponse du service
        response = requests.get(
            self.URL,
            params={"serie": "serie_A"}
        )

        # Vérifie qu'il y a une réponse
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["source"], "mysql")

        # Vérifie qu'il ya des valeurs renvoyées
        resultat = data["resultat"]
        self.assertIn("moyenne", resultat)
        self.assertIn("mediane", resultat)
        self.assertIn("ecart_type", resultat)
        self.assertIn("minimum", resultat)
        self.assertIn("maximum", resultat)

    def test_missing_parameter(self):
        """Vérifie qu'il n'y a pas d'erreur html"""
        response = requests.get(self.URL)
        self.assertEqual(response.status_code, 400)

    def test_unknown_series(self):
        """Vérifie que des données incohérente renvoie une erreur"""
        response = requests.get(
            self.URL,
            params={"serie": "inexistante"}
        )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()