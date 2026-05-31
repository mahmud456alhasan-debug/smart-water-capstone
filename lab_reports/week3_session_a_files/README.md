# SCS-CN Runoff Calculator

**Author:** Mahmudul Hasan  
**Student ID:** 4125999049  
**Course:** Software Development — Week 3 Session A (Agile Scaffolding)

Calculate runoff depth (Q) from rainfall (P) and curve number (CN) using the
USDA SCS Curve Number method, for flood-risk screening of a watershed.

## Setup

```bash
# Optional: on Ubuntu, if venv creation fails:
#   sudo apt install python3.8-venv

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

### Single calculation
```bash
python3 -m src.cli single 50 80
# Output: P = 50.0 mm, CN = 80  ->  Q = 24.36 mm
```

### Batch processing
```bash
python3 -m src.cli batch
```

### Table
```bash
python3 -m src.cli table 50 70 80 90 --labels forest pasture residential
```

### Plot
```bash
python3 -m src.cli plot --max-P 150 --CN 70 80 90 98
python3 -m src.cli plot --max-P 150 --CN 70 80 90 98 --output runoff_curves.png
```

## Tests

```bash
python3 -m pytest tests/ -v
```

## Data

- `data/cn_lookup.csv` — Land-use → CN mapping
- `data/sample_rainfall.csv` — Sample rainfall events by watershed

## Assumptions

- Initial abstraction Ia = 0.2 × S (standard SCS assumption)
- Curve number CN ∈ [1, 100]
- Runoff Q is clipped to rainfall P (physical upper bound)
