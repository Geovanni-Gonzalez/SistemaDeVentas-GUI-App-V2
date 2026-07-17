# CV_EVIDENCE — SistemaDeVentas-GUI-App-V2

Reinforcement evidence (Python, SQLite, Tkinter). Unique angle: deliberate V1→V2 evolution.

## Unique evidence

| Item | Evidence |
|---|---|
| Refactor narrative: flat-file system (V1 repo) → layered SQLite system with generic Repository | `src/repository.py`, `src/database.py` vs. SistemaDeVentas--GUI-App (V1) |
| Centralized logging around data access | `src/logger.py` used in repository error paths |
| Modular Tkinter UI at medium scale (6 windows + theming) | `src/ui/` |

## Optional resume bullet

- Re-architected a flat-file sales management desktop app into a layered Python/SQLite system (generic repository with error logging, seed scripts, analytics, and CSV export), demonstrating deliberate refactoring across versions.

## ATS keywords (incremental)

SQLite, repository pattern, refactoring, Tkinter, desktop CRUD, data export, logging.
