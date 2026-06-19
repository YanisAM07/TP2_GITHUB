"""
benchmark.py

Script de benchmark permettant de comparer les performances
de calculs réalisés en Python natif et via la bibliothèque
statistique développée en C.

Les mesures sont effectuées à l'aide du module time afin
d'évaluer l'intérêt de l'utilisation d'une implémentation
native pour les traitements numériques.
"""

import random
import time
import statistics

import c_bridge as C


N = 100000
NB_TESTS = 100

data = [random.uniform(0, 1000) for _ in range(N)]


def benchmark_python():
    """
    Mesure le temps d'exécution de la fonction
    de calcul de moyenne fournie par Python.
    """
    debut = time.perf_counter()

    for _ in range(NB_TESTS):
        statistics.mean(data)

    fin = time.perf_counter()
    return fin - debut


def benchmark_c():
    """
    Mesure le temps d'exécution de la fonction
    de calcul de moyenne implémentée en C.
    """
    debut = time.perf_counter()

    for _ in range(NB_TESTS):
        C.moyenne(data)

    fin = time.perf_counter()
    return fin - debut


if __name__ == "__main__":
    # Exécution du benchmark Python.
    temps_python = benchmark_python()

    # Exécution du benchmark C.
    temps_c = benchmark_c()

    # Affichage des paramètres du test.
    print("\n=== Benchmark Moyenne ===")
    print(f"Nombre de valeurs : {N:,}")
    print(f"Nombre d'exécutions : {NB_TESTS}")

    # Affichage des temps mesurés.
    print(f"\nPython : {temps_python:.6f} s")
    print(f"C      : {temps_c:.6f} s")

    # Calcul du facteur d'accélération obtenu
    # par l'utilisation de l'implémentation C.
    if temps_c > 0:
        gain = temps_python / temps_c
        print(f"\nAccélération : x{gain:.2f}")