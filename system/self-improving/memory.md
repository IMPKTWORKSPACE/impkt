# system/self-improving/memory.md

## Reglas de ejecución mejoradas (apend after ogni correction/lesson)

_Aprendí estas lecciones ejecutando el sistema IMPKT:_

### Sobre ejecución autónoma
- Cada task completada → documentar en `system/state.md` ANTES de avanzar
- Nunca asumir que la sesión persistirá — guardar todo en disco en cada milestone
- Si una tarea falla, analizar el error ANTES de reintentar (no ciego retry)

### Sobre configuración de agentes
- Cada lead (Mila, Lena, Sofia, Finn, Nova) tiene SOUL.md propio en su directorio
- Pipeline de comunicación entre leads: JSON en `pipeline/[from]-to-[to]/`
- System prompts deben ser específicos, no vagos — incluir ejemplos de output

### Sobre memoria y continuidad
- `system/state.md` = verdad única del estado del sistema
- `system/festival/impkt-migration/campaigns/impkt-migration/state.yaml` = progreso de la migración
- `system/memory/` = logs de ejecución por fecha

### Sobre herramientas
- graphify hook activo — leer `graphify-out/GRAPH_REPORT.md` antes de Glob/Grep
- PreToolUse hook en `.claude/settings.json` ya configurado para graphify
- pip en Windows: usar `/c/Python314/Scripts/pip.exe` (no `pip` directo)

### Sobre OpenClaw
- NO modificar nada en `C:\Users\oscar\.openclaw\` — solo lectura
- Solo usar OpenClaw como Telegram bot, no como executor
- Si algo se rompe en OpenClaw, documentar en `audit/problems-found.md`

### Sobre Graphify
- `.graphifyignore` excluye: tools/graphify/, graphify-out/, .git/
- Si grafo parece outdated, re-ejecutar `system/run-graphify.py`
- graph.html es visual — se puede abrir en browser para verificación

### Corrections registry
[Append corrections here when Gabriel corrects something]