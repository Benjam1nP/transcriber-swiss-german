# Transcriber Swiss German

Transkribiert Meeting-Aufnahmen (Schweizerdeutsch und Hochdeutsch gemischt) **lokal** auf dem eigenen Computer
und speichert den Text mit Zeitstempeln als `.txt`-Datei.

- Läuft auf **Windows, macOS und Linux**
- **Keine Audiodaten verlassen den Computer.** Aus dem Internet werden nur einmalig die Programme und das Modell geladen.
- Modell: [`Flurin17/whisper-large-v3-turbo-swiss-german`](https://huggingface.co/Flurin17/whisper-large-v3-turbo-swiss-german),
  ein für Schweizerdeutsch nachtrainiertes Whisper-Modell von OpenAI

---

## Kurzfassung

1. Python installieren (einmalig, siehe [Schritt 1](#schritt-1-python-installieren-einmalig))
2. Dieses Projekt als ZIP herunterladen und entpacken
3. Audiodatei in den Ordner **`input`** legen
4. Startdatei doppelklicken: `start-windows.bat` / `start-mac.command` / `start-linux.sh`
5. Transkript im Ordner **`output`** öffnen

---

## Schritt-für-Schritt-Anleitung

### Schritt 1: Python installieren (einmalig)

Benötigt wird **Python 3.10 bis 3.14**. Python 3.15 wird noch nicht unterstützt.
Ist Python schon installiert, direkt mit Schritt 2 weitermachen. Die Startdatei meldet es, falls etwas fehlt.

<details>
<summary><b>Windows</b></summary>

1. <https://www.python.org/downloads/windows/> öffnen und den **Windows installer (64-bit)** einer Version 3.12, 3.13 oder 3.14 herunterladen.
2. Den Installer starten.
3. **Wichtig:** Unten im ersten Fenster das Häkchen bei **"Add python.exe to PATH"** setzen.
4. Auf **"Install Now"** klicken und warten, bis die Installation fertig ist.

</details>

<details>
<summary><b>macOS</b></summary>

1. <https://www.python.org/downloads/macos/> öffnen und den **macOS 64-bit universal2 installer** einer Version 3.12, 3.13 oder 3.14 herunterladen.
2. Die `.pkg`-Datei öffnen und durch die Installation klicken.

Empfohlen ist ein Mac mit Apple-Chip (M1, M2, M3, …). Ältere Intel-Macs werden von aktuellem PyTorch nicht mehr unterstützt.

</details>

<details>
<summary><b>Linux</b></summary>

Python ist meist schon installiert. Zusätzlich wird das venv-Modul gebraucht, z.B. unter Ubuntu/Debian:

```bash
sudo apt install python3 python3-venv
```

</details>

### Schritt 2: Projekt herunterladen

1. Oben auf dieser GitHub-Seite auf den grünen Knopf **Code** und dann **Download ZIP** klicken.
2. Das ZIP entpacken (Rechtsklick → *Alle extrahieren…* unter Windows bzw. Doppelklick unter macOS).
   - **Windows:** möglichst an einen **kurzen Ort** entpacken, z.B. `C:\transcriber`, nicht tief verschachtelt im Download-Ordner.

Danach sieht der Ordner so aus:

```
transcriber-swiss-german-main/
├── input/               ← hier kommen die Audiodateien hinein
├── output/              ← hier erscheinen die Transkripte
├── start-windows.bat
├── start-mac.command
├── start-linux.sh
└── ... (weitere Programmdateien, nicht verändern)
```

### Schritt 3: Audiodatei in `input` legen

Eine oder mehrere Aufnahmen in den Ordner **`input`** kopieren.
Unterstützt werden u.a. **mp3, m4a, wav, mp4, mov, aac, flac, ogg, opus, webm, wma, amr, 3gp**,
also auch Videodateien von Teams/Zoom oder Sprachmemos vom iPhone.

### Schritt 4: Starten

| System | So starten |
|---|---|
| **Windows** | `start-windows.bat` doppelklicken. Erscheint *"Der Computer wurde durch Windows geschützt"*: auf **Weitere Informationen → Trotzdem ausführen** klicken. |
| **macOS** | `start-mac.command` doppelklicken. Beim **ersten Mal** blockiert macOS die Datei meistens. Dann **Rechtsklick → Öffnen → Öffnen**. Klappt das nicht: *Systemeinstellungen → Datenschutz & Sicherheit*, ganz unten **"Trotzdem öffnen"**. |
| **Linux** | Terminal im Ordner öffnen und `./start-linux.sh` ausführen. |

Es öffnet sich ein schwarzes Fenster (Terminal), das den Fortschritt anzeigt. **Das Fenster nicht schliessen**, bis
*"Fertig. Enter drücken zum Schliessen"* bzw. *"Drücken Sie eine beliebige Taste"* erscheint.

**Beim ersten Start** wird automatisch alles Nötige eingerichtet. Das dauert je nach Internetverbindung **5–20 Minuten**:

```
Erster Start: erstelle Python-Umgebung in ... 
Installiere benötigte Pakete (einmalig, kann 5-15 Minuten dauern) ...
Lade Modell Flurin17/whisper-large-v3-turbo-swiss-german auf cpu ...
(Beim ersten Start wird das Modell heruntergeladen, ca. 1.6 GB.)

[1/1] meeting.m4a
  Dauer: 00:47:12 – transkribiere ...
  Fertig in 3105s -> output/meeting.txt

Alle Dateien verarbeitet.
```

Ab dem zweiten Start entfällt die Installation und es geht direkt mit der Transkription los.

### Schritt 5: Ergebnis öffnen

Im Ordner **`output`** liegt pro Audiodatei eine Textdatei mit gleichem Namen, z.B. `meeting.m4a` → `meeting.txt`:

```
[00:00:00 - 00:00:28] Guten Morgen zusammen, wir fangen jetzt mit dem Meeting an. Als Erstes schauen wir das Budget an.
[00:00:28 - 00:00:55] Ja, ich habe die Zahlen vom letzten Quartal mitgebracht ...
```

- Die Zeitangaben sind **Stunden:Minuten:Sekunden** ab Beginn der Aufnahme.
- **Schweizerdeutsch wird auf Hochdeutsch ausgeschrieben.** So hat das Modell es gelernt.
- Die Datei ist UTF-8 und lässt sich mit jedem Editor, Word usw. öffnen.

### Weitere Aufnahmen

Einfach neue Dateien in `input` legen und wieder starten. **Bereits transkribierte Dateien werden übersprungen.**
Um eine Datei neu zu transkribieren, die zugehörige `.txt` in `output` löschen.

---

## Wie lange dauert es?

| Computer | Ungefähre Dauer für 1 Stunde Aufnahme |
|---|---|
| Normaler Laptop/PC ohne Grafikkarte (CPU) | ca. 1–2 Stunden |
| Mac mit Apple-Chip (M1/M2/M3/…) | deutlich schneller als CPU |
| Linux mit NVIDIA-Grafikkarte | wenige Minuten |

Unter Windows wird standardmässig die CPU-Version von PyTorch installiert, auch wenn eine NVIDIA-Karte vorhanden ist.
Während der Transkription den Computer nicht in den Ruhezustand gehen lassen.

---

## Häufige Probleme

| Problem | Lösung |
|---|---|
| *"Kein passendes Python (3.10 bis 3.14) gefunden"* | Python gemäss [Schritt 1](#schritt-1-python-installieren-einmalig) installieren. Unter Windows das Häkchen **"Add python.exe to PATH"** nicht vergessen, sonst Python neu installieren. |
| *"Keine Audiodateien im Ordner input gefunden"* | Datei liegt nicht direkt in `input` (z.B. in einem Unterordner) oder hat eine unbekannte Endung. |
| *"Fehler bei der Installation der Pakete"* | Internetverbindung prüfen und neu starten. In Firmennetzen blockiert evtl. ein Proxy/Firewall den Download, dann im Heimnetz versuchen. |
| *"Fehler beim Lesen der Datei"* | Datei ist beschädigt oder kein Audio. Mit einem Player prüfen, ggf. als mp3/wav exportieren. |
| macOS: *"kann nicht geöffnet werden, da der Entwickler nicht verifiziert werden kann"* | Rechtsklick → **Öffnen**, oder *Systemeinstellungen → Datenschutz & Sicherheit → Trotzdem öffnen*. Alternativ im Terminal: `bash start-mac.command` |
| Linux: *"Permission denied"* | `chmod +x start-linux.sh` und erneut starten, oder `bash start-linux.sh`. |
| Es ist etwas kaputtgegangen und soll neu eingerichtet werden | Die Python-Umgebung löschen (siehe unten) und neu starten. |

---

## Deinstallieren / Speicherplatz freigeben

Das Tool belegt nach dem ersten Start einige GB. Zum vollständigen Entfernen:

1. Den Projektordner löschen.
2. Die Python-Umgebung löschen:
   - **Windows:** `%LOCALAPPDATA%\transcriber-swiss-german` (in die Adresszeile des Explorers eingeben)
   - **macOS/Linux:** liegt als `.venv` im Projektordner und ist mit Schritt 1 schon weg
3. Das heruntergeladene Modell löschen:
   - **Windows:** `%USERPROFILE%\.cache\huggingface\hub\models--Flurin17--whisper-large-v3-turbo-swiss-german`
   - **macOS/Linux:** `~/.cache/huggingface/hub/models--Flurin17--whisper-large-v3-turbo-swiss-german`

---

## Wie es technisch funktioniert

1. Die **Startdatei** (`start-*.bat/.command/.sh`) sucht ein passendes Python und ruft `starter.py` auf.
2. **`starter.py`** erstellt beim ersten Mal eine eigene Python-Umgebung (venv) und installiert die Pakete aus
   `requirements.txt` (PyTorch, transformers, PyAV). Ändert sich `requirements.txt`, wird automatisch nachinstalliert.
3. **`transkribieren.py`**:
   - liest jede Audiodatei aus `input` mit PyAV ein (bringt einen eigenen Decoder mit, ffmpeg ist nicht nötig) und wandelt sie in 16 kHz Mono um,
   - wählt automatisch das schnellste Gerät: NVIDIA-GPU (CUDA), Apple Silicon (MPS) oder CPU,
   - transkribiert mit dem Whisper-Modell in 30-Sekunden-Abschnitten (Sprache Deutsch),
   - schreibt die Abschnitte mit Zeitstempeln nach `output/<name>.txt`.

| Datei | Zweck |
|---|---|
| `transkribieren.py` | Die eigentliche Transkription (input → output) |
| `starter.py` | Richtet die Python-Umgebung automatisch ein und startet die Transkription |
| `start-windows.bat`, `start-mac.command`, `start-linux.sh` | Startdateien zum Doppelklicken |
| `requirements.txt` | Benötigte Python-Pakete |

### Für Entwickler: manuell ausführen

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python transkribieren.py
```

## Grenzen

- **Zeitstempel sind abschnittsweise** (Blöcke von einigen Sekunden bis knapp einer Minute), nicht pro Satz oder Wort.
- **Keine Sprechererkennung:** Es wird nicht angegeben, *wer* spricht.
- Wie bei jeder Spracherkennung: Namen, Fachbegriffe und durcheinander redende Personen können falsch erkannt werden.
  **Wichtige Stellen immer mit der Aufnahme abgleichen.**
