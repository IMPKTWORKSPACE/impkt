# plan/migration-festival.md

## Concepto de Festival en IMPKT

Festival es la metodología interna de planificación de IMPKT. Cada festival tiene:

- **Campaign** — objetivo macroeconómico de la campaña
- **Phases** — fases mayores de trabajo
- **Sequences** — secuencias de trabajo relacionadas
- **Tasks** — tareas atómicas y ejecutables

Festival funciona en un loop contínuo:
1. Leer la siguiente tarea del festival activo
2. Ejecutar la tarea
3. Verificar que se completó
4. Marcar como completada
5. Avanzar a la siguiente

---

## Campaign: impkt-migration

**Objetivo:** Migrar de OpenClaw a IMPKT nativo (Claude Code + Antigravity + RUFLO)
**Duración estimada:** 4-6 semanas
**Stakeholder:** Gabriel (decisiones estratégicas y aprobaciones)
**Directorio base:** `C:\Users\oscar\impkt\`
**Directorio de estado:** `system\festival\impkt-migration\`

---

## FASE 1: Fundaciones del Sistema

**Objetivo:** Construir la base sobre la cual opera todo el sistema IMPKT.
**Entregable:** Sistema base configurado, Agent Teams listos, graphify activo.

### Sequence 1.1: Configuración Base

| Task | Descripción | Estado |
|------|-------------|--------|
| 1.1.1 | Instalar RUFLO (`npx ruflo@latest init --wizard`) | COMPLETADO |
| 1.1.2 | Configurar Agent Teams (5 leads) en settings.json | PENDIENTE |
| 1.1.3 | Documentar identidad de cada lead (Mila, Lena, Sofia, Finn, Nova) | PENDIENTE |
| 1.1.4 | Crear system prompts para los 5 leads | PENDIENTE |
| 1.1.5 | Configurar Scheduled tasks para heartbeat del sistema | PENDIENTE |

**Notas de Sequence 1.1:**
- RUFLO ya instalado según estado actual
- Agent Teams se configuran via `settings.json` con la sintaxis de Claude Code
- Cada lead recibe un workspace dedicado en `agents/<lead-name>/`
- Heartbeat: task programada cada 15 minutos que actualiza `system/state.md`

---

### Sequence 1.2: Sistema de Memoria

| Task | Descripción | Estado |
|------|-------------|--------|
| 1.2.1 | Configurar state.md con capas (CONTEXT, MEMORY, daily logs) | PENDIENTE |
| 1.2.2 | Implementar protocolo de session handoff | PENDIENTE |
| 1.2.3 | Crear self-improving memory para el sistema | PENDIENTE |
| 1.2.4 | Configurar proactivity state | PENDIENTE |

**Notas de Sequence 1.2:**
- `system/state.md` se estructura con secciones delineated por `---`
- Session handoff: al final de cada sesión, escribir resumen en `system/state.md` incluyendo última tarea, siguiente tarea, decisiones y problemas
- Self-improving memory: al completar cada task, el sistema escribe lecciones aprendidas en `system/memory-lessons.md`
- Proactivity state: tracking de qué tasks están pendientes de proactivación

---

### Sequence 1.3: Graphify Completo

| Task | Descripción | Estado |
|------|-------------|--------|
| 1.3.1 | Construir grafo de TODO el workspace (no solo la raíz) | PENDIENTE |
| 1.3.2 | Configurar --watch para auto-rebuild en cambios | PENDIENTE |
| 1.3.3 | Crear wiki del workspace | PENDIENTE |
| 1.3.4 | Instalar git hooks para graph rebuild post-commit | PENDIENTE |

**Notas de Sequence 1.3:**
- Graphify está en `C:\Users\oscar\impkt\tools\graphify\`
- Revisar README de graphify para opciones de `--watch` y recursive traversal
- Git hook: `.git\hooks\post-commit` que ejecuta `node graphify.js --rebuild`
- Wiki del workspace: archivo `knowledge\index.md` que sirve como entrada principal

---

## FASE 2: OpenClaw como Telegram Bot

**Objetivo:** Reducir OpenClaw a su función mínima: bot de Telegram para Gabriel.
**Entregable:** OpenClaw funcionando solo como Telegram bot, sin agents ni memory ni cron.
**Dependencias:** Puede correr en paralelo con FASE 1.

### Sequence 2.1: Configuración Mínima

| Task | Descripción | Estado |
|------|-------------|--------|
| 2.1.1 | Verificar que OpenClaw sigue funcionando como Telegram bot | PENDIENTE |
| 2.1.2 | Desconectar todo lo que no sea Telegram (memory, agents, cron) | PENDIENTE |
| 2.1.3 | Limpiar openclaw.json de secciones no usadas | PENDIENTE |
| 2.1.4 | Hacer backup limpio de .openclaw | PENDIENTE |

**Notas de Sequence 2.1:**
- NO modificar nada en `C:\Users\oscar\.openclaw\` — es solo referencia
- Backup se hace copiando a `C:\Users\oscar\impkt\backup\openclaw\`
- Limpiar `openclaw.json` significa dejar solo la sección `telegram` y credenciales necesarias
- Los agents, memory, cron, swarm se documentan como descartados en `audit/discarded-assets.md`

---

### Sequence 2.2: Testing de Telegram

| Task | Descripción | Estado |
|------|-------------|--------|
| 2.2.1 | Verificar que Telegram bot responde | PENDIENTE |
| 2.2.2 | Documentar commands disponibles del bot | PENDIENTE |
| 2.2.3 | Configurar Telegram como canal de comunicación de Gabriel | PENDIENTE |

**Notas de Sequence 2.2:**
- Commands típicos esperados: `/start`, `/status`, `/help`, `/leads`
- Documentar en `system/openclaw-commands.md` los commands disponibles
- Telegram como canal: garantizar que Gabriel recibe notifications de tasks importantes

---

## FASE 3: Agente Principal IMPKT (El Director)

**Objetivo:** Construir la identidad y configuración del sistema central (yo, el Director).
**Entregable:** Director configurado con SOUL.md, system prompts propios, y protocolo de handover.
**Dependencias:** FASE 1 completa.

### Sequence 3.1: Identidad

| Task | Descripción | Estado |
|------|-------------|--------|
| 3.1.1 | Crear SOUL.md para el sistema IMPKT (basado en auditoría de Jarvis) | PENDIENTE |
| 3.1.2 | Crear identidad del "Director" | PENDIENTE |
| 3.1.3 | Documentar reglas de comunicación | PENDIENTE |
| 3.1.4 | Definir response structure (WHY/STEPS/TOOLS/MEASURE/RISKS) | PENDIENTE |

**Notas de Sequence 3.1:**
- SOUL.md se inspira en `C:\Users\oscar\.openclaw\workspace\SOUL.md`
- Identidad del Director: soy el orchestrator central de IMPKT, mi trabajo es coordinar los 5 leads
- Response structure copiada de las reglas de no negociar de CLAUDE.md
- Reglas de comunicación: mínimo 1 actualización a Gabriel por día, solo escalar cuando hay decisión requerida

---

### Sequence 3.2: Configuración del Director

| Task | Descripción | Estado |
|------|-------------|--------|
| 3.2.1 | Actualizar CLAUDE.md propio para IMPKT | PENDIENTE |
| 3.2.2 | Configurar workspace del Director | PENDIENTE |
| 3.2.3 | Implementar sistema de memoria en capas | PENDIENTE |
| 3.2.4 | Crear protocolo de handover entre sesiones | PENDIENTE |

**Notas de Sequence 3.2:**
- CLAUDE.md ya existe en `C:\Users\oscar\impkt\CLAUDE.md` — necesita actualización tras auditoría de OpenClaw
- Workspace del Director: `C:\Users\oscar\impkt\` con subdirectorios para cada dominio
- Memoria en capas: CONTEXT (estado actual) → MEMORY (historial de decisiones) → daily logs (actividad diaria)
- Handover: protocolo documentado en `system/handover-protocol.md`

---

## FASE 4: Implementación de Agent Teams

**Objetivo:** Configurar los 5 leads con sus identities, tools, y pipelines completos.
**Entregable:** 5 leads operativos y documentados, cada uno con su workspace y métricas.
**Dependencias:** FASE 3 completa (el Director coordina los leads).

### Sequence 4.1: Mila (Marketing)

| Task | Descripción | Estado |
|------|-------------|--------|
| 4.1.1 | Definir system prompt completo de Mila | PENDIENTE |
| 4.1.2 | Configurar herramientas de Mila (SEO, content, campaigns) | PENDIENTE |
| 4.1.3 | Implementar pipeline de generación de leads | PENDIENTE |
| 4.1.4 | Crear métricas y dashboard de Mila | PENDIENTE |

**Métricas de Mila:** leads generados/mes, tráfico SEO, engagement campaigns.

---

### Sequence 4.2: Lena (Outreach)

| Task | Descripción | Estado |
|------|-------------|--------|
| 4.2.1 | Definir system prompt completo de Lena | PENDIENTE |
| 4.2.2 | Configurar pipeline de primer contacto | PENDIENTE |
| 4.2.3 | Implementar scoring de calificación | PENDIENTE |
| 4.2.4 | Crear templates de discovery | PENDIENTE |

**Métricas de Lena:** tasa de respuesta primer contacto, score promedio de leads, conversions a qualified.

---

### Sequence 4.3: Sofia (Sales)

| Task | Descripción | Estado |
|------|-------------|--------|
| 4.3.1 | Definir system prompt completo de Sofia | PENDIENTE |
| 4.3.2 | Configurar pipeline de propuestas | PENDIENTE |
| 4.3.3 | Implementar sistema de pricing (con catálogo de servicios) | PENDIENTE |
| 4.3.4 | Crear templates de cierre | PENDIENTE |

**Métricas de Sofia:** proposals enviadas, close rate, ticket promedio.

---

### Sequence 4.4: Finn (Production)

| Task | Descripción | Estado |
|------|-------------|--------|
| 4.4.1 | Definir system prompt completo de Finn | PENDIENTE |
| 4.4.2 | Configurar Claude Code como builder | PENDIENTE |
| 4.4.3 | Implementar pipeline de desarrollo | PENDIENTE |
| 4.4.4 | Crear checklist de QA para cada proyecto | PENDIENTE |

**Métricas de Finn:** proyectos completados, tiempo de entrega, satisfaction score.

---

### Sequence 4.5: Nova (Client Comms)

| Task | Descripción | Estado |
|------|-------------|--------|
| 4.5.1 | Definir system prompt completo de Nova | PENDIENTE |
| 4.5.2 | Configurar pipeline de seguimiento post-venta | PENDIENTE |
| 4.5.3 | Implementar sistema de soporte nivel 1 | PENDIENTE |
| 4.5.4 | Crear templates de comunicación | PENDIENTE |

**Métricas de Nova:** CSAT, tiempo de respuesta, issues resueltos nivel 1.

---

## FASE 5: Repositorio de Ideas

**Objetivo:** Crear el sistema de intake, evaluación e implementación de ideas de Gabriel.
**Entregable:** Pipeline completo de ideas funcional con scheduled polling.
**Dependencias:** FASE 1 (sistema base necesita estar listo).

### Sequence 5.1: Setup

| Task | Descripción | Estado |
|------|-------------|--------|
| 5.1.1 | Crear estructura de carpetas (inbox/processing/approved/implemented/discarded) | PENDIENTE |
| 5.1.2 | Implementar script de detección de nuevas ideas | PENDIENTE |
| 5.1.3 | Crear template de idea (formato YAML frontmatter) | PENDIENTE |

**Estructura de carpetas:**
```
ideas/
├── inbox/           # Material sin procesar
├── processing/      # En evaluación
├── approved/        # Aprobadas para implementar
├── implemented/     # Ya implementadas
├── discarded/       # Descartadas con justificación
├── index.md         # Índice con estado de cada idea
└── templates/
    └── idea-template.md
