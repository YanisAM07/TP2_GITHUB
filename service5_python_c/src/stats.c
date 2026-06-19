/*
 * stats.c - Fonctions statistiques appelees depuis Python via ctypes.
 *
 * Chaque fonction exposee recoit un pointeur vers un tableau de double et
 * une taille entiere. Le code C ne connait pas la longueur d'un tableau
 * passe par pointeur : c'est donc toujours Python qui transmet aussi n.
 */

#include <math.h>
#include <stdlib.h>
#include <string.h>

#if defined(_WIN32)
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __attribute__((visibility("default")))
#endif

/*
 * Calcule la moyenne arithmetique d'un tableau de nombres.
 *
 * Retourne 0.0 si le pointeur est nul ou si la taille est invalide afin
 * d'eviter un acces memoire dangereux cote C.
 */
EXPORT double calcul_moyenne(double *tableau, int n) {
    if (tableau == NULL || n <= 0) {
        return 0.0;
    }

    double somme = 0.0;
    for (int i = 0; i < n; i++) {
        somme += tableau[i];
    }

    return somme / n;
}

/*
 * Calcule la variance non biaisee, equivalente a ddof=1 en Python/NumPy.
 *
 * Cette version divise par n - 1, ce qui correspond a un echantillon.
 * Au moins deux valeurs sont necessaires pour obtenir une variance utile.
 */
EXPORT double calcul_variance(double *tableau, int n) {
    if (tableau == NULL || n <= 1) {
        return 0.0;
    }

    double moyenne = calcul_moyenne(tableau, n);
    double somme_carres = 0.0;

    for (int i = 0; i < n; i++) {
        double diff = tableau[i] - moyenne;
        somme_carres += diff * diff;
    }

    return somme_carres / (n - 1);
}

/*
 * Calcule l'ecart-type a partir de la variance non biaisee.
 */
EXPORT double calcul_ecart_type(double *tableau, int n) {
    return sqrt(calcul_variance(tableau, n));
}

/*
 * Fonction de comparaison utilisee par qsort pour trier les doubles.
 */
static int compare_doubles(const void *a, const void *b) {
    double da = *(const double *)a;
    double db = *(const double *)b;

    return (da > db) - (da < db);
}

/*
 * Calcule la mediane sans modifier le tableau d'origine.
 *
 * La fonction copie les donnees avant de les trier, car la liste Python
 * transmise a ctypes ne doit pas etre reorganisee en silence par le code C.
 */
EXPORT double calcul_mediane(double *tableau, int n) {
    if (tableau == NULL || n <= 0) {
        return 0.0;
    }

    double *copie = (double *)malloc((size_t)n * sizeof(double));
    if (copie == NULL) {
        return 0.0;
    }

    memcpy(copie, tableau, (size_t)n * sizeof(double));
    qsort(copie, (size_t)n, sizeof(double), compare_doubles);

    double mediane;
    if (n % 2 == 0) {
        mediane = (copie[n / 2 - 1] + copie[n / 2]) / 2.0;
    } else {
        mediane = copie[n / 2];
    }

    free(copie);
    return mediane;
}

/*
 * Retourne la plus petite valeur du tableau.
 */
EXPORT double calcul_min(double *tableau, int n) {
    if (tableau == NULL || n <= 0) {
        return 0.0;
    }

    double min = tableau[0];
    for (int i = 1; i < n; i++) {
        if (tableau[i] < min) {
            min = tableau[i];
        }
    }

    return min;
}

/*
 * Retourne la plus grande valeur du tableau.
 */
EXPORT double calcul_max(double *tableau, int n) {
    if (tableau == NULL || n <= 0) {
        return 0.0;
    }

    double max = tableau[0];
    for (int i = 1; i < n; i++) {
        if (tableau[i] > max) {
            max = tableau[i];
        }
    }

    return max;
}

/*
 * Calcule le produit scalaire de deux vecteurs de meme longueur.
 *
 * La verification de longueur est realisee dans app.py et c_bridge.py.
 * C recoit seulement la taille commune n et parcourt les deux tableaux.
 */
EXPORT double produit_scalaire(double *v1, double *v2, int n) {
    if (v1 == NULL || v2 == NULL || n <= 0) {
        return 0.0;
    }

    double resultat = 0.0;
    for (int i = 0; i < n; i++) {
        resultat += v1[i] * v2[i];
    }

    return resultat;
}
