# openclaw.json — Desglose Completo

**Archivo:** `C:\Users\oscar\.openclaw\openclaw.json`
**Version:** 2026.4.9 (2026-04-10T01:47:41.470Z)
**Tamano:** ~12KB (28KB original — se redujo significativamente, seal不透)
**Estado:** Funcional pero con secciones huérfanas

---

## meta

```json
"lastTouchedVersion": "2026.4.9",
"lastTouchedAt": "2026-04-10T01:47:41.470Z"
```

- Qué es: Metadata de versionado del archivo de configuración.
- Qué hace: Registra última versión y timestamp de modificación.
- Funciona: Sí.
- útil para IMPKT: No. Claude Code no tiene version tracking así — se maneja con git.
- Cómo replicar: N/A (descartado).

---

## env

```json
"MINIMAX_API_KEY": "sk-cp-...",
"PERPLEXITY_API_KEY": "pplx-..."
```

- Qué es: Variables de entorno storeadas en el config en lugar de en el sistema.
- Qué hace: Permite a OpenClaw inyectar API keys en los plugins sin variables de sistema.
- Funciona: Sí, pero peligroso — las claves viven en texto plano en un archivo JSON legible.
- útil para IMPKT: Parcial. Para Claude Code, usar variables de entorno reales (`.env` o session vars de Antigravity). NO guardar secrets en JSON.
- Cómo replicar: En Antigravity, las API keys se configuran por sesión o en `.env` en `C:\Users\oscar\impkt\.env`.

---

## wizard

```json
"lastRunAt": "2026-04-10T01:47:33.349Z",
"lastRunVersion": "2026.4.9",
"lastRunCommand": "doctor",
"lastRunMode": "local"
```

- Qué es: Registro del último run del wizard de setup de OpenClaw.
- Qué hace: Apoya en diagnostics cuando algo falla.
- Funciona: Sí.
- útil para IMPKT: No. OpenClaw usa `doctor` como diagnostic; Claude Code tiene sus propios mecanismos de diagnostics (`mcp__ide__getDiagnostics`).
- Cómo replicar: N/A (descartado).

---

## browser

```json
"enabled": true,
"remoteCdpTimeoutMs": 3000,
"remoteCdpHandshakeTimeoutMs": 5000,
"defaultProfile": "browserbase",
"profiles": {
  "browserbase": {
    "cdpUrl": "wss://connect.browserbase.com?apiKey=bb_live_r-...",
    "color": "#F97316"
  }
}
```

- Qué es: Configuración del browser automation via CDP (Chrome DevTools Protocol).
- Qué hace: Permite control de navegador headless para scraping, testing, automatización web.
- Funciona: Parcial. BrowserBase es un servicio externo de pago; el perfil está configurado pero requiere cuenta activa.
- útil para IMPKT: Sí, el concepto. IMPKT usa el browser agent nativo de Antigravity (Chromium headless integrado) — no necesita BrowserBase externo.
- Cómo replicar: En Antigravity, usar el browser agent nativo. No requiere configuración de CDP externo.

---

## auth

```json
"profiles": {}
```

- Qué es: Perfiles de autenticación guardados (social logins, credenciales de servicios).
- Qué hace: Permite guardar tokens de acceso a servicios (no secrets de API, esos van en `env`).
- Funciona: Sí, pero vacío.
- útil para IMPKT: No para IMPKT mismo. Pero el patrón de guardar auth por perfil es útil si IMPKT necesita OAuth flows para clientes.
- Cómo replicar: N/A de momento.

---

## models

```json
"mode": "merge",
"providers": {
  "ollama": { ... },
  "openrouter": { ... },
  "minimax": { ... },
  "anthropic": { ... }
}
```

- Qué es: Sistema de routing de modelos con costos y context windows.
- Qué hace: Permite a OpenClaw seleccionar el modelo correcto por tipo de tarea (chat vs coding vs search).

**Providers:**

### ollama (Ollama Cloud)
- Modelos: `minimax-m2.7:cloud`, `glm-5:cloud`
- Costo: $0 (free tier)
- Context window: 204,800 (minimax-m2.7)
- API: ollama (conecta a Ollama Cloud como bridge)

