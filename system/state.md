# IMPKT — Estado del Sistema

**Ultima actualizacion:** 2026-04-13
**Archivo de continuidad:** Si la sesion se corta, leer este archivo primero.

---

## IDENTIDAD DEL SISTEMA

IMPKT ("Impakt") es el sistema operativo central de una agencia de servicios digitales
y automatizacion con IA para PyMEs en Mexico.

**Yo soy el Director.** Gabriel es el unico ser humano que interviene — solo para
decisiones estrategicas y aprobaciones. Todo lo demas lo ejecuto yo.

**Mi cerebro default:** MiniMax M2.7 (90% de las tareas)
**Mi cerebro premium:** Claude Sonnet/Opus (Gabriel lo activa manualmente)
**Sandbox:** Google Antigravity (Claude Code CLI)
**Comunicacion con Gabriel:** 3 bots de Telegram independientes

---

## COMO SE CONSTRUYO ESTE SISTEMA

Todo comenzo con las instrucciones en CLAUDE.md (la constitucion). Aqui documentado
como se hizo cada fase.

---

### FASES DE CONSTRUCCION (TAREA 0)

#### 0.1 — Verificacion de pre-requisitos (IMPKT-INSTALL-GUIDE.md)

Gabriel leyó el install guide antes de nuestra primera sesion. Verificamos:
- Workspace `C:\Users\oscar\impkt\` existe
- Git inicializado
- Claude Code v2.1.104 funcionando
- Variables de entorno MiniMax configuradas
- Antigravity abierto con el workspace cargado
- Graphify clonado en `tools/graphify/`

**Problema encontrado:** `ANTHROPIC_BASE_URL` estaba configurado como
`https://api.minimax.io/anthropic` en lugar de `https://api.minimax.chat/v1`.
Gabriel dijo: "Si ya funciona, no lo corrijas." Se dejó como estaba.

#### 0.2 — Obsidian Vault

**Objetivo:** Conectar Obsidian a mi para knowledge mapping.

**Hallazgo:** El directorio `C:\Users\oscar\impkt` ya tiene `.obsidian/` — es un vault
valido de Obsidian. El install guide decia que el vault debia estar en `knowledge/`,
pero Gabriel eligió usar la raíz directamente.

**Accion:** Gabriel abrió Obsidian, hizo "Open another vault", navegó a la raíz
`C:\Users\oscar\impkt` y lo abrió. Obsidian registró el vault automáticamente en
`obsidian.json` bajo el perfil del usuario que lo abrió.

**Verificacion:** `.obsidian/` existe y `obsidian.json` contiene el vault.

#### 0.3 — Graphify (Knowledge Graph)

