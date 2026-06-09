import requests

url = "http://localhost:5001/matrices/add"

data = {
        "A": [[1,2],[3,4]],
        "B": [[5,6],[7,8]]
    }

response = requests.post(url, json=data)

print(response.json())
print(f"L'opération utilisée est {response.json()["operation"]}.")
print(f"Le résultat du calcul A est {response.json()["resultat"][0]}.")
print(f"Le résultat du calcul B est {response.json()["resultat"][1]}.")