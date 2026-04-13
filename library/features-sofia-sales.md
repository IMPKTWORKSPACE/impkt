# Features para SOFIA — Sales

**Fecha:** 2026-04-13
**Agente:** Sofia (SALES)

---

## Generador de propuestas PDF

**CRITICO.** Se construira en FASE 5 como `tools/proposal-generator/`

**Funcionalidades requeridas:**
- Input: nombre cliente, servicios, datos de contacto
- Output: PDF profesional con branding IMPKT
- Secciones: portada, servicios, timeline, pricing, terminos, contacto
- NO mostrar precios unitarios del catalogo (precios personalizados por propuesta)
- Guardar en `projects/[cliente]/proposals/`

**Branding IMPKT:**
- Nombre: IMPKT
- Tagline: "Impacto medible, no promesas"
- Tono: Directo, profesional
- WhatsApp: 8115339022

---

## Calculator de pricing

**Regla de Gabriel:** Setup = 100-150% del mensual (incluye 1er mes)

**11 servicios:**

| Servicio | Setup | Mensual |
|----------|-------|---------|
| Landing Page | $5,000 | $2,500 |
| Sitio Corporativo | $9,000 | $4,500 |
| E-commerce | $12,000 | $6,000 |
| SEO Local | $12,000 | $6,000 |
| Social Media | $10,000 | $5,000 |
| Campanas Outreach | $24,000 | $12,000 |
| WhatsApp Automation | $6,000 | $3,000 |
| Email Automation | $5,000 | $2,500 |
| CRM Setup | $5,000 | N/A |

**Script:** Se construira en FASE 5 como parte de proposal-generator.

---

## Templates de propuestas

**Por tipo de servicio:**

1. **Landing Page** — propuesta corta (2 paginas)
2. **Sitio Corporativo** — propuesta media (4 paginas)
3. **SEO** — propuesta larga con milestones (6 paginas)
4. **Paquete completo** — propuesta premium con todos los servicios

**Templates:** Se construiran en FASE 5.

---

## Workflow de follow-up post-propuesta

**Sin herramienta especial.**

**Workflow propuesto:**
1. Sofia envia propuesta (Gabriel envia si es email, o se agenda reunion)
2. Esperar 3 dias → follow-up
3. Esperar 7 dias → segundo follow-up
4. Esperar 14 dias → oferta final o descarte

**Tracking:** En el archivo del prospecto en `pipeline/lena-sofia/`

---

## Integracion con pipeline

Sofia recibe de Lena y pasa a Finn.

**Archivo de transicion:** `pipeline/lena-to-sofia/[lead].md`
**Output:** `pipeline/sofia-to-finn/[deal].md`

**Formatos ya definidos en `plan/agent-teams.md`.**

---

## Resumen de installation para Sofia

| Accion | Prioridad | Nota |
|--------|-----------|------|
| proposal-generator tool | Critica | Construir en FASE 5 |
| Pricing calculator | Critica | Incluido en proposal-generator |
| Proposal templates | Critica | Construir en FASE 5 |
| Follow-up workflow | Media | Construir en FASE 5 |

---

## Dependencias pendientes

- **Ninguna** — Sofia puede funcionar completamente con las herramientas internas
- Cuando Gabriel tenga Stripe, se agrega integracion de pagos
