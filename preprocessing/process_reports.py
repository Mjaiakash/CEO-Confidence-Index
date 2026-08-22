from __future__ import annotations

import json
import re
from pathlib import Path

from config import PROCESSED_DIR, REPORT_DIR
from preprocessing.clean_text import clean_text
from preprocessing.pdf_parser import extract_text
from preprocessing.sections import extract_sections


def parse_metadata(path: Path) -> tuple[str, int]:
    stem = path.stem
    year_match = re.search(r"(20\d{2})", stem)
    year = int(year_match.group(1)) if year_match else 0
    company = stem[: year_match.start()].strip(" _-") if year_match else stem
    return company or "Unknown", year


def process_reports() -> int:
    count = 0
    for pdf in sorted(REPORT_DIR.glob("*.pdf")):
        company, year = parse_metadata(pdf)
        text = clean_text(extract_text(pdf))
        payload = {"company": company, "year": year, "source": pdf.name, "sections": extract_sections(text)}
        output = PROCESSED_DIR / f"{pdf.stem}.json"
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        count += 1
    return count


if __name__ == "__main__":
    print(f"Processed {process_reports()} reports")
