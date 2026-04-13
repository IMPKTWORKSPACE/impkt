# HEARTBEAT.md — IMPKT System Heartbeat

## Heartbeat check cada 1 hora (durante sesión activa)

### Verificaciones automáticas:

1. **Graphify graph** — ¿actualizado?
   - Si hay archivos nuevos en `graphify-out/` con fecha > último rebuild, notificar
   - Comando: `ls -la graphify-out/graph.json`

2. **Ideas inbox** — ¿hay nuevas ideas?
   - Si `ideas/inbox/` tiene archivos, el processor las toma
   - No necesito hacer nada manual — el scheduled task se encarga

3. **Pipeline** — ¿hay leads en espera?
   - Verificar si alguna carpeta de pipeline tiene archivos sin mover
   - Si alguien no pasó un lead al siguiente paso, documentar bottleneck

4. **Alertas** — ¿hay alertas pendientes?
   - Revisar `system/alerts/` — si hay alertas de más de 3 días, hacer cleanup

5. **Festival state** — ¿estado correcto?
   - Si session se cortó, el state.yaml ya tiene el último estado
   - Al reiniciar, continuar desde `next_task`

### Si todo está bien:
- Responder: `HEARTBEAT_OK`
- No generar output innecesario

### Si hay problemas:
- Documentar en `system/alerts/[fecha]-[problema].md`
- Reportar a Gabriel al inicio de la siguiente sesión

### Para scheduled tasks fuera de sesión:
El sistema de scheduled tasks de Antigravity corre heartbeats cuando la sesión está activa.
Si no hay sesión activa, las tareas se acumulan y ejecutan cuando vuelvas.

## Métricas del sistema (para reporting a Gabriel)

Cada semana, reportar:
- Leads en pipeline (por etapa)
- Ideas procesadas (approved/discarded)
- Tasks completadas de Festival
- Estado general del sistema