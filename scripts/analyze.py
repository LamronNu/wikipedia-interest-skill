import pandas as pd


def analyze_trend(df):
    """
    Analyze the trend of Wikipedia pageviews.

    Returns a dictionary with basic trend metrics.
    """

    if df.empty:
        return {
            "status": "no_data",
            "message": "No pageview data available."
        }

    df = df.sort_values("date").copy()

    # Basic metrics
    start_views = int(df["views"].iloc[0])
    end_views = int(df["views"].iloc[-1])

    total_views = int(df["views"].sum())
    average_views = float(df["views"].mean())
    median_views = float(df["views"].median())

    # Percentage change from first to last observation
    if start_views != 0:
        change_percent = (
            (end_views - start_views) / start_views
        ) * 100
    else:
        change_percent = None

    # Simple trend based on linear regression
    x = range(len(df))
    slope = pd.Series(df["views"].values).corr(
        pd.Series(list(x))
    )

    if slope is None or pd.isna(slope):
        trend = "unclear"
    elif slope > 0.2:
        trend = "increasing"
    elif slope < -0.2:
        trend = "decreasing"
    else:
        trend = "stable"

    # Maximum and minimum
    max_row = df.loc[df["views"].idxmax()]
    min_row = df.loc[df["views"].idxmin()]

    return {
        "status": "ok",
        "start_date": df["date"].iloc[0].strftime("%Y-%m-%d"),
        "end_date": df["date"].iloc[-1].strftime("%Y-%m-%d"),
        "start_views": start_views,
        "end_views": end_views,
        "change_percent": round(change_percent, 2)
        if change_percent is not None else None,
        "total_views": total_views,
        "average_daily_views": round(average_views, 2),
        "median_daily_views": round(median_views, 2),
        "trend": trend,
        "max_views": int(max_row["views"]),
        "max_date": max_row["date"].strftime("%Y-%m-%d"),
        "min_views": int(min_row["views"]),
        "min_date": min_row["date"].strftime("%Y-%m-%d"),
    }

