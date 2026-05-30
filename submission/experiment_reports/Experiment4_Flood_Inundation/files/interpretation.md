# Experiment 4: Physical Interpretation and Limitations

## Physical interpretation

- **Terrain:** Synthetic 100x100 DEM (seed 42), elevation 35.96--68.81 m; median 53.9 m.
- **Valleys flood first:** Central depression and low cells wet before ridges when water level rises from 40 m.
- **Accelerated growth:** Largest step increase in flooded % occurs near 49.5--50.0 m as the water surface crosses many cells near median elevation.
- **Spatial connectivity:** At ~48--50 m, inundation patches merge across the valley floor (visible on contour-overlaid maps).
- **Monotonic curve:** Flooded area and volume increase non-decreasing with stage - consistent with a flat bathtub surface.

## Seed sensitivity (@ 50 m water level)

| Seed | z_min (m) | z_max (m) | Flooded % |
|------|-----------|-----------|-----------|
| 42 | 35.96 | 68.81 | 25.25 |
| 7 | 36.00 | 69.14 | 25.45 |
| 99 | 35.06 | 69.39 | 25.04 |

Inundation percentage depends on terrain realization; different seeds change valley depth and therefore wet cell counts at the same absolute stage.

## Performance (this machine)

| Task | Runtime (ms) |
|------|----------------|
| DEM load (`dem_data.npy`) | 0.23 |
| Single `calculate_flood` | 0.04 |
| Full curve (21 levels) | 2.68 |

## Limitations (model assumptions)

1. **Flat water surface** - no slope along the flood wave.
2. **No hydraulic routing** - isolated depressions could fill in reality only if connected.
3. **No flow momentum** - no Saint-Venant or 2D hydrodynamics.
4. **No infiltration or evaporation** - water does not leave the surface.
5. **No buildings or levees** - barriers are not represented.

Despite these simplifications, bathtub DEM inundation is widely used for rapid flood screening, scenario comparison, and teaching DEM-based risk mapping.
