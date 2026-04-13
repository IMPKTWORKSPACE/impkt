# Veredicto — Auditoría de OpenClaw para IMPKT

**Fecha:** 2026-04-12
**Auditor:** Sistema IMPKT (agente Claude Code en Antigravity)
**Scope:** Todo el contenido de `C:\Users\oscar\.openclaw\`

---

## Resumen Ejecutivo

OpenClaw es un **sistema funcional pero con problemas profundos**. Después de semanas/meses de operación, presenta:

- **4 de 12 agentes huérfanos** (configurados pero no usados, o viceversa)
- **3 de 3 cron jobs deshabilitados** (el motor de automatización está apagado)
- **Backend de Mission Control incierto** (timeout en jobs que dependen de él)
- **openclaw.json reducido de 28KB a 12KB** (secciones enteras eliminadas sin documentación)
- **BrowserBase CDP no responde** (automatización de browser offline)

A pesar de esto, el sistema tiene **assets valioso** que deben preservarse en la migración a Claude Code.

---

## El Mejor Aporte de OpenClaw

### 1. Identidad de Agente (Jarvis)

Los archivos `SOUL.md` y `AGENTS.md` capturan algo importante: **un agente no es solo un modelo — es un sistema con identidad, metodología, y memoria**. Jarvis tiene:
- Propósito claro ("co-architect", "Level 0 — supreme manager")
- Reglas de comunicación (formal, bilingüe, depth over speed)
- Structure de respuesta (WHY, EXACT STEPS, TOOLS, MEASURE, RISKS)
- Startup routine (leer archivos de estado en orden)

**Esto se replica en IMPKT** como `CLAUDE.md` + `system/state.md` + `system/memory.md`.

### 2. Sistema de Memoria en Capas

El sistema de OpenClaw para continuidad de sesión es sofisticado:

```
SOUL.md (quién soy) → AGENTS.md (cómo opero) →
CONTEXT.md (session handoff) → MEMORY.md (estado de negocio) →
memory/YYYY-MM-DD.md (logs diarios) →
~/self-improving/ (correcciones, preferences) →
~/proactivity/ (seguimiento proactivo)
```

**Para IMPKT**, esto se replica con:
```
CLAUDE.md → system/state.md → system/memory.md →
system/self-improving/ → system/proactivity/
```

### 3. Workforce de Sub-Agentes

La idea de que el agente principal (Jarvis) crea y dirige sub-agentes especializados es correcta. OpenClaw tiene 12 roles definidos (code-reviewer, debugger, deployment-engineer, etc.). **IMPKT necesita lo mismo** — Finn (PRODUCTION) no hace todo solo, tiene skills帮她.

### 4. Hooks Automation

Los hooks internos (`command-logger` + `session-memory`) automatizan logging sin intervención del agente. **Esto es exactly lo que IMPKT necesita** para no perder estado entre sesiones.

### 5. Config de Modelos (Routing)

El sistema de routing de OpenClaw (tareas ligeras → M2.7 free, coding → Claude Code, research → Perplexity) es exactamente el patrón que IMPKT usa. **Se migra a variables de entorno**.

---

## Lo Que IMPKT Debe Tomar de OpenClaw

| Asset | Valor | Forma de Migración |
|-------|-------|-------------------|
| Identidad (SOUL.md) | Identidad clara del sistema | CLAUDE.md (revisar y alinear) |
| Startup routine (AGENTS.md) | Metodología de operación | system/state.md + system/memory.md |
| Memoria en capas | Continuidad sin amnesia | system/self-improving/ + system/proactivity/ |
| Hooks automation | Logging automático | settings.json PreToolUse hooks |
| Config de modelos | Routing correcto | Variables de entorno en .env |
| Sistema de pricing IMPKT | 11 servicios documentados | Ya en CLAUDE.md |
| Workforce roles | Patrones de sub-agentes | skills/ o plan/agent-teams.md |

---

## Lo Que IMPKT Debe Descartar de OpenClaw

| Asset | Razón de Descarte |
|-------|-------------------|
| OpenClaw como executor | Claude Code lo reemplaza |
| Mission Control (docker) | No disponible en Antigravity |
| AgentDB | Requiere Node.js 18+ |
| Swarm orchestration (Claude Flow) | CLI no existe |
| BrowserBase | CDP down + redundante con Antigravity |
| memorySearch vectorial | No necesario para escala |
| Agentes huérfanos | Limpiar, no migrar |
| Ollama glm-5 | Deprecated |
| Gateway dashboard | No existe en nuevo sistema |

---

## Prioridades de Implementación

### PRIORIDAD 1: Construir Identidad IMPKT (TAREA 0.6 completada)

**Antes de hacer cualquier cosa**, IMPKT necesita saber quién es.

```
system/
  CLAUDE.md          ← Existe, necesita revisión para alineación con identidad IMPKT
  state.md           ← Existe, necesita contenido real (por ahora solo template)
  self-improving/   ← Por crear
  proactivity/       ← Por crear
  token-rules.md     ← Existe, necesita verificar contenido
