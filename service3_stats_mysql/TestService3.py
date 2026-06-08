# test_service3.py — Tests unitaires Python (client HTTP)
# Lancer avec : python test_service3.py
# Le service Flask doit tourner sur http://localhost:5003

import urllib.request
import urllib.parse
import json
import sys

BASE = "http://localhost:5003"
PASS = 0
FAIL = 0


def get(path):
    """Effectue un GET et retourne (status_code, json_body)."""
    try:
        with urllib.request.urlopen(BASE + path) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())
    except Exception as e:
        print(f"  [ERREUR RÉSEAU] {e}")
        print("  → Le service Flask est-il lancé sur le port 5003 ?")
        sys.exit(1)


def check(nom, status_code, body, expected_status, check_fn=None):
    """Vérifie un test et affiche le résultat."""
    global PASS, FAIL
    ok = (status_code == expected_status)
    if ok and check_fn:
        ok = check_fn(body)
    if ok:
        PASS += 1
        print(f"  ✅ PASS — {nom}")
    else:
        FAIL += 1
        print(f"  ❌ FAIL — {nom}")
        print(f"     HTTP {status_code} | body: {json.dumps(body)[:200]}")


# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Tests : GET /db/stats/describe ===\n")

# Test 1 : série existante — doit retourner 200 avec les stats
s, b = get("/db/stats/describe?serie=serie_A")
check(
    "serie_A existe → 200 + champs stats présents",
    s, b, 200,
    lambda body: 'resultat' in body and 'moyenne' in body['resultat']
)

# Test 2 : paramètre 'serie' manquant → 400
s, b = get("/db/stats/describe")
check("paramètre 'serie' absent → 400", s, b, 400)

# Test 3 : série inexistante → 404
s, b = get("/db/stats/describe?serie=serie_INEXISTANTE_XYZ")
check("série inexistante → 404", s, b, 404)

# Test 4 : vérification valeurs serie_A (si données d'exemple chargées)
s, b = get("/db/stats/describe?serie=serie_A")
if s == 200:
    r = b.get('resultat', {})
    check(
        "serie_A : n=10, moyenne≈14.32, min=8.70",
        s, b, 200,
        lambda body: (
            body['resultat']['n'] == 10 and
            abs(body['resultat']['moyenne'] - 14.32) < 0.5 and
            abs(body['resultat']['minimum'] - 8.70) < 0.01
        )
    )

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Tests : GET /db/stats/correlation ===\n")

# Test 5 : deux séries existantes → 200 avec r et p_value
s, b = get("/db/stats/correlation?serie_x=serie_A&serie_y=serie_B")
check(
    "serie_A vs serie_B → 200 + r présent",
    s, b, 200,
    lambda body: 'resultat' in body and 'r' in body['resultat']
)

# Test 6 : serie_x manquante → 400
s, b = get("/db/stats/correlation?serie_y=serie_B")
check("serie_x absent → 400", s, b, 400)

# Test 7 : serie_y manquante → 400
s, b = get("/db/stats/correlation?serie_x=serie_A")
check("serie_y absent → 400", s, b, 400)

# Test 8 : une série inexistante → 404
s, b = get("/db/stats/correlation?serie_x=serie_A&serie_y=serie_INEXISTANTE")
check("une série inexistante → 404", s, b, 404)

# Test 9 : champ 'source' = 'mysql'
s, b = get("/db/stats/correlation?serie_x=serie_A&serie_y=serie_B")
check(
    "source = 'mysql' dans la réponse",
    s, b, 200,
    lambda body: body.get('source') == 'mysql'
)

# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"  Résultat : {PASS} PASS / {PASS + FAIL} tests")
if FAIL > 0:
    print(f"  {FAIL} test(s) FAIL — vérifiez le service et les données MySQL.")
else:
    print("  Tous les tests passent ✅")
print()