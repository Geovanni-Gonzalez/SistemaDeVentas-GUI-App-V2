# IMPROVEMENT_ROADMAP — SistemaDeVentas-GUI-App-V2

Backlog priorizado. Impacto/Esfuerzo: Alto/Medio/Bajo.

## Quick Wins

| # | Mejora | Impacto | Esfuerzo | Prioridad |
|---|---|---|---|---|
| 1 | Hashear contraseñas (`hashlib.sha256`+salt) en `auth.py` y `Acceso.txt`; eliminar el usuario `admin;admin` | Alto | Bajo | P0 |
| 2 | Commitear el untracking de `sistema_ventas.db` y el CSV generado (aplicado en esta revisión) | Medio | Bajo | P0 |
| 3 | GitHub Topics: `python`, `tkinter`, `sqlite`, `crud`, `desktop-app` + descripción; enlazar V1↔V2 en ambos READMEs (narrativa de evolución) | Medio | Bajo | P1 |
| 4 | Captura de la UI (facturación o analítica) en el README | Medio | Bajo | P1 |

## Mejoras técnicas

| # | Mejora | Impacto | Esfuerzo | Prioridad |
|---|---|---|---|---|
| 5 | Tests con SQLite en memoria para `Repository` y `analytics` + ejecutarlos en CI (hoy solo `compileall`) | Alto | Medio | P1 |
| 6 | Whitelist de nombres de tabla en `Repository` (hoy interpola f-string) | Medio | Bajo | P1 |
| 7 | Completar emailer con config por variables de entorno, o retirar los módulos esqueleto (email/WhatsApp) | Medio | Medio | P2 |

## Mejoras de GitHub

Ya presentes: badge CI, LICENSE, `.gitignore`. Faltan: Topics (item 3), captura (item 4), enunciado o descripción del problema en `docs/`.
