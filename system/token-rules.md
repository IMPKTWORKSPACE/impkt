# system/token-rules.md

## Reglas de optimización de tokens para IMPKT

1. **NO leer archivos completos** si solo necesitas una sección. Usa `head -n`, `tail -n`, `grep`, `find`.
2. **Agrupar verificaciones** en UN solo comando compuesto.
3. **NO repetir comandos** — guardar resultados en `system/cache/` como `.md` temporal.
4. **Archivos > 200 líneas**: leer primeras 50 para estructura, luego buscar lo específico.
5. **Escribir resultados de trabajo** en archivos `.md` conforme avanzan — no acumular en memoria.
6. **Si una tarea falla**: analizar el error ANTES de reintentar.
7. **Cada respuesta concisa y orientada a acción** — no repetir contexto ya en archivos.
8. **Carpeta de cache**: `system/cache/` — limpiar cuando ya no sirva.
9. **Verificar antes de actuar**: leer archivo una vez, editar lo mínimo necesario.
10. **Sesiones largas pueden caer ~12h**: guardar TODO en disco antes de cada milestone.