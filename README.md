# EMPATH

**A Multilingual Auditor–Judge Benchmark for Safety Evaluation of Emotional-Support Chatbots**

Author: **Camilo Chacón Sartori** ([ORCID 0000-0002-8543-9893](https://orcid.org/0000-0002-8543-9893)) — MindSurf.

Artifact accompanying the paper *"EMPATH: A Multilingual Auditor–Judge Benchmark
for Safety Evaluation of Emotional-Support Chatbots,"* accepted at MICAI 2026
(Springer LNAI). Preprint: arXiv [2606.30256](https://arxiv.org/abs/2606.30256).
Archived on Zenodo: [10.5281/zenodo.20844846](https://doi.org/10.5281/zenodo.20844846).

## Contents

- **`empath/`** — the benchmark instrument: seed instructions, personas, the
  19-metric rubrics across 5 dimensions (`dimensions/`), the auditor–judge
  pipeline (`solvers/`, `scorers/`, `tasks/`, `judges/`), and scenario tooling.
  Built on Inspect AI with a Petri-derived auditor. Targets are pluggable Inspect
  providers; the harness injects no system prompt of its own.

- **`results/`** — processed results behind the paper's figures:
  - `s1_calibration.json` — S1 judge calibration (standard vs. strict rubric over
    the 57 grid conversations).
  - `s2_grid_and_interjudge.json` — S2 three-model grid (judge A) and cross-family
    inter-judge agreement (judge B).
  - `s3_en_grid_and_retest.json` — the en-US replication under the same protocol:
    three-model grid (aggregates 8.16, 8.11, 8.00), five-run means and spreads,
    and cross-family inter-judge agreement.
  - `locale_retest_five_runs.json` — per-model, per-metric five-run scores in both
    locales (57 rows), with medians and per-metric significance. This is the file
    behind the locale-linked soft-spot analysis.
  - `p5_deepseek_temperature0_en.json` — deepseek-v4-pro re-run five times at
    temperature 0 in en-US: per-metric spread across identical re-runs.
  - `figures/` — the published figures (taxonomy, calibration, grid heatmap,
    inter-judge agreement).

- **`human_eval/`** — preliminary clinician-concordance study (anonymized):
  - `clinician_ratings.csv` — two licensed psychologists' blind pairwise ratings of
    50 synthetic transcripts, per metric/sub-dimension, for two **undisclosed**
    systems (`System_A` / `System_B`).
  - `clinician_notes.csv` — the clinicians' free-text observations (these reference
    the on-screen response order, which was randomized per rater).
  - `judge_preferences.csv` — the EMPATH judge's preference per item.
  - `reproduce_concordance.py` — recomputes the judge–clinician and
    clinician–clinician agreement (% and Gwet's AC1) from the two CSVs above.

## Anonymization and scope

- The two rated systems are deliberately undisclosed (`System_A` / `System_B`); **no
  key** mapping them to real systems is included, and the paper reports no
  system-vs-system comparison. Clinician identities are anonymized
  (`Clinician_1` / `Clinician_2`).
- Provider-specific target/model adapters are **not** included; targets are
  pluggable Inspect providers.
- All conversations are **synthetic** (auditor-generated role-play); there is no
  patient or end-user data.

## Reproducing the human-concordance result

```
cd human_eval
python reproduce_concordance.py
```

prints, for each clinician and for the two clinicians against each other, the
preference-agreement rate and Gwet's AC1 (the prevalence-robust coefficient used
in the paper).

## Citation

```bibtex
@misc{chaconsartori2026empath,
  title         = {{EMPATH}: A Multilingual Auditor--Judge Benchmark for Safety
                   Evaluation of Emotional-Support Chatbots},
  author        = {Chac\'on Sartori, Camilo},
  year          = {2026},
  eprint        = {2606.30256},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CL}
}
```

## License

- **Code** (`empath/`): Apache-2.0 — see [`LICENSE`](LICENSE).
- **Data** (`results/`, `human_eval/`): CC-BY-4.0 — see [`LICENSE-DATA-CC-BY-4.0.txt`](LICENSE-DATA-CC-BY-4.0.txt).

© 2026 MindSurf.
