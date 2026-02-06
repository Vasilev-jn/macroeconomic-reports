from argparse import ArgumentParser
from pathlib import Path
from typing import Sequence

from stafit.csv_reader import read_csv_files
from stafit.reports import available_reports, get_report

try:
    from tabulate import tabulate as _tabulate
except ModuleNotFoundError:  # pragma: no cover
    _tabulate = None


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Generate reports from macroeconomic CSV files.")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Paths to CSV files with macroeconomic data.",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=available_reports(),
        help="Report name. Supported value: average-gdp.",
    )
    return parser


def _validate_files(file_args: Sequence[str], parser: ArgumentParser) -> list[Path]:
    paths = [Path(item) for item in file_args]

    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        parser.error(f"file not found: {', '.join(missing)}")

    return paths


def _format_markdown_table(
    rows: list[list[object]], headers: list[str], floatfmt: str = ".2f"
) -> str:
    rendered_rows: list[list[str]] = []
    for row in rows:
        rendered_rows.append(
            [
                format(value, floatfmt) if isinstance(value, float) else str(value)
                for value in row
            ]
        )

    widths = [len(header) for header in headers]
    for row in rendered_rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    header_line = "| " + " | ".join(
        header.ljust(widths[index]) for index, header in enumerate(headers)
    ) + " |"
    separator_line = "|-" + "-|-".join("-" * width for width in widths) + "-|"
    body_lines = [
        "| " + " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)) + " |"
        for row in rendered_rows
    ]
    return "\n".join([header_line, separator_line, *body_lines])


def _render_table(rows: list[list[object]], headers: list[str]) -> str:
    if _tabulate is not None:
        return _tabulate(rows, headers=headers, tablefmt="github", floatfmt=".2f")

    return _format_markdown_table(rows, headers, floatfmt=".2f")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    files = _validate_files(args.files, parser)

    rows = read_csv_files(files)
    report = get_report(args.report)
    table = report.build(rows)

    print(_render_table(table.rows, table.headers))
    return 0
