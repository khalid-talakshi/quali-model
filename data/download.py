import fastf1
import pandas as pd
from fastf1.ergast import Ergast
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

ergast = Ergast()

years = [i for i in range(2018, 2025)]

df = None


fastf1.Cache.enable_cache("./data/cache", use_requests_cache=True)


def download_quali_results(year: int, round: int, ergast=Ergast()):
    circuit_info = ergast.get_circuits(year, round, limit=1)
    circuit_id = circuit_info["circuitId"].item()

    session = fastf1.get_session(year, round, "Q")
    session.load()
    results = session.results[
        [
            "DriverId",
            "TeamName",
            "Q1",
            "Q2",
            "Q3",
            "Position",
        ]
    ]

    results["Q1"] = results["Q1"].dt.total_seconds()
    results["Q2"] = results["Q2"].dt.total_seconds()
    results["Q3"] = results["Q3"].dt.total_seconds()
    results["circuit_id"] = circuit_id
    results["round_number"] = round
    results["year_id"] = year

    return results


def download_quali_results_year(year: int):
    res = pd.DataFrame()
    schedule = fastf1.get_event_schedule(year)
    race_schedule = schedule[schedule["EventFormat"] != "testing"]
    gp_rounds = race_schedule["RoundNumber"].tolist()

    for round in gp_rounds:
        df = download_quali_results(year, round)

        res = pd.concat([res, df])

    return res


def download_quali_results_years(years: list):
    res = pd.DataFrame()
    for year in years:
        df = download_quali_results_year(year)
        res = pd.concat([res, df])
    return res


res: pd.DataFrame = download_quali_results_years([i for i in range(2018, 2026)])
res.to_csv("./data/quali-results.csv")
