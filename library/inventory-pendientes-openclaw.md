# Inventario: Pendientes de OpenClaw

**Fecha:** 2026-04-13
**Fuente:** audit/useful-assets.md + audit/skills-inventory.md

---

## Assets de OpenClaw — Estado de migracion

| # | Asset | Prioridad | Estado en IMPKT |
|---|-------|-----------|----------------|
| 1 | SOUL.md + AGENTS.md (identidad) | CRITICA | CLAUDE.md existe — necesita revision de alineacion |
| 2 | Memoria en capas | CRITICA | system/state.md existe — necesita completar |
| 3 | Workforce roles | MEDIA | Patrones en plan/agent-teams.md |
| 4 | Hooks automation | CRITICA | NO configurados — pendiente FASE 3/4 |
| 5 | pair-programming skill | ALTA | NO migrado — pendiente FASE 3 |
| 6 | Config de modelos (routing) | ALTA | ANTHROPIC_BASE_URL/CLAUDE_MODEL en settings.local.json |
| 7 | TOOLS.md (stack reference) | MEDIA | NO creado — pendiente FASE 7 |
| 8 | Sistema de pricing | ALTA | Ya en CLAUDE.md |
| 9 | heartbeat-rules | ALTA | Ya en system/token-rules.md |
| 10 | self-improving skill | CRITICA | system/self-improving/ existe parcialmente |

---

## Skills de OpenClaw — Estado de migracion

**Total en OpenClaw:** 31 skills sandbox + 2 globales
**Utiles para IMPKT:** 17
**Ya migradas:** 0
**Pendientes de migracion:** 17

### Skills criticas para migrar (FASE 3)

| Skill | Para que sirve | Archivo fuente |
|-------|---------------|----------------|
| self-improving | Mejora continua con memoria tiered | `workspace/skills/self-improving/SKILL.md` |
| proactivity | Follow-through y boundaries | `workspace/skills/proactivity/SKILL.md` |
| coding-agent | PTY vs no-PTY, background execution | `workspace/skills/coding-agent/SKILL.md` |
| landing-builder | Construccion de landing pages | `workspace/skills/landing-builder/SKILL.md` |
| proposal-generator | Generar proposals comerciales | `workspace/skills/proposal-generator/SKILL.md` |
| obsidian | Integracion con vault | `workspace/skills/obsidian/SKILL.md` |

### Skills a evaluar e instalar (FASE 3)

| Skill | Para que sirve | Status OpenClaw |
|-------|---------------|-----------------|
| data-analysis | KPIs y reportes | Disponible |
| delegation | Como delegar a sub-agentes | Disponible |
| task-decomposer | Descomponer tareas complejas | Disponible |
| task-planner | Planificacion de tareas | Disponible |
| context-compactor | Compactar contexto | Disponible |
| context-recovery | Recuperar sesiones interrumpidas | Disponible |
| humanizer | Hacer output mas natural | Disponible |
| summarize | Resumir contenido largo | Disponible |
| oracle | Prediccion y planeacion | Disponible |
| proactive-messenger | Mensajeria proactiva | Disponible |
| session-logs | Logging de sesiones | Disponible |

### Skills a evaluar (requieren cuenta/config)

| Skill | Para que sirve | Status OpenClaw | Requiere |
|-------|---------------|-----------------|----------|
| api-gateway | 100+ APIs via Maton OAuth | Configurada | MATON_API_KEY |
| github | GitHub CLI integration | CLI sin auth | gh CLI |
| n8n-mcp | n8n automation | Configurado | n8n instance |
| moltguard | Security guard | Requiere plugin install | Antigravity support |
| ui-ux-pro-max-skill | Design system | "To install" | Instalacion |

### Skills DESCARTADAS (no utiles para IMPKT)

- blogwatcher
- awesome-design-md
- gateway-dashboard-sync
- gemini
- gog
- nano-pdf
- references
- xurl
- openclaw-heartbeat

---

## Lo que NO se migrara de OpenClaw

| Componente | Razon |
|-----------|-------|
| OpenClaw como executor | Reemplazado por Claude Code |
| Mission Control (docker) | No disponible en Antigravity |
| AgentDB | Requiere Node.js 18+ |
| Swarm orchestration (Claude Flow) | CLI no existe |
| BrowserBase | CDP down + redundante |
| memorySearch vectorial | No necesario para escala |
| Agentes huerfanos (6) | Limpiar, no migrar |
| Ollama glm-5 | Deprecated |
| Gateway dashboard | No existe |

---

## Resumen de gap

**Skills instaladas en IMPKT:** 0 (solo graphify como skill)
**Skills pendientes:** 17+
**Plugin de Claude Code instalados:** 0
**Plugins pendientes:** 11+

**Proximo paso:** FASE 2 — Mapear features por area de agente
