# IMPKT — Self-Check Post-Install Verification

## Fecha: 2026-04-12

## Checklist del install guide

- [x] Workspace `C:\Users\oscar\impkt\` creado
- [x] Git inicializado en el workspace
- [x] Claude Code instalado y funcionando (v2.1.104)
- [x] Variables de entorno de MiniMax configuradas
- [x] Redirección a MiniMax verificada (API_KEY=SET, MODEL=MiniMax-M2.7)
- [x] Antigravity abierto con el workspace cargado (sesión actual)
- [x] Graphify clonado en `tools/graphify/`
- [x] Obsidian: vault existente en `C:\Users\oscar\impkt` (directorio raíz ya es vault Obsidian, tiene `.obsidian/`)
- [x] Festival: estructura replicada manualmente en `system/festival/`
- [x] Acceso al vault de OpenClaw verificado
- [x] CLAUDE.md copiado al workspace
- [x] Backup de .openclaw creado (carpeta `openclaw-backup-2026-04-12/` — zip con error de permisos)

## Notas importantes

### ANTHROPIC_BASE_URL
Está configurado como `https://api.minimax.io/anthropic` en lugar del `https://api.minimax.chat/v1` que dice el install guide.
**Gabriel dijo: "Si ya funciona, no lo corrijas."** — Se deja como está.

### Festival
Instalación en WSL falló. Estructura replicada manualmente en `system/festival/`:
```
system/festival/
├── impkt-migration/
│   ├── campaigns/
│   └── festivals/{planning,active,completed}/
```

### Obsidian Vault
El vault de Obsidian ES `C:\Users\oscar\impkt` — el directorio raíz ya tiene `.obsidian/` lo que lo convierte en vault válido.
El install guide dice que el vault debe apuntar a `knowledge/` — esa carpeta no existe todavía, pero el vault actual está en la raíz.
**Pendiente: Clarificar con Gabriel si el vault debe ser `knowledge/` o si sirve el de la raíz.**

### Backup
El zip falló por permisos en `sessions/`, pero se creó una carpeta `openclaw-backup-2026-04-12/` como fallback.