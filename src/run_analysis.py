"""Run the mobility and economy analysis from the command line.

This script is designed for local execution in VS Code. It uses the clean
processed dataset because the original course-platform raw files are not
available in this repository.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "ladb_mobility_economy_2024_clean.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


REQUIRED_COLUMNS = {
    "city",
    "country",
    "year",
    "JamsDelay",
    "TrafficIndexLive",
    "JamsLengthInKms",
    "JamsCount",
    "MinsDelay",
    "TravelTimeLivePer10KmsMins",
    "TravelTimeHistoricPer10KmsMins",
    "city_gdp_capita",
    "unemployment_pct",
    "pm25",
    "population",
}


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load and validate the processed project dataset."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Place ladb_mobility_economy_2024_clean.csv in data/processed/."
        )

    data = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"The dataset is missing required columns: {missing}")

    return data


def print_summary(data: pd.DataFrame) -> None:
    """Print a compact summary of the dataset."""
    print("Dataset shape:", data.shape)
    print("Years:", sorted(data["year"].unique()))
    print("Countries:", sorted(data["country"].unique()))
    print("\nTop 5 cities by traffic delay:")
    print(data.sort_values("JamsDelay", ascending=False)[["city", "country", "JamsDelay"]].head())


def save_boxplot(data: pd.DataFrame) -> None:
    """Save a boxplot of traffic delay."""
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data, y="JamsDelay", showmeans=True)
    plt.title("Traffic delay distribution in Latin American cities, 2024")
    plt.ylabel("Jam delay")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "jams_delay_boxplot.png", dpi=150)
    plt.close()


def save_gdp_histogram(data: pd.DataFrame) -> None:
    """Save a histogram of city GDP per capita."""
    plt.figure(figsize=(8, 6))
    plt.hist(data["city_gdp_capita"], bins=10, alpha=0.75)
    plt.title("GDP per capita distribution, 2024")
    plt.xlabel("GDP per capita")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "gdp_per_capita_histogram.png", dpi=150)
    plt.close()


def save_delay_gdp_scatter(data: pd.DataFrame) -> None:
    """Save a scatter plot comparing delay and GDP per capita."""
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=data, x="city_gdp_capita", y="JamsDelay", hue="country")
    plt.title("Traffic delay vs GDP per capita, 2024")
    plt.xlabel("GDP per capita")
    plt.ylabel("Jam delay")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "delay_vs_gdp_scatter.png", dpi=150)
    plt.close()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_data()
    print_summary(data)
    save_boxplot(data)
    save_gdp_histogram(data)
    save_delay_gdp_scatter(data)
    print(f"\nCharts saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
