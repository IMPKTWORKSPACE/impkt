# CONTEXT.md — Session Handoff

**Fecha:** 2026-04-12
**Última actualización:** 11:20 AM CST

## Estado actual del sistema

**Fase:** TAREA 3 — Ejecución de migración (FASE 1 en progreso)
**Agent Teams:** 5 leads configurados (Mila, Lena, Sofia, Finn, Nova) con SOUL.md individuales
**Pipeline:** Estructura creada en `pipeline/` (mila-to-lena, lena-to-sofia, etc.)
**Graphify:** Funcional con grafo de 68 nodos en `graphify-out/`
**RUFLO:** Instalado (v3.5.80)

## Qué se completó hoy

- TAREA 0 ✅ — Sistema construido (Obsidian, Graphify, Festival structure)
- TAREA 1 ✅ — Auditoría de OpenClaw (8 archivos en `audit/`)
- TAREA 2 ✅ — Planes creados (features-map, agent-teams, ideas-repository, migration-festival)
- FASE 1, SEQ 1.1, Tasks 1.1.1-1.1.4 ✅ — Agent Teams configurados

## Qué sigue (inmediato)

1. SEQ 1.1.5 — Scheduled tasks para heartbeat del sistema
2. SEQ 1.2 — Sistema de memoria en capas
3. SEQ 1.3 — Graphify completo del workspace

## Pipeline activo

```
Mila → Lena → Sofia → Finn → Nova
```
Por ahora vacío (no hay clientes aún). Cuando lleguen leads, fluirán por el pipeline.

## Problemas abiertos

1. ANTHROPIC_BASE_URL = `https://api.minimax.io/anthropic` (no chat.minimax) — funcionando, dejado
2. Festival se replica manualmente (no se pudo instalar en WSL)
3. Obsidian vault = raíz impkt (no knowledge/)

## Reglas críticas recordadas

- NO modificar `C:\Users\oscar\.openclaw\` — solo lectura
- NO ejecutar `docker compose down -v` — NUNCA
- Guardar TODO en disco antes de cada milestone

## Notas para próxima sesión

- Si sesión se corta, leer `system/state.md` y continuar en FASE 1
- Graphify hook activo — leer GRAPH_REPORT.md antes de Glob/Grep
- OpenClaw solo como Telegram bot (no como executor)