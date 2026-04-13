# Plugins Instalados — Claude Code

**Fecha:** 2026-04-13
**Alcance:** user (todos los proyectos)

---

## Metodo de instalacion

```bash
claude plugin install [nombre] --scope user
```

---

## Plugins instalados

| Plugin | Version | Status | Para que sirve |
|--------|---------|--------|---------------|
| frontend-design | ? | Instalado | Generacion de frontend diferenciado, no generico-IA |
| code-review | ? | Instalado | PR review con agentes paralelo y confidence scoring |
| commit-commands | ? | Instalado | Git workflow: commit, push, PR en un command |
| hookify | ? | Instalado | Crear hooks custom sin editar JSON |
| plugin-dev | ? | Instalado | Toolkit para crear plugins propios |
| pr-review-toolkit | ? | Instalado | 6 agentes especializados para review granular |
| feature-dev | ? | Instalado | Workflow 7-fases para desarrollo de features |
| security-guidance | ? | Instalado | Hook PreToolUse para warnings de seguridad |
| agent-sdk-dev | ? | Instalado | Dev kit para construir apps con Claude Agent SDK |

---

## Plugins NO instalados

| Plugin | Razon |
|--------|-------|
| ralph-wiggum | No encontrado en marketplace |

---

## Verificacion

```bash
ls ~/.claude/plugins/
cat ~/.claude/plugins/installed_plugins.json
```

---

## Notas

- **frontend-design:** Skill built-in, se activa automatico en tareas frontend
- **security-guidance:** Hook automatico, requiere verificacion de que funciona
- **ralph-wiggum:** Nombre diferente en marketplace o no disponible

---

## Pending verification

- Verificar que security-guidance hook funciona (ejecutar un Edit y ver si warned)
- Verificar que frontend-design se activa automaticamente
- Probar `/commit` command de commit-commands
- Probar `/code-review` de code-review
