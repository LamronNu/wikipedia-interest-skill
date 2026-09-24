import requests
import pandas as pd


def get_pageviews(language, article, start_date, end_date):
    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/"
        f"per-article/{language}.wikipedia.org/all-access/user/"
        f"{article}/daily/{start_date}/{end_date}"
    )

    headers = {
        "User-Agent": "WikipediaInterestSkill/0.1 (contact: your-email@example.com)"
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["items"])

    df["date"] = pd.to_datetime(
        df["timestamp"],
        format="%Y%m%d%H"
    )

    return df[["date", "views"]]
