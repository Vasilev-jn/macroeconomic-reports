import csv
from pathlib import Path
from typing import Iterable


def read_csv_files(paths: Iterable[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for path in paths:
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            rows.extend(reader)

    return rows
