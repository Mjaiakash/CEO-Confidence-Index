from __future__ import annotations

from database.database import init_db
from scraper.registry import write_registry


if __name__ == "__main__":
    init_db()
    path = write_registry()
    print(f"Initialized database and wrote {path}")
