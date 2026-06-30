# EMPATH

**A Multilingual Auditor–Judge Benchmark for Safety Evaluation of Emotional-Support Chatbots**

Author: **Camilo Chacón Sartori** ([ORCID 0000-0002-8543-9893](https://orcid.org/0000-0002-8543-9893)) — MindSurf.

Companion artifact to the paper *"EMPATH: A Multilingual Auditor–Judge Benchmark
for Safety Evaluation of Emotional-Support Chatbots"* (arXiv: [2606.30256](https://arxiv.org/abs/2606.30256)).

## Contents

- **`empath/`** — the benchmark instrument: seed instructions, personas, the
  19-metric rubrics across 5 dimensions (`dimensions/`), the auditor–judge
  pipeline (`solvers/`, `scorers/`, `tasks/`, `judges/`), and scenario tooling.
  Built on Inspect AI with a Petri-derived auditor. Targets are pluggable Inspect
  providers; the harness injects no system prompt of its own.

- **`results/`** — processed results behind the paper's figures:
  `s1_calibration.json` (judge calibration, standard vs. strict rubric),
  `s2_grid_and_interjudge.json` (three-model grid + cross-family inter-judge
  agreement), and `figures/`.

- **`human_eval/`** — preliminary clinician-concordance study: two licensed
  psychologists' blind pairwise ratings of 50 synthetic transcripts
  (`clinician_ratings.csv`), their free-text notes (`clinician_notes.csv`), the
  judge's per-item preferences (`judge_preferences.csv`), and
  `reproduce_concordance.py`, which recomputes the agreement coefficients.

## Scope and privacy

- The two rated systems in the clinician study are **deliberately undisclosed**
  (`System_A` / `System_B`); the paper reports no system-vs-system comparison
  (see its ethics and conflict-of-interest statement). Clinician identities are
  **anonymized** (`Clinician_1` / `Clinician_2`).
- All conversations are **synthetic** (auditor-generated role-play); there is no
  patient or end-user data.
- Provider-specific target adapters are not included; targets are pluggable.

## Reproduce the human-concordance result

```
cd human_eval
python reproduce_concordance.py
```

prints, for each clinician and for the two clinicians against each other, the
preference-agreement rate and Gwet's AC1.

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
