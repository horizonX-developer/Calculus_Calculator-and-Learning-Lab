# v2.11 — Curriculum audit and coverage matrix

This is an **evidence-based initial inventory**, not a certification of complete curriculum coverage. “Selected examples” means the code exposes a related solver or example, not that every problem in the topic works. “Not verified” is not necessarily absent. “Partial” does not mean fully taught or tested.

## Initial audit totals

| Subject | Listed topics | Partially evidenced | Not yet verified |
|---|---:|---:|---:|
| Differential Calculus | 27 | 13 | 14 |
| Integral Calculus | 32 | 18 | 14 |
| Differential Equations | 31 | 10 | 21 |

## Evidence inspected

- `app.py`: three general calculators and curriculum navigation.
- `applications.py`: Riemann sums, area, volume methods, arc length, surface area, improper/numerical integration.
- `ode_methods.py`: exact and homogeneous first-order methods.
- `practice.py`, `practice_generator.py`, `practice_topics.py`, `scenario_generator.py`: selected practice templates.
- `volume_visualizer.py`, `cross_section_visualizer.py`: selected 3D visualization modes.

## Criteria before calling a topic complete

A topic must have (1) appropriate solver and domain handling, (2) verified worked steps, (3) varied exercises by difficulty, (4) meaningful graph or explicit reason why none applies, (5) student-friendly input guidance, and (6) dedicated mathematical tests.

## Priority implementation sequence

1. v2.12: limits, continuity, derivative-from-definition, derivative rules and associated exercises.
2. v2.13: related rates, optimization, curve sketching, mean value theorem and approximation.
3. v2.14–15: integration techniques, numerical sums, areas, solids and other applications.
4. v2.16–17: first- and higher-order ODEs, modeling, transforms and numerical methods.
5. v2.18+: connect practice, visualizations and guided steps to each audited topic.

See `CURRICULUM_AUDIT.csv` for the full topic-by-topic matrix.
