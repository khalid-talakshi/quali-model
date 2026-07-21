from pathlib import Path
from typing import Annotated, Literal

import typer
from typer import Typer
from src.data.download import (
    download_quali_results,
    download_quali_results_year,
    download_quali_results_years,
)

app = Typer(no_args_is_help=True)


@app.callback()
def main():
    """Tools for working with F1 qualifying result data."""


@app.command()
def download(
    years: Annotated[
        list[int],
        typer.Argument(
            help="One or more seasons to download, for example: 2024 2025. "
            "The optional 'years' keyword is also accepted."
        ),
    ] = [],
    round_number: Annotated[
        int | None,
        typer.Option(
            "--round", "-r", help="Race round to download. Only valid with one year."
        ),
    ] = None,
    output_format: Annotated[
        Literal["csv"],
        typer.Option("--format", "-f", help="Output file format."),
    ] = "csv",
    output_path: Annotated[
        Path,
        typer.Option("--to", "-o", help="Path to write the downloaded data."),
    ] = Path("./quali-results.csv"),
):

    if len(years) > 1 and round_number is not None:
        raise typer.BadParameter("--round can only be used when downloading one year.")

    if len(years) == 1 and round_number is not None:
        df = download_quali_results(years[0], round_number)
    elif len(years) == 1 and round_number is None:
        df = download_quali_results_year(years[0])
    else:
        years = [i for i in range(2018, 2026)]
        df = download_quali_results_years(years)

    if output_format == "csv":
        df.to_csv(output_path, index=False)

    return years


if __name__ == "__main__":
    app()
