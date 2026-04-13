# AGENTS.md — IMPKT Director Operations

## Session Startup

Antes de hacer cualquier cosa:

1. Leer `system/state.md` — estado del sistema (fase actual, qué se completó)
2. Leer `system/festival/impkt-migration/campaigns/impkt-migration/state.yaml` — progreso de Festival
3. Revisar `system/alerts/` — acciones pendientes para Gabriel
4. Revisar `system/memory/` — último daily log

No preguntar permiso. Solo hacerlo.

## Comunicación con Gabriel

- Canal directo: esta sesión (Claude Code en Antigravity)
- Canal asíncrono: `ideas/inbox/` → Gabriel deposita material para evaluación
- Alertas: `system/alerts/` → yo documento acciones pendientes

## Sistema de memoria

- `system/state.md` — verdad única del estado actual del sistema
- `system/festival/` — progreso de la migración y tasks
- `system/memory/YYYY-MM-DD.md` — logs diarios de ejecución
- `system/self-improving/memory.md` — correcciones y lecciones learned
- `system/proactivity/memory.md` — reglas proactivas y límites

## Red Lines

- No modificar `C:\Users\oscar\.openclaw\` — referencia solo, no se toca
- No ejecutar `docker compose down -v` — nunca
- No inventar configuración — si no sé, documentar en `system/questions-for-gabriel.md`
- No prometer timeline sin consultar el plan (`plan/migration-festival.md`)

## Tools y Capabilities

- **Read/Write/Edit/Bash** — base del sistema
- **Glob/Grep** — búsqueda de archivos
- **WebFetch/WebSearch** — investigación
- **Graphify** — knowledge graph (leo `graphify-out/GRAPH_REPORT.md` antes de buscar archivos)
- **Agent tool** — sub-agents para tareas paralelas
- **Scheduled tasks** — heartbeat y procesamiento

## Graphify (Knowledge Graph)

graphify está activo. Antes de responder preguntas sobre el codebase o arquitectura:
1. Leer `graphify-out/GRAPH_REPORT.md`
2. Si necesito más detalle, usar `graphify query` en terminal

## Pipeline de Leads

Cuando Gabriel me da información de un lead/cliente:
1. Crear archivo JSON en la carpeta de pipeline correspondiente
2. Notificar al lead siguiente en la cadena
3. Documentar en `system/memory/YYYY-MM-DD.md`

## Alertas

Para crear una alerta para Gabriel:
```
system/alerts/[fecha]-[short-name].md
---
title: "[Breve descripción]"
urgencia: [alta|media|baja]
deadline: [si hay]
 Gabriel necesita: [qué acción]
---
[Detalle]
```

## Heartbeat

Cada sesión nueva: verificar si hay scheduled tasks pendientes de ejecutar.
El heartbeat de sistema está configurado con git hooks (graphify se rebuild en cada commit).

## Ejecución de tasks

Cuando Gabriel me pide ejecutar algo:
1. Si está en Festival, marcar como in_progress en state.yaml
2. Ejecutar
3. Verificar que funcionó
4. Documentar resultado en state.md y daily log
5. Avanzar al siguiente task

---

_Este archivo evoluciona con el sistema._