### openrouter
- Modelos: `Hunter Alpha` (1M context), `Step 3.5 Flash free` (256k context)
- API key configurada

### minimax (Direct)
- Modelos: `MiniMax-M2.7`, `MiniMax-M2.7-highspeed`
- Costo: $0.30 input / $1.20 output / $0.03 cacheRead / $0.12 cacheWrite
- Context window: 200,000 — maxTokens: 8,192
- API: `https://api.minimax.io/anthropic` con `${MINIMAX_API_KEY}`

### anthropic
- Modelo: `claude-sonnet-4-20250514` (Sonnet 4)
- Costo: $3 input / $15 output
- Context window: 200,000 — maxTokens: 8,192
- API: `https://api.anthropic.com` con `${ANTHROPIC_API_KEY}`

**Estado:** Funcional. Todos los providers tienen API keys configuradas.

**útil para IMPKT:** CRÍTICO. El patrón de routing por tipo de tarea es exactamente lo que IMPKT necesita. La config de modelos (costos, context windows, maxTokens) es migrable.

**Cómo replicar:** Crear `C:\Users\oscar\impkt\.env` con:
```
ANTHROPIC_BASE_URL=https://api.minimax.chat/v1
CLAUDE_MODEL=MiniMax-M2.7
MINIMAX_API_KEY=...
PERPLEXITY_API_KEY=...
```

El routing de modelo se hace por variable `CLAUDE_MODEL` (MiniMax M2.7 default, Gabriel cambia a Sonnet/Opus manualmente para premium).

---

## agents

```json
"defaults": {
  "model": { "primary": "minimax/MiniMax-M2.7" },
  "models": { ... },
  "workspace": "C:\\Users\\oscar\\.openclaw\\workspace",
  "memorySearch": { "enabled": false, "provider": "gemini" },
  "compaction": {
    "mode": "safeguard",
    "reserveTokens": 20000,
    "keepRecentTokens": 25000,
    "memoryFlush": { "enabled": true, "softThresholdTokens": 4000 }
  },
  "sandbox": { "mode": "off", "browser": { "enabled": true } }
},
"list": [ ... 10 agentes ... ]
```

### defaults

- **model.primary:** `minimax/MiniMax-M2.7` — modelo por defecto para todos los agentes.
- **models:** Aliases y routing. `minimax` alias para MiniMax-M2.7, `claude-sonnet-4` alias para Sonnet.
- **workspace:** `C:\Users\oscar\.openclaw\workspace` — directorio base para archivos de estado.
- **memorySearch.enabled:** `false` — búsqueda en memoria deshabilitada.
- **compaction:** Config de auto-compactación de contexto cuando se acerca al límite de tokens. Modo `safeguard` con umbrales de 20k/25k tokens.
- **sandbox.mode:** `off` — sandbox deshabilitado por defecto.

**Estado:** Funcional.

**útil para IMPKT:** Sí. El patrón de compaction con `reserveTokens` y `keepRecentTokens` es muy bueno. En Claude Code, la auto-compactación se maneja con `system/token-rules.md` y escritura proactiva a `system/state.md`.

### agents.list

10 agentes declarados en el config:

| ID | Name | Workspace | Tipo |
|----|------|-----------|------|
| `main` | — | (default workspace) | main |
| `mc-gateway-8f6ce89e` | Jarvis Main Gateway Agent | workspace-gateway-8f6ce89e | mc-gateway |
| `mc-gateway-cc9bd917` | Jarvis mission control gateway Gateway Agent | workspace-gateway-cc9bd917 | mc-gateway |
| `mc-c57f7e3f` | Client Comms Lead | workspace-mc-c57f7e3f | mc-lead |
| `mc-52c78d33` | Outreach Lead | workspace-mc-52c78d33 | mc-lead |
| `mc-0b90aca2` | Production Lead | workspace-mc-0b90aca2 | mc-lead |
| `mc-8b12584e` | Sales Pipeline Lead | workspace-mc-8b12584e | mc-lead |
| `lead-4fd9682e` | Lena | workspace-lead-4fd9682e | lead |
| `lead-900f679d` | Finn | workspace-lead-900f679d | lead |
| `lead-dedaed8f` | Nova | workspace-lead-dedaed8f | lead |

