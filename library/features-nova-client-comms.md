# Features para NOVA — Client Comms

**Fecha:** 2026-04-13
**Agente:** Nova (CLIENT COMMS)

---

## Sistema de tickets/issues

**Sin herramienta especial.** Proposal:

1. **Carpeta por cliente:** `clients/[cliente-slug]/`
2. **Archivo de issues:** `clients/[cliente-slug]/issues.md`
3. **Archivo de onboarding:** `clients/[cliente-slug]/onboarding.md`
4. **Archivo de metricas:** `clients/[cliente-slug]/metrics.md`

**Formatos a definir en FASE 5.**

---

## Templates de comunicacion post-entrega

**Templates necesarios:**
1. **Bienvenida:** Mensaje inicial post-entrega (WhatsApp)
2. **Reporte mensual:** Formato de reporte de metricas para cliente
3. **Renewal:** Mensaje de renovacion (30 dias antes del fin de contrato)
4. **Upsell:** Mensaje de expansion de servicios
5. **Churn prevention:** Mensaje cuando se detecta riesgo

**Construir en FASE 5 como parte de `tools/pipeline-manager/`.**

---

## Workflow de feedback collection

**Pregunta de feedback (30 dias post-entrega):**
```
"Como ha sido tu experiencia con [servicio]?
Del 1 al 10, que tan satisfecho estas?
Hay algo que podamos mejorar?"
```

**Template:** Se construira en FASE 5.

---

## Alertas de atencion

**Triggers para alertar a Gabriel:**

1. **Churn risk:** Cliente no ha renovado a 30 dias del fin de contrato
2. **Satisfaccion baja:** Feedback < 6/10
3. **Sin contacto:** 60 dias sin interaccion
4. **Issues tecnicos:** Mas de 3 issues abiertos en 30 dias

**Sistema:** `system/alerts/` para crear alertas.
Gabriel recibe notificacion via Telegram Director bot.

---

## Reportes de satisfaccion

**NPS score (Net Promoter Score):**
- Pregunta: "Del 0 al 10, que tan probable es que nos recomiendes?"
- 9-10: Promotor
- 7-8: Pasivo
- 0-6: Detractor

**Tracking:** En `clients/[cliente]/metrics.md`

---

## Resumen de installation para Nova

| Accion | Prioridad | Nota |
|--------|-----------|------|
| Client folder structure | Critica | Construir en FASE 5 |
| Templates de comunicacion | Critica | Construir en FASE 5 |
| Feedback collection template | Media | Construir en FASE 5 |
| Alertas de churn | Media | Construir en FASE 5 |
| NPS tracking | Media | Construir en FASE 5 |

---

## Dependencias pendientes

- Ninguna — Nova funciona completamente con filesystem
- Cuando se implemente WhatsApp Business, se conecta para mensajes automaticos
