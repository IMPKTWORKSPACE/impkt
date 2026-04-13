# Mapa de Infraestructura — OpenClaw

## Arquitectura General

```
Gabriel (humano)
    |
    +-- Telegram --> OpenClaw Bot (@Jarvis_OpenclawV1_Bot)
    |                    |
    |                    +-- Gateway (localhost:18789)
    |                    |       |
    |                    |       +-- OpenClaw CLI (main agent)
    |                    |       |       |
    |                    |       |       +-- Workspace (C:\Users\oscar\.openclaw\workspace)
    |                    |       |       |       |
    |                    |       |       |       +-- SOUL.md, USER.md, AGENTS.md, CONTEXT.md, MEMORY.md, HEARTBEAT.md
    |                    |       |       |       +-- skills/ (31 skills)
    |                    |       |       |       +-- memory/ (daily logs YYYY-MM-DD.md)
    |                    |       |       |       +-- swarm/ (task queue)
    |                    |       |       |       +-- tools/ (generators)
    |                    |       |       |       +-- scripts/ (PowerShell)
    |                    |       |       |       +-- projects/, core/, references/
    |                    |       |       |
    |                    |       |       +-- Lead Agents (Lena, Finn, Nova)
    |                    |       |       |       workspaces separados
    |                    |       |       |
    |                    |       +-- MC Gateway Agents (2)
    |                    |       |       workspaces para Mission Control
    |                    |       |
    |                    +-- Plugins (7)
    |                    |       |
    |                    |       +-- openclaw-web-search (npm)
    |                    |       +-- telegram (bot integration)
    |                    |       +-- perplexity (web search)
    |                    |       +-- minimax (model provider)
    |                    |       +-- openrouter (model provider)
    |                    |       +-- anthropic (model provider)
    |                    |       +-- browser (CDP automation)
    |                    |
    |                    +-- Cron Jobs (3 jobs, TODOS DESHABILITADOS)
    |                    |       |
    |                    |       +-- Context Rollover (0 0 * * *) — disabled
    |                    |       +-- Health Check (0 * * * *) — disabled (timeout errors)
    |                    |       +-- IMPKT Auto Task Generator (0 21 * * *) — disabled (timeout errors)
    |                    |
    |                    +-- Memory (SQLite: C:\Users\oscar\.openclaw\memory\main.sqlite)
    |                    |
    |                    +-- Extensions (openclaw-web-search instalado)
    |
    +-- Mission Control (docker local, puerto 8000/3000)
    |       |
    |       +-- Backend: Python API modules
    |       +-- Frontend: React dashboard (localhost:3000)
    |       +-- Agentes en docker: Mila, Sofia, y boards
    |
    +-- BrowserBase (CDP externo, costo adicional)
    |       WSS: connect.browserbase.com
    |       Estado: ⚠️ CDP no responde según MEMORY.md
```

---

## Flujo de Comunicación

### Flujo 1: Gabriel → OpenClaw (Telegram)

```
Telegram message (Gabriel)
    --> @Jarvis_OpenclawV1_Bot (token: 8689877980:AAFlNoZdK9uOLnxn...)
    --> OpenClaw gateway (localhost:18789)
    --> main agent (Jarvis)
    --> Responde por Telegram (dmPolicy: pairing, allowFrom: 7069567895)
```

### Flujo 2:main agent → Lead Agents

```
main agent (Jarvis) decide delegar
    --> workspace/lead-*/
    --> Lee AGENTS.md para saber qué hacer
    --> Crean sus propios archivos de estado (SOUL.md, CONTEXT.md)
    --> Reportan a main via contexto
```

### Flujo 3: Heartbeat (scheduler)

```
Cron job triggered (deshabilitado en config)
    --> wakeMode: now
    --> agentTurn / systemEvent
    --> Ejecuta tarea en isolated session
    --> Reporta por Telegram (delivery.channel: telegram, to: 7069567895)
```

### Flujo 4: External Services

```
OpenClaw
    --> Perplexity API (web search)
    --> Minimax API (model)
    --> OpenRouter API (model)
    --> Anthropic API (model)
    --> BrowserBase CDP (browser automation)
    --> Maton (api-gateway, 100+ OAuth integrations)
```

---

## Datos Persistidos

### Archivos de estado (workspace/)

| Archivo | Qué guarda | Supervivencia |
|---------|------------|---------------|
| SOUL.md | Identidad, propósito, reglas de operación | Reinicios de sesión |
| USER.md | Perfil de Gabriel, situación actual, preferencias | Largo plazo |
| AGENTS.md | Startup routine, reglas de memoria | Largo plazo |
| CONTEXT.md | Session handoff — última sesión, siguiente paso | Reinicios |
| MEMORY.md | Estado del negocio, roadmap, config importante | Largo plazo |
| HEARTBEAT.md | Tareas periódicas, reglas de token | Largo plazo |
| IDENTITY.md | Nombre, vibe, emoji, avatar | Largo plazo |
| TOOLS.md | Stack de herramientas, API keys, servicios | Largo plazo |
| memory/YYYY-MM-DD.md | Logs diarios de actividad | 14 días (pruneAfter) |
| swarm/tasks/queue.json | Tareas generadas para boards | Reinicios |

### Datos en filesystem (no workspace)

