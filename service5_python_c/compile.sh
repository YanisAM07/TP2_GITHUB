#!/usr/bin/env bash

# Compile src/stats.c en bibliotheque partagee chargeable par ctypes.
#
# Le script detecte l'OS pour produire le bon format de bibliotheque :
# - Linux : lib/stats.so
# - macOS : lib/stats.dylib
# - Windows avec Git Bash/MinGW : lib/stats.dll

set -euo pipefail

SRC_DIR="src"
LIB_DIR="lib"
SRC_FILE="${SRC_DIR}/stats.c"

if [[ ! -f "${SRC_FILE}" ]]; then
    echo "Erreur : fichier source introuvable : ${SRC_FILE}" >&2
    exit 1
fi

mkdir -p "${LIB_DIR}"

case "$(uname -s)" in
    Darwin*)
        OUT_FILE="${LIB_DIR}/stats.dylib"
        SHARED_FLAGS=(-dynamiclib)
        ;;
    MINGW*|MSYS*|CYGWIN*)
        OUT_FILE="${LIB_DIR}/stats.dll"
        SHARED_FLAGS=(-shared)
        ;;
    *)
        OUT_FILE="${LIB_DIR}/stats.so"
        SHARED_FLAGS=(-shared -fPIC)
        ;;
esac

echo "[1/2] Compilation de ${SRC_FILE}..."
gcc "${SHARED_FLAGS[@]}" -O2 -Wall -Wextra -o "${OUT_FILE}" "${SRC_FILE}" -lm

echo "[2/2] Bibliotheque creee : ${OUT_FILE}"
echo "Compilation reussie !"
