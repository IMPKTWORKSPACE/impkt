# Assets Útiles — OpenClaw para IMPKT

Estos son los componentes de OpenClaw que SÍ tienen valor para el nuevo sistema IMPKT y deben replicarse en Claude Code.

---

## 1. SOUL.md + AGENTS.md — Identidad del Sistema (CRÍTICO)

**Archivos:** `C:\Users\oscar\.openclaw\workspace\SOUL.md` (69 líneas), `AGENTS.md` (70 líneas)

**Qué hacen:**
- **SOUL.md:** Define a Jarvis como "the strategic brain", "co-architect", "Level 0 — supreme manager". Reglas de comunicación (formal, bilingüe), estructura de respuesta (WHY, EXACT STEPS, TOOLS, MEASURE, RISKS), reglas de decisión.
- **AGENTS.md:** Startup routine (leer SOUL → USER → CONTEXT → MEMORY), sistema de memoria en capas, red lines, external vs internal.

**Valor:** Estos archivos capturan la identidad y metodología de operación del agente. Son el "cerebro" del sistema.

**Cómo replicar para IMPKT:**
```
impkt/system/
  CLAUDE.md          # Identidad, propósito, reglas de comunicación
  AGENTS.md          # Startup routine, memoria, red lines
  HEARTBEAT.md       # Tareas periódicas
```

El CLAUDE.md ya existe en `C:\Users\oscar\impkt\CLAUDE.md` — pero necesita alinearse más con la identidad de IMPKT (no de Jarvis). Revisar después de esta auditoría.

---

## 2. Sistema de Memoria en Capas (CRÍTICO)

**Archivos:**
- `CONTEXT.md` (~110 líneas) — Session handoff, ~500 bytes, se actualiza al final de cada sesión
- `MEMORY.md` (~120 líneas) — Estado del negocio, roadmap, config, service catalog, agentes válidos
- `memory/YYYY-MM-DD.md` — Logs diarios (captura eventos, contexto, decisiones)
- `~/self-improving/` — Execution-improvement memory (preferences, workflows, corrections)
- `~/proactivity/` — Proactive boundaries, session state, working buffer

**Qué hace:**
```
Startup: SOUL → USER → CONTEXT → MEMORY (en main sessions)
On-demand: memory/YYYY-MM-DD.md para contexto específico
Continuous: self-improving para calidad de ejecución
Proactive: proactivity para anticipación y seguimiento
```

**Valor:** Permite que el agente "despierte" con contexto de dónde se quedó, qué se decidió, qué sigue. Sin esto, cada sesión empieza de cero.

**Cómo replicar para IMPKT:**
```
impkt/system/
  state.md           # Session handoff (equivalente a CONTEXT.md)
  memory.md          # Estado del negocio (equivalente a MEMORY.md)
  self-improving/    # Corrections, patterns, preferences
  proactivity/       # Session state, working buffer, heartbeat
impkt/memory/        # Logs diarios YYYY-MM-DD.md
```

**Ya creado en IMPKT:**
- `C:\Users\oscar\impkt\system\state.md` existe
- `C:\Users\oscar\impkt\system\` existe

---

## 3. Workforce de Sub-Agentes (12 roles) — Adaptable a IMPKT

**Referencia:** `C:\Users\oscar\.openclaw\workspace\skills\n8n-mcp\.claude\agents\`

**Agents definidos:**
- code-reviewer
- context-manager
- debugger
- deployment-engineer
- mcp-backend-engineer

**Adicional en otros skills:**
- task-decomposer
- task-planner
- delegation

**El concepto es migrable:** IMPKT necesita roles similares cuando crezca:

| Rol OpenClaw | Rol equivalente IMPKT |
|-------------|---------------------|
| code-reviewer | QA en PRODUCTION (Finn revisa antes de entregar) |
| debugger | Client Comms (Nova maneja bugs) |
| deployment-engineer | Finn (deploya a Vercel) |
| context-manager | Agente principal (maneja contexto de cada board) |
| task-decomposer | Festival (descompone en phases/sequences/tasks) |

**Cómo replicar:** No como agents separados en workspaces, sino como skills o patrones dentro del sistema IMPKT. Cuando un lead agent necesita help, puede invocar un skill especializado.

---

## 4. Hooks Automation — CRÍTICO (replicable en Claude Code)

**Archivos:** `openclaw.json` → sección `hooks`

**Qué hace:**
```json
"hooks": {
  "internal": {
    "enabled": true,
    "entries": {
      "command-logger": { "enabled": true },
      "session-memory": { "enabled": true }
    }
  }
}
```

- **command-logger:** Registra cada comando ejecutado. Útil para debugging y audit trail.
- **session-memory:** Guarda estado de sesión automáticamente. No depende del agente para escribir CONTEXT.md.

**Valor:** Automatiza logging sin que el agente tenga que hacerlo manualmente.

**Cómo replicar en Claude Code:**

En `settings.json` de Claude Code:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "command-logger",
        "prompt": "Before executing a bash or write tool, log the command to system/command-log.md with timestamp and command. Keep it to one line."
      },
      {
        "name": "session-memory",
        "prompt": "After every 5 tool calls, automatically write current context summary to system/state.md. Include: last action, next pending, any errors."
      }
    ]
  }
}
```

**Alternativa nativa:** Claude Code tiene skill `update-config` para configurar hooks. Verificar si PreToolUse hooks están soportados en la versión actual.

---

## 5. pair-programming Skill — Útil para desarrollo

**Archivo:** `C:\Users\oscar\.openclaw\workspace\skills\coding-agent\SKILL.md` (317 líneas)

