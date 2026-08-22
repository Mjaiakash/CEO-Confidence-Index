from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

REPORT_DIR = ROOT_DIR / os.getenv("REPORT_DIR", "data/raw/annual_reports")
TRANSCRIPT_DIR = ROOT_DIR / os.getenv("TRANSCRIPT_DIR", "data/raw/transcripts")
PROCESSED_DIR = ROOT_DIR / os.getenv("PROCESSED_DIR", "data/processed")
OUTPUT_DIR = ROOT_DIR / os.getenv("OUTPUT_DIR", "data/outputs")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT_DIR / 'ceo_confidence.db'}")
FINBERT_MODEL = os.getenv("FINBERT_MODEL", "ProsusAI/finbert")

for directory in (REPORT_DIR, TRANSCRIPT_DIR, PROCESSED_DIR, OUTPUT_DIR):
    directory.mkdir(parents=True, exist_ok=True)
