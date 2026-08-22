from __future__ import annotations

from pathlib import Path

import fitz


def extract_text(pdf_path: str | Path) -> str:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(path)
    chunks: list[str] = []
    with fitz.open(path) as document:
        for page in document:
            chunks.append(page.get_text("text"))
    return "\n".join(chunks).strip()

