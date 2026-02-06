from collections import defaultdict
from statistics import mean
from typing import Sequence

from stafit.reports.base import CsvRow, ReportTable


class AverageGDPReport:
    name = "average-gdp"

    def build(self, rows: Sequence[CsvRow]) -> ReportTable:
        gdp_by_country: dict[str, list[float]] = defaultdict(list)

        for row in rows:
            gdp_by_country[row["country"]].append(float(row["gdp"]))

        report_rows = [
            [country, mean(values)]
            for country, values in gdp_by_country.items()
        ]
        report_rows.sort(key=lambda item: (-item[1], item[0]))

        return ReportTable(headers=["country", "average_gdp"], rows=report_rows)
