import unittest
import requests

class test_s2(unittest.TestCase):
    """Classe de test du service 2"""

    data = {"data":[1,2,3]}

    def test_describe(self):
        URL = "http://127.0.0.1:5002/stats/describe"
        response  =  requests.post(
            URL,
            json=self.data
        )
        reponse = response.json()

        self.assertEqual(1, reponse["resultat"]["ecart_type"])
        self.assertEqual(2, reponse["resultat"]["etendue"])
        self.assertEqual(3, reponse["resultat"]["maximum"])
        self.assertEqual(2, reponse["resultat"]["medianne"])
        self.assertEqual(1, reponse["resultat"]["minimum"])
        self.assertEqual(2, reponse["resultat"]["moyenne"])
        self.assertEqual(3, reponse["resultat"]["n"])
        self.assertEqual(1.5, reponse["resultat"]["q1"])
        self.assertEqual(2.5, reponse["resultat"]["q3"])
        self.assertEqual(1, reponse["resultat"]["variance"])
    
