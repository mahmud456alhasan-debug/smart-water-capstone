# Validation Strategy

Swiss Cheese verification across AI-assisted development and physical modeling.

## Layers

| Layer | Implementation |
|-------|----------------|
| AI review | Human correction of 9/52 reviewed deliverables (83% first-pass) |
| Unit tests | **88** pytest cases across capstone and experiment modules |
| Physical rules | Hand-validated reference cases (e.g. SCS-CN Q = 13.80 mm) |
| Validation CLI | 4 dedicated `validate_*` scripts with batch checks |
| Report evidence | PDF reports, figures, `audit_summary.txt` per experiment |

## Results snapshot

| Experiment | Validation outcome |
|------------|-------------------|
| Rainfall | Alert thresholds + forecast pipeline tested with mocked API |
| SCS-CN runoff | Reference case Q = 13.80 mm at P = 50, CN = 80 |
| Reservoir | Monte Carlo P10/P50/P90; constraint satisfaction |
| Flood | **9/9** physical checks (monotonicity, bounds, DEM) |

## Threats to validity

- OpenWeather spatial/temporal sparsity
- SCS-CN lumped CN parameterization
- Bathtub flood model simplification
- LLM hallucination risk in AI-generated code

Full analysis: [AI Engineering Portfolio](AI-Engineering-Portfolio.md)

## Related

- [Home](Home.md)
- [Reproducibility Guide](Reproducibility-Guide.md)
