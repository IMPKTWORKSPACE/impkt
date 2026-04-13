# Inventario de Agentes — OpenClaw

**Total declarado en openclaw.json:** 10
**Total en directorio agents/:** 12 directorios físicos
**Huérfanos (en filesystem pero no en config):** 2
**Estado general:** Mixto — agentes lead (Lena/Finn/Nova) activos; 4 mc-leads huérfanos

---

## Agentes DECLARADOS en openclaw.json

### Grupo: Main

| Campo | Valor |
|-------|-------|
| ID | `main` |
| Nombre | (sin nombre específico — es el agente raíz) |
| Workspace | `C:\Users\oscar\.openclaw\workspace` |
| agentDir | `C:\Users\oscar\.openclaw\agents\main\` |
| heartbeat | No declarado (usa defaults) |
| Estado | ACTIVO |

---

### Grupo: MC Gateways (2)

#### mc-gateway-8f6ce89e

| Campo | Valor |
|-------|-------|
| ID | `mc-gateway-8f6ce89e-c7fb-412d-8026-b4bbd212cdaf` |
| Nombre | Jarvis Main Gateway Agent |
| Workspace | `C:\Users\oscar\.openclaw\workspace-gateway-8f6ce89e-c7fb-412d-8026-b4bbd212cdaf` |
| agentDir | `C:\Users\oscar\.openclaw\agents\mc-gateway-8f6ce89e-c7fb-412d-8026-b4bbd212cdaf\agent` |
| heartbeat | every: 24h, includeReasoning: false, target: last |
| Estado | ACTIVO |

#### mc-gateway-cc9bd917

| Campo | Valor |
|-------|-------|
| ID | `mc-gateway-cc9bd917-7d39-4aa0-b3cd-49a67ad0e343` |
| Nombre | Jarvis mission control gateway Gateway Agent |
| Workspace | `C:\Users\oscar\.openclaw/workspace-gateway-cc9bd917-7d39-4aa0-b3cd-49a67ad0e343` |
| agentDir | `C:\Users\oscar\.openclaw\agents\mc-gateway-cc9bd917-7d39-4aa0-b3cd-49a67ad0e343\agent` |
| heartbeat | every: 24h |
| Estado | ACTIVO |

---

### Grupo: MC Leads (4) — TODOS HUÉRFANOS

#### mc-c57f7e3f

| Campo | Valor |
|-------|-------|
| ID | `mc-c57f7e3f-a6dc-4785-97d1-43003041c84b` |
| Nombre | Client Comms Lead |
| Workspace | `C:\Users\oscar\.openclaw\workspace-mc-c57f7e3f-a6dc-4785-97d1-43003041c84b` |
| agentDir | `C:\Users\oscar\.openclaw\agents\mc-c57f7e3f-a6dc-4785-97d1-43003041c84b\agent` |
| heartbeat | every: 24h |
| Estado | **HUÉRFANO** — en config pero no en uso. MEMORY.md dice "eliminar". |

#### mc-52c78d33

| Campo | Valor |
|-------|-------|
| ID | `mc-52c78d33-0dbe-488c-a812-f5ca297115ca` |
| Nombre | Outreach Lead |
| Workspace | `C:\Users\oscar\.openclaw\workspace-mc-52c78d33-0dbe-488c-a812-f5ca297115ca` |
| agentDir | `C:\Users\oscar\.openclaw\agents\mc-52c78d33-0dbe-488c-a812-f5ca297115ca\agent` |
| heartbeat | every: 24h |
| Estado | **HUÉRFANO** — MEMORY.md indica eliminar. |

#### mc-0b90aca2

| Campo | Valor |
|-------|-------|
| ID | `mc-0b90aca2-e735-4f12-b978-360faa955aa7` |
| Nombre | Production Lead |
| Workspace | `C:\Users\oscar\.openclaw\workspace-mc-0b90aca2-e735-4f12-b978-360faa955aa7` |
| agentDir | `C:\Users\oscar\.openclaw\agents\mc-0b90aca2-e735-4f12-b978-360faa955aa7\agent` |
| heartbeat | every: 24h |
| Estado | **HUÉRFANO** — MEMORY.md indica eliminar. |

#### mc-8b12584e

| Campo | Valor |
|-------|-------|
| ID | `mc-8b12584e-0708-417b-8b7e-cc33c0c31384` |
| Nombre | Sales Pipeline Lead |
| Workspace | `C:\Users\oscar\.openclaw\workspace-mc-8b12584e-0708-417b-8b7e-cc33c0c31384` |
| agentDir | `C:\Users\oscar\.openclaw\agents\mc-8b12584e-0708-417b-8b7e-cc33c0c31384\agent` |
| heartbeat | every: 24h |
| Estado | **HUÉRFANO** — MEMORY.md indica eliminar. |

---

### Grupo: Leads (3) — ACTIVOS

#### lead-4fd9682e

| Campo | Valor |
|-------|-------|
| ID | `lead-4fd9682e-9735-4786-9c4e-aaab81090e26` |
| Nombre | **Lena** |
| Workspace | `C:\Users\oscar\.openclaw/workspace-lead-4fd9682e-9735-4786-9c4e-aaab81090e26` |
| agentDir | `C:\Users\oscar\.openclaw\agents\lead-4fd9682e-9735-4786-9c4e-aaab81090e26\agent` |
| heartbeat | every: 24h |
| Rol en IMPKT | OUTREACH — primer contacto, calificación, discovery |
| Estado | **ACTIVO** |

#### lead-900f679d

| Campo | Valor |
|-------|-------|
| ID | `lead-900f679d-88d0-46f4-9357-c0bd57fe20e3` |
| Nombre | **Finn** |
| Workspace | `C:\Users\oscar\.openclaw/workspace-lead-900f679d-88d0-46f4-9357-c0bd57fe20e3` |
| agentDir | `C:\Users\oscar\.openclaw\agents\lead-900f679d-88d0-46f4-9357-c0bd57fe20e3\agent` |
| heartbeat | every: 24h |
| Rol en IMPKT | PRODUCTION — builder + Claude Code, construye y entrega |
| Estado | **ACTIVO** |

#### lead-dedaed8f

| Campo | Valor |
|-------|-------|
| ID | `lead-dedaed8f-ae9c-47bb-aadd-1d25095e797b` |
| Nombre | **Nova** |
| Workspace | `C:\Users\oscar\.openclaw/workspace-lead-dedaed8f-ae9c-47bb-aadd-1d25095e797b` |
| agentDir | `C:\Users\oscar\.openclaw\agents\lead-dedaed8f-ae9c-47bb-aadd-1d25095e797b\agent` |
| heartbeat | every: 24h |
| Rol en IMPKT | CLIENT COMMS — post-deal, seguimiento, bugs |
| Estado | **ACTIVO** |

---

## Agentes HUÉRFANOS (en filesystem, NO en openclaw.json)

### mc-gateway-6dad1190

| Campo | Valor |
|-------|-------|
| Directorio | `C:\Users\oscar\.openclaw\agents\mc-gateway-6dad1190-291b-4608-b38a-7ae088cb1347\` |
| Nombre | (sin nombre en workspace — solo existe el dir) |
| Estado | **HUÉRFANO** — existe en filesystem pero NO está en openclaw.json |
| Notas | No fue migrado a la nueva estructura de agentes |

### mc-297b86b5

| Campo | Valor |
|-------|-------|
| Directorio | `C:\Users\oscar\.openclaw\agents\mc-297b86b5-5fc0-49e4-8207-3a2c4f9d8551\` |
| Nombre | (sin nombre en workspace — solo existe el dir) |
| Estado | **HUÉRFANO** — existe en filesystem pero NO está en openclaw.json |
| Notas | MEMORY.md señala este ID como huérfano |

---

## Agentes REFERENCIADOS en MEMORY.md pero NO en openclaw.json

MEMORY.md lista también:
- `lead-dd86bb76` (Mila — MARKETING)
- `lead-d5048423` (Sofia — SALES)

Estos agentes están en MEMORY.md pero NO en openclaw.json. No existen como directorios en agents/. Esto indica que fueron creados en Mission Control (docker) pero nunca dados de alta en openclaw.json.

---

## Resumen

| Categoría | Count | Notas |
|-----------|-------|-------|
| main | 1 | Activo |
| mc-gateway | 2 | Ambos activos |
| mc-lead (huérfanos en config) | 4 | mc-c57f7e3f, mc-52c78d33, mc-0b90aca2, mc-8b12584e |
| lead (Lena/Finn/Nova) | 3 | Activos — roles definidos |
| Huérfanos en filesystem | 2 | mc-gateway-6dad1190, mc-297b86b5 |
| Referencias en MEMORY sin config | 2 | Mila, Sofia — en Mission Control docker |
| **Total** | **14** | |

---

## Patrón de workspaces

OpenClaw crea un workspace separado por agente:
```
.openclaw/
  workspace/                          # main
  workspace-gateway-*/                # mc-gateways
  workspace-mc-*/                     # mc-leads (huérfanos)
  workspace-lead-*/                    # leads
