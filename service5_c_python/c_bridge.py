"""
c_bridge.py

Module assurant la communication entre Python et la bibliothèque
statistique développée en langage C.

Le chargement de la bibliothèque dynamique est réalisé à l'aide
du module ctypes. Les fonctions C sont ensuite encapsulées dans
des fonctions Python afin de simplifier leur utilisation par
l'application Flask.

Ce module agit comme une couche d'abstraction entre Python et C.
"""

import ctypes
import os
import platform

# Détermination automatique de l'extension de la bibliothèque

# selon le système d'exploitation utilisé.

_ext = '.so'

if platform.system() == 'Darwin':
    ext = '.dylib'
elif platform.system() == 'Windows':
    _ext = '.dll'

# Construction du chemin vers la bibliothèque compilée.

_lib_path = os.path.join(
    os.path.dirname(__file__),
    'lib',
    f'stats{_ext}'
)

# Vérification de la présence de la bibliothèque.

if not os.path.exists(_lib_path):
    raise FileNotFoundError(
    f'Bibliothèque C introuvable : {_lib_path}\n'
    'Exécutez ./compile.sh pour compiler stats.c'
    )

# Chargement dynamique de la bibliothèque.

_lib = ctypes.CDLL(_lib_path)

# Type représentant un pointeur vers un tableau de doubles.

_DoublePtr = ctypes.POINTER(ctypes.c_double)

# Déclaration des signatures des fonctions C.

# Ces informations permettent à ctypes de connaître

# les types des paramètres et du résultat attendu.

# calcul_moyenne(double *tableau, int n)

_lib.calcul_moyenne.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_moyenne.restype = ctypes.c_double

# calcul_variance(double *tableau, int n)

_lib.calcul_variance.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_variance.restype = ctypes.c_double

# calcul_ecart_type(double *tableau, int n)

_lib.calcul_ecart_type.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_ecart_type.restype = ctypes.c_double

# calcul_mediane(double *tableau, int n)

_lib.calcul_mediane.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_mediane.restype = ctypes.c_double

# calcul_min(double *tableau, int n)

_lib.calcul_min.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_min.restype = ctypes.c_double

# calcul_max(double *tableau, int n)

_lib.calcul_max.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_max.restype = ctypes.c_double

# produit_scalaire(double *v1, double *v2, int n)

_lib.produit_scalaire.argtypes = [
_DoublePtr,
_DoublePtr,
ctypes.c_int
]
_lib.produit_scalaire.restype = ctypes.c_double

def _to_c_array(python_list):
    """
    Convertit une liste Python en tableau C.

    ```
    Parameters
    ----------
    python_list : list[float]
        Liste de valeurs numériques.

    Returns
    -------
    tuple
        Tableau C de type double ainsi que sa taille.
    """

    arr = (ctypes.c_double * len(python_list))(*python_list)

    return arr, len(python_list)

def moyenne(valeurs: list[float]) -> float:
    """
    Calcule la moyenne arithmétique d'une série de valeurs.

    Parameters
    ----------
    valeurs : list[float]
        Données à analyser.

    Returns
    -------
    float
        Moyenne calculée par la bibliothèque C.
    """

    arr, n = _to_c_array(valeurs)

    return round(_lib.calcul_moyenne(arr, n), 6)

def variance(valeurs: list[float]) -> float:
    """
    Calcule la variance d'une série statistique.

    Parameters
    ----------
    valeurs : list[float]
        Données à analyser.

    Returns
    -------
    float
        Variance calculée par la bibliothèque C.
    """

    arr, n = _to_c_array(valeurs)

    return round(_lib.calcul_variance(arr, n), 6)

def ecart_type(valeurs: list[float]) -> float:
    """
    Calcule l'écart-type d'une série statistique.

    ```
    Parameters
    ----------
    valeurs : list[float]
        Données à analyser.

    Returns
    -------
    float
        Écart-type calculé par la bibliothèque C.
    """

    arr, n = _to_c_array(valeurs)

    return round(_lib.calcul_ecart_type(arr, n), 6)

def mediane(valeurs: list[float]) -> float:
    """
    Calcule la médiane d'une série de valeurs.

    Parameters
    ----------
    valeurs : list[float]
        Données à analyser.

    Returns
    -------
    float
        Médiane calculée par la bibliothèque C.
    """

    arr, n = _to_c_array(valeurs)

    return round(_lib.calcul_mediane(arr, n), 6)

def minimum(valeurs: list[float]) -> float:
    """
    Détermine la valeur minimale d'une série.

    Parameters
    ----------
    valeurs : list[float]
        Données à analyser.

    Returns
    -------
    float
        Plus petite valeur observée.
    """

    arr, n = _to_c_array(valeurs)

    return round(_lib.calcul_min(arr, n), 6)

def maximum(valeurs: list[float]) -> float:
    """
    Détermine la valeur maximale d'une série.

    Parameters
    ----------
    valeurs : list[float]
        Données à analyser.

    Returns
    -------
    float
        Plus grande valeur observée.
    """

    arr, n = _to_c_array(valeurs)

    return round(_lib.calcul_max(arr, n), 6)

def dot_product(v1: list[float], v2: list[float]) -> float:
    """
    Calcule le produit scalaire de deux vecteurs.

    Parameters
    ----------
    v1 : list[float]
        Premier vecteur.
    v2 : list[float]
        Second vecteur.

    Returns
    -------
    float
        Produit scalaire calculé par la bibliothèque C.

    Raises
    ------
    ValueError
        Levée lorsque les deux vecteurs n'ont pas la même taille.
    """

    if len(v1) != len(v2):
        raise ValueError(
            "Les deux vecteurs doivent avoir la même longueur"
        )

    a1, n = _to_c_array(v1)
    a2, _ = _to_c_array(v2)

    return round(
        _lib.produit_scalaire(a1, a2, n),
        6
    )