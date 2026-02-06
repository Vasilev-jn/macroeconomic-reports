from dataclasses import dataclass
from typing import Protocol, Sequence

CsvRow = dict[str, str]


@dataclass(frozen=True)
class ReportTable:
    headers: list[str]
    rows: list[list[object]]


class Report(Protocol):
    name: str

    def build(self, rows: Sequence[CsvRow]) -> ReportTable:
        """Build report data for console output."""
