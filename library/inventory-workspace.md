# Inventario: Workspace IMPKT

**Fecha:** 2026-04-13

---

## Estructura de archivos

```
C:\Users\oscar\impkt\
├── CLAUDE.md                    # Constitucion del sistema
├── SOUL.md                      # Director identity
├── AGENTS.md                    # Roles de agentes
├── HEARTBEAT.md                 # Heartbeat del sistema
├── USER.md                      # Gabriel (usuario)
├── CONTEXT.md                   # Session handoff
├── MEMORY.md                    # Estado de negocio
│
├── agents/                      # 5 lead agents
│   ├── mila/marketing/SOUL.md
│   ├── lena/outreach/SOUL.md
│   ├── sofia/sales/SOUL.md
│   ├── finn/production/SOUL.md
│   └── nova/client-comms/SOUL.md
│
├── teams/
│   └── impkt-main/config.json    # Team config
│
├── pipeline/                    # Lead pipeline
│   ├── mila-to-lena/
│   ├── lena-to-sofia/
│   ├── sofia-to-finn/
│   ├── finn-to-nova/
│   ├── archive/
│   ├── lost/
│   └── README.md
│
├── ideas/                       # Ideas repository
│   ├── inbox/
│   ├── processing/
│   ├── approved/
│   ├── implemented/
│   ├── discarded/
│   ├── process-ideas.py         # (existente, necesita mejora en FASE 6)
│   └── index.md
│
├── system/
│   ├── state.md                  # Estado del sistema (este archivo referencia)
│   ├── self-check.md
│   ├── token-rules.md
│   ├── self-improving/memory.md
│   ├── proactivity/
│   │   ├── memory.md
│   │   ├── session-state.md
│   │   └── memory/working-buffer.md
│   ├── memory/2026-04/2026-04-12.md
│   ├── alerts/2026-04-12-system-ready.md
│   ├── festival/impkt-migration/
│   │   └── campaigns/impkt-migration/
│   │       └── state.yaml
│   ├── bots/
│   │   ├── director/bot.py       # Director bot (CORRIENDO)
│   │   ├── reporter/bot.py       # Reporter bot (CORRIENDO)
│   │   └── ideas/bot.py          # Ideas bot (CORRIENDO)
│   ├── graphify-out/             # Knowledge graph
│   │   ├── GRAPH_REPORT.md (38KB)
│   │   ├── graph.json (119KB)
│   │   ├── graph.html (266KB)
│   │   ├── detect.json
│   │   └── cache/
│   └── run-graphify.py           # Script custom para graphify
│
├── graphify-out/                 # Copia en raiz
│
├── tools/graphify/              # Repo clonado
│   ├── ARCHITECTURE.md
│   ├── CHANGELOG.md
│   └── graphify/ (modulos Python)
│
├── audit/                       # Auditoria OpenClaw
│   ├── config-analysis.md
│   ├── agents-inventory.md
│   ├── skills-inventory.md
│   ├── infrastructure-map.md
│   ├── problems-found.md
│   ├── useful-assets.md
│   ├── discarded-assets.md
│   └── verdict.md
│
├── plan/                        # Planes de arquitectura
│   ├── features-map.md
│   ├── agent-teams.md
│   ├── ideas-repository.md
│   ├── migration-festival.md
│   ├── telegram-architecture.md
│   └── schedule.md
│
├── library/                      # (esta carpeta — FASE 1)
│   ├── inventory-claude-code.md
│   ├── inventory-antigravity.md
│   ├── inventory-workspace.md
│   └── inventory-pendientes-openclaw.md
│
└── .git/                        # Git repo
```

---

## Bots de Telegram (corriendo)

| Bot | PID | Status |
|-----|-----|--------|
| director/bot.py | 2914 | Corriendo |
| reporter/bot.py | 2915 | Corriendo |
| ideas/bot.py | 2916 | Corriendo |

Tokens: Verificados operativos via Telegram API getUpdates.

---

## Ideas repository

- `ideas/inbox/` — existe, vacio
- `ideas/processing/` — existe, vacio
- `ideas/approved/` — existe, vacio
- `ideas/implemented/` — existe, vacio
- `ideas/discarded/` — existe, vacio
- `ideas/process-ideas.py` — existe (FASE 6 lo mejorara)

---

## Pipeline

6 etapas, todas vacias (sin leads todavia).

---

## Archivos .md en workspace

~65 archivos .md distribuidos en:
- audit/ (8)
- plan/ (6)
- system/ (15+)
- agents/ (5 SOUL.md)
- raiz (SOUL.md, AGENTS.md, CLAUDE.md, etc.)
- library/ (4 — recien creados)
- graphify-out/ (1 GRAPH_REPORT.md)

---

## Cosas faltantes en workspace

Segun el festival FASE 5, estas herramientas no existen aun y hay que construirlas:
- `tools/proposal-generator/` — NO existe
- `tools/lead-research/` — NO existe
- `tools/humanizer/` — NO existe
- `tools/pipeline-manager/` — NO existe

Segun FASE 6:
- `ideas/RULES.md` — NO existe (se creara en FASE 6)