```

**Template de idea (YAML frontmatter):**
```yaml
---
id: idea-001
title: "[título]"
source: "[link/archivo/texto]"
received: YYYY-MM-DD
status: inbox|processing|approved|implemented|discarded
evaluation:
  utility_score: 1-10
  effort: low|medium|high
  strategic_fit: yes|no|maybe
  notes: ""
---
```

---

### Sequence 5.2: Workflow

| Task | Descripción | Estado |
|------|-------------|--------|
| 5.2.1 | Implementar pipeline de evaluación automática | PENDIENTE |
| 5.2.2 | Configurar scheduled task de polling | PENDIENTE |
| 5.2.3 | Crear index.md actualizado | PENDIENTE |
| 5.2.4 | Implementar conversión a tasks de Festival | PENDIENTE |

**Notas de Sequence 5.2:**
- Polling: scheduled task cada hora que revisa `ideas/inbox/`
- Evaluación automática: extraer contenido relevante, puntuar utilidad, esfuerzo y strategic fit
- Conversión a tasks: approved ideas se convierten en tasks dentro del festival activo más reciente
- index.md: tabla con todas las ideas, su estado, y fecha de última actualización

---

## FASE 6: Testing End-to-End

**Objetivo:** Validar que todo el sistema funciona correctamente de extremo a extremo.
**Entregable:** Reporte de testing completo con bottlenecks identificados y optimizaciones aplicadas.
**Dependencias:** TODO lo anterior completo.

### Sequence 6.1: Prueba de Integración

| Task | Descripción | Estado |
|------|-------------|--------|
| 6.1.1 | Simular un lead completo (Mila → Lena → Sofia → Finn → Nova) | PENDIENTE |
| 6.1.2 | Verificar que memoria persiste entre agentes | PENDIENTE |
| 6.1.3 | Probar que el Director supervisa correctamente | PENDIENTE |
| 6.1.4 | Documentar bottlenecks | PENDIENTE |

**Notas de Sequence 6.1:**
- Simular significa ejecutar el pipeline completo con datos de prueba controlados
- Memoria persistente: verificar que `system/state.md` se actualiza correctamente entre agentes
- Supervisión del Director: verificar que el Director recibe updates y puede intervenir si es necesario

---

### Sequence 6.2: Performance

| Task | Descripción | Estado |
|------|-------------|--------|
| 6.2.1 | Medir latencia de Agent Teams | PENDIENTE |
| 6.2.2 | Verificar que graphify no degrade performance | PENDIENTE |
| 6.2.3 | Optimizar prompts si es necesario | PENDIENTE |

**Notas de Sequence 6.2:**
- Latencia objetivo: <5 segundos por handover entre agentes
- Graphify: medir overhead de rebuild completo vs rebuild incremental
- Optimizaciones: reducir tokens en system prompts si es necesario, cachear resultados comunes

---

## Timeline Sugerido

| Semana | Fases | Entregables |
|--------|-------|-------------|
| **Semana 1** | FASE 1 + FASE 2 | Sistema base funcionando, OpenClaw mínimo como Telegram bot |
| **Semana 2** | FASE 3 + FASE 4 | Director + 5 leads configurados y documentados |
| **Semana 3** | FASE 5 | Repositorio de ideas operativo con polling activo |
| **Semana 4** | FASE 6 | Testing completo, ajustes, reporte final |

> **Nota:** La semana 4-6 puede extenderse según el tamaño del proyecto de migración y dependencias con Gabriel.

---

## Dependencias Entre Fases

```
FASE 1 (Fundaciones)
    ├── COMPLETA ANTES de FASE 3
    └── Puede correr en paralelo con FASE 2

