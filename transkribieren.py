"""Transkribiert alle Audiodateien aus ./input nach ./output (je eine .txt mit Zeitstempeln).

Modell: Flurin17/whisper-large-v3-turbo-swiss-german (Schweizerdeutsch + Hochdeutsch).
Bereits transkribierte Dateien werden übersprungen.
"""

import os
import sys
import time
from pathlib import Path

os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")  # Apple Silicon: fehlende Operationen auf CPU ausführen

import av
import numpy as np
import torch
from transformers import pipeline
from transformers.utils import logging as hf_logging

hf_logging.set_verbosity_error()

MODEL_ID = "Flurin17/whisper-large-v3-turbo-swiss-german"
SAMPLE_RATE = 16000
AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".m4a", ".mp4", ".aac", ".flac", ".ogg", ".opus",
    ".wma", ".webm", ".mkv", ".mov", ".amr", ".3gp",
}

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


def format_ts(seconds: float | None) -> str:
    if seconds is None:
        return "--:--:--"
    seconds = int(seconds)
    return f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


def pick_device():
    if torch.cuda.is_available():
        return "cuda:0", torch.float16
    if torch.backends.mps.is_available():
        return "mps", torch.float32
    return "cpu", torch.float32


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

    device, dtype = pick_device()
    print(f"Lade Modell {MODEL_ID} auf {device} ...")
    print("(Beim ersten Start wird das Modell heruntergeladen, ca. 1.6 GB.)")
    asr = pipeline(
        "automatic-speech-recognition",
        model=MODEL_ID,
        dtype=dtype,
        device=device,
    )
    # Das Modell liefert eos_token_id als Liste; der Whisper-Zeitstempel-Prozessor erwartet eine Zahl.
    for gen_cfg in (asr.model.generation_config, getattr(asr, "generation_config", None)):
        if gen_cfg is not None and isinstance(gen_cfg.eos_token_id, list):
            gen_cfg.eos_token_id = gen_cfg.eos_token_id[0]

    for i, path in enumerate(todo, 1):
        print(f"\n[{i}/{len(todo)}] {path.name}")
        start = time.time()
        try:
            audio = load_audio(path)
        except Exception as e:
            print(f"  Fehler beim Lesen der Datei: {e}")
            continue
        print(f"  Dauer: {format_ts(len(audio) / SAMPLE_RATE)} – transkribiere ...")

        result = asr(
            {"raw": audio, "sampling_rate": SAMPLE_RATE},
            chunk_length_s=30,
            batch_size=8 if device.startswith("cuda") else 1,
            return_timestamps=True,
            generate_kwargs={"language": "german", "task": "transcribe"},
        )

        lines = []
        for chunk in result.get("chunks", []):
            text = chunk["text"].strip()
            if not text:
                continue
            ts_start, ts_end = chunk["timestamp"]
            if ts_end is None:
                ts_end = len(audio) / SAMPLE_RATE
            lines.append(f"[{format_ts(ts_start)} - {format_ts(ts_end)}] {text}")
        if not lines:
            lines.append(result.get("text", "").strip())

        out_path = OUTPUT_DIR / f"{path.stem}.txt"
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  Fertig in {time.time() - start:.0f}s -> output/{out_path.name}")

    print("\nAlle Dateien verarbeitet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
