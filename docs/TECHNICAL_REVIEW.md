# TECHNICAL_REVIEW — SistemaDeVentas-GUI-App-V2

Fecha de revisión: 2026-07-16
Método: análisis estático, CI y git. Sin enunciado en `docs/`. Sin ejecución (app Tkinter interactiva); CI hace `compileall`.

## 1. Comprensión del proyecto

Segunda iteración de un sistema de ventas de escritorio en **Python/Tkinter** (~2,030 LOC): evolución de la V1 basada en archivos planos hacia **SQLite con patrón Repository**, más módulos de analítica, reportes, exportación CSV ("cloud sync"), logging, escáner y clientes de email/WhatsApp (estos últimos como esqueleto con placeholders, honestamente señalado en el README).

## 2. Arquitectura

| Capa | Evidencia |
|---|---|
| Repository genérico sobre SQLite (mapper `from_row`, conexiones administradas, errores logueados) | `src/repository.py`, `src/database.py` |
| Dominio y modelos | `src/models.py` |
| UI Tkinter modular (6 ventanas + tema) | `src/ui/` |
| Servicios auxiliares | `analytics.py`, `reports.py`, `cloud_sync.py`, `logger.py`, `emailer.py` (esqueleto), `whatsapp_client.py` |
| Seed reproducible | `seed_data.py` |

## 3. Fortalezas

1. Narrativa de evolución V1→V2 (archivos planos → BD + capas) — evidencia de refactor deliberado, el README lo articula.
2. Repository con manejo de errores y logging centralizado — patrón correcto para el tamaño del proyecto.
3. Honestidad en el README sobre módulos pendientes de configuración (email/WhatsApp).

## 4. Debilidades y riesgos

| Hallazgo | Severidad | Nota |
|---|---|---|
| **Contraseñas en texto plano**: `data/Acceso.txt` trackeado (`admin;admin`) y comparación directa en `auth.py` (`user.password == password`) | Media | Hashear con `hashlib` (mismo hallazgo que MiniWaze) |
| ~~`sistema_ventas.db` (binario) y export CSV generado trackeados~~ | — | Corregido: `git rm --cached` + `.gitignore` |
| `SELECT * FROM {self.table_name}` con f-string — inyección si `table_name` fuera externo (hoy es interno, riesgo latente) | Baja-Media | Whitelist de tablas |
| Sin tests; CI solo `compileall` | Media | `analytics`/`repository` son testeables con SQLite en memoria |
| Módulos esqueleto (emailer con placeholder comentado) | Baja | Completar o retirar para no diluir el repo |

## 5. Evaluación profesional

- Nivel demostrado: **Junior+**. Estructura por capas correcta y evolución visible; auth de texto plano y falta de tests marcan el techo.
- Rol en el portafolio: refuerza Python/SQLite/Tkinter; su valor diferencial es la **historia de refactor V1→V2**. Citar V2 (no V1) si se menciona.

## 6. Recomendaciones

Ver `IMPROVEMENT_ROADMAP.md`. P0: hashear credenciales; commitear untracking del .db.
