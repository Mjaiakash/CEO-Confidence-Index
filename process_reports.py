from pathlib import Path
import re
from config import REPORT_DIR, PROCESSED_DIR
from preprocessing.parser import extract_text
from preprocessing.cleaner import clean_text


def parse_metadata(filename: str):
    match = re.match(r"(.+?)_(\d{4})\.pdf$", filename)
    if not match:
        return filename.removesuffix(".pdf"), None
    return match.group(1).replace("_", " "), int(match.group(2))


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    processed = 0
    for pdf in sorted(REPORT_DIR.glob("*.pdf")):
        text = clean_text(extract_text(pdf))
        company, year = parse_metadata(pdf.name)
        suffix = str(year) if year else "unknown"
        output = PROCESSED_DIR / f"{company.replace(' ', '_')}_{suffix}.txt"
        output.write_text(text, encoding="utf-8")
        print(f"Processed {company} {year or ''}".strip())
        processed += 1
    print(f"Completed: {processed} reports")


if __name__ == "__main__":
    main()
