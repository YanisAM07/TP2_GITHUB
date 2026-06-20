import unittest
import json
import numpy as np
from app import app
from scipy import stats


class BaseTestCase(unittest.TestCase):
    """Classe de base avec client Flask et méthode helper."""

    def setUp(self):
        self.client = app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def post(self, route, payload):
        return self.client.post(
            route,
            data=json.dumps(payload),
            headers=self.headers
        )


# ──────────────────────────────────────────────
# /stats/describe
# ──────────────────────────────────────────────

class TestDescribe(BaseTestCase):

    def test_valeurs_correctes(self):
        """Vérifie les résultats calculés sur [1, 2, 3]."""
        response = self.post("/stats/describe", {"data": [1, 2, 3]})
        self.assertEqual(200, response.status_code)

        data = response.get_json()
        self.assertEqual("description", data["operation"])

        r = data["resultat"]
        self.assertEqual(3,    r["n"])
        self.assertEqual(2.0,  r["moyenne"])
        self.assertEqual(2.0,  r["medianne"])
        self.assertEqual(1.0,  r["ecart_type"])   # ddof=1
        self.assertEqual(1.0,  r["variance"])     # ddof=1
        self.assertEqual(1.0,  r["minimum"])
        self.assertEqual(3.0,  r["maximum"])
        self.assertEqual(2.0,  r["etendue"])
        self.assertEqual(1.5,  r["q1"])
        self.assertEqual(2.5,  r["q3"])

    def test_cle_manquante(self):
        """Renvoie 400 si la clé 'data' est absente."""
        response = self.post("/stats/describe", {"mauvaise_cle": [1, 2, 3]})
        self.assertEqual(400, response.status_code)
        self.assertIn("erreur", response.get_json())

    def test_liste_trop_courte(self):
        """Renvoie 400 si moins de 2 valeurs."""
        response = self.post("/stats/describe", {"data": [42]})
        self.assertEqual(400, response.status_code)

    def test_valeurs_non_numeriques(self):
        """Renvoie 400 si les valeurs ne sont pas des nombres."""
        response = self.post("/stats/describe", {"data": ["a", "b", "c"]})
        self.assertEqual(400, response.status_code)

    def test_valeurs_flottantes(self):
        """Accepte des flottants et renvoie 200."""
        response = self.post("/stats/describe", {"data": [1.5, 2.5, 3.5]})
        self.assertEqual(200, response.status_code)
        r = response.get_json()["resultat"]
        self.assertAlmostEqual(2.5, r["moyenne"], places=4)


# ──────────────────────────────────────────────
# /stats/correlation
# ──────────────────────────────────────────────

class TestCorrelation(BaseTestCase):

    def test_correlation_parfaite_positive(self):
        """r = 1.0 pour deux séries identiques."""
        response = self.post("/stats/correlation", {"x": [1, 2, 3], "y": [1, 2, 3]})
        self.assertEqual(200, response.status_code)

        r = response.get_json()["resultat"]
        self.assertAlmostEqual(1.0, r["r"], places=3)
        self.assertTrue(r["significatif"])
        self.assertEqual("forte", r["interpretation"])

    def test_correlation_negative(self):
        """r = -1.0 pour deux séries inversées."""
        response = self.post("/stats/correlation", {"x": [1, 2, 3], "y": [3, 2, 1]})
        self.assertEqual(200, response.status_code)

        r = response.get_json()["resultat"]
        self.assertAlmostEqual(-1.0, r["r"], places=3)
        self.assertEqual("forte", r["interpretation"])

    def test_longueurs_differentes(self):
        """Renvoie 400 si x et y n'ont pas la même longueur."""
        response = self.post("/stats/correlation", {"x": [1, 2, 3], "y": [1, 2]})
        self.assertEqual(400, response.status_code)
        self.assertIn("erreur", response.get_json())

    def test_cle_y_manquante(self):
        """Renvoie 400 si la clé 'y' est absente."""
        response = self.post("/stats/correlation", {"x": [1, 2, 3]})
        self.assertEqual(400, response.status_code)

    def test_cle_x_manquante(self):
        """Renvoie 400 si la clé 'x' est absente."""
        response = self.post("/stats/correlation", {"y": [1, 2, 3]})
        self.assertEqual(400, response.status_code)

    def test_interpretation_moderee(self):
        response = self.post("/stats/correlation", {
            "x": [1, 2, 3, 4, 5],
            "y": [2, 1, 5, 3, 4]   # r = 0.6 → "modérée"
        })
        self.assertEqual(200, response.status_code)
        r = response.get_json()["resultat"]
        self.assertEqual("modérée", r["interpretation"])


# ──────────────────────────────────────────────
# /stats/test_normalite
# ──────────────────────────────────────────────