```

**Verificar:** `system/self-check.md` — si no existe o está incompleto, la identidad no está lista.

### PRIORIDAD 2: Sistema de Memoria (TAREA 0.2)

Con `system/state.md` funcionando:
- El agente sabe dónde quedó en cada sesión
- No empieza de cero cada vez
- Las decisiones se preservan entre reinicios

**Hito:**Primera sesión que sobreviva a un restart sin perder contexto.

### PRIORIDAD 3: Configurar Routing de Modelos

```
.env
  ANTHROPIC_BASE_URL=https://api.minimax.chat/v1
  CLAUDE_MODEL=MiniMax-M2.7
  MINIMAX_API_KEY=...
  PERPLEXITY_API_KEY=...
```

**Hito:** `echo $CLAUDE_MODEL` retorna `MiniMax-M2.7` en Antigravity.

---

## Lo Que Esta Auditoría NO Resuelve

1. **La limpieza de agentes huérfanos** — requiere acción de Gabriel (confirmar antes de borrar directorios)
2. **El destino del bot de Telegram** — se mantiene como canal de Gabriel, pero cómo se integra con Claude Code aún está por definir
3. **El estado de Mission Control** — verificar manualmente si el docker sigue corriendo (aunque ya no se use)
4. **La pérdida de secciones en openclaw.json** — no hay backup visible en el filesystem, las secciones eliminadas no se recuperan

---

## Conclusión Final

**OpenClaw fue un buen laboratorio.** Demostró que un agente puede operar de forma autónoma, mantener contexto, generar tasks, y comunicar via Telegram. Los problemas vinieron de:

1. **Complejidad excesiva** — demasiados componentes (docker, Node.js backend, browser externo, AgentDB)
2. **Mantenimiento insuficiente** — cron jobs apagados, agentes huérfanos, config drifting
3. **Decisión arquitectónica incorrecta** —Claude Flow como executor no era la herramienta correcta

**IMPKT empieza limpio.** Un solo executor (Claude Code), identidad clara (CLAUDE.md), memoria robusta (system/), y metodología estructurada (Festival). OpenClaw es la referencia, no el destino.

---

## Archivos Generados en Esta Auditoría

```
impkt/audit/
  config-analysis.md      ← Desglose de openclaw.json
  agents-inventory.md      ← Los 12 agentes, 6 huérfanos
  skills-inventory.md      ← 31 skills, 17 útiles
  infrastructure-map.md    ← Cómo todo se conecta
  problems-found.md        ← 7 problemas documentados
  useful-assets.md        ← 10 assets a migrar
  discarded-assets.md     ← 10 assets a descartar
  verdict.md              ← Este archivo
```

**Estado:** Auditoría completada. Listo para avanzar a TAREA 2 (Planear Arquitectura).