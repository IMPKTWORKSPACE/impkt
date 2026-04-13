# Inventario de Skills — OpenClaw

**Total de skills en workspace:** 31
**Skills globales del sistema:** self-improving (instalada), proactivity (instalada)
**Skills sandbox:** 31 (skills de ClipHub/hub install)

---

## Skills Globales (Instaladas en el sistema OpenClaw)

### 1. self-improving

| Campo | Valor |
|-------|-------|
| Slug | `self-improving` |
| Version | 1.2.16 |
| Líneas SKILL.md | 250 |
| Descripción | Self-reflection + Self-criticism + Self-learning + Self-organizing. Agent evalúa su propio trabajo, detecta errores, mejora permanentemente. |
| Cuándo usar | (1) comando/tool/API falla; (2) usuario corrige; (3) descubro mejor approach; (4) user explícitamente instala |
| Arquitectura | ~/self-improving/ con tiers: HOT (memory.md ≤100 lines), WARM (projects/, domains/), COLD (archive/) |
| Datos persistidos | `C:\Users\oscar\self-improving\` |
| Estado | ✅ Instalada y funcionando |
| útil para IMPKT | **SÍ — CRÍTICO**. Sistema de mejora continua con memoria tiered. Se replica como `C:\Users\oscar\impkt\system\` |
| Cómo replicar | Crear `C:\Users\oscar\impkt\system\` con: memory.md, corrections.md, heartbeat-state.md, projects/, domains/, archive/ |

### 2. proactivity

| Campo | Valor |
|-------|-------|
| Slug | `proactivity` |
| Líneas SKILL.md | ~150+ (varios .md) |
| Descripción | Proactive follow-through, state recovery, initiative boundaries. Evita que el agente espere pasivamente. |
| Archivos | boundaries.md, execution.md, heartbeat-rules.md, memory-template.md, migration.md |
| Datos persistidos | `C:\Users\oscar\proactivity\` |
| Estado | ✅ Instalada |
| útil para IMPKT | **SÍ**. Necesario para operación autónoma. Se integra en `system/state.md` |
| Cómo replicar | Crear `C:\Users\oscar\impkt\system\proactivity\` con los mismos archivos |

---

## Skills Sandbox (31 skills en workspace/skills/)

### api-gateway

| Campo | Valor |
|-------|-------|
| Líneas SKILL.md | ~150+ |
| Descripción | 100+ APIs via Maton (OAuth). Referencias a: ActiveCampaign, Airtable, Apollo, Asana, Calendly, GitHub, Google Workspace, HubSpot, Jira, Notion, Salesforce, Stripe, y 80+ más. |
| Referencias | `workspace/skills/api-gateway/references/` — 125+ READMEs de APIs |
| Estado | ✅ Configurada (MATON_API_KEY configurada) |
| útil para IMPKT | **SÍ** — API integration layer. Útil para conectar IMPKT con CRMs, herramientas de marketing, etc. de clientes. |
| Cómo replicar | Mantener como referencia. Para IMPKT, usar MCP servers para las APIs más comunes (Notion, GitHub, Google). No instalar Maton a menos que se necesite OAuth universal. |

### awesome-design-md

| Campo | Valor |
|-------|-------|
| Descripción | Design reference system — translate design files into code. Contiene design-md/airbnb, design-md/airtable, etc. |
| Estado | ⚠️ No usada activamente |
| útil para IMPKT | Parcial. El pair-programming con el coding agent y ui-ux-pro-max-skill cubren esto mejor. |

### blogwatcher

| Campo | Valor |
|-------|-------|
| Descripción | Monitoreo de blogs/feeds de industria. |
| Estado | ✅ Disponible |
| útil para IMPKT | No directamente. IMPKT no tiene necesidad de monitorear blogs de industria. |

### coding-agent

| Campo | Valor |
|-------|-------|
| Líneas SKILL.md | 317 |
| Descripción | Delega tareas de código a Codex, Claude Code, o Pi agents via background process. Soporta PTY mode para agents interactivos. |
| Binarios requeridos | claude, codex, opencode, pi |
| Funciones | one-shot tasks, background execution, PR reviews, parallel fixing con git worktrees |
| Estado | ✅ Instalada |
| útil para IMPKT | **SÍ**. Patrón de ejecutar Claude Code en background con `--print --permission-mode bypassPermissions` es exactamente lo que IMPKT necesita para el builder (Finn). |
| Cómo replicar | Instalar en Claude Code como skill o simplemente usar Bash con background execution directamente. La documentación de PTY vs no-PTY es valiosa. |

### context-compactor

| Campo | Valor |
|-------|-------|
| Descripción | Compacta contexto de sesión automáticamente para evitar overflow de tokens. |
| Estado | ✅ Disponible como skill |
| útil para IMPKT | **SÍ**. El principio de auto-compactación es crítico. Se replica con `system/token-rules.md` (regla: antes de >5 exec calls, snapshot context). |

### context-recovery

| Campo | Valor |
|-------|-------|
| Descripción | Recupera estado después de sesiones interrumpidas. |
| Estado | ✅ Disponible |
| útil para IMPKT | **SÍ**. Principio: después de cada fase, escribir estado a `system/state.md`. |

### context-tracker

| Campo | Valor |
|-------|-------|
| Descripción | Track de uso de tokens y contexto. |
| Estado | ✅ Disponible |
| útil para IMPKT | Sí, para monitoreo. Se replica con `system/token-rules.md`. |

### data-analysis

| Campo | Valor |
|-------|-------|
| Líneas SKILL.md | ~100+ |
| Descripción | Análisis de datos, KPIs, charts. Archivos: chart-selection.md, decision-briefs.md, metric-contracts.md, pitfalls.md |
| Estado | ✅ Disponible |
| útil para IMPKT | **SÍ**. Para generar reportes de métricas para Gabriel (dashboard de leads,status de campañas, revenue). |

### delegation

| Campo | Valor |
|-------|-------|
| Descripción | Cómo delegar tareas efectivamente a sub-agentes. |
| Estado | ✅ Disponible |
| útil para IMPKT | Sí. Para cuando IMPKT delegue a los 5 lead agents. |

### gateway-dashboard-sync

| Campo | Valor |
|-------|-------|
| Descripción | Sincronización con dashboard del gateway. |
| Estado | ⚠️ Depende de Mission Control (docker local) |
| útil para IMPKT | No. Mission Control backend se descarta. |

### gemini

| Campo | Valor |
|-------|-------|
| Descripción | Google Workspace CLI via `gog`. Integración con Google Calendar, Gmail, etc. |
| Estado | ⚠️ gog no disponible en Windows |
| útil para IMPKT | No en Antigravity. GCP integración no es prioridad para IMPKT. |

### github

| Campo | Valor |
|-------|-------|
| Descripción | GitHub CLI integration. |
| Estado | CLI instalada, sin auth |
| útil para IMPKT | Sí, para cuando IMPKT gestione repos de clientes. |

### gog

| Campo | Valor |
|-------|-------|
| Descripción | Google Workspace CLI (alternativa a gemini). |
| Estado | No disponible en Windows |
| útil para IMPKT | No. |

### humanizer

| Campo | Valor |
|-------|-------|
| Descripción | Hace outputs más naturales/humanos. |
| Estado | ✅ Disponible |
| útil para IMPKT | Sí. Para cuando IMPKT genere contenido para clientes (no tan robótico). |

### landing-builder

| Campo | Valor |
|-------|-------|
| Descripción | Construcción de landing pages. |
| Estado | ✅ Disponible |
| útil para IMPKT | **SÍ**. Uno de los servicios principales de IMPKT. Usar como base para el builder pipeline. |

### memory-template (dentro de self-improving)

| Campo | Valor |
|-------|-------|
| Descripción | Template para archivos de memoria. |
| Estado | ✅ Parte de self-improving |
| útil para IMPKT | Sí, para crear `system/state.md` y otros archivos de estado. |

### moltguard

| Campo | Valor |
|-------|-------|
| Descripción | Security guard para prompt injection. |
| Estado | ⚠️ Requiere plugin install |
| útil para IMPKT | Sí. IMPKT procesa inputs de clientes — seguridad es importante. Instalar cuando Antigravity lo soporte. |

### n8n-mcp

| Campo | Valor |
|-------|-------|
| Descripción | Integración con n8n (automation platform). Archivos: .claude/agents/ (code-reviewer, context-manager, debugger, deployment-engineer, mcp-backend-engineer) |
| Estado | ⚠️ n8n-mcp configurado pero skill dice "Sin instancia n8n" |
| útil para IMPKT | **SÍ**. n8n es buena opción para automation de workflows de clientes (WhatsApp, email, CRM). La skill incluye agents especializados para debugging y deployment. |

### nano-pdf

| Campo | Valor |
|-------|-------|
| Descripción | Manipulación de PDFs. |
| Estado | ✅ Disponible |
| útil para IMPKT | No directamente. Procesamiento de documentos de clientes puede necesitarlo. |

### obsidian

| Campo | Valor |
|-------|-------|
| Descripción | Integración con Obsidian vault. |
| Estado | ✅ Disponible |
| útil para IMPKT | **SÍ**. IMPKT usa Obsidian + Graphify para knowledge mapping. |

### openclaw-heartbeat (dentro de self-improving)

| Campo | Valor |
|-------|-------|
| Descripción | Seed para heartbeat de OpenClaw. |
| Estado | ✅ Parte de self-improving |
| útil para IMPKT | No. Se replica con skill `schedule` de Claude Code. |

### oracle

| Campo | Valor |
|-------|-------|
| Descripción | Predicción y planificación. |
| Estado | ✅ Disponible |
| útil para IMPKT | Sí, para planificación estratégica. |

### proactive-messenger

| Campo | Valor |
|-------|-------|
| Descripción | Mensajería proactiva. |
| Estado | ✅ Disponible |
| útil para IMPKT | Sí, integrado con proactivity skill. |

### proposal-generator

| Campo | Valor |
|-------|-------|
| Descripción | Genera proposals comerciales. |
| Estado | ✅ Disponible |
| útil para IMPKT | **SÍ**. IMPKT vende propuestas — esto es directo. Adaptar al catálogo de servicios de IMPKT (11 servicios, 4 categorías). |

### references

| Campo | Valor |
|-------|-------|
| Descripción | Referencias varias. |
| Estado | ✅ Disponible |
| útil para IMPKT | No directamente. |

### session-logs

| Campo | Valor |
|-------|-------|
| Descripción | Logging de sesiones. |
| Estado | ✅ Disponible |
| útil para IMPKT | Sí, para audit trail. |

### summarize

| Campo | Valor |
|-------|-------|
| Descripción | Resume contenido largo. |
| Estado | ✅ Disponible |
| útil para IMPKT | Sí. Para resumir inputs de Gabriel, artículos, reportes. |

### task-decomposer

| Campo | Valor |
|-------|-------|
| Descripción | Descompone tareas complejas en subtareas. |
| Estado | ✅ Disponible |
| útil para IMPKT | Sí. Para proyectos grandes (landing pages, e-commerce, campañas SEO). |

### task-planner

| Campo | Valor |
|-------|-------|
| Descripción | Planificación de tareas. |
| Estado | ✅ Disponible |
| útil para IMPKT | Sí. Integrado con Festival methodology. |

### ui-ux-pro-max-skill

| Campo | Valor |
|-------|-------|
| Descripción | Design system para coding agent. Sub-skills: banner-design, brand, design, design-system. |
| Estado | ⚠️ "To install" según TOOLS.md |
| útil para IMPKT | **SÍ**. Para el servicio de Desarrollo Web — diseño profesional de interfaces. |

### xurl

| Campo | Valor |
|-------|-------|
| Descripción | URL shortening/extensión. |
| Estado | ✅ Disponible |
| útil para IMPKT | No. |

---

## Resumen

| Skill | Estado | útil para IMPKT | Prioridad |
|-------|--------|-----------------|-----------|
| self-improving | ✅ | **SÍ** | CRÍTICA |
| proactivity | ✅ | **SÍ** | CRÍTICA |
| api-gateway | ✅ | **SÍ** | ALTA |
| coding-agent | ✅ | **SÍ** | ALTA |
| data-analysis | ✅ | **SÍ** | ALTA |
| delegation | ✅ | Sí | MEDIA |
| landing-builder | ✅ | **SÍ** | ALTA |
| proposal-generator | ✅ | **SÍ** | ALTA |
| task-decomposer | ✅ | **SÍ** | ALTA |
| task-planner | ✅ | Sí | MEDIA |
| obsidian | ✅ | **SÍ** | ALTA |
| humanizer | ✅ | Sí | MEDIA |
| context-compactor | ✅ | **SÍ** | ALTA |
| context-recovery | ✅ | **SÍ** | ALTA |
| github | ⚠️ | Sí | MEDIA |
| n8n-mcp | ⚠️ | **SÍ** | ALTA |
| ui-ux-pro-max-skill | ⚠️ | **SÍ** | ALTA |
| summarize | ✅ | Sí | MEDIA |
| oracle | ✅ | Sí | MEDIA |
| proactive-messenger | ✅ | Sí | MEDIA |
| session-logs | ✅ | Sí | MEDIA |
| moltguard | ⚠️ | Sí | MEDIA |
| blogwatcher | ✅ | No | DESCARTAR |
| awesome-design-md | ⚠️ | Parcial | DESCARTAR |
| gateway-dashboard-sync | ⚠️ | No | DESCARTAR |
| gemini | ⚠️ | No | DESCARTAR |
| gog | ⚠️ | No | DESCARTAR |
| nano-pdf | ✅ | No | BAJA |
| references | ✅ | No | DESCARTAR |
| xurl | ✅ | No | DESCARTAR |
| openclaw-heartbeat | ✅ | No | DESCARTAR |

**Total útiles: 17 de 31**
**Total descartadas: 14**

---

## Skills que necesitan instalación en IMPKT

1. **moltguard** — cuando Antigravity lo soporte
2. **ui-ux-pro-max-skill** — instalar cuando se active el servicio de Desarrollo Web
3. **n8n-mcp** — cuando se configure n8n para automation de clientes
4. **github** — configurar auth cuando se necesiten integraciones con repos de clientes

---

## Archivos de skills más importantes para IMPKT

| Archivo | Líneas | Valor |
|---------|--------|-------|
| workspace/skills/SKILL.md | 250 | Framework de skill (self-improving) |
| workspace/skills/setup.md | 196 | Setup de self-improving |
| workspace/skills/coding-agent/SKILL.md | 317 | Coding agent patterns |
| workspace/skills/techniques.md | 169 | Técnicas de ejecución |
| workspace/skills/scaling.md | 125 | Scaling patterns |
| workspace/skills/operations.md | 144 | Operaciones |
| workspace/skills/pitfalls.md | 120 | Trampas comunes |
| workspace/skills/learning.md | 106 | Mecánicas de aprendizaje |
| workspace/skills/data-analysis/SKILL.md | ~100 | Análisis de datos |