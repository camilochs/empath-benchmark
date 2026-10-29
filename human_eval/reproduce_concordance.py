"""
Recompute the preliminary human-concordance result from the anonymized CSVs:
judge vs each clinician, and clinician vs clinician, as preference-agreement rate
and Gwet's AC1 (prevalence-robust chance-corrected agreement).

Usage:  python reproduce_concordance.py
Only the Python standard library is required.
"""
import csv
from collections import defaultdict


def load_clinician_prefs(path="clinician_ratings.csv"):
    # one preferred_system per (clinician, entry); rows repeat it across sub-metrics
    pref = defaultdict(dict)  # clinician -> {entry: 'System_A'|'System_B'|'none'}
    for r in csv.DictReader(open(path)):
        pref[r["clinician"]][r["entry_id"]] = r["preferred_system"]
    return pref


def load_judge_prefs(path="judge_preferences.csv"):
    return {r["entry_id"]: r["judge_preferred_system"] for r in csv.DictReader(open(path))}


def agreement(a, b):
    """a, b: dict entry -> 'System_A'/'System_B' (ignore 'none'/'tie'). Returns n, %agree, Gwet AC1."""
    keys = [k for k in a if k in b
            and a[k] in ("System_A", "System_B") and b[k] in ("System_A", "System_B")]
    n = len(keys)
    if n == 0:
        return 0, float("nan"), float("nan")
    agree = sum(1 for k in keys if a[k] == b[k])
    pa = agree / n
    pi = (sum(a[k] == "System_A" for k in keys) + sum(b[k] == "System_A" for k in keys)) / (2 * n)
    pe = 2 * pi * (1 - pi)               # Gwet's AC1 chance term (2 categories)
    ac1 = (pa - pe) / (1 - pe) if pe != 1 else float("nan")
    return n, pa, ac1


def main():
    clin = load_clinician_prefs()
    judge = load_judge_prefs()
    names = sorted(clin)
    print(f"{'comparison':<34}{'n':>4}{'agree%':>9}{'Gwet AC1':>10}")
    for c in names:
        n, pa, ac1 = agreement(judge, clin[c])
        print(f"{'judge vs '+c:<34}{n:>4}{pa*100:>8.0f}%{ac1:>+10.2f}")
    if len(names) == 2:
        n, pa, ac1 = agreement(clin[names[0]], clin[names[1]])
        print(f"{names[0]+' vs '+names[1]:<34}{n:>4}{pa*100:>8.0f}%{ac1:>+10.2f}")


if __name__ == "__main__":
    main()
