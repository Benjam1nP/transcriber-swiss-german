@echo off
rem Doppelklick: transkribiert alle Dateien aus "input" nach "output".
chcp 65001 >nul
cd /d "%~dp0"
set "PY="
for %%V in (3.12 3.13 3.11 3.10) do (
    if not defined PY (
        py -%%V -c "import venv, ensurepip" >nul 2>&1 && set "PY=py -%%V"
    )
)
if not defined PY (
    python -c "import sys, venv, ensurepip; sys.exit(not (3,10) <= sys.version_info[:2] <= (3,13))" >nul 2>&1 && set "PY=python"
)
if not defined PY (
    echo Kein passendes Python ^(3.10 bis 3.13^) gefunden.
    echo Bitte Python 3.12 von https://www.python.org/downloads/windows/ installieren
    echo und bei der Installation "Add python.exe to PATH" anhaken.
    goto :end
)
%PY% starter.py
:end
echo.
pause
