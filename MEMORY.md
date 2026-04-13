# MEMORY.md — Estado del negocio IMPKT

**Última actualización:** 2026-04-12
**Fase del negocio:** Phase 0 — Fundaciones

## Quién es Gabriel

- Gabriel Martinez, Ciudad Apodaca, México
- 3 agencias planeadas: Software/Marketing Digital (IMPKT), Créditos/Finanzas, Bienes Raíces
- Trabaja con OpenClaw como "Jarvis" (cerebro estratégico)
- Quiere: 3 negocios autónomos pasivos en etapa 4

## IMPKT — Agencia actual

**Servicios (11):**
- Landing Page ($5k setup / $2.5k mensual)
- Sitio Corporativo ($9k / $4.5k)
- E-commerce ($12k / $6k)
- SEO Local ($12k / $6k, mín 3 meses)
- Social Media ($10k / $5k)
- Campañas Outreach ($24k / $12k)
- WhatsApp Automation ($6k / $3k)
- Email Automation ($5k / $2.5k)
- CRM Setup ($5k one-time)
- Diagnóstico Express ($2.5k one-time)
- Mentoría Mensual ($6k/mes)

**ICP:** PyMEs 5-100 empleados en México, operación física establecida, presencia digital débil

**Regla de pricing:** Setup = 100-150% del mensual

## Arquitectura de agentes

```
Gabriel
  └─→ Mila (MARKETING) → Lena (OUTREACH) → Sofia (SALES) → Finn (PRODUCTION) → Nova (CLIENT COMMS)
```

- Cada lead tiene su propio directorio en `agents/[lead]/[role]/SOUL.md`
- Pipeline de comunicación en `pipeline/[from]-to-[to]/`
- Memoria en capas: CONTEXT.md → MEMORY.md → `memory/YYYY-MM-DD.md`

## Estado de herramientas

| Herramienta | Estado | Notes |
|---|---|---|
| Claude Code | ✅ Funcional | v2.1.104 |
| MiniMax M2.7 | ✅ Configurado | ANTHROPIC_BASE_URL corregido |
| Graphify | ✅ Funcional | Hook activo, grafo de 68 nodos |
| Obsidian | ✅ Vault conectado | Raíz impkt como vault |
| Festival | ✅ Replicado manualmente | `system/festival/` |
| RUFLO | ✅ Instalado | v3.5.80 |
| OpenClaw | ✅ Solo Telegram | Ya no es executor |

## Pipeline actual

Vacío — no hay clientes aún. Phase 0.

## Tareas pendientes (Festival)

1.1.5 — Scheduled tasks para heartbeat
1.2 — Sistema de memoria en capas
1.3 — Graphify completo
2-6 — Resto de fases de migración

## Métricas (cuando haya operación)

- Leads generados / semana
- Tasa de conversión (lead → client)
- Revenue mensual
- NPS de clientes
- Proyectos completados a tiempo