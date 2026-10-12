#!/usr/bin/env bash
# Doppelklick: transkribiert alle Dateien aus "input" nach "output".
cd "$(dirname "$0")" || exit 1

PY=""
for c in python3.12 python3.13 python3.11 python3.10 python3 python; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys, venv, ensurepip; sys.exit(not (3,10) <= sys.version_info[:2] <= (3,13))' 2>/dev/null; then
        PY="$c"; break
    fi
done

if [ -z "$PY" ]; then
    echo "Kein passendes Python (3.10 bis 3.13) gefunden."
    echo "Bitte Python 3.12 installieren: https://www.python.org/downloads/macos/"
else
    "$PY" starter.py
fi

echo
read -r -p "Fertig. Enter drücken zum Schliessen ..." _
