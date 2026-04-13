# Inventario: Antigravity

**Fecha:** 2026-04-13

---

## Environment

| Herramienta | Version | Path |
|------------|---------|------|
| Bash | Git Bash | /usr/bin/bash |
| Node.js | v22.22.2 | which node |
| Python | 3.14.3 | which python |
| Git | 2.53.0.windows.2 | which git |
| npm | 10.9.7 | which npm |
| pip | disponible | /c/Python314/Scripts/pip.exe |
| pip3 | disponible | /c/Python314/Scripts/pip3.exe |

---

## Features CLI disponibles

| Feature | Verificado | Notas |
|---------|-----------|-------|
| Bash | Si | Git Bash, full |
| Claude Code CLI | Si | v2.1.104 |
| Node/npm | Si | Para MCPs y RUFLO |
| Python | Si | 3.14.3 |
| Git | Si | Integracion native |
| RUFLO | Si | npx ruflo@latest |
| pip | Si | Python packages |

---

## Features Antigravity (requiere verificacion visual por Gabriel)

| Feature | Status CLI | Requiere UI | Notas |
|---------|-----------|-------------|-------|
| Ghost Runtimes | No verificado | SI | Containers efimeros para testing |
| Browser agent | No verificado | SI | En sidebar de Antigravity |
| Artifact system | No verificado | SI | Generacion automatica de artifacts |
| Agent Manager | No verificado | SI | Gestion de agents en interfaz |
| Planning Agent (Gemini) | No verificado | SI | Tasks de research y planning |
| Fast Agent (Gemini) | No verificado | SI | Tareas rapidas |
| UI Browser Agent (Gemini) | No verificado | SI | Web navigation |
| Deployment scripts | No verificado | SI | Deploy a GCP |
| Headless mode | Si verificado | No | flag -p funciona |

---

## GitHub CLI

**gh:** NO instalado en PATH
**Token disponible:** [EN GITHUB SECRETS — no committed]
**Ubicacion gh:** no encontrado en /c/Program Files/GitHubCLI/ ni en perfiles de usuario
**Alternativa:** Usar GitHub API via curl/Python para todas las operaciones GitHub

**Accion:** Documentado en needs-gabriel.md — Gabriel debe instalar gh CLI para workflow Git mas fluido.

---

## Docker

**Estado:** NO disponible (restringido por sandboxing de Antigravity segun CLAUDE.md)
**Docker compose:** NO ejecutar nunca (regla absoluta)

---

## Verificacion pendiente por Gabriel (UI)

Estas features requieren que Gabriel abra la interfaz de Antigravity y verifique:

1. **Ghost Runtimes:** Abrir un proyecto, verificar si hay opcion de runtime efimero
2. **Browser agent:** Verificar si hay icono de browser en la barra lateral
3. **Artifact system:** Verificar si al generar codigo aparecen artifacts
4. **Agent Manager:** Verificar que aparece en el menu o sidebar

**Archivo destino:** `library/needs-gabriel.md` — se compilara en FASE 7

---

## Resumen

- **CLI:** Full functionality
- **GUI features:** No verificadas (pendiente Gabriel)
- **GitHub CLI:** No instalada (token disponible, gh no en PATH)
- **Docker:** Bloqueado por sandbox
