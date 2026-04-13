# Ideas Repository — Reglas

## Flujo

```
Gabriel deposita material
    → ideas/inbox/
    → [process-ideas.py] detecta, procesa, evalua
    → ideas/approved/  (si pasa umbrales)
    → ideas/discarded/ (si no pasa)
    → ideas/implemented/ (cuando se completa)
```

## Scoring

| Score | Significado |
|-------|-------------|
| Relevancia 6+ | Relevante para IMPKT/PyMEs Mexico |
| Implementabilidad 5+ | Factible en Antigravity |
| ROI 6+ | Vale la pena el esfuerzo |

**Aprobacion automatica:** (relevancia + roi) / 2 >= 7

## Tags y Leads

| Tag | Lead asignado |
|-----|--------------|
| marketing | Mila |
| sales | Sofia |
| automation | Finn |
| web | Finn |
| ai | Finn |
| productividad | Nova |
| mexico | Lena |

## Formatos aceptados

- URL (una linea en archivo .txt)
- Texto plano
- Articulos copiados

## Formatos NO aceptados

- Archivos binarios
- URLs que requieren login

## Processor

Se ejecuta cada 10 minutos via cron. Tambien se puede correr manualmente:

```bash
python ideas/process-ideas.py
```

## Index

`ideas/index.md` se actualiza automaticamente. Muestra:
- Ideas aprobadas recientes
- Ideas descartadas recientes
- Stats globales

## conexion con bot

El bot `@impkt_ideas_bot` permite:
- `/idea [url]` — agregar idea desde URL
- `/status` — ver stats
- `/approved` — listar aprobadas
- `/discard [id]` — descartar idea
- `/approve [id]` — aprobar idea manualmente

## Decisiones que SOLO Gabriel toma

- Aprobar ideas con ROI bajo pero valor estrategico
- Descartar ideas con score alto
- Cambiar lead asignado
- Modificar umbrales de scoring
