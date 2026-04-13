# Features para MILA — Marketing

**Fecha:** 2026-04-13
**Agente:** Mila (MARKETING)

---

## Web Search

**MiniMax M2.7:** El modelo base tiene capacidades de web search integradas.
Verificar si funciona en Claude Code con el provider actual.

**Test:**
```bash
claude -p "Busca las ultimas tendencias de marketing digital para PyMEs en Mexico 2026" --allowedTools Bash
```

Si no funciona, el fallback es curl a search engines publicos.

---

## Claude in Chrome

**Disponibilidad:** Requiere extension de Chrome de Anthropic.
**Verificacion:** Gabriel debe verificar si tiene la extension instalada en Chrome.

**Si existe:** Lena y Mila pueden usarlo para research de prospectos y competidores.
**Si NO existe:** Documentado en needs-gabriel.md.

---

## Computer Use

**Disponibilidad:** Feature avanzada de Anthropic. NO disponible en MiniMax M2.7.
Requiere Claude con capacidad de browser control.

**Verificado:** No disponible en el plan actual.

---

## Content Humanizer

**Problema:** Contenido generado por IA suena robotico.
**Solucion:** Se construira en FASE 5 como `tools/humanizer/`

Proceso:
1. Generar contenido con Mila
2. Pasar por humanizer
3. Output: contenido con tono IMPKT (directo, técnico, sin jerga)

---

## SEO Analysis

**Sin plugin oficial.** Opciones:
1. WebSearch con prompts estructurados para auditorias SEO basicas
2. Investigar si hay MCP de SEO en la comunidad
3. Construir workflow custom en FASE 5

**Lo que se puede hacer sin herramientas especiales:**
- Analisis de meta tags (leer HTML con curl)
- Verificar Google Business Profile via search
- Revisar keywords en contenido con Grep

---

## Social Media Content Generator

**Sin herramienta especial.** Mila genera contenido y usa templates.

**Templates a crear (en FASE 5):**
- Post para LinkedIn (por industria)
- Post para Instagram
- Thread para Twitter/X
- Email newsletter template

---

## Content Templates por Industria

Basado en el ICP de IMPKT (PyMEs 5-100 empleados en Mexico):

| Industria | Tono | Servicios relevantes |
|-----------|------|---------------------|
| Restaurantes | Casual-fino, experiencias | WhatsApp, Landing, SEO local |
| Clinicas | Profesional, confianza | Sitio corporativo, SEO, WhatsApp |
| Veterinarias | Cálido, familiar | Landing, Social media, SEO |
| Retail | Promocional, urgente | E-commerce, Campanas |
| Servicios B2B | Corporativo, ROI | Sitio corporativo, SEO, Outreach |

---

## Research de competidores

Mila necesita investigar a los competidores de cada prospecto.

**Workflow propuesto:**
1. `curl` al sitio del prospecto
2. WebSearch: "[industria del prospecto] Mexico servicios digitales"
3. Identificar que tienen y que les falta
4. Generar brief de oportunidades

---

## Resumen de installation para Mila

| Accion | Prioridad | Nota |
|--------|-----------|------|
| Verificar web search de MiniMax | Critica | Testear |
| Content humanizer | Critica | Construir en FASE 5 |
| SEO templates | Media | Construir en FASE 5 |
| Social media templates | Media | Construir en FASE 5 |
| Research workflow | Media | Construir en FASE 5 |
| Claude in Chrome extension | Baja | Si existe, usar |

---

## Dependencias pendientes

- Extension Claude in Chrome (verificar si Gabriel la tiene)
- Humanizer tool (FASE 5)
- Templates de contenido (FASE 5)