FASE 2 (OpenClaw mínimo)
    └── Puede correr en paralelo con FASE 1

FASE 3 (Director) ─── COMPLETA ANTES de FASE 4
    └── Sin Director no hay coordinación de leads

FASE 4 (Agent Teams)
    └── Depende de FASE 3

FASE 5 (Ideas)
    └── Depende de FASE 1 (sistema base)

FASE 6 (Testing)
    └── Depende de TODO lo anterior
```

---

## Archivos de Estado de Festival

Ubicación: `system\festival\impkt-migration\`

```
system/festival/impkt-migration/
├── CAMPAIGN_GOAL.md          # Este documento (referencia)
├── state.yaml                # Estado actual de cada phase/sequence/task
├── festivals/
│   ├── planning/             # Tasks futuras no iniziadas
│   ├── active/               # Task actualmente en ejecución
│   └── completed/            # Tasks completadas (con evidencia)
└── logs/
    └── session-logs/         # Logs de cada sesión de trabajo
```

**Formato de state.yaml:**
```yaml
campaign: impkt-migration
current_phase: 1
current_sequence: 1.2
current_task: 1.2.1
phases:
  1:
    status: in_progress
    sequences_completed: [1.1]
    sequences_in_progress: [1.2]
  2:
    status: pending
  3:
    status: pending
  4:
    status: pending
  5:
    status: pending
  6:
    status: pending
last_updated: YYYY-MM-DDTHH:MM:SS
next_action: description of next step
blockers: []
```

---

## Reglas de Ejecución

1. **Una tarea a la vez.** No avanzar a la siguiente task hasta verificar que la actual se completó.
2. **Documentar evidencia.** Al completar cada task, guardar output/evidencia en `system/festival/impkt-migration/festivals/completed/`.
3. **Actualizar state.yaml** después de cada task completada.
4. **Si una task falla:** analizar error, documentar en `system/problems-found.md`, reintentar max 2 veces antes de escalar a Gabriel.
5. **Sesiones largas:** guardar estado cada 30 minutos mínimo en `system/state.md`.
6. **Handover:** al terminar sesión, escribir resumen en `system/state.md` incluyendo qué se hizo, qué sigue, y qué bloqueos hay.

---

_Festival: impkt-migration · Creado: 2026-04-12 · Sistema IMPKT_
