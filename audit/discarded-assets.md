# Assets Descartados — OpenClaw para IMPKT

Estos componentes de OpenClaw NO tienen valor para el nuevo sistema IMPKT. Se descartan por las razones indicadas.

---

## 1. AgentDB — Requiere Node.js 18+ y agentic-flow

**Qué es:** Sistema de base de datos de agentes con queries vectoriales y memoria persistente.

**Ubicación:** `C:\Users\oscar\.openclaw\agents\main\agent.db\` (probablemente)

**Por qué se descarta:**
- Requiere **Node.js 18+** — Antigravity no tiene Node.js guarantee
- Requiere **agentic-flow** — paquete adicional que no está en el stack de Antigravity
- OpenClaw mismo no lo está usando activamente (memorySearch está `enabled: false`)
- El sistema de archivos (CONTEXT.md, MEMORY.md) funciona bien para el caso de uso

**Alternativa para IMPKT:** `system/state.md` + `system/memory.md` en archivos JSON/markdown. Suficiente para la escala de IMPKT.

---

## 2. Swarm Orchestration Avanzada — Requiere Claude Flow CLI

**Qué es:** Sistema de coordinación multi-agente con swarm topologies, Q-Learning router, y 100+ tipos de agentes.

**Referencia:** `workspace/skills/swarm-orchestration/` (mencionado en TOOLS.md como "✅ Available")

**Por qué se descarta:**
- **Requiere Claude Flow CLI** — no existe en el stack de Claude Code
- **Requiere backend de orchestrator** — el sistema actual de OpenClaw swarm usa un orchestrator que corre en Node.js
- **Q-Learning router** — overkill para 5 boards + Gabriel
- Claude Code Agent Teams tiene su propia forma de orquestar sub-agents — no necesita swarm

**Alternativa para IMPKT:** Agent Teams nativo de Claude Code. Los 5 lead agents se crean con `agent:teams` y se coordinan via Festival methodology.

---

## 3. BrowserBase Profile — CDP Externo, Costo Adicional

**Qué es:** Automatización de browser via BrowserBase (servicio cloud de CDP).

**Config:** `openclaw.json` → `browser.profiles.browserbase`

**Por qué se descarta:**
- **CDP no responde** según MEMORY.md — el servicio está down o la key está vencida
- **Costo adicional** — BrowserBase es servicio de pago, no necesario
- **Redundante** — Antigravity tiene browser agent nativo (Chromium headless) que cubre las necesidades de IMPKT sin costo extra

**Alternativa para IMPKT:** Browser agent nativo de Antigravity. Configurado en el contexto de Antigravity, no en settings.

---

## 4. v3-* Skills — Descartados/Abandonados

**Qué son:** Skills que empiezan con `v3-` o tienen versión 0.3.7.

**Ubicación probable:** `workspace/skills/v3-*` o skills con metadata de versión anterior.

**Por qué se descarta:**
- **Versión 0.3.7** — muy antigua, abandonada
- **No aparecen en el inventario actual** de los 31 skills en workspace/skills/
- Si existieron en versiones anteriores, fueron removidos

**No hay nada que migrar** — estos assets ya no existen.

---

## 5. OpenClaw como Executor — Se Muda a Claude Code

**Qué es:** OpenClaw como orchestrator + executor para tareas de desarrollo, automation, y coordinación.

**Por qué se descarta:**
- **Gabriel decidió** que el executor será Claude Code nativo (CLI dentro de Antigravity)
- OpenClaw se reduce a **solo bot de Telegram** — comunicación, no ejecución
- La potencia de Claude Code para coding, análisis, y operación es superior a lo que OpenClaw puede ofrecer como executor

**Qué se preserva de OpenClaw:**
- Bot de Telegram (config de channels/telegram)
- Workspace/skills/ para contenido copy-pasteado
- SOUL.md, AGENTS.md, CONTEXT.md como templates

**Qué NO se preserva:**
- El CLI de OpenClaw como herramienta principal
- Los agents workspaces (se reemplazan con Claude Code worktrees)
- El gateway (no se necesita — Claude Code es CLI)
- Los cron jobs de OpenClaw (se reemplazan con Claude Code scheduled agents)

---

## 6. Mission Control Backend Python — Requiere Backend Corriendo

**Qué es:** Stack de Mission Control en docker:
- Backend: Python API modules (puerto 8000)
- Frontend: React dashboard (puerto 3000)
- Agentes: Mila, Sofia, boards en contenedores docker

**Archivos:** `mission-control.tar.gz` (866KB), `mission-control.zip` (1.29MB)

**Por qué se descarta:**
- **Docker restringido** en Antigravity sandbox — no se puede correr docker compose
- **Backend no accesible** — los cron jobs que dependen de MC dan timeout
- **No migrable** — el backend Python requiere una infrastructure específica (docker, puertos, tokens) que no existe en el nuevo stack
- **Redundante** — Claude Code Agent Teams + Festival pueden cubrir las necesidades de coordinación de boards sin un backend separado

**Qué se pierde:**
- Dashboard visual de Mission Control (el frontend React en puerto 3000)
- La separación visual de boards (MARKETING/SALES/etc. como tabs)

**Qué se gana:**
- Sistema más simple (un solo executor en lugar de dos interacting backends)
- Menos puntos de fallo (sin docker, sin backend separado)
- Más portable (todo en archivos + Claude Code CLI)

**Nota:** La **identidad de los 5 boards** (Mila/Lena/Sofia/Finn/Nova) SÍ se preserva. Solo el mecanismo de implementación cambia (Agent Teams en lugar de docker containers).

---

## 7. gateway-dashboard-sync Skill

**Archivo:** `workspace/skills/gateway-dashboard-sync/`

**Por qué se descarta:**
- Depende de Mission Control (docker local)
- No hay dashboard en el nuevo sistema
- MC backend se descarta

**Útil para:** N/A — functionality ya no existe

---

## 8. Ollama Cloud Models (glm-5) — Deprecated

**Qué es:** Provider ollama en openclaw.json con modelos:
- `minimax-m2.7:cloud` (gratis, free tier)
- `glm-5:cloud` (deprecated según TOOLS.md)

**Por qué se descarta:**
- **glm-5 deprecated** — no usar
- **minimax-m2.7:cloud vía ollama** — redundante. Ya hay acceso directo a Minimax via `${MINIMAX_API_KEY}` con API `anthropic-messages`
- El provider ollama es un bridge innecesario cuando Minimax Direct funciona

**Qué usar:** Minimax Direct (`minimax` provider en openclaw.json). Ya configurado y funcionando.

---

## 9. memorySearch (Elasticsearch/Gemini) — No Necesario

**Qué es:** Búsqueda vectorial en memoria (memories embeddings).

**Config:** `memorySearch: { "enabled": false, "provider": "gemini" }`

**Por qué se descarta:**
- **enabled: false** — no se usa
- **Requiere proveedor** (gemini) — capa adicional de complejidad
- **Sistema de archivos funciona** — CONTEXT.md + MEMORY.md + grep es suficiente para la escala de IMPKT

**Alternativa para IMPKT:** Búsqueda manual con herramientas nativas (Grep, Glob de Claude Code). Si el knowledge base crece mucho, se puede agregar search vectorial después.

---

## 10. extended-credits Skill (Agencia 2)

**Qué es:** Skills específicos para Agency 2 (Credits & Financial Services).

**Ubicación:** Probablemente en `workspace/skills/` o `projects/agency2/`

**Por qué se descarta:**
- **Agency 2 en Stage 0** — no existe aún
- **Agency 1 es prioridad** — no construimos features para agencies que no existen
- Cuando Agency 2 se active, se crearán los skills correspondientes

**Qué hacer:** Mantener como referencia en `C:\Users\oscar\.openclaw\workspace\` (solo lectura). No migrar hasta que Agency 2 esté activa.

---

## Resumen de Assets Descartados

| # | Asset | Razón Principal | Recuperable |
|---|-------|-----------------|-------------|
| 1 | AgentDB | Node.js 18+ requerido, agentic-flow no disponible | No |
| 2 | Swarm orchestration (Claude Flow) | CLI no existe en Claude Code | No |
| 3 | BrowserBase profile | CDP down + costo adicional | No |
| 4 | v3-* skills | Abandondados, versión 0.3.7 | No |
| 5 | OpenClaw como executor | Gabriel decidió usar Claude Code | No |
| 6 | MC backend Python | Docker restringido en Antigravity | No |
| 7 | gateway-dashboard-sync | Depende de MC descartado | No |
| 8 | Ollama glm-5 | Deprecated | No |
| 9 | memorySearch vectorial | No necesario para escala IMPKT | No |
| 10 | extended-credits (Agency 2) | Agency 2 no existe aún | No |