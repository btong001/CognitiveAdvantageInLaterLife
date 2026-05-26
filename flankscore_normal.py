import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DATA_FILE = Path("BS_dataset_cleaned.csv")
HISTOGRAM_FILE = Path("flankscore_histogram.png")


def load_flankscore_values(csv_path: Path) -> list[float]:
    values = []

    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        reader.fieldnames = [name.strip() for name in reader.fieldnames or []]

        for row in reader:
            cleaned_row = {
                key.strip(): value.strip()
                for key, value in row.items()
                if key is not None
            }
            values.append(float(cleaned_row["flankscore"]))

    return values


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def moment_variance(values: list[float], mu_hat: float) -> float:
    squared_differences = [(value - mu_hat) ** 2 for value in values]
    return sum(squared_differences) / len(values)



def normal_density(x: float, mu_hat: float, sigma_hat: float) -> float:
    coefficient = 1 / (sigma_hat * math.sqrt(2 * math.pi))
    exponent = -((x - mu_hat) ** 2) / (2 * sigma_hat**2)
    return coefficient * math.exp(exponent)


def print_normal_summary(values: list[float]) -> None:
    mu_hat = mean(values)
    sigma_squared_hat = moment_variance(values, mu_hat)
    sigma_hat = math.sqrt(sigma_squared_hat)

    print(f"participants: {len(values)}")
    print(f"mean: {mu_hat:.4f}")
    print(f"variance: {sigma_squared_hat:.4f}")
    print(f"estimated standard deviation: {sigma_hat:.4f}")


def save_histogram(values: list[float], output_path: Path) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(values, bins=20, color="#4c78a8", edgecolor="white")
    plt.title("Histogram of flankscore")
    plt.xlabel("flankscore")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


if __name__ == "__main__":
    flankscore_values = load_flankscore_values(DATA_FILE)
    print_normal_summary(flankscore_values)
    save_histogram(flankscore_values, HISTOGRAM_FILE)
