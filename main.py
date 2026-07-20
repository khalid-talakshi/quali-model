from typing import Literal
from typer import Typer
from src.data.download import (
    download_quali_results,
    download_quali_results_year,
    download_quali_results_years,
)

app = Typer()


@app.command()
def download(
    years: list[int],
    round: int | None = None,
    format: Literal["csv"] = "csv",
    to: str = "./quali-results.csv",
):
    if len(years) == 1 and round is not None:
        df = download_quali_results(years[0], round)
    elif len(years) == 1 and round is None:
        df = download_quali_results_year(years[0])
    else:
        df = download_quali_results_years(years)

    if format == "csv":
        df.to_csv(to)


if __name__ == "__main__":
    app()