```

**Problema:** Esta estructura es difícil de mantener. Cada workspace tiene sus propios archivos de estado (SOUL.md, CONTEXT.md, etc.) pero comparten archivos del workspace principal via paths relativos.

**Cómo IMPKT lo replica:** En Claude Code con Agent Teams, cada lead agent es un worktree git separado, no un workspace OpenClaw. Más limpio, más portable.

---

## Configuración de heartbeat

Todos los agentes activos usan heartbeat de 24h. Esto es poco frecuente para un sistema activo.

Para IMPKT, los heartbeats deberían ser:
- Agentes principales: cada 1-2 horas
- Sistema de salud: cada 30 min
- Ver `audit/problems-found.md` para ver que los cron jobs están deshabilitados

---

## Conclusión

- **Agentes activos útiles:** main, mc-gateway-8f6ce89e, mc-gateway-cc9bd917, lead-4fd9682e (Lena), lead-900f679d (Finn), lead-dedaed8f (Nova)
- **Agentes huérfanos a limpiar:** mc-c57f7e3f, mc-52c78d33, mc-0b90aca2, mc-8b12584e, mc-gateway-6dad1190, mc-297b86b5
- **Mila y Sofia** existen en Mission Control (docker) pero no en openclaw.json — problema de sincronización entre sistemas