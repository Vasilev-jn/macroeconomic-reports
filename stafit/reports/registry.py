from stafit.reports.average_gdp import AverageGDPReport
from stafit.reports.base import Report

_REPORTS: dict[str, Report] = {
    AverageGDPReport.name: AverageGDPReport(),
}


def available_reports() -> tuple[str, ...]:
    return tuple(sorted(_REPORTS))


def get_report(name: str) -> Report:
    return _REPORTS[name]
