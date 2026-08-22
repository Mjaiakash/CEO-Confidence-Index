from pathlib import Path
import requests
from config import REPORT_DIR

DEFAULT_HEADERS = {"User-Agent": "CEO-Confidence-Index/1.0 (research project)"}


def download_pdf(url: str, company: str, year: int, timeout: int = 60) -> Path:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "").lower()
    if "pdf" not in content_type and not url.lower().split("?")[0].endswith(".pdf"):
        raise ValueError(f"URL does not appear to be a PDF: {url}")

    safe_company = "_".join(company.split())
    target = REPORT_DIR / f"{safe_company}_{year}.pdf"
    target.write_bytes(response.content)
    return target
