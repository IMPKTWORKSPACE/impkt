# Inventario: Claude Code

**Fecha:** 2026-04-13
**Version:** 2.1.104

---

## Skills instaladas

Solo 1 skill:
- `graphify` — en `~/.claude/skills/graphify/SKILL.md`
  - Hook PreToolUse para knowledge graph
  - Instalada 2026-04-12

**Pendiente:** Instalar las 6 skills definidas en FASE 3 del festival.

---

## Settings

**Archivo:** `~/.claude/settings.local.json` (existe)
**Archivo global:** `~/.claude/settings.json` (NO existe — settings.local.json es el activo)

**Contenido de settings.local.json:**
- Permisos configurados: Bash, Read, entorno ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL, CLAUDE_MODEL
- Sin hooks activos
- Sin plugins instalados
- Sin MCPs configurados

**Hooks:** NO configurados. Pendiente: hooks de seguridad, graphify, session-memory.

---

## Plugins

**Estado:** 0 plugins instalados. Directorio `.claude/plugins/` existe pero vacio.

**Plugins planeados (FASE 3):**
- frontend-design (CRITICO — Finn lo necesita)
- code-review (QA)
- feature-dev (workflow)
- commit-commands (Git)
- plugin-dev (construir propios)
- pr-review-toolkit
- security-guidance (CRITICO)
- hookify
- ralph-wiggum
- agent-sdk-dev
- explanatory-output-style
- learning-output-style

---

## MCPs

**Estado:** 0 MCPs configurados. `.claude/mcp.json` NO existe.

**MCPs a evaluar (FASE 3):**
- filesystem
- fetch/web
- github
- sqlite
- playwright
- supabase

---

## RUFLO

**Version:** 3.5.80 (ya inicializado — NO se puede re-inicializar)
**Comando:** `npx ruflo@latest status` responde "Run ruflo init to initialize"
**Estado:** Usable para orquestacion si se configura

---

## Git hooks (graphify)

Post-commit y post-checkout instalados en el repo de graphify.
No verificado si git hooks del repo principal (impkt) los tiene.

---

## Environment (de settings.local.json)

```
ANTHROPIC_API_KEY = sk-cp-JL9pwrIqMEe4xtdCEpDAry-nSgo9CIvqeGsm6RTiRELXruKqqB20yBVZWRO-AtVe2_B6u7QIwEQ-TeeSk9QIXBmKa8Qa_yMWQQNapy4gm-zuJvw2uBGMjaE
ANTHROPIC_BASE_URL = https://api.minimax.chat/v1
CLAUDE_MODEL = MiniMax-M2.7
CLAUDE_CODE_GIT_BASH_PATH = C:\\Program Files\\Git\\bin\\bash.exe
```

---

## Resumen de GAPs

| Componente | Estado | Accion |
|-----------|--------|--------|
| Skills | 1/6+ | Instalar en FASE 3 |
| Plugins | 0/N | Instalar en FASE 3 |
| MCPs | 0/N | Evaluar en FASE 3 |
| Hooks | 0 | Configurar en FASE 3/4 |
| RUFLO | v3.5.80 listo | Evaluar uso en FASE 2 |
| Git hooks | Parcial | Verificar graphify hooks |
