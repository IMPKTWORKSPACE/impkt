# Features Nativas Verificadas — Claude Code + Antigravity

**Fecha:** 2026-04-13

---

## Features de Claude Code verificadas (CLI)

| Feature | Status | Verificado | Como |
|---------|--------|-----------|------|
| CLAUDE.md | ✅ Activo | Si | Se lee al inicio de cada sesion |
| Skills | ✅ 8 instaladas | Si | `ls ~/.claude/skills/` |
| Plugins | ✅ 9 instalados | Si | `claude plugins list` |
| MCPs | ✅ 3 configurados | Si | `.claude/mcp.json` existe |
| Read/Write/Edit | ✅ Funcional | Si | Usado en esta sesion |
| Bash | ✅ Funcional | Si | Git Bash disponible |
| Glob/Grep | ✅ Funcional | Si | Herramientas nativas |
| WebFetch | ✅ Funcional | Si | curl disponible |
| Git tools | ✅ Funcional | Si | git integrado |
| Headless mode | ✅ Funcional | Si | `-p` flag funciona |
| Agents | ✅ 20 agentes | Si | `claude agents` lista 20 |
| Hooks system | ✅ Disponible | Si | En settings + plugins |
| MCP config | ✅ Disponible | Si | `claude mcp add` funciona |

---

## Features NO disponibles via CLI

| Feature | Status | Nota |
|---------|--------|------|
| Scheduled tasks | ❌ No existe | `claude schedule` no es subcomando |
| Channels | ❌ No existe | `claude channels` no existe |
| Team command | ❌ No existe | `claude team` no disponible |
| computer-use | ❌ No disponible | Requiere extension Chrome |
| Ghost Runtimes | ⚠️ UI only | Requiere verificacion visual |

---

## Scheduled Tasks — Solucion alternativa

**Problema:** No existe `claude schedule` como subcomando.
**Solucion:** Usar CronCreate tool de Claude Code para scheduling.

```
/help  # Buscar cron o schedule commands
```

**Alternativa Windows:** Crear script Python que ejecute los bots y programar con Task Scheduler de Windows.

---

## Agent Teams

**Discovery:** `claude agents` lista 20 agentes de los plugins instalados.

**Agentes disponibles:**
- Built-in: claude-code-guide, Explore, general-purpose, Plan, statusline-setup
- De plugins: code-reviewer, code-architect, code-explorer (feature-dev), pr-review-toolkit agents, hookify agents, plugin-dev agents, agent-sdk-dev agents

**Para configurar Agent Teams de IMPKT:**
- Ya existe `teams/impkt-main/config.json`
- El feature de "Agent Teams" nativo puede no existir como subcomando
- Los 5 leads (Mila, Lena, Sofia, Finn, Nova) usan Agent tool para invocarse

---

## Hooks — Estado

**PreToolUse y PostToolUse:** Disponibles en settings.json.
**Installados:** Los plugins installed activan sus propios hooks automaticamente.

**Para ver hooks activos:**
```bash
claude --debug 2>&1 | grep -i hook
```

**security-guidance plugin:** Instaldo — activa un hook PreToolUse que warn sobre vulnerabilidades.

---

## Claude in Chrome

**Flag disponible:** `--chrome` en CLI
**Status:** Requiere extension de Chrome instalada
**Verificacion:** Gabriel debe abrir Chrome y verificar si tiene la extension Claude

---

## Features de Antigravity (requieren verificacion visual por Gabriel)

| Feature | Status | Como verificar |
|---------|--------|---------------|
| Ghost Runtimes | ⚠️ ? | Abrir Antigravity, buscar opcion de runtime efimero |
| Browser agent | ⚠️ ? | Buscar icono de browser en sidebar |
| Artifact system | ⚠️ ? | Generar codigo, ver si aparecen artifacts |
| Agent Manager | ⚠️ ? | Buscar en menu o sidebar |

**AGREGAR A needs-gabriel.md**

---

## Resumen

- **CLI:** Full functionality — todas las herramientas nativas funcionan
- **Scheduled tasks:** NO existe como subcomando — usar CronCreate tool
- **Channels:** NO existe
- **Agent Teams:** Hay agents pero el concepto de "team" puede no existir como feature
- **Antigravity GUI:** Pendiente verificacion visual por Gabriel
