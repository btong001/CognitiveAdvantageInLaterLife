import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DATA_FILE = Path("BS_dataset_cleaned.csv")


def load_rows(csv_path: Path) -> list[dict[str, str]]:

    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        reader.fieldnames = [name.strip() for name in reader.fieldnames or []]
        rows = []
        for row in reader:
            rows.append(
                {
                    key.strip(): value.strip()
                    for key, value in row.items()
                    if key is not None
                }
            )
    return rows


def extract_xy(rows: list[dict[str, str]], x_key: str, y_key: str
) -> tuple[list[float], list[float]]:
    
    x_values = []
    y_values = []

    for row in rows:
        x_values.append(float(row[x_key]))
        y_values.append(float(row[y_key]))

    return x_values, y_values


def write_scatter_plot(rows: list[dict[str, str]], x_key: str, y_key: str, title: str, output_path: Path
) -> None:
    
    x_values, y_values = extract_xy(rows, x_key, y_key)

    plt.figure(figsize=(8, 5))
    plt.scatter(x_values, y_values, alpha=0.7, edgecolors="none")
    plt.title(title)
    plt.xlabel(x_key)
    plt.ylabel(y_key)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


if __name__ == "__main__":

    rows = load_rows(DATA_FILE)

    write_scatter_plot(
        rows,
        "aoa2",
        "flankscore",
        "Scatter Plot of aoa2 vs flankscore",
        Path("aoa2_flankscore_scatter.png"),
    )

    write_scatter_plot(
        rows,
        "aoa2",
        "wcst_error",
        "Scatter Plot of aoa2 vs wcst_error",
        Path("aoa2_wcst_error_scatter.png"),
    )
