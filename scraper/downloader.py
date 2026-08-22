from __future__ import annotations

from pathlib import Path

import requests
from tqdm import tqdm

DEFAULT_HEADERS = {"User-Agent": "CEO-Confidence-Index/1.0 (research project)"}


def download_file(url: str, destination: str | Path, timeout: int = 60) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, headers=DEFAULT_HEADERS, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with path.open("wb") as handle:
            for chunk in tqdm(response.iter_content(chunk_size=1024 * 64), desc=path.name, unit="B", unit_scale=True):
                if chunk:
                    handle.write(chunk)
    return path


def download_pdf(url: str, company: str, year: int, timeout: int = 60) -> Path:
    safe_company = "_".join(company.split())
    return download_file(url, Path("data/raw/annual_reports") / f"{safe_company}_{year}.pdf", timeout)