| Path | Qué guarda | Supervivencia |
|------|------------|---------------|
| .openclaw/openclaw.json | Config de sistema completo | Largo plazo |
| .openclaw/memory/main.sqlite | SQLite de memoria | Largo plazo |
| .openclaw/cron/jobs.json | Definición de cron jobs | Largo plazo |
| agents/*/agent/ | Config de workspace por agente | Largo plazo |
| workspace-gateway-*/ | Workspaces de gateway agents | Largo plazo |
| workspace-lead-*/ | Workspaces de lead agents | Largo plazo |

### Datos efímeros

| Dónde | Qué | Notas |
|-------|-----|-------|
| Contexto de sesión | Historial de conversación | Se pierde en reset |
| memorySearch | Búsqueda en memoria (disabled) | No usado |
| sandbox | Modo sandbox (off) | No activo |

---

## Modelo de Datos de Negocio (OpenClaw)

```
IMPKT
├── Branding: impkt.mx, WhatsApp 8115339022
├── Service Catalog: 11 servicios, 4 categorías
├── Board Architecture: MARKETING → OUTREACH → SALES → PRODUCTION → CLIENT COMMS
├── Queens: Mila, Lena, Sofia, Finn, Nova
├── Pricing: Setup = 100-150% del monthly
└── ICP: PyMEs 5-100 empleados, México, operación física, presencia digital débil
```

---

## Conexiones Externas

### API Keys configuradas (en env de openclaw.json)

```
MINIMAX_API_KEY: [EN GITHUB SECRETS - NO COMMIT]
PERPLEXITY_API_KEY: [EN GITHUB SECRETS - NO COMMIT]
BrowserBase API Key: [EN GITHUB SECRETS - NO COMMIT]
Maton API Key: [EN GITHUB SECRETS - NO COMMIT]
OpenRouter API Key: [EN GITHUB SECRETS - NO COMMIT]
```

### Servicios externos usados

| Servicio | Uso | Estado |
|----------|-----|--------|
| Ollama Cloud | Modelos free (minimax-m2.7:cloud, glm-5:cloud) | ⚠️ glm-5 deprecated |
| Minimax Direct | Modelo primario ($0.30/$1.20 per 1M tokens) | ✅ Activo |
| OpenRouter | Hunter Alpha (1M context) | ⚠️ Sin uso aparente |
| Anthropic | Claude Sonnet 4 ($3/$15 per 1M tokens) | ⚠️ Sin uso aparente |
| Perplexity | Web search | ✅ Activo |
| BrowserBase | Cloud browser (CDP) | ⚠️ No responde |
| Vercel | Landing page hosting | ✅ Cuenta existe, re-auth pendiente |
| Supabase | Backend DB + auth | ✅ Cuenta existe |
| Stripe | Payments | ✅ Cuenta existe |

---

## Mission Control (Backend Python)

```
.mission-control.tar.gz (866KB)
mission-control.zip (1.29MB)
openclaw-mission-control-master/

Backend (Python):
- API modules para agents
- Dashboard frontend (React, puerto 3000)
- Token: 20NKqtSiwY435RhfcBFzXjeJVaDsL8Q9gdPHUAuxTbWvEl17yGopIrkn6OMCmZ

Endpoints:
- Backend: http://localhost:8000/api/v1
- Frontend: http://localhost:3000

Estado: ⚠️ Backend en docker, funciona según MEMORY.md pero cron jobs que dependen de él dan timeout
```

---

## Problems en la infraestructura

1. **Cron jobs deshabilitados** — El motor de automatización está apagado
2. **BrowserBase CDP no responde** — La automatización de browser está offline
3. **Mission Control backend no accesible** — Los 2 MC gateway agents intentan reacharlo pero dan timeout
4. **glm-5:cloud deprecated** — Modelo en ollama sin uso, puede causar confusiones
5. **4 agentes huérfanos** — Configuración inconsistente entre openclaw.json y filesystem
6. **memorySearch deshabilitado** — Búsqueda vectorial en memoria no disponible

---

## Cómo se traduce esto para IMPKT en Claude Code

```
Gabriel (humano)
    |
    +-- Telegram --> OpenClaw (solo bot, se mantiene)
    |                    |
    |                    +-- Claude Code CLI (Antigravity)
    |                    |       |
    |                    |       +-- system/ (SOUL.md, AGENTS.md equivalent)
    |                    |       |       |
    |                    |       |       +-- CLAUDE.md (identidad IMPKT)
    |                    |       |       +-- token-rules.md (optimización)
    |                    |       |       +-- state.md (continuidad)
    |                    |       |       +-- self-improving/ (mejora continua)
    |                    |       |       +-- proactivity/ (iniciativa)
    |                    |       |
    |                    |       +-- Agent Teams (5 leads)
    |                    |       |       |
    |                    |       |       +-- Mila (MARKETING)
    |                    |       |       +-- Lena (OUTREACH)
    |                    |       |       +-- Sofia (SALES)
    |                    |       |       +-- Finn (PRODUCTION)
    |                    |       |       +-- Nova (CLIENT COMMS)
    |                    |       |
    |                    |       +-- Festival/ (metodología)
    |                    |       +-- knowledge/ (Obsidian + Graphify)
    |                    |       +-- ideas/ (repositorio de ideas)
    |                    |       +-- audit/ (esta auditoría)
    |                    |       +-- plan/ (arquitectura)
    |                    |
    |                    +-- RUFLO (orquestación, npm)
    |
    +-- Google Antigravity (sandbox, browser agent, Ghost Runtimes)
    +-- Perplexity API (web search, configurada)
    +-- Minimax API (modelo default, $0.30/$1.20)
```