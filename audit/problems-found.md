# Problemas Encontrados — OpenClaw

## Problema 1: openclaw.json reducido de 28KB a 12KB

**Gravedad:** ALTA — Señal不透

**Qué pasó:**
- El archivo `openclaw.json` era de ~28KB en versiones anteriores
- El archivo actual (2026.4.9) mide ~12KB
- Se eliminaron secciones enteras, no solo se vaciaron

**Secciones que YA NO EXISTEN:**
- `identity` — identidad del sistema
- `flows` — flujos de automation
- `subagents` — sub-agentes adicionales
- `tasks` — sistema de tareas
- `sandbox` — configuración global de sandbox
- `media` — configuración de media
- `logs` — configuración de logging

**Teorías:**
1. **Wizard de cleanup:** El `openclaw doctor` o `wizard` pudo haber hecho un cleanup agresivo de secciones no usadas
2. **Migración incompleta:** Algo o alguien removió secciones que se consideraban obsoletas sin documentar por qué
3. **Fallo de sync:** El archivo fue sobrescrito parcialmente durante una actualización

**Impacto:**
- Se perdió la config de `identity` (nombre, emoji, avatar del sistema)
- Se perdió el sistema de `flows` de automation
- Se perdió el tracking de `tasks`
- La sección `sandbox` ya no existe (ahora sandbox es por agente, no global)

**Recomendación:** Investigar si estas secciones están en un backup. Verificar qué pasó con `identity` en particular.

---

## Problema 2: Cron Jobs DESHABILITADOS

**Gravedad:** ALTA

**Estado actual de los 3 cron jobs:**

| Job | Schedule | Estado | Last Run | Error |
|-----|----------|--------|----------|-------|
| Context Rollover | 0 0 * * * | **DISABLED** | 1775714480266 (skipped) | disabled |
| Health Check | 0 * * * * | **DISABLED** | 1775757600033 (error) | timeout |
| Auto Task Generator | 0 21 * * * | **DISABLED** | 1775712592328 (error) | timeout |

**Health Check error:**
```
lastError: "Request timed out before a response was generated.
Please try again, or increase `agents.defaults.timeoutSeconds` in your config."
consecutiveErrors: 3
```

**Auto Task Generator error:**
```
lastError: Same timeout error
consecutiveErrors: 4
```

**Contexto:** Los jobs fueron deshabilitados manualmente después de múltiples errores de timeout. Esto deja a OpenClaw sin motor de automatización — funciona solo cuando Gabriel le habla.

**Impacto:**
- Sin heartbeats automáticos
- Sin context rollover nocturno
- Sin generación automática de tareas
- Sin health checks

**Esto explica por qué IMPKT tiene 0 clientes y 0 revenue** — el sistema no trabaja cuando Gabriel no está interactuando.

---

## Problema 3: Memory Compaction en false

**Gravedad:** MEDIA

**Verificando config:**
```json
"compaction": {
  "mode": "safeguard",
  "reserveTokens": 20000,
  "keepRecentTokens": 25000,
  "memoryFlush": {
    "enabled": true,
    "softThresholdTokens": 4000
  }
}
```

**Espera — esto dice `enabled: true`**

Revisando de nuevo el openclaw.json original... no, `memoryFlush.enabled` está en `true`. Pero en `defaults.sandbox` el modo es `off`.

El problema no es compaction — es que **memorySearch está deshabilitado:**
```json
"memorySearch": {
  "enabled": false,
  "provider": "gemini"
}
```

**Impacto:** No hay búsqueda semántica en memoria. El agente no puede encontrar información relevante sin buscar manualmente en archivos.

**Recomendación:** Habilitar `memorySearch` o decidir que el sistema de archivos (CONTEXT.md, MEMORY.md) es suficiente para el caso de uso de IMPKT.

---

## Problema 4: Agentes Huérfanos

**Gravedad:** MEDIA

### Agentes en openclaw.json pero sin uso (MEMORY.md los marca para eliminar):

| ID | Nombre | Workspace | Razón |
|----|--------|-----------|-------|
| mc-c57f7e3f | Client Comms Lead | workspace-mc-c57f7e3f | Versión vieja, Mila la reemplazó en MC |
| mc-52c78d33 | Outreach Lead | workspace-mc-52c78d33 | Versión vieja, Lena la reemplazó |
| mc-0b90aca2 | Production Lead | workspace-mc-0b90aca2 | Versión vieja, Finn la reemplazó |
| mc-8b12584e | Sales Pipeline Lead | workspace-mc-8b12584e | Versión vieja, Sofia la reemplazó |

