import csv
from pathlib import Path


DATA_FILE = Path("BS_dataset_cleaned.csv")
GOOD_WCST_ERROR_THRESHOLD = 12
EARLY_LEARNER_MAX_AOA2 = 12


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


def probability_of_good_wcst_error(rows: list[dict[str, str]]) -> None:
    groups = {
        "Early learners (< 12)": {"total": 0, "good": 0},
        "Later learners (>= 12)": {"total": 0, "good": 0},
    }

    for row in rows:
        aoa2 = float(row["aoa2"])
        wcst_error = float(row["wcst_error"])

        if aoa2 < EARLY_LEARNER_MAX_AOA2:
            group_name = "Early learners (< 12)"
        else:
            group_name = "Later learners (>= 12)"

        groups[group_name]["total"] += 1
        if wcst_error < GOOD_WCST_ERROR_THRESHOLD:
            groups[group_name]["good"] += 1

    for group_name, stats in groups.items():
        total = stats["total"]
        good = stats["good"]
        probability = good / total if total else 0
        print(group_name)
        print(f"  participants: {total}")
        print(f"  good wcst_error values: {good}")
        print(f"  probability of a good wcst_error: {probability:.4f}")


if __name__ == "__main__":
    probability_of_good_wcst_error(load_rows(DATA_FILE))
