# Features GLOBALES — Todo IMPKT

**Fecha:** 2026-04-13
**Aplicable a:** Todos los agentes

---

## Scheduled Tasks

**Disponibilidad:** Verificar si existe en Claude Code Pro.

**Test:**
```bash
claude --help 2>/dev/null | grep -i schedule
```

**Si existe:** Configurar heartbeat para Reporter bot (reporte diario a Gabriel).
**Si NO existe:** Usar cron externo o Windows Task Scheduler como fallback.

**Pendiente verificar.**

---

## Channels

**Disponibilidad:** Verificar si existe en Claude Code Pro.

**Uso potencial:** Recibir eventos de GitHub (push, PR), triggers externos.

**Pendiente verificar.**

---

## Headless mode

**Estado:** YA VERIFICADO — funciona con `-p` flag.

```bash
claude -p "task description" --allowedTools "Read,Bash"
```

**Uso:** Ejecucion programatica sin terminal.

---

## Agent Teams config

**Archivo:** `teams/impkt-main/config.json` — YA EXISTE.

**Estado:** Necesita validacion de que funciona con la version actual de Claude Code.
**Nota:** Claude Code Agent Teams es una feature que requiere configuracion en settings.json.
**Verificar.**

---

## Knowledge Graph (Graphify)

**Estado:** YA INSTALADO.
- `graphify-out/` existe con GRAPH_REPORT.md, graph.json, graph.html
- Skill en `~/.claude/skills/graphify/`
- Hook PreToolUse para lectura de GRAPH_REPORT.md antes de Glob/Grep

**Pendiente:** Ejecutar rebuild despues de este festival para incluir todos los archivos nuevos.

---

## Memory system

**Estado:** YA CONFIGURADO.
- `system/state.md` — estado del sistema
- `system/memory/` — logs diarios
- `system/self-improving/` — mejoras
- `system/proactivity/` — seguimiento

**Funciona:** Continua entre sesiones.

---

## Git workflow

**Archivos:** `.git/` existe. **Pendiente:** .gitignore completo.

**Reglas de GitHub (del festival):**
- Todo repo = PRIVADO
- NO subir .env, API keys, tokens, credentials
- Tokens de bots en `system/bots/*/bot.py` → NO commit

**.gitignore completo a crear:**

```
# Environment
.env
.env.*
*.key
*.pem

# Credentials
credentials/
system/bots/*/bot.py
*.credentials.json

# Python
__pycache__/
*.pyc
*.pyo
.venv/

# Node
node_modules/

# Graphify
graphify-out/cache/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/settings.json
.claude/backups/

# Logs
*.log
system/bots/*/run.log

# Obsidian
.obsidian/workspace.json
.obsidian/graph.json
```

---

## Hooks del sistema

**PreToolUse y PostToolUse hooks disponibles (de la investigacion):**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/security-check.sh"
          }
        ]
      }
    ]
  }
}
```

**Hooks a configurar (FASE 4):**
1. **Graphify hook:** Leer GRAPH_REPORT.md antes de Glob/Grep (YA EXISTE como skill)
2. **Security hook:** Bloquear comandos dangerous (rm -rf, etc.)
3. **Session-memory hook:** Guardar estado automaticamente

**Install:** `hookify` plugin ayuda a crear hooks sin editar JSON a mano.

---

## Claude Code Pro features por verificar

| Feature | Status | Como verificar |
|---------|--------|---------------|
| Scheduled tasks | ? | `claude schedule --help` |
| Channels | ? | `claude channels --help` |
| Agent Teams | ? | `claude team --help` |
| Ghost Runtimes | ? | UI de Antigravity |

**Pendiente:** Agregar a `needs-gabriel.md` para verificacion visual.

---

## Resumen de installation global

| Accion | Prioridad | Nota |
|--------|-----------|------|
| .gitignore completo | Critica | Crear ahora |
| Scheduled tasks | Media | Verificar si existe |
| Hooks de seguridad | Media | FASE 4 |
| Graphify rebuild | Alta | FASE 7 |
| Agent Teams validation | Media | Verificar funciona |