**Detalles completos en:** `audit/agents-inventory.md`

**Estado:** 8 válidos, 4 huérfanos (ver `problems-found.md`).

**útil para IMPKT:** Sí. La estructura de agentes leads + gateways es el modelo para los 5 boards de IMPKT (Mila/Lena/Sofia/Finn/Nova). Pero en Claude Code se replica con Agent Teams nativo, no con workspaces separados.

**Cómo replicar:** Con `agent:teams` en Claude Code, crear 5 lead agents. Cada uno con su propio workspace/estado. El scheduler `cron` de Claude Code maneja heartbeats.

---

## tools

```json
"profile": "full",
"alsoAllow": ["ollama_web_search", "ollama_web_fetch"],
"web": { "search": { "enabled": true, "provider": "perplexity" }, "fetch": { "enabled": true } },
"exec": { "host": "gateway", "security": "full", "applyPatch": { "workspaceOnly": true } }
```

- Qué es: Control de herramientas disponibles para los agentes.
- Qué hace:
  - `profile: "full"` = todas las herramientas habilitadas.
  - `alsoAllow`: herramientas adicionales más allá del default (web search/fetch de Ollama).
  - `web.search`: Perplexity como provider de búsqueda.
  - `exec`: Config de ejecución remota via gateway. Security `full` significa sandboxed.

**Estado:** Funcional. Perplexity search configurado como provider.

**útil para IMPKT:** Parcial. Claude Code tiene sus propios controls de herramientas via settings.json y flags de CLI. No necesita esta config.

---

## commands

```json
"native": "auto",
"nativeSkills": "auto",
"restart": true,
"ownerDisplay": "raw"
```

- Qué es: Config de cómo se manejan los comandos del sistema.
- Qué hace:
  - `native: "auto"` = OpenClaw decide qué comandos ejecutar como nativos.
  - `nativeSkills: "auto"` = skills se cargan automáticamente.
  - `restart: true` = permite reiniciar el gateway desde chat.
  - `ownerDisplay: "raw"` = muestra el owner raw en lugar de formateado.

**Estado:** Funcional.

**útil para IMPKT:** No directamente. En Claude Code los comandos slash y skills se manejan diferente.

---

## approvals

```json
"exec": { "enabled": false }
```

- Qué es: Approval workflow para ejecución de comandos.
- Qué hace: Si `enabled: true`, cada ejecución requiere approval de Gabriel antes de ejecutarse.
- Funciona: Configurado en `false` (deshabilitado) — ejecución libre.
- útil para IMPKT: Depende. Para IMPKT en producción, quizás wanting approval en ciertos comandos sensibles. En Claude Code se configura con `permissions` en settings.json.
- Cómo replicar: En settings.json de Claude Code: `permissions: { allowDangerous: false }` para mode estricto.

---

## session

```json
"dmScope": "main",
"reset": { "idleMinutes": 60 },
"maintenance": { "mode": "enforce", "pruneAfter": "14d" }
```

- Qué es: Configuración de sesiones y mantenimiento.
- Qué hace:
  - `dmScope: "main"` = DMs van al agente main.
  - `idleMinutes: 60` = reset de sesión después de 60 min sin actividad.
  - `pruneAfter: "14d"` = datos de sesión se podan después de 14 días.

**Estado:** Funcional.

**útil para IMPKT:** Sí. El prune de 14 días es buena práctica. En Claude Code, session management es diferente — la continuidad se maneja con `system/state.md`.

---

## hooks

```json
"internal": {
  "enabled": true,
  "entries": {
    "command-logger": { "enabled": true },
    "session-memory": { "enabled": true }
  }
}
```

- Qué es: Sistema de hooks internos para automatización.
- Qué hace:
  - `command-logger`: registra cada comando ejecutado.
  - `session-memory`: guarda estado de sesión automáticamente.

**Estado:** Funcional.

**útil para IMPKT:** SÍ. Los hooks son una de las features más valiosas de OpenClaw. En Claude Code, esto se replica con `PreToolUse` hooks en settings.json:

```json
"hooks": {
  "PreToolUse": [
    { "name": "command-logger", "prompt": "..." },
    { "name": "session-memory", "prompt": "..." }
  ]
}
```

