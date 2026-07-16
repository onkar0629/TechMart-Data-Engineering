
from pathlib import Path
import csv
from typing import Iterable, Dict, Any

def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def write_csv(path: Path, headers: Iterable[str], rows: Iterable[Dict[str, Any]]) -> None:
    ensure_directory(path.parent)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(headers))
        writer.writeheader()
        writer.writerows(rows)
