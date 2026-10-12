"""Richtet beim ersten Start automatisch die Python-Umgebung ein und startet dann die Transkription.

Wird von start-windows.bat / start-mac.command / start-linux.sh aufgerufen.
"""

import hashlib
import os
import subprocess
import sys
import venv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REQUIREMENTS = BASE_DIR / "requirements.txt"


def venv_dir() -> Path:
    if os.name == "nt":
        # Kurzer Pfad ausserhalb des Projektordners: torch sprengt sonst leicht das 260-Zeichen-Limit von Windows.
        local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(local) / "transcriber-swiss-german" / "venv"
    return BASE_DIR / ".venv"


def venv_python(vdir: Path) -> Path:
    return vdir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def main() -> int:
    if sys.version_info < (3, 10) or sys.version_info >= (3, 14):
        print(f"Python {sys.version.split()[0]} wird nicht unterstützt. Bitte Python 3.10 bis 3.13 installieren")
        print("(empfohlen: 3.12, https://www.python.org/downloads/).")
        return 1

    vdir = venv_dir()
    py = venv_python(vdir)
    marker = vdir / ".requirements-hash"
    req_hash = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()

    if not py.exists():
        print(f"Erster Start: erstelle Python-Umgebung in {vdir} ...")
        venv.create(vdir, with_pip=True)

    if not marker.exists() or marker.read_text().strip() != req_hash:
        print("Installiere benötigte Pakete (einmalig, kann 5-15 Minuten dauern) ...")
        subprocess.run([str(py), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(py), "-m", "pip", "install", "-r", str(REQUIREMENTS)], check=True)
        marker.write_text(req_hash)

    return subprocess.run([str(py), str(BASE_DIR / "transkribieren.py")]).returncode


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError:
        print("\nFehler bei der Installation der Pakete. Internetverbindung prüfen und erneut starten.")
        sys.exit(1)
