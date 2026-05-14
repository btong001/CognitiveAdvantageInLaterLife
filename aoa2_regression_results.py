import csv
from pathlib import Path

from scipy.stats import linregress

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


def extract_values(rows: list[dict[str, str]], predictor: str, outcome: str
) -> tuple[list[float], list[float]]:
    
    predictor_values = []
    outcome_values = []

    for row in rows:
        predictor_values.append(float(row[predictor]))
        outcome_values.append(float(row[outcome]))

    return predictor_values, outcome_values


def run_regression(rows: list[dict[str, str]], predictor: str, outcome: str
) -> None:
    
    predictor_values, outcome_values = extract_values(rows, predictor, outcome)
    result = linregress(predictor_values, outcome_values)

    print(f"{predictor} predicting {outcome}")
    print(f"  participants: {len(predictor_values)}")
    print(f"  slope: {result.slope:.4f}")
    print(f"  intercept: {result.intercept:.4f}")
    print(f"  r: {result.rvalue:.4f}")
    print(f"  R^2: {result.rvalue ** 2:.4f}")
    print(f"  p value: {result.pvalue:.4f}")
    print(f"  standard error: {result.stderr:.4f}")


if __name__ == "__main__":

    rows = load_rows(DATA_FILE)
    run_regression(rows, "aoa2", "flankscore")
    run_regression(rows, "aoa2", "wcst_error")