### Agentes en filesystem pero NO en openclaw.json:

| Directorio | Nombre | Razón |
|------------|--------|-------|
| mc-gateway-6dad1190 | (sin nombre) | Creado y nunca dado de alta en config |
| mc-297b86b5 | (sin nombre) | Creado y nunca dado de alta en config |

### Agentes referenciados en MEMORY.md pero no en openclaw.json:

| ID | Nombre | Razón |
|----|--------|-------|
| lead-dd86bb76 | Mila | Existe en Mission Control (docker) pero no en openclaw.json |
| lead-d5048423 | Sofia | Existe en Mission Control (docker) pero no en openclaw.json |

**Total de inconsistency:** 6 entradas huérfanas o desincronizadas.

**Impacto:**
- Configuración confusa
- Posibles conflictos si se reactivan sin cleanup
- Dificultad para mantener el sistema

**Recomendación:** Limpiar en la siguiente sesión con Gabriel — eliminar dirs de agentes huérfanos y actualizar openclaw.json.

---

## Problema 5: Mission Control Backend — ¿Funcionando?

**Gravedad:** MEDIA

**Datos:**
- Backend corre en docker (contenedor)
- Puerto 8000 para API, puerto 3000 para frontend
- Token: `20NKqtSiwY435RhfcBFzXjeJVaDsL8Q9gdPHUAuxTbWvEl17yGopIrkn6OMCmZ`
- MEMORY.md dice: "✅ Conectado (docker local)"

**Però:**
- Los cron jobs que dependen de Mission Control dan timeout
- Los MC gateway agents (mc-gateway-8f6ce89e, mc-gateway-cc9bd917) están declarados en openclaw.json
- No hay evidencia de que los gateway agents estén comunicándose exitosamente con MC

**Análisis:**
- El frontend (React) podría estar funcionando pero la API podría tener problemas
- O los gateway agents no están haciendo nada (solo declarados, no activos)
- O el timeout es del modelo (MiniMax M2.7) no del backend

**Recomendación:** Verificar manualmente:
1. `docker ps` —ver si el contenedor está corriendo
2. `curl http://localhost:8000/api/system/health` —ver si la API responde
3. Revisar logs del contenedor MC

---

## Problema 6: BrowserBase CDP No Responde

**Gravedad:** BAJA (para IMPKT — se usa browser agent nativo de Antigravity)

**Config:**
```json
"browser": {
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
}
```

**MEMORY.md dice:**
```
Browserbase | ⚠️ CDP no responde
```

**Impacto:** Automatización de browser via BrowserBase no funciona. Pero para IMPKT esto es irrelevante — Antigravity tiene su propio browser agent (Chromium headless).

---

## Problema 7: glm-5:cloud Deprecado

**Gravedad:** BAJA

**En openclaw.json, provider ollama:**
```json
{
  "id": "glm-5:cloud",
  "name": "glm-5:cloud",
  "reasoning": true,
  "input": ["text"],
  "cost": { "input": 0, "output": 0, ... },
  "contextWindow": 202752
}
```

**TOOLS.md dice:**
```
glm-5:cloud | Ollama Cloud | **DEPRECATED** | —
```

**Impacto:**
- Modelo declarado en config pero no se usa
- No genera errores, solo confusión
- Posible confusión si alguien intenta usar este modelo

---

## Resumen de Problemas

| # | Problema | Gravedad | Acción inmediata |
|---|----------|----------|------------------|
| 1 | openclaw.json reducido de 28KB a 12KB | ALTA | Investigar backup, documentar pérdida |
| 2 | Cron jobs deshabilitados | ALTA | Habilitarlos o reemplazar con Claude Code scheduler |
| 3 | memorySearch deshabilitado | MEDIA | Decidir si se necesita o no |
| 4 | 6 agentes huérfanos | MEDIA | Limpiar en siguiente sesión con Gabriel |
| 5 | MC backend — status incierto | MEDIA | Verificar con `docker ps` y curl |
| 6 | BrowserBase CDP no responde | BAJA | No relevante para IMPKT |
| 7 | glm-5:cloud deprecated | BAJA | Limpiar en config |