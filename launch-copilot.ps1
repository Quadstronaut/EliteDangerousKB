<#
.SYNOPSIS
    Launches the COVAS ED Knowledge Copilot REPL.
    Health-checks Ollama and the virtual environment before starting.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = $PSScriptRoot

# ---------------------------------------------------------------------------
# 1. Check Ollama is running
# ---------------------------------------------------------------------------
Write-Host "[COVAS] Checking Ollama..." -ForegroundColor Cyan
try {
    $tags = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5
    Write-Host "[COVAS] Ollama OK — $(($tags.models | Measure-Object).Count) model(s) loaded." -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "ERROR: Ollama is not running or not reachable at http://localhost:11434." -ForegroundColor Red
    Write-Host ""
    Write-Host "Start it with:" -ForegroundColor Yellow
    Write-Host "    ollama serve" -ForegroundColor White
    Write-Host ""
    Write-Host "Then re-run this script." -ForegroundColor Yellow
    exit 1
}

# ---------------------------------------------------------------------------
# 2. Check .venv exists
# ---------------------------------------------------------------------------
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Host ""
    Write-Host "ERROR: Python virtual environment not found at .venv\" -ForegroundColor Red
    Write-Host ""
    Write-Host "Create it with:" -ForegroundColor Yellow
    Write-Host "    python -m venv .venv" -ForegroundColor White
    Write-Host "    .venv\Scripts\pip install -r requirements.txt" -ForegroundColor White
    Write-Host ""
    exit 1
}
Write-Host "[COVAS] .venv OK." -ForegroundColor Green

# ---------------------------------------------------------------------------
# 3. Launch REPL
# ---------------------------------------------------------------------------
Write-Host "[COVAS] Starting COVAS copilot..." -ForegroundColor Cyan
Write-Host ""
# Force UTF-8 so qwen output (en-dashes, arrows, °) doesn't crash or mojibake on
# a legacy cp1252 console (Windows PowerShell 5.1 default).
$env:PYTHONUTF8 = "1"
& $VenvPython -m copilot.repl
