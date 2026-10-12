# Transcriber Swiss German

Transkribiert Meeting-Aufnahmen (Schweizerdeutsch und Hochdeutsch gemischt) **lokal** auf dem eigenen Computer.
Es werden keine Audiodaten ins Internet hochgeladen.

Modell: [`Flurin17/whisper-large-v3-turbo-swiss-german`](https://huggingface.co/Flurin17/whisper-large-v3-turbo-swiss-german)

## So geht's

1. Oben auf GitHub **Code → Download ZIP** klicken und das ZIP entpacken.
   - **Windows:** am besten an einen kurzen Ort entpacken, z.B. `C:\transcriber`.
2. Die Audiodatei(en) in den Ordner **`input`** legen (mp3, m4a, wav, mp4, ogg, flac, ...).
3. Starten:

   | System | Datei | Hinweis |
   |---|---|---|
   | Windows | `start-windows.bat` doppelklicken | Bei "Der Computer wurde durch Windows geschützt": *Weitere Informationen → Trotzdem ausführen* |
   | macOS | `start-mac.command` doppelklicken | Beim ersten Mal: Rechtsklick → *Öffnen*. Falls blockiert: *Systemeinstellungen → Datenschutz & Sicherheit → Trotzdem öffnen*. Alternativ im Terminal: `bash start-mac.command` |
   | Linux | `./start-linux.sh` im Terminal | |

4. Das Transkript erscheint im Ordner **`output`** als `.txt` mit Zeitstempeln, z.B.:

   ```
   [00:00:00 - 00:00:28] Guten Morgen zusammen, mir fanged grad a mit em Meeting ...
   ```

Bereits transkribierte Dateien werden beim nächsten Start übersprungen. Um eine Datei neu zu transkribieren, die zugehörige `.txt` in `output` löschen.

## Voraussetzung: Python

Nur **Python 3.10 bis 3.13** muss installiert sein (empfohlen 3.12): <https://www.python.org/downloads/>

- **Windows:** bei der Installation **"Add python.exe to PATH"** anhaken.
- **macOS:** Installer von python.org verwenden (Apple Silicon M1/M2/M3/... empfohlen; ältere Intel-Macs werden von aktuellem PyTorch nicht mehr unterstützt).
- **Linux:** z.B. `sudo apt install python3 python3-venv`

Alles andere (PyTorch, transformers, Audio-Decoder) wird beim **ersten Start automatisch** installiert.
Ein separates ffmpeg ist nicht nötig.

## Gut zu wissen

- **Erster Start dauert länger:** Pakete (ca. 1–3 GB) und das Modell (ca. 1.6 GB) werden einmalig heruntergeladen.
- **Geschwindigkeit:** Mit NVIDIA-Grafikkarte (CUDA) oder Apple Silicon (MPS) schnell. Auf reiner CPU deutlich langsamer,
  grob 1–2× die Länge der Aufnahme.
- **Zeitstempel** sind abschnittsweise (Blöcke von einigen Sekunden bis ca. 30 Sekunden), nicht pro Wort.
- Die Python-Umgebung liegt unter Windows in `%LOCALAPPDATA%\transcriber-swiss-german\venv`, sonst im Projektordner unter `.venv`.
  Zum Zurücksetzen einfach diesen Ordner löschen.

## Dateien

| Datei | Zweck |
|---|---|
| `transkribieren.py` | Die eigentliche Transkription (input → output) |
| `starter.py` | Richtet die Python-Umgebung automatisch ein und startet die Transkription |
| `start-windows.bat`, `start-mac.command`, `start-linux.sh` | Startdateien zum Doppelklicken |
| `requirements.txt` | Benötigte Python-Pakete |
