from pathlib import Path

import pytest

from stafit.cli import main


def _write_csv(path: Path, rows: list[str]) -> None:
    header = "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
    path.write_text(header + "".join(rows), encoding="utf-8")


def test_cli_builds_average_gdp_report_for_multiple_files(
    workspace_tmp_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    first = workspace_tmp_dir / "first.csv"
    second = workspace_tmp_dir / "second.csv"
    _write_csv(
        first,
        [
            "United States,2023,25462,2.1,3.4,3.7,339,North America\n",
            "China,2023,17963,5.2,2.5,5.2,1425,Asia\n",
        ],
    )
    _write_csv(
        second,
        [
            "United States,2022,23315,2.1,8.0,3.6,338,North America\n",
            "China,2022,17734,3.0,2.0,5.6,1423,Asia\n",
            "Germany,2022,4072,1.8,8.7,3.1,83,Europe\n",
        ],
    )

    exit_code = main(
        [
            "--files",
            str(first),
            str(second),
            "--report",
            "average-gdp",
        ]
    )

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "| country" in output
    assert output.index("United States") < output.index("China") < output.index("Germany")


def test_cli_fails_when_file_does_not_exist(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--files", "missing.csv", "--report", "average-gdp"])

    error_output = capsys.readouterr().err

    assert exc_info.value.code == 2
    assert "file not found: missing.csv" in error_output


def test_cli_fails_for_unknown_report(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--files", "data.csv", "--report", "unknown-report"])

    error_output = capsys.readouterr().err

    assert exc_info.value.code == 2
    assert "invalid choice" in error_output
