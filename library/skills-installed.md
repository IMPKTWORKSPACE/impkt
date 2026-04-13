# Skills Instaladas — Claude Code

**Fecha:** 2026-04-13

---

## Skills instaladas

| Skill | Ubicacion | Origen | Para que sirve |
|-------|-----------|--------|---------------|
| graphify | `~/.claude/skills/graphify/` | Previa (2026-04-12) | Knowledge graph para navegar codebase |
| landing-builder | `~/.claude/skills/landing-builder/` | OpenClaw vault | Generacion de landing pages con UI/UX Pro Max |
| proposal-generator | `~/.claude/skills/proposal-generator/` | OpenClaw vault | Generar proposals PDF con branding IMPKT |
| coding-agent | `~/.claude/skills/coding-agent/` | OpenClaw vault | Delegar tareas de codigo con PTY patterns |
| lead-research | `~/.claude/skills/lead-research/` | Nuevo (stub) | Investigar prospectos digitalmente |
| content-humanizer | `~/.claude/skills/content-humanizer/` | Nuevo (stub) | Post-procesar contenido para que no suene a IA |
| seo-optimizer | `~/.claude/skills/seo-optimizer/` | Nuevo (stub) | Optimizar contenido para SEO local Mexico |
| client-onboarding | `~/.claude/skills/client-onboarding/` | Nuevo (stub) | Onboarding de clientes nuevos |

---

## Skills parciales (de OpenClaw, no copiadas)

| Skill | Status | Nota |
|-------|--------|------|
| self-improving | Parcial | Solo archivos en system/self-improving/ — SKILL.md no copiada |
| proactivity | Parcial | Solo archivos en system/proactivity/ — SKILL.md no copiada |

---

## Skills de OpenClaw no migradas

Estas skills existen en OpenClaw vault pero NO se copiaron a Claude Code:

| Skill | Razon |
|-------|-------|
| data-analysis | Bajo priority, se evalua en FASE 5 |
| delegation | Bajo priority |
| task-decomposer | Bajo priority, se evalua en FASE 5 |
| task-planner | Bajo priority |
| context-compactor | Bajo priority |
| context-recovery | Bajo priority |
| humanizer | Ya como content-humanizer |
| summarize | Bajo priority |
| oracle | Bajo priority |
| proactive-messenger | Bajo priority |
| session-logs | Bajo priority |

---

## Skills por construir en FASE 5

Las siguientes skills seran construidas completamente en FASE 5:
- lead-research (stub existe — completar)
- content-humanizer (stub existe — completar)
- seo-optimizer (stub existe — completar)
- client-onboarding (stub existe — completar)

---

## Verificacion

```bash
ls ~/.claude/skills/
```

Expected output:
- graphify/
- landing-builder/
- proposal-generator/
- coding-agent/
- lead-research/
- content-humanizer/
- seo-optimizer/
- client-onboarding/

---

## Nota sobre self-improving y proactivity

Estas skills ya tienen sus archivos de memoria en:
- `system/self-improving/` — systema de mejora continua
- `system/proactivity/` — seguimiento proactivo

Los archivos SKILL.md completos de OpenClaw no se copiaron porque la funcionalidad
ya esta integrada en system/. Si se necesitan las SKILL.md completas, se pueden
copiar de:
- `C:\Users\oscar\.openclaw\workspace\skills\self-improving\SKILL.md`
- `C:\Users\oscar\.openclaw\workspace\skills\proactivity\SKILL.md`
