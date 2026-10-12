"""Transkribiert alle Audiodateien aus ./input nach ./output (je eine .txt mit Zeitstempeln).

Modell: Flurin17/whisper-large-v3-turbo-swiss-german (Schweizerdeutsch + Hochdeutsch),
umgewandelt für faster-whisper (CTranslate2, int8).
Bereits transkribierte Dateien werden übersprungen.
"""

import os
import sys
import time
from pathlib import Path

import av
import numpy as np
import ctranslate2
from faster_whisper import WhisperModel

MODEL_ID = os.environ.get("TRANSCRIBER_MODEL", "Benjam1nP/whisper-large-v3-turbo-swiss-german-ct2-int8")
SAMPLE_RATE = 16000
AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".m4a", ".mp4", ".aac", ".flac", ".ogg", ".opus",
    ".wma", ".webm", ".mkv", ".mov", ".amr", ".3gp",
}
TRANSCRIBE_OPTIONS = dict(
    language="de",
    task="transcribe",
    beam_size=5,
    vad_filter=True,  # Stille überspringen, eine Zeile pro Äusserung
    # Verhindert erfundenen Text in Pausen und am Ende der Aufnahme
    word_timestamps=True,
    hallucination_silence_threshold=2.0,
)
MAX_WORDS_PER_SECOND = 8
HALLUCINATION_PHRASES = (
    "untertitelung des zdf", "untertitel im auftrag des zdf", "untertitel von stephanie geiges",
    "vielen dank fürs zuschauen", "danke fürs zuschauen", "copyright wdr",
)

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"


def load_audio(path: Path) -> np.ndarray:
    """Dekodiert beliebige Audio-/Videodateien zu 16 kHz mono float32 (ohne System-ffmpeg)."""
    resampler = av.AudioResampler(format="flt", layout="mono", rate=SAMPLE_RATE)
    chunks = []
    with av.open(str(path)) as container:
        stream = container.streams.audio[0]
        for frame in container.decode(stream):
            for out in resampler.resample(frame):
                chunks.append(out.to_ndarray().reshape(-1))
        for out in resampler.resample(None):
            chunks.append(out.to_ndarray().reshape(-1))
    if not chunks:
        raise ValueError("keine Audiodaten gefunden")
    return np.concatenate(chunks).astype(np.float32)


def format_ts(seconds: float) -> str:
    seconds = int(seconds)
    return f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


def load_model() -> tuple[WhisperModel, str]:
    if ctranslate2.get_cuda_device_count() > 0:
        try:
            return WhisperModel(MODEL_ID, device="cuda", compute_type="int8_float16"), "cuda"
        except Exception as e:
            print(f"(NVIDIA-GPU nicht nutzbar, verwende CPU: {e})")
    return WhisperModel(MODEL_ID, device="cpu", compute_type="int8"), "cpu"


def is_hallucination(text: str, start: float, end: float) -> bool:
    """Whisper erfindet manchmal Text in Stille, typischerweise am Ende der Aufnahme."""
    lower = text.lower()
    if any(phrase in lower for phrase in HALLUCINATION_PHRASES):
        return True
    # Echte Sprache hat ca. 2-4 Wörter pro Sekunde; erfundene Segmente oft 15+ Wörter in <1 s
    words = len(text.split())
    return words >= 3 and words / max(end - start, 0.1) > MAX_WORDS_PER_SECOND


def transcribe(model: WhisperModel, audio: np.ndarray) -> list[str]:
    segments, _ = model.transcribe(audio, **TRANSCRIBE_OPTIONS)
    lines = []
    for seg in segments:
        text = seg.text.strip()
        if not any(c.isalnum() for c in text) or is_hallucination(text, seg.start, seg.end):
            continue
        line = f"[{format_ts(seg.start)} - {format_ts(seg.end)}] {text}"
        print("  " + line, flush=True)
        lines.append(line)
    return lines


def main() -> int:
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    files = sorted(p for p in INPUT_DIR.iterdir() if p.suffix.lower() in AUDIO_EXTENSIONS)
    todo = [p for p in files if not (OUTPUT_DIR / f"{p.stem}.txt").exists()]

    if not files:
        print(f"Keine Audiodateien im Ordner '{INPUT_DIR}' gefunden.")
        print("Lege z.B. eine .mp3/.m4a/.wav-Datei in den Ordner 'input' und starte erneut.")
        return 0
    if not todo:
        print("Alle Dateien in 'input' wurden bereits transkribiert (siehe Ordner 'output').")
        return 0

    print(f"Lade Modell {MODEL_ID} ...")
    print("(Beim ersten Start wird das Modell heruntergeladen, ca. 0.8 GB.)")
    model, device = load_model()
    print(f"Modell geladen (Gerät: {device}).")

    for i, path in enumerate(todo, 1):
        print(f"\n[{i}/{len(todo)}] {path.name}")
        start = time.time()
        try:
            audio = load_audio(path)
        except Exception as e:
            print(f"  Fehler beim Lesen der Datei: {e}")
            continue
        print(f"  Dauer: {format_ts(len(audio) / SAMPLE_RATE)} – transkribiere ...")

        try:
            lines = transcribe(model, audio)
        except RuntimeError as e:
            if device != "cuda":
                raise
            # z.B. fehlende CUDA-Bibliotheken (cuBLAS/cuDNN): auf CPU weitermachen
            print(f"  NVIDIA-GPU-Fehler ({e}), wechsle auf CPU ...")
            model, device = WhisperModel(MODEL_ID, device="cpu", compute_type="int8"), "cpu"
            lines = transcribe(model, audio)

        out_path = OUTPUT_DIR / f"{path.stem}.txt"
        tmp_path = out_path.with_suffix(".txt.part")
        tmp_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        tmp_path.replace(out_path)
        print(f"  Fertig in {time.time() - start:.0f}s -> output/{out_path.name}")

    print("\nAlle Dateien verarbeitet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
