from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
REPORT_DIR = DATA_DIR / "annual_reports"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "outputs"
LOG_DIR = BASE_DIR / "logs"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'ceo_confidence.db'}")
FINBERT_MODEL = os.getenv("FINBERT_MODEL", "ProsusAI/finbert")

for directory in (REPORT_DIR, TRANSCRIPT_DIR, PROCESSED_DIR, OUTPUT_DIR, LOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)
