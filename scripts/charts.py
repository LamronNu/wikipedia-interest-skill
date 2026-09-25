import matplotlib.pyplot as plt


def create_chart(df, output_path):
    df = df.sort_values("date")

    plt.figure(figsize=(12, 5))
    plt.plot(df["date"], df["views"])

    plt.title("Wikipedia pageviews")
    plt.xlabel("Date")
    plt.ylabel("Views")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path
