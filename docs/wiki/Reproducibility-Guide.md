# Reproducibility Guide

How to reproduce reports, figures, and validation results.

## Quick start

```bash
git clone https://github.com/mahmud456alhasan-debug/smart-water-capstone.git
cd smart-water-capstone
python3 -m pip install -r requirements.txt
streamlit run app/main.py
pytest -q
```

Copy `dem.npy` into `data/` for the flood tab.

## PDF reports

| Document | Location |
|----------|----------|
| AI Engineering Portfolio | `submission/portfolio/` |
| Experiment 1–4 reports | `submission/experiment_reports/` |
| Release bundle (short names) | `release/` |
| Weekly lab reports (16) | `lab_reports/` |

Regenerate experiment PDFs: see [submission/README.md](../../submission/README.md) in the main repo.

## Audit summaries

Each experiment includes `audit_summary.txt` in its submission folder — reproducibility scorecards for figures, tests, and validation CLIs.

## Lab report appendices

Appendix code and prompt logs: `lab_reports/week*_files/`

## Release

Official PDF bundle: [v1.0 — Smart Water Lab Submission](https://github.com/mahmud456alhasan-debug/smart-water-capstone/releases/tag/v1.0.0)

## Related

- [Home](Home.md)
- [Validation Strategy](Validation-Strategy.md)