**Graphify** (https://github.com/safishamsi/graphify) conecta notas de Obsidian entre
sí usando tree-sitter AST + LLM para extraer relaciones.

**Instalacion:**
1. Graphify ya estaba clonado en `tools/graphify/`
2. RUFLO ya estaba instalado (v3.5.80) — no se pudo re-inicializar
3. El CLI de graphify no soporta `.` como comando (solo install/query/save-result)
4. Se ejecuto via script personalizado en `system/run-graphify.py`
5. Se descubrio que `extract()` requiere `list[Path]` no `(path, text)`
6. Se construyó un generador de reportes custom

**Resultado del primer grafo:**
- `graphify-out/GRAPH_REPORT.md` — 38KB
- `graphify-out/graph.json` — nodos y edges
- `graphify-out/graph.html` — 266KB, visualizacion interactiva
- `graphify-out/cache/` — cache SHA256 para re-runs
- Primer grafo: 516 nodos, 36 edges, 480 comunidades

**Git hooks instalados:** post-commit y post-checkout para mantener el grafo
actualizado.

#### 0.4 — Festival Methodology

**Festival** es la metodología interna de project planning de IMPKT.

**Instalacion original en WSL:** Falló (WSL no disponible en el entorno).

**Solucion:** Se replicó la estructura manualmente en `system/festival/`:
```
system/festival/
└── impkt-migration/
    └── campaigns/
        └── impkt-migration/
            └── state.yaml
```

**Estructura de un festival:**
- Campaign = objetivo grande
- Phases = etapas mayores
- Sequences = grupos de tasks
- Tasks = unidades atomicas ejecutables

#### 0.5 — Sistema de memoria en capas

Inspirado en OpenClaw, implementado con:

```
CLAUDE.md              → Constitucion, identidad, reglas
system/state.md        → Estado actual, siguiente paso, decisiones
system/memory/         → Logs diarios (YYYY-MM-DD.md)
system/self-improving/ → Correcciones y preferencias aprendidas
system/proactivity/    → Seguimiento proactivo de tareas
```

**Archivos creados:**
- `system/token-rules.md` — 10 reglas de optimizacion de tokens
- `system/self-check.md` — checklist post-install
- `system/memory/2026-04/2026-04-12.md` — daily log del primer dia
- `system/proactivity/memory.md`
- `system/proactivity/session-state.md`
- `system/proactivity/memory/working-buffer.md`

#### 0.6 — Auto-evaluacion (self-check)

**Archivo:** `system/self-check.md` — Verifico que todo lo anterior esta funcional
antes de avanzar a TAREA 1.

---

## TAREA 1 — AUDITORIA DE OPENCLAW

**Scope:** Todo en `C:\Users\oscar\.openclaw\` — SOLO LECTURA, nunca modificar.

**Archivos generados en `audit/`:**
```
audit/config-analysis.md      — openclaw.json desglosado (reducido de 28KB a 12KB)
audit/agents-inventory.md     — 12 agentes, 6 huérfanos
audit/skills-inventory.md     — 31 skills, 17 útiles
audit/infrastructure-map.md   — Cómo todo se conecta
audit/problems-found.md       — 7 problemas documentados
audit/useful-assets.md        — 10 assets a migrar
audit/discarded-assets.md     — 10 assets a descartar
audit/verdict.md              — Resumen ejecutivo
```

**Problemas críticos encontrados en OpenClaw:**
1. openclaw.json reducido de 28KB a 12KB (secciones eliminadas sin documentación)
2. 3 de 3 cron jobs deshabilitados (automatizacion apagada)
3. 6 de 12 agentes huérfanos
4. BrowserBase CDP no responde
5. Backend de Mission Control incierto
6. AgentDB requiere Node.js 18+ (no disponible)
7. Gateway dashboard no existe

**Assets útiles migrados a IMPKT:**
- Identidad de agente (SOUL.md) → CLAUDE.md
- Sistema de memoria en capas → system/memory/ + system/proactivity/
- Hooks de automation → settings.json PreToolUse hooks
- Config de modelos/routing → Variables de entorno
- Sistema de pricing IMPKT → Ya en CLAUDE.md

**Lo descartado:**
- OpenClaw como executor (reemplazado por Claude Code)
- Mission Control docker (no disponible en Antigravity)
- AgentDB, Swarm orchestration, BrowserBase
- Agentes huérfanos, Ollama glm-5

---

## TAREA 2 — PLANEAR LA NUEVA ARQUITECTURA

**Archivos generados en `plan/`:**

```
plan/features-map.md          — 34.6KB — Todas las features nativas de cada herramienta
plan/agent-teams.md           — 29.8KB — Diseño de los 5 leads
plan/ideas-repository.md      — 13.4KB — Sistema de repositorio de ideas
plan/migration-festival.md    — 15.8KB — Plan completo de migracion
plan/telegram-architecture.md — Arquitectura de 3 bots (reemplaza OpenClaw)
plan/schedule.md              — Schedule de tareas
```

### Arquitectura decidida por Gabriel

| Componente | Herramienta |
|------------|-------------|
| Sandbox | Google Antigravity |
| Executor | Claude Code CLI |
| Cerebro default (90%) | MiniMax M2.7 |
| Cerebro premium (10%) | Claude Sonnet/Opus (manual) |
| Orquestacion | RUFLO nativo (npm: ruflo@latest) |
| Metodologia | Festival (interna) |
| Comunicacion Gabriel | 3 bots Telegram (nuevo) |
| Knowledge mapping | Obsidian + Graphify |

### 5 Agent Teams

```
Gabriel
   |
   +-> Mila (MARKETING) -> Genera leads, contenido, campañas, SEO
   |         |
   |         +-> Lena (OUTREACH) -> Primer contacto, calificación, discovery
   |                      |
   |                      +-> Sofia (SALES) -> Pre-deal, propuestas, pricing, cierre
   |                                   |
   |                                   +-> Finn (PRODUCTION) -> Builder principal
   |                                                |
   |                                                +-> Nova (CLIENT COMMS) -> Post-deal, soporte
```

**Cada lead tiene:**
- `agents/{lead}/SOUL.md` — identidad, rol, metricas, pipeline
- Workspace propio en `agents/{lead}/`
- Configuracion en `teams/impkt-main/config.json`

### Catalogo de servicios (11 servicios, 4 categorías)

**Setup = 100-150% del mensual (regla de Gabriel)**

| Servicio | Setup | Mensual |
|----------|-------|---------|
| Landing Page | $5,000 | $2,500 |
| Sitio Corporativo | $9,000 | $4,500 |
| E-commerce | $12,000 | $6,000 |
| SEO Local (min 3 meses) | $12,000 | $6,000 |
| Social Media | $10,000 | $5,000 |
| Campañas Outreach | $24,000 | $12,000 |
| WhatsApp Automation | $6,000 | $3,000 |
| Email Automation | $5,000 | $2,500 |
| CRM Setup | $5,000 | N/A |

---

## TAREA 3 — EJECUCION DE LA MIGRACION

### FASE 1 — Fundaciones ✅ (completada 2026-04-12 11:30 AM)

- RUFLO ya estaba inicializado (v3.5.80)
- 5 Agent Teams creados con SOUL.md completos
- Pipeline estructurado en 6 carpetas (mila-to-lena, lena-to-sofia, etc.)
- teams/impkt-main/config.json creado
- Sistema de memoria en capas funcionando

### FASE 2 — Comunicacion Telegram ✅ (completada 2026-04-13 00:45 AM)

**Decision de Gabriel:** OpenClaw se ELIMINA. Se reemplaza con 3 bots propios.

**PRINCIPIO:** Cada bot ES su seccion. Comunicacion DIRECTA, sin clones ni intermediarios.

#### Los 3 Bots (todos operativos, PIDs 2914, 2915, 2916)

**@impkt_director_bot** — Token: `8610839715:AAG2G_Vww2oTDaUIMPxcRjpZFz3OZZ69p8g`
- Canal directo Gabriel ↔ Director (YO)
- Comandos: /hola /status /pipeline /festival /alerts /memory /leads
- Seguridad: ChatID 7069567895 configurado

**@impkt_reporter_bot** — Token: `8770963569:AAHSYelKhVmqvNsT8GImt-5X4CQ1i3oY-po`
- Reporter independiente — genera sus propios reportes
- Comandos: /hola /report /weekly /daily /metrics /lead [id] /subscribe [id]
- Seguridad: ChatID 7069567895 configurado

**@impkt_ideas_bot** — Token: `8770191324:AAE0zSo4iCr6MIXP2e-MfOEihTNqxKlVT4Y`
- Repositorio de ideas con procesamiento directo
- Comandos: /hola /idea [url|texto] /status /approved /implemented /discard [id] /approve [id]
- Incluye scoring algorithm, curl URL fetching, gestion de archivos de ideas
- Seguridad: ChatID 7069567895 configurado

#### Implementacion tecnica

- Lenguaje: Python 3.14 (`C:\Python314\python.exe`)
- Libreria: python-telegram-bot v22.7
- Cada bot es un proceso independiente con su propio handler
- Los bots no se comunican entre si — operan independientemente
- Director = YO conectado a Telegram; Reporter e Ideas = scripts independientes
- Nohay intermediarios, no hay clones

#### Comandos para gestionar los bots

```bash
# Iniciar un bot
nohup /c/Python314/python.exe system/bots/director/bot.py > system/bots/director/run.log 2>&1 &

# Verificar que estan corriendo (via Telegram API)
curl "https://api.telegram.org/bot{TOKEN}/getUpdates?timeout=1&limit=1"

# Matar un bot
taskkill //PID {PID}
```

### FASE 3 — Director Identity ✅

- SOUL.md del Director creado
- AGENTS.md, HEARTBEAT.md, USER.md, CONTEXT.md, MEMORY.md actualizados
- 5 leads configurados con SOUL.md completos

### FASE 4 — Leads con trabajo real ⏳ (PENDIENTE)

- Pipeline vacio — no hay leads todavia
- Gabriel traera los primeros prospectos
- El sistema movera leads por las etapas Mila → Lena → Sofia → Finn → Nova

### FASE 5 — Ideas Repository ⏳ (PENDIENTE)

- Bot Ideas operativo
- `ideas/inbox/`, `ideas/approved/`, `ideas/discarded/`, `ideas/implemented/` existen
- `ideas/process-ideas.py` existe
- Reglas del repositorio de ideas: discusion pendiente con Gabriel

### FASE 6 — Testing End-to-End ⏳ (PENDIENTE)

- Testing completo del flujo: lead entra → pasa por todas las etapas → sale implementado
- Testing de los 3 bots en produccion real
- Verificacion de memoria entre sesiones

---

## ESTRUCTURA ACTUAL DEL WORKSPACE

```
C:\Users\oscar\impkt\
├── CLAUDE.md                    # Constitucion del sistema (este archivo de referencia)
│
├── SOUL.md                      # Yo (Director) — identidad
├── AGENTS.md                    # Agentes y roles
├── HEARTBEAT.md                 # Heartbeat del sistema
├── USER.md                      # Gabriel
├── CONTEXT.md                   # Session handoff
├── MEMORY.md                    # Estado de negocio
│
├── agents/
│   ├── mila/marketing/SOUL.md   # Marketing lead
│   ├── lena/outreach/SOUL.md     # Outreach lead
│   ├── sofia/sales/SOUL.md       # Sales lead
│   ├── finn/production/SOUL.md   # Production lead
│   └── nova/client-comms/SOUL.md # Client comms lead
│
├── teams/
│   └── impkt-main/config.json    # Team config
│
├── pipeline/
│   ├── mila-to-lena/
│   ├── lena-to-sofia/
│   ├── sofia-to-finn/
│   ├── finn-to-nova/
│   ├── archive/
│   └── lost/
│
├── ideas/
│   ├── inbox/
│   ├── processing/
│   ├── approved/
│   ├── implemented/
│   ├── discarded/
│   ├── process-ideas.py
│   └── index.md
│
├── system/
│   ├── state.md                  # ESTE ARCHIVO
│   ├── self-check.md             # Verificacion post-install
│   ├── token-rules.md            # Reglas de optimizacion
│   ├── self-improving/memory.md
│   ├── proactivity/memory.md
│   ├── proactivity/session-state.md
│   ├── proactivity/memory/working-buffer.md
│   ├── memory/
│   │   └── 2026-04/2026-04-12.md
│   ├── alerts/
│   │   └── 2026-04-12-system-ready.md
│   ├── festival/
│   │   └── impkt-migration/
│   │       └── campaigns/
│   │           └── impkt-migration/
│   │               └── state.yaml
│   ├── bots/
│   │   ├── director/bot.py       # Director bot (YO a Telegram)
│   │   ├── reporter/bot.py       # Reporter bot
│   │   └── ideas/bot.py          # Ideas bot
│   ├── graphify-out/             # Knowledge graph
│   │   ├── GRAPH_REPORT.md
│   │   ├── graph.json
│   │   ├── graph.html
│   │   └── cache/
│   └── run-graphify.py           # Script custom para graphify
│
├── audit/                        # Auditoria OpenClaw
│   ├── config-analysis.md
│   ├── agents-inventory.md
│   ├── skills-inventory.md
│   ├── infrastructure-map.md
│   ├── problems-found.md
│   ├── useful-assets.md
│   ├── discarded-assets.md
│   └── verdict.md
│
├── plan/                         # Planes de arquitectura
│   ├── features-map.md
│   ├── agent-teams.md
│   ├── ideas-repository.md
│   ├── migration-festival.md
│   ├── telegram-architecture.md
│   └── schedule.md
│
├── graphify-out/                 # (copia en raíz también)
├── tools/graphify/               # Repo de graphify
└── .git/                         # Git del workspace
```

---

## DECISIONES REGISTRADAS

1. **Raiz = Vault Obsidian** — El vault es `C:\Users\oscar\impkt` directamente,
   no `knowledge/`. Gabriel abrió Obsidian y registró la raíz como vault.

2. **ANTHROPIC_BASE_URL no se toca** — Funcionaba con la URL existente.
   Gabriel dijo: "Si ya funciona, no lo corrijas."

3. **OpenClaw ELIMINADO como executor** — Reemplazado por Claude Code + 3 bots Telegram.

4. **3 bots, no 1** — Arquitectura: Director (YO), Reporter (independiente),
   Ideas (independiente). Principio: cada bot ES su seccion.

5. **Festival replicado manualmente** — WSL no disponible, se creó la estructura
   a mano en `system/festival/`.

6. **RUFLO no se re-inicializó** — Ya estaba configurado (v3.5.80).

7. **Setup = 100-150% del mensual** — Regla de pricing de Gabriel.

8. **ChatID 7069567895 autorizado** — Solo Gabriel puede usar los 3 bots.

---

## PROBLEMAS ENCONTRADOS Y SOLUCIONES

| Problema | Solucion |
|----------|---------|
| RUFLO ya estaba inicializado | No se re-inicializó, se usa como está |
| graphify CLI no soporta `.` | Script personalizado en `system/run-graphify.py` |
| `extract()` signature distinta | Se construyó generador de reportes custom |
| graphify `--wiki` no funciona como CLI | Se usa `--platform claude` para instalar skill |
| sleep + pipe bloqueado | Usar background jobs o monitor tool |
| UnicodeEncodeError en terminals | Evitar emojis en print, usar Python para APIs |
| WSL no disponible para fest | Estructura replicada manualmente |
| Backup zip falló (permisos sessions/) | Se creó carpeta en lugar de zip |

---

## ARCHIVOS CREADOS POR FASIS

### Fase TAREA 0
```
system/token-rules.md
system/self-check.md
system/memory/2026-04/2026-04-12.md
system/self-improving/memory.md
system/proactivity/memory.md
system/proactivity/session-state.md
system/proactivity/memory/working-buffer.md
system/festival/impkt-migration/campaigns/impkt-migration/state.yaml
system/run-graphify.py
graphify-out/GRAPH_REPORT.md (primera versión)
graphify-out/graph.json (primera versión)
graphify-out/graph.html (primera versión)
```

### Fase TAREA 1
```
audit/config-analysis.md
audit/agents-inventory.md
audit/skills-inventory.md
audit/infrastructure-map.md
audit/problems-found.md
audit/useful-assets.md
audit/discarded-assets.md
audit/verdict.md
```

### Fase TAREA 2
```
plan/features-map.md
plan/agent-teams.md
plan/ideas-repository.md
plan/migration-festival.md
plan/telegram-architecture.md
plan/schedule.md
```

### Fase TAREA 3 (en ejecucion)
```
SOUL.md
AGENTS.md
HEARTBEAT.md
USER.md
CONTEXT.md
MEMORY.md
agents/mila/marketing/SOUL.md
agents/lena/outreach/SOUL.md
agents/sofia/sales/SOUL.md
agents/finn/production/SOUL.md
agents/nova/client-comms/SOUL.md
teams/impkt-main/config.json
ideas/process-ideas.py
ideas/inbox/
ideas/processing/
ideas/approved/
ideas/implemented/
ideas/discarded/
ideas/index.md
system/bots/director/bot.py
system/bots/reporter/bot.py
system/bots/ideas/bot.py
system/festival/impkt-migration/campaigns/impkt-migration/state.yaml (actualizado)
system/state.md (este archivo, reescrito completo)
```

---

## SIGUIENTE PASO

**DETENIDO — Nuevo Festival viene.**

Gabriel detiene el progreso de impkt-migration en FASE 4.
FASE 4, 5 y 6 quedan pendientes. Nuevo Festival por definir.

---

_Ultima actualizacion completa: 2026-04-13 01:00 AM_
