# Compile src/stats.c en bibliotheque Windows stats.dll avec MinGW-w64.
#
# Ce script complete compile.sh pour les postes Windows qui n'utilisent pas
# Git Bash. Il suppose que gcc est disponible dans le PATH.

$ErrorActionPreference = "Stop"

$srcDir = "src"
$libDir = "lib"
$srcFile = Join-Path $srcDir "stats.c"
$outFile = Join-Path $libDir "stats.dll"

if (-not (Test-Path -LiteralPath $srcFile)) {
    throw "Fichier source introuvable : $srcFile"
}

if (-not (Get-Command gcc -ErrorAction SilentlyContinue)) {
    throw "gcc est introuvable. Installe MinGW-w64 ou utilise un environnement Linux/macOS avec ./compile.sh."
}

New-Item -ItemType Directory -Force -Path $libDir | Out-Null

Write-Host "[1/2] Compilation de $srcFile..."
& gcc -shared -O2 -Wall -Wextra -o $outFile $srcFile -lm

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "[2/2] Bibliotheque creee : $outFile"
Write-Host "Compilation reussie !"
