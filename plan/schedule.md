# plan/schedule.md

## Scheduled Tasks — IMPKT System

### Ideas Processor (cada 10 minutos)
```bash
# Run ideas/process-ideas.py cada 10 min
# (dentro de sesión activa de Antigravity)
```

### Graphify rebuild (git hooks)
- post-commit: rebuild AST graph (code only)
- post-checkout: rebuild AST graph

### Heartbeat check (cada 1 hora durante sesión)
- Verificar graphify-out/ actualizado
- Verificar ideas/inbox/ vacío
- Verificar pipeline sin bottlenecks

### Weekly report (para Gabriel)
- Cada lunes: estado del sistema, métricas de pipeline

---

## Cron expression reference

| Frecuencia | Expression |
|---|---|
| Cada 10 min | `*/10 * * * *` |
| Cada hora | `0 * * * *` |
| Cada día 9am | `0 9 * * *` |
| Cada lunes 9am | `0 9 * * 1` |

## Configurar scheduled tasks en Antigravity

Pending: configurar scheduled tasks via Antigravity para que corran cuando la sesión esté activa.