**Qué hace:**
- Detalla cómo ejecutar coding agents (Codex, Claude Code, Pi, OpenCode)
- Explica PTY mode vs no-PTY (crítico: Codex/Pi/OpenCode necesitan PTY, Claude Code NO)
- Patrones: one-shot, background, worktree para PR reviews, parallel fixing
- Auto-notify on completion (usar `openclaw system event`)

**Valor:** La documentación de PTY vs no-PTY es directamente aplicable cuando IMPKT haga desarrollo con Claude Code en background.

**Cómo replicar:** Crear `impkt/skills/coding-agent.md` con los patrones relevantes adaptados a la configuración de IMPKT.

---

## 6. Config de Modelos — Routing por Tipo de Tarea (MIGRABLE)

**Archivos:** `openclaw.json` → sección `models`, `workspace/TOOLS.md`

**Qué hace:**
```
Chat, planning → minimax-m2.7:cloud (free)
Heavy analysis → minimax-m2.7:cloud (Plus)
Coding → Claude Code (Pro)
Research → Perplexity Search API
Autonomous multi-step → Perplexity Agent API
```

**Valores de config migrables:**
- contextWindow: 200,000 para MiniMax-M2.7
- maxTokens: 8,192
- cost: $0.30 input / $1.20 output / $0.03 cacheRead / $0.12 cacheWrite
- modelo primario: `minimax/MiniMax-M2.7`

**Cómo replicar:** Variables de entorno en `impkt/.env`:
```
ANTHROPIC_BASE_URL=https://api.minimax.chat/v1
CLAUDE_MODEL=MiniMax-M2.7
MINIMAX_API_KEY=...
MINIMAX_API_KEY_MINIMAX=...  # si hay separate key para Plus
PERPLEXITY_API_KEY=...
```

---

## 7. TOOLS.md — Archivo de Referencia de la Pila Completa

**Archivo:** `C:\Users\oscar\.openclaw\workspace\TOOLS.md` (~82 líneas)

**Qué hace:**
- Lista todos los modelos activos con provider y costo
- Lista todas las skills disponibles con estado
- Lista API keys configuradas con fecha
- Lista servicios de Gabriel (Vercel, Supabase, Stripe)
- Notas de configuración

**Valor:** Un solo archivo que captura TODO el stack. Útil para onboarding, debugging, y entender el estado del sistema.

**Cómo replicar:** Crear `impkt/system/STACK.md` con:
- Modelos activos
- API keys (referencia a .env, no valores)
- Servicios conectados
- Estado de cada integración
- Configuración importante

---

## 8. Sistema de Pricing de IMPKT

**Archivos:** `MEMORY.md`, `CONTEXT.md`, `agency-1/service-catalog.md`

**Qué hace:**
- Define los 11 servicios con setup y monthly
- Regla: Setup = 100-150% del monthly (incluye 1er mes)
- Tablas de pricing por categoría
- Paquetes profesionales con descuento

**Valor:** Ya está definido y documentado. No se pierde — se mantiene en IMPKT como source of truth.

**Ubicación en IMPKT:** `C:\Users\oscar\impkt\CLAUDE.md` (ya incluye el catálogo en sección INFORMACIÓN DE REFERENCIA)

---

## 9. heartbeat-rules.md — Reglas de Token y Heartbeat

**Archivo:** `workspace/skills/heartbeat-rules.md` (54 líneas)

**Qué hace:**
```markdown
1. No exec loops — si falla, analizar antes de reintentar
2. Batch commands — combinar checks en UN exec
3. Snapshot before heavy debugging — guardar contexto primero
```

**Reglas de heartbeat:**
- 1 tarea por rotation
- Frequency según token usage (>75% → cada 2h, >90% → cada 4h)
- Midnight-8am off (excepto critical alerts)
- NO_REPLY rules: same content, just "ok", Gabriel no menciona Jarvis

**Valor:** Framework de operación para tareas periódicas. Directly applicable a IMPKT.

**Cómo replicar:** Ya está en `impkt/system/token-rules.md` (TAREA 0). Verificar que las heartbeat-rules.md estén incorporadas.

---

## 10. self-improving Skill — Framework de Mejora Continua

**Archivo:** `workspace/skills/self-improving/SKILL.md` (250 líneas)

**Qué hace:**
- Sistema de aprendizaje deCorrecciones y self-reflection
- Tiered memory: HOT (≤100 lines) / WARM (projects/domains/) / COLD (archive/)
- Promotion/demotion rules (3x → promote, 30 días → demote, 90 días → archive)
- Conflict resolution (project > domain > global)
- heartbeat-state.md para tracking de mantenimiento

**Valor:** Framework completo para que el sistema mejore con el tiempo sin intervención de Gabriel.

**Cómo replicar:** Crear `impkt/system/self-improving/` con la misma estructura. La skill ya está instalada en OpenClaw — se copia la estructura.

---

## Resumen de Assets Útiles

| # | Asset | Prioridad | Estado de réplica |
|---|-------|-----------|------------------|
| 1 | SOUL.md + AGENTS.md (identidad) | CRÍTICA | CLAUDE.md existe, necesita revisión |
| 2 | Memoria en capas | CRÍTICA | system/state.md existe, necesita completar |
| 3 | Workforce roles | MEDIA | Patrones copiados a plan/agent-teams.md |
| 4 | Hooks automation | CRÍTICA | settings.json hooks a configurar |
| 5 | pair-programming skill | ALTA | Copiar a skills/coding-agent.md |
| 6 | Config de modelos (routing) | ALTA | Migrar a .env |
| 7 | TOOLS.md (stack reference) | MEDIA | Crear system/STACK.md |
| 8 | Sistema de pricing | ALTA | Ya en CLAUDE.md |
| 9 | heartbeat-rules | ALTA | Ya en system/token-rules.md |
| 10 | self-improving skill | CRÍTICA | system/self-improving/ por crear |