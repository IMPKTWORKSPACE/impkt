# INVENTARIO GLOBAL — ~/.claude/

**Fecha:** 2026-04-13
**Rutas:**
- Global config: `C:\Users\graci\.claude\`
- Workspace config: `C:\Users\oscar\impkt\.claude\`
- Skills globales: `C:\Users\graci\.claude\skills\`

---

## Skills Globales (en ~/.claude/skills/)

| Skill | Tipo | Estado | Para quién |
|-------|------|--------|------------|
| graphify | custom | Implementada | Global (knowledge graph) |
| landing-builder | custom | Implementada (de OpenClaw) | Finn |
| proposal-generator | custom | Implementada (de OpenClaw) | Sofia |
| coding-agent | custom | Implementada (de OpenClaw) | Finn |
| lead-research | custom | Stub vacio | Lena |
| content-humanizer | custom | Stub vacio | Global |
| seo-optimizer | custom | Stub vacio | Mila |
| client-onboarding | custom | Stub vacio | Nova |

**Stubs a implementar:** lead-research, seo-optimizer, content-humanizer, client-onboarding. Los stubs existen como archivos SKILL.md vacios.

---

## Plugins Instalados y Habilitados

**Archivo:** `~/.claude/settings.json` (habilitados)
**Registro:** `~/.claude/plugins/installed_plugins.json`

| Plugin | Habilitado | Cache path | Util para IMPKT |
|--------|-----------|------------|-----------------|
| frontend-design | SI | claude-plugins-official/frontend-design | Finn (QA/UX) |
| code-review | SI | claude-plugins-official/code-review | Finn (QA) |
| commit-commands | SI | claude-plugins-official/commit-commands | Global (git) |
| hookify | SI | claude-plugins-official/hookify | Global (hooks) |
| plugin-dev | SI | claude-plugins-official/plugin-dev | Global (dev) |
| pr-review-toolkit | SI | claude-plugins-official/pr-review-toolkit | Finn (QA) |
| feature-dev | SI | claude-plugins-official/feature-dev | Finn (dev) |
| security-guidance | SI | claude-plugins-official/security-guidance | Global (auditoria) |
| agent-sdk-dev | SI | claude-plugins-official/agent-sdk-dev | Global (dev) |
| skill-creator | SI (nuevo) | cache/skill-creator | Global (crear skills) |
| mcp-server-dev | SI (nuevo) | cache/mcp-server-dev | Global (crear MCPs) |

---

## Plugins en Marketplace (NO instalados — solo cache)

### external_plugins/

| Plugin | Skills | Descripcion | Util para IMPKT |
|--------|--------|-------------|-----------------|
| asana | NO | Gestor de tareas | NO |
| context7 | NO | Context manager | NO |
| discord | access, configure | Chat | NO |
| firebase | NO | Backend | NO |
| github | NO | Git integration | NO (ya tenemos gh API) |
| gitlab | NO | Git integration | NO |
| greptile | NO | Code search | NO |
| imessage | access, configure | Mensajeria Mac | NO (Windows) |
| laravel-boost | NO | Laravel tooling | NO |
| linear | NO | Gestor de proyectos | NO |
| playwright | NO | Browser automation | Evaluando (Finn - QA) |
| serena | NO | CLI tool | NO |
| supabase | NO | Backend | NO |
| telegram | access, configure | MCP Telegram (requiere Bun) | Evaluando (ya tenemos bots Python) |
| terraform | NO | Infrastructure as code | NO |

**No instalados:** Ninguno es critico para IMPKT en este momento.

### official plugins/ (en marketplace)

| Plugin | Skills | Descripcion | Util para IMPKT |
|--------|--------|-------------|-----------------|
| clangd-lsp | NO | C/C++ LSP | NO |
| claude-code-setup | NO | Setup helper | NO |
| claude-md-management | NO | MD file management | NO |
| code-simplifier | NO | Simplificar codigo | NO |
| csharp-lsp | NO | C# LSP | NO |
| example-plugin | NO | Plugin ejemplo | NO |
| explanatory-output-style | NO | Output styling | NO |
| gopls-lsp | NO | Go LSP | NO |
| jdtls-lsp | NO | Java LSP | NO |
| kotlin-lsp | NO | Kotlin LSP | NO |
| learning-output-style | NO | Output styling | NO |
| lua-lsp | NO | Lua LSP | NO |
| math-olympiad | NO | Math problems | NO |
| mcp-server-dev | SI (instalado) | Build MCP servers | **SI** — para WhatsApp, email, CRM |
| php-lsp | NO | PHP LSP | NO |
| playground | NO | Code playground | NO |
| ralph-loop | NO | Ralph Wiggum loops | Evaluando |
| ruby-lsp | NO | Ruby LSP | NO |
| rust-analyzer-lsp | NO | Rust LSP | NO |
| session-report | NO | Session reports | NO |
| skill-creator | SI (instalado) | Create skills | **SI** — crear skills custom |
| swift-lsp | NO | Swift LSP | NO |
| typescript-lsp | NO | TypeScript LSP | NO |
| agent-sdk-dev | SI (habilitado) | Agent SDK dev | Global (dev) |
| hookify | SI (habilitado) | Hooks system | Global (hooks) |
| plugin-dev | SI (habilitado) | Plugin development | Global (dev) |
| pr-review-toolkit | SI (habilitado) | PR review | Finn (QA) |
| code-review | SI (habilitado) | Code review | Finn (QA) |
| feature-dev | SI (habilitado) | Feature dev | Finn (dev) |
| security-guidance | SI (habilitado) | Security | Global (auditoria) |
| frontend-design | SI (habilitado) | Frontend | Finn (production) |

---

## Skills disponibles por Plugin instalado

### skill-creator
1 skill: `skill-creator` — crear skills desde cero, mejorar existentes, medir performance

### mcp-server-dev
3 skills: `build-mcp-server`, `build-mcp-app`, `build-mcpb`

---

## Lo que el brief decia pero NO existe

| Mentioned | Realidad |
|-----------|----------|
| wondelai-skills | NO EXISTE en este sistema |
| anthropic-agent-skills | NO EXISTE |
| superpowers plugin | NO EXISTE (plugin completo) |

---

## Recomendaciones de instalación

### Alta prioridad (implementar ahora)
1. **Stub skills** → implementar lead-research, seo-optimizer, content-humanizer, client-onboarding
2. **mcp-server-dev** → usar para construir MCPs de WhatsApp y email automation

### Evaluar despues
- **telegram MCP** → Requiere Bun. Los 3 bots actuales en Python funcionan bien. Evaluar si tiene ventaja.
- **playwright** → Podria ayudar a Finn con QA de landing pages automtizado
- **ralph-loop** → Metodologia de loops iterativos. Interesante para fases de building.

---

## Config de Hooks (workspace)

`C:\Users\oscar\impkt\.claude\settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Glob|Grep",
      "hooks": [{
        "type": "command",
        "command": "[ -f graphify-out/graph.json ] && echo '...graphify context...' || true"
      }]
    }]
  }
}
```

Este hook inyecta contexto de Graphify antes de Glob/Grep. **Activo.**

---

_Ultima actualizacion: 2026-04-13_
