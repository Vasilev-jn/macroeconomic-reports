import pytest

from stafit.reports.average_gdp import AverageGDPReport


def test_average_gdp_report_builds_sorted_table() -> None:
    report = AverageGDPReport()
    rows = [
        {"country": "United States", "gdp": "25462"},
        {"country": "United States", "gdp": "23315"},
        {"country": "United States", "gdp": "22994"},
        {"country": "China", "gdp": "17963"},
        {"country": "China", "gdp": "17734"},
        {"country": "China", "gdp": "17734"},
        {"country": "Germany", "gdp": "4086"},
        {"country": "Germany", "gdp": "4072"},
        {"country": "Germany", "gdp": "4257"},
    ]

    table = report.build(rows)

    assert table.headers == ["country", "average_gdp"]
    assert [row[0] for row in table.rows] == ["United States", "China", "Germany"]
    assert table.rows[0][1] == pytest.approx(23923.666666666668)
    assert table.rows[1][1] == pytest.approx(17810.333333333332)
    assert table.rows[2][1] == pytest.approx(4138.333333333333)