class TestNormalite(BaseTestCase):

    def test_distribution_normale(self):
        """Distribution normale, vérifie structure ET cohérence des valeurs."""
        np.random.seed(42)
        valeurs = np.random.normal(loc=0, scale=1, size=200).tolist()
        response = self.post("/stats/test_normalite", {"data": valeurs})
        self.assertEqual(200, response.status_code)

        res = response.get_json()

        # structure
        self.assertEqual("test_normalite_shapiro_wilk", res["operation"])
        self.assertIn("resultats", res)

        r = res["resultats"]

        # clés présentes
        self.assertIn("statistique", r)
        self.assertIn("p_value", r)
        self.assertIn("est_normalite", r)
        self.assertIn("interpretation", r)

        # valeurs cohérentes
        self.assertGreater(r["statistique"], 0)
        self.assertLessEqual(r["statistique"], 1)
        self.assertGreater(r["p_value"], 0.05)
        self.assertTrue(r["est_normalite"])
        self.assertEqual("Distribution normale (p > 0.05)", r["interpretation"])

    def test_distribution_non_normale(self):
        """Valeurs bimodales extrêmes, vérifie structure ET cohérence des valeurs."""
        valeurs = [1] * 50 + [100] * 50
        response = self.post("/stats/test_normalite", {"data": valeurs})
        self.assertEqual(200, response.status_code)

        res = response.get_json()

        # structure
        self.assertEqual("test_normalite_shapiro_wilk", res["operation"])
        self.assertIn("resultats", res)

        r = res["resultats"]

        # clés présentes
        self.assertIn("statistique", r)
        self.assertIn("p_value", r)
        self.assertIn("est_normalite", r)
        self.assertIn("interpretation", r)

        # valeurs cohérentes
        self.assertGreater(r["statistique"], 0)
        self.assertLessEqual(r["statistique"], 1)
        self.assertLess(r["p_value"], 0.05)        # p <= 0.05 → non normale
        self.assertFalse(r["est_normalite"])
        self.assertEqual("Distribution non normale (p <= 0.05)", r["interpretation"])

    def test_limite_5000_valeurs(self):
        """Renvoie 400 si plus de 5000 valeurs."""
        valeurs = list(range(5001))
        response = self.post("/stats/test_normalite", {"data": valeurs})
        self.assertEqual(400, response.status_code)
        self.assertIn("erreur", response.get_json())

    def test_cle_manquante(self):
        """Renvoie 400 si la clé 'data' est absente."""
        response = self.post("/stats/test_normalite", {"mauvaise_cle": [1, 2, 3]})
        self.assertEqual(400, response.status_code)

# ──────────────────────────────────────────────
# /stats/test_student
# ──────────────────────────────────────────────

class TestStudent(BaseTestCase):

    def test_groupes_tres_differents(self):
        response = self.post("/stats/test_student", {
            "groupe1": [1, 2, 3, 4, 5],
            "groupe2": [100, 101, 102, 103, 104]
        })
        self.assertEqual(200, response.status_code)

        res = response.get_json()
        self.assertEqual("test_t_student", res["operation"])

        r = res["resultat"]

        # clés présentes
        self.assertIn("t_statistique", r)
        self.assertIn("p_value", r)
        self.assertIn("difference_significative", r)

        # valeurs exactes (pas de random → on peut les vérifier)
        self.assertAlmostEqual(-99.0, r["t_statistique"], places=4)
        self.assertLess(r["p_value"], 0.05)
        self.assertTrue(r["difference_significative"])

    def test_groupes_similaires(self):
        """Deux groupes quasi-identiques, pas de différence significative."""
        groupe1 = [5.0, 5.05, 4.97, 5.02, 5.01]
        groupe2 = [5.0, 4.99, 5.03, 5.01, 4.98]

        # calcul des valeurs attendues
        t_attendu, p_attendu = stats.ttest_ind(groupe1, groupe2)

        response = self.post("/stats/test_student", {
            "groupe1": groupe1,
            "groupe2": groupe2
        })
        self.assertEqual(200, response.status_code)

        res = response.get_json()
        self.assertEqual("test_t_student", res["operation"])

        r = res["resultat"]
        self.assertIn("t_statistique", r)
        self.assertIn("p_value", r)
        self.assertIn("difference_significative", r)

        self.assertAlmostEqual(round(float(t_attendu), 4), r["t_statistique"], places=4)
        self.assertAlmostEqual(round(float(p_attendu), 6), r["p_value"], places=6)
        self.assertGreater(r["p_value"], 0.05)
        self.assertFalse(r["difference_significative"])

    def test_groupe2_manquant(self):
        """Renvoie 400 si 'groupe2' est absent."""
        response = self.post("/stats/test_student", {"groupe1": [1, 2, 3]})
        self.assertEqual(400, response.status_code)
        self.assertIn("erreur", response.get_json())

    def test_groupe1_manquant(self):
        """Renvoie 400 si 'groupe1' est absent."""
        response = self.post("/stats/test_student", {"groupe2": [1, 2, 3]})
        self.assertEqual(400, response.status_code)

    def test_operation_dans_reponse(self):
        """Le champ 'operation' doit valoir 'test_t_student'."""
        response = self.post("/stats/test_student", {
            "groupe1": [1, 2, 3, 4, 5],
            "groupe2": [6, 7, 8, 9, 10]
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual("test_t_student", response.get_json()["operation"])


if __name__ == "__main__":
    unittest.main()