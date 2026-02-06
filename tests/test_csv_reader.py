from pathlib import Path

from stafit.csv_reader import read_csv_files


def _write_csv(path: Path, rows: list[str]) -> None:
    header = "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
    path.write_text(header + "".join(rows), encoding="utf-8")


def test_read_csv_files_reads_rows_from_all_files(workspace_tmp_dir: Path) -> None:
    first = workspace_tmp_dir / "first.csv"
    second = workspace_tmp_dir / "second.csv"
    _write_csv(
        first,
        [
            "United States,2023,25462,2.1,3.4,3.7,339,North America\n",
            "China,2023,17963,5.2,2.5,5.2,1425,Asia\n",
        ],
    )
    _write_csv(second, ["Germany,2023,4086,-0.3,6.2,3.0,83,Europe\n"])

    rows = read_csv_files([first, second])

    assert len(rows) == 3
    assert rows[0]["country"] == "United States"
    assert rows[1]["country"] == "China"
    assert rows[2]["country"] == "Germany"


def test_read_csv_files_handles_utf8_bom(workspace_tmp_dir: Path) -> None:
    source = workspace_tmp_dir / "bom.csv"
    content = (
        "\ufeffcountry,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
        "Germany,2023,4086,-0.3,6.2,3.0,83,Europe\n"
    )
    source.write_text(content, encoding="utf-8")

    rows = read_csv_files([source])

    assert rows[0]["country"] == "Germany"
