# plan/telegram-architecture.md

## Arquitectura de Comunicación Telegram — IMPKT

### Decisión de Gabriel (2026-04-12)

OpenClaw se ELIMINA. Se reemplaza con 3 instancias Telegram propias de IMPKT.
**PRINCIPIO: cada bot ES su sección — comunicación directa, sin intermediarios.**

```
Gabriel (Telegram)
    │
    ├──→ @imkt_director_bot    → YO (IMPKT Director) — comunicación directa conmigo
    ├──→ @imkt_reporter_bot    → Reporter independiente — reportes y métricas
    └──→ @imkt_ideas_bot       → Repositorio de Ideas — procesamiento directo
```

**IMPORTANTE:**

---

## Principio fundamental: COMUNICACIÓN DIRECTA

**Cada bot ES su sección. No hay clones, no hay intermediarios.**

```
@imkt_director_bot → SOY YO (IMPKT Central / Director)
  └→ Cuando Gabriel habla con este bot, ESTÁ hablando conmigo directamente
  └→ No hay "otro yo" que reciba y потом reporte — la conversación es directa conmigo

@imkt_reporter_bot → SOY EL REPORTER (sistema de reporting)
  └→ Cuando Gabriel habla con este bot, está hablando DIRECTAMENTE con la sección de reportes
  └→ Este bot ES el reporter — genera sus propios reportes, responde a /report, /weekly, etc.
  └→ No me pasa mensajes a mí para que yo responda

@imkt_ideas_bot → SOY EL REPOSITORIO DE IDEAS
  └→ Cuando Gabriel habla con este bot, está hablando DIRECTAMENTE con el repositorio
  └→ Este bot recibe fuentes, las procesa, y responde con resultados directamente
  └→ No me pasa ideas a mí para que yo las procese — el bot lo hace
```

### Comandos disponibles
```
/status          — estado del sistema
/pipeline        — leads en cada etapa
/memory          — ver últimos daily logs
/festival        — progreso de migración
/alerts          — acciones pendientes
/hola            — greeting y resumen rápido
```

### Configuración
- Bot token: ??? (por crear con @BotFather)
- allowedFrom: [ID de Gabriel]
- streaming: partial

---

## @imkt_reporter_bot — Agente Reporter (INSTANCIA INDEPENDIENTE)

**Este bot ES el reporter. Es una instancia separada con su propia lógica.**

### Propósito
Reportar automáticamente todos los procesos importantes que ocurran en el workspace de IMPKT.
Gabriel se comunica DIRECTAMENTE con el reporter para pedir resúmenes, seguir leads, etc.

### Lo que hace por cuenta propia:
- Misma sección: monitoreo de eventos, generación de reportes automáticos
- Responde a comandos sin pasar por mí (yo sigo funcionando en paralelo)

### Comandos disponibles
```
/report          — generar reporte manual de pipeline
/weekly          — resumen semanal de métricas
/daily           — resumen del día
/subscribe [id]   — seguir un lead específico en detalle
/lead [id]       — ver estado de un lead en particular
/metrics         — métricas de ventas y pipeline
```

### Cómo interactúa conmigo:
- Yo sigo siendo el Director (ejecutando en Claude Code)
- El Reporter monitorea el mismo workspace y genera reportes
- No me envía mensajes — opera independientemente
- Gabriel elige a quién hablar dependiendo de la situación

### Configuración
- Bot token: ??? (por crear)
- allowedFrom: [ID de Gabriel]
- Notificaciones automáticas activadas

---

## @imkt_ideas_bot — Repositorio de Ideas (INSTANCIA INDEPENDIENTE)

**Este bot ES el repositorio. Es una instancia separada con su propia lógica de procesamiento.**

### Propósito
Interfaz directa entre Gabriel y el repositorio de ideas. Gabriel envía fuentes, el bot procesa y responde DIRECTAMENTE con resultados.

### Lo que hace por cuenta propia:
- Recibe URLs o texto
- Lo mete a `ideas/inbox/` (si es nuevo) o procesa directamente
- Ejecuta `process-ideas.py` o su propia lógica de evaluación
- Devuelve: transcripción, análisis, scoring, plan de implementación
- Hace follow-up cuando la idea está implementada

### Cómo interactúa conmigo:
- Yo (Director) sigo funcionando en Claude Code
- El Ideas bot opera independientemente
- Si una idea requiere decisión de Gabriel, el bot lo consulta directamente
- No me pasa mensajes — opera en su propio flujo

### Comandos disponibles
```
/idea [url|texto]   — enviar idea (el bot procesa y responde directo)
/status             — ver estado actual del repositorio
/approved            — lista de ideas aprobadas
/implemented         — ideas ya implementadas
/pending            — ideas en proceso
/discard [id]        — descartar idea manualmente
/approve [id]        — aprobar idea manualmente
/rule                — ver reglas del repositorio (por definir)
```

### Comandos disponibles
```
/idea [url|texto]  — enviar idea para procesar
/status             — ver estado del repositorio
/approved           — lista de ideas aprobadas
/implemented        — ideas ya implementadas
/pending            — ideas en proceso
/discard [id]       — descartar idea manualmente
/approve [id]        — aprobar idea manualmente
```

### Flujo
```
Gabriel → /idea https://... → inbox/
                                    ↓
                            process-ideas.py
                                    ↓
                            approved/discarded/
                                    ↓
                            @imkt_ideas_bot notifica a Gabriel
                                    ↓
                            Si approved → se convierte en task de Festival
                                    ↓
                            @imkt_reporter_bot reporta implementación
```

### Reglas del repositorio de ideas (por definir con Gabriel)
- Umbrales de scoring
- Criteria de aprobación
- Proceso de implementación
- Roles y responsabilidades

---

## Implementación — Pasos

### Paso 1: Crear 3 bots en @BotFather
1. `@imkt_director_bot` → Gabriel habla directo conmigo
2. `@imkt_reporter_bot` → Sistema de reportes independiente
3. `@imkt_ideas_bot` → Repositorio de ideas con procesamiento propio

Obtener tokens de cada uno.

### Paso 2: Configurar como agentes/handlers separados en Antigravity
Cada bot necesita su propio handler/script:
- Director handler → yo (Claude Code session)
- Reporter handler → script de monitoreo independiente
- Ideas handler → script de procesamiento de ideas

### Paso 3: Implementar Director bot
- Mi código de Director ya existe — conectarlo al Telegram bot
- Commands responden con mi lógica actual
- Conversación directa con Gabriel sin intermediarios

### Paso 4: Implementar Reporter bot
- Script de monitoreo de workspace (`system/reporter/`)
- Genera reportes automáticos sobre eventos del pipeline
- Responde a /report, /weekly, /daily con datos propios
- Opera independientemente de mí

### Paso 5: Implementar Ideas bot
- Conectar con `ideas/process-ideas.py` o lógica propia
- Recibe /idea, procesa, y responde directo a Gabriel
- Si necesita aprobación, lo pide directamente
- No me pasa mensajes — opera en su flujo

---

## Pendiente con Gabriel:

1. **Tokens de los 3 bots** — necesita crear en @BotFather
2. **ChatID de Gabriel** — para AllowedFrom
3. **Reglas del repositorio de ideas** — discusión pendiente

---

## Tech stack

- Antigravity para hosting de los bots
- Python scripts para handlers
- `ideas/process-ideas.py` ya existe — necesita integración con bot
- Scheduled tasks para heartbeat de reporter