Ver `useful-assets.md` para detalle completo.

---

## channels

```json
"defaults": {
  "heartbeat": { "showOk": false, "showAlerts": true, "useIndicator": true }
},
"channels": {
  "telegram": {
    "enabled": true,
    "dmPolicy": "pairing",
    "botToken": "8689877980:AAFlNoZdK9uOLnxnfl6ME6uF2q4Q-Rr5Ceg",
    "allowFrom": [7069567895],
    "groupPolicy": "allowlist",
    "streaming": { "mode": "partial" }
  }
}
```

- Qué es: Configuración de canales de comunicación.
- Qué hace: Conecta OpenClaw al bot de Telegram de Jarvis (@Jarvis_OpenclawV1_Bot). Solo Gabriel (ID: 7069567895) puede interactuar.

**Estado:** Funcional. Último component activo de OpenClaw.

**útil para IMPKT:** SÍ. OpenClaw se mantiene como bot de Telegram para IMPKT. Es lo único que se preserva de OpenClaw en el nuevo sistema.

**Cómo replicar:** Mantener la config de Telegram. En Antigravity, Claude Code puede integrarse con Telegram via MCP o scripts.

---

## gateway

```json
"port": 18789,
"mode": "local",
"bind": "lan",
"controlUi": { ... },
"auth": { "mode": "token", "token": "BA5C784EE6DF..." },
"tailscale": { "mode": "off" },
"nodes": { "denyCommands": [] }
```

- Qué es: Configuración del gateway HTTP de OpenClaw.
- Qué hace: Expone una UI de control y API en el puerto 18789. Token de auth para seguridad. Permite connections desde la LAN.

**Estado:** Funcional. Puerto 18789 activo.

**útil para IMPKT:** No. Claude Code no tiene gateway separado — es CLI nativo. El token de gateway es información útil para debug pero no se replica.

---

## plugins

```json
"allow": ["openclaw-web-search", "telegram", "perplexity", "minimax", "openrouter", "anthropic", "browser"],
"entries": { ... },
"installs": { ... }
```

- Qué es: Sistema de plugins de OpenClaw.
- Qué hace: Habilita integración con servicios externos (web search, Telegram, providers de IA, browser).

**Plugins instalados:**
- `openclaw-web-search` (@ollama/openclaw-web-search@0.2.2) — instalado desde npm

**有用:** El concepto de plugins es útil. En Claude Code, esto se replica con MCP servers y npm packages. No hay sistema de plugins equivalente — se usa npm global o local.

---

## Secciones ausentes (fueron removidas)

Las siguientes secciones YA NO EXISTEN en el archivo actual (12KB) pero estaban en versiones anteriores (28KB):

- `identity` — identidad del sistema (nombre, emoji, avatar)
- `flows` — flujos de automation (probablemente eliminados o movidos)
- `subagents` — sub-agentes adicionales
- `tasks` — sistema de tareas
- `sandbox` — configuración de sandbox (global)
- `media` — configuración de media
- `logs` — configuración de logging

**Nota:** El achicamiento de 28KB a 12KB es sospechoso. Estas secciones no fueron simplemente vaciadas — fueron eliminadas. Ver `problems-found.md`.

---

## Resumen de utilidad por sección

| Sección | Funciona | útil para IMPKT | Cómo replicar |
|---------|----------|-----------------|---------------|
| meta | Sí | No | Git versioning |
| env | Sí | No (seguro) | Variables de sesión Antigravity |
| wizard | Sí | No | MCP diagnostics |
| browser | Parcial | No | Browser agent nativo Antigravity |
| auth | Sí | No | N/A |
| models | Sí | **SÍ** | Variables de entorno + settings.json |
| agents | Parcial | **SÍ** | Claude Code Agent Teams |
| tools | Sí | No | Claude Code tools |
| commands | Sí | No | Slash commands nativos |
| approvals | Sí | Depende | settings.json permissions |
| session | Sí | **SÍ** | system/state.md |
| hooks | Sí | **SÍ** | PreToolUse hooks en settings.json |
| channels | Sí | **SÍ** | Mantener Telegram, integrar con Claude Code |
| gateway | Sí | No | N/A (CLI nativo) |
| plugins | Sí | No | MCP servers |