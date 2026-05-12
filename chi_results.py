import csv
from pathlib import Path

from scipy.stats import chi2_contingency


DATA_FILE = Path("BS_dataset_cleaned.csv")
EARLY_LEARNER_MAX_AOA2 = 12
GOOD_FLANKSCORE_THRESHOLD = 51
GOOD_WCST_ERROR_THRESHOLD = 12


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


def build_contingency_table(
    rows: list[dict[str, str]], outcome: str, good_threshold: float
) -> list[list[int]]:
    early_good = 0
    early_not_good = 0
    later_good = 0
    later_not_good = 0

    for row in rows:
        aoa2 = float(row["aoa2"])
        score = float(row[outcome])

        is_early = aoa2 < EARLY_LEARNER_MAX_AOA2
        is_good = score < good_threshold

        if is_early and is_good:
            early_good += 1
        elif is_early and not is_good:
            early_not_good += 1
        elif not is_early and is_good:
            later_good += 1
        else:
            later_not_good += 1

    return [
        [early_good, early_not_good],
        [later_good, later_not_good],
    ]


def describe_chi_square(
    rows: list[dict[str, str]], outcome: str, good_threshold: float
) -> None:
    contingency_table = build_contingency_table(rows, outcome, good_threshold)
    chi2, p_value, degrees_of_freedom, expected = chi2_contingency(contingency_table)

    print(f"Chi-square test for aoa2 group vs {outcome}")
    print("  Contingency table:")
    print("    Early learners:", contingency_table[0])
    print("    Later learners:", contingency_table[1])
    print(f"  Chi-square: {chi2:.4f}")
    print(f"  p-value: {p_value:.6f}")
    print(f"  Degrees of freedom: {degrees_of_freedom}")
    print("  Expected counts:")
    print(f"    Early learners: [{expected[0][0]:.2f}, {expected[0][1]:.2f}]")
    print(f"    Later learners: [{expected[1][0]:.2f}, {expected[1][1]:.2f}]")


if __name__ == "__main__":
    rows = load_rows(DATA_FILE)
    describe_chi_square(rows, "flankscore", GOOD_FLANKSCORE_THRESHOLD)
    describe_chi_square(rows, "wcst_error", GOOD_WCST_ERROR_THRESHOLD)
