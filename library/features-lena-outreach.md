# Features para LENA — Outreach

**Fecha:** 2026-04-13
**Agente:** Lena (OUTREACH)

---

## Web Search

Mismo que Mila — para investigar prospectos antes del contacto.

---

## Claude in Chrome

Si existe (verificado por Mila), usar para:
- Navegar perfil de LinkedIn del prospecto
- Ver sitio web de la empresa
- Revisar reseñas de Google

---

## Templates de contacto por canal

**3 canales:**
1. **WhatsApp** — mensaje inicial corto, follow-up
2. **Email** — mensaje formal (SIN email automatizado por ahora)
3. **LinkedIn DM** — mensaje directo a decision maker

**NOTA CRITICA:** Gabriel NO tiene servicio de email profesional.
Lena NO puede enviar emails automatizados.

**Solucion temporal:**
- Lena genera los drafts de email
- Gabriel los copia y los envia manualmente desde su cuenta personal
- Una vez que Gabriel configure Resend/SendGrid, Lena automatiza

---

## Sistema de follow-up

**Sin herramienta especial.** Lena usa:
- `system/alerts/` para crear alertas de follow-up
- Pipeline filesystem para tracking de prospectos
- Scheduled tasks (si disponible) para recordatorios

**Workflow propuesto:**
1. Lena contacta prospecto
2. Si no responde en 48h → crear alerta en `system/alerts/followup-[prospecto].md`
3. Si no responde en 7 dias → agendar re-contacto en 30 dias
4. Si no responde en 3 intentos → mover a archive

---

## Lead Scoring

**Criterios para calificar prospectos:**

| Criterio | Peso | Pregunta |
|----------|------|----------|
| Tamano | 20% | 5-100 empleados? |
| Operacion digital | 20% | Tienen sitio web, redes, presencia online? |
| Problema claro | 25% | Puedo identificar que les falta? |
| Budget visible | 20% | Hay senales de que pueden pagar? |
| Timeline | 15% | Necesidad inmediata o a futuro? |

**Score:** 1-10 por criterio, ponderado.

---

## CRM en filesystem

**Ya existe:** `pipeline/` con 6 etapas.

**Lo que falta (FASE 5):**
- `tools/pipeline-manager/` — scripts para mover leads
- Templates de archivos de lead por etapa
- Tracking de timestamps y notas

---

## Resumen de installation para Lena

| Accion | Prioridad | Nota |
|--------|-----------|------|
| Templates de mensaje por canal | Critica | Construir en FASE 5 |
| Workflow de follow-up | Critica | Construir en FASE 5 |
| Lead scoring | Media | Construir en FASE 5 |
| Pipeline manager scripts | Media | Construir en FASE 5 |
| Web search | Critica | Compartido con Mila |
| Claude in Chrome | Media | Si existe |

---

## Dependencias pendientes

- **Email profesional (Resend/SendGrid):** CRITICO para automatizacion de outreach
  - Documentado en needs-gabriel.md
  - Gabriel debe activar cuenta
- Claude in Chrome extension (verificar con Gabriel)
