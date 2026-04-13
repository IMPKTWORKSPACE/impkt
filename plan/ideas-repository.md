# Repositorio de Ideas — IMPKT

## ¿Qué es el Repositorio de Ideas?

El Repositorio de Ideas es el sistema de captura y procesamiento de material externo que alimenta la operación de IMPKT. Es el lugar donde Gabriel deposita cualquier cosa que encuentra útil — artículos, videos, repositorios, enlaces, ideas sueltas — y el sistema se encarga de evaluarlo, decidir si es relevante, planear la implementación y convertirlo en trabajo ejecutable.

El objetivo es que Gabriel nunca tenga que pensar en clasificar o dar seguimiento a una idea. Deposita, y el sistema hace el resto.

---

## Arquitectura del repositorio

```
impkt/
├── ideas/
│   ├── inbox/              # Material sin procesar (Gabriel deposita aquí)
│   ├── processing/         # En evaluación por el sistema
│   ├── approved/           # Aprobadas para implementar
│   ├── implemented/        # Ya implementadas
│   ├── discarded/          # Descartadas con justificación
│   └── index.md            # Índice con estado de cada idea
```

Estado actual de directorios: creados (vacíos).

---

## Flujo completo de una idea

### Fase 1: Inbox (Gabriel)

Gabriel deposita material en `ideas/inbox/` sin formato específico. Formatos soportados:

- URLs escritas en un archivo `.md` o `.txt` (una por línea o una por archivo)
- Archivos `.md` con contenido copiado/pegado
- Archivos `.pdf` (el sistema extrae texto)
- Archivos `.txt` con texto libre
- Enlaces a repositorios de GitHub u otras plataformas

Regla: un archivo o enlace por entrada. Si Gabriel quiere compartir tres artículos, hace tres archivos en inbox.

### Fase 2: Detección (sistema automático)

El sistema detecta nuevo material en inbox mediante un scheduled task que corre cada 15 minutos (o manualmente cuando Gabriel lo active).

Al detectar nuevo material:
1. Genera timestamp de entrada
2. Crea un archivo de trabajo en `ideas/processing/` con naming convention `idea-YYYYMMDD-HHMMSS-slug.md`
3. Registra la idea en `ideas/index.md` con estado `processing`

### Fase 3: Extracción (sistema automático)

Para cada idea en processing, el sistema ejecuta:

**URL:**
- Usa WebFetch para obtener el contenido
- Parsea título, descripción, contenido principal
- Detecta si es un video (YouTube, Vimeo) y si tiene transcript disponible
- Si es un repo de GitHub: extrae README, tecnologías usadas, estructura

**Archivo local (.md, .txt, .pdf):**
- Lee el contenido directamente del filesystem
- PDF: extracción de texto plano (limitado a texto extraíble, no OCR)

**Video (con URL de plataforma con transcript):**
- YouTube: intenta obtener transcript via ytdl-org/pytube o servicio externo
- Si no hay transcript disponible: marca como `sin-transcripcion` y usa título/descripción únicamente

El resultado de la extracción se escribe en la sección `## Material` del archivo de idea.

### Fase 4: Evaluación (sistema automático)

Con el contenido extraído, el sistema evalúa usando prompts estructurados. Cada dimensión scoring 1-10:

| Dimensión | Pregunta que responde |
|---|---|
| **Relevancia** | ¿Qué tan directamente aplica a PyMEs en México con 5-100 empleados? |
| **Implementabilidad** | ¿Qué tan rápido puede IMPKT implementar esto con las herramientas actuales? |
| **ROI** | ¿Aporta ingresos, eficiencia o capacidad diferenciada a la agencia? |
| **Diferenciación** | ¿Nos da ventaja competitiva frente a otras agencias digitales en México? |

Criterios adicionales que pueden sumar puntos:
- Complementa alguno de los 5 leads (Mila, Lena, Sofia, Finn, Nova)
- Conecta con alguno de los 11 servicios de IMPKT
- Automatiza un proceso que Gabriel hace manualmente hoy
- Genera contenido o activos reutilizables

Criterios que restan puntos:
- Requiere tecnología incompatible con el stack actual
- Solo aplica a empresas grandes (enterprise), no a PyMEs
- No tiene forma de medirse (contradice la promesa de IMPKT)

### Fase 5a: Aprobación (si scoring >= 7 en al menos 3 dimensiones y promedio >= 7)

El sistema:
1. Mueve el archivo de `processing/` a `approved/`
2. Completa el frontmatter con scores y estado
3. Escribe la sección `## Plan de implementación` con pasos concretos
4. Identifica al lead responsable (Mila/Lena/Sofia/Finn/Nova)
5. Crea una task de Festival correspondiente
6. Actualiza `index.md`

### Fase 5b: Descarte (si scoring < 7)

El sistema:
1. Mueve el archivo de `processing/` a `discarded/`
2. Completa el frontmatter con scores, estado y justificación de descarte
3. Actualiza `index.md`

### Fase 6: Implementación

La task de Festival asociada se ejecuta por el lead asignado. Al completarse:
1. El lead mueve el archivo de `approved/` a `implemented/`
2. Documenta el resultado: qué se implementó, qué se aprendió, qué se rechazó del plan original
3. Actualiza `index.md`

---

## Formato de cada idea

Cada archivo de idea sigue esta estructura exacta:

```markdown
---
id: idea-2026-04-12-001
fecha: 2026-04-12
fecha-ingreso: 2026-04-12T10:30:00
fuente: https://articulo-o-video-url.com
tipo: url | archivo | repo
tags: [marketing, automation, seo, sales, web]
lead: Mila | Lena | Sofia | Finn | Nova
relevancia: 8
implementabilidad: 6
roi: 7
diferenciacion: 7
promedio: 7.0
estado: processing | approved | implemented | discarded
justificacion-descarte: null | "texto si fue descartada"
---

## Resumen

[Resumen en 3 oraciones extraído del contenido original]

## Material

[Contenido extraído: texto del artículo, transcript, README del repo]

## Por qué es útil para IMPKT

[Análisis del sistema: qué aporta, a quién le sirve, cómo conecta con los servicios]

## Plan de implementación

[Pasos específicos y concretos, numerados, ejecutables por el lead asignado]

## Asignado a

[Lead responsable] — [razón por la que se le asigna a ese lead]

## Resultado de implementación

[Completado por el lead al terminar — qué se hizo, qué se aprendió, enlaces a activos]
```

---

## Index.md — Estado global

Ubicación: `ideas/index.md`

```markdown
# Ideas Repository — IMPKT

## Stats

| Métrica | Cantidad |
|---|---|
| Total recibidas | 24 |
| Procesando | 2 |
| Aprobadas | 8 |
| Implementadas | 10 |
| Descartadas | 4 |

## Ideas activas (approved + processing)

| ID | Fecha | Lead | Tags | Promedio | Estado |
|---|---|---|---|---|---|
| idea-2026-04-12-001 | 2026-04-12 | Mila | [seo, content] | 7.8 | approved |
| idea-2026-04-12-002 | 2026-04-12 | Finn | [automation, whatsapp] | 7.2 | processing |

## Ideas recientes (últimas 5)

### idea-2026-04-12-001 — approved
**Fuente:** https://articulo-sobre-seo-local...
**Resumen:** Caso de estudio sobre estrategia SEO para consultorios médicos...
**Lead:** Mila | **Tags:** seo, content | **Promedio:** 7.8

### idea-2026-04-12-002 — processing
**Fuente:** repo-de-github/automacion-whatsapp...
**Resumen:** Repo con template de bots de WhatsApp usando...
**Lead:** Finn | **Tags:** automation, whatsapp | **Promedio:** 7.2

---

## Ideas implementadas (últimas 3)

- idea-2026-03-15-003 — Sistema de scoring de leads (Lena, 2026-03-20)
- idea-2026-03-10-001 — Templates de email outreach automatizado (Sofia, 2026-03-18)
- idea-2026-02-28-002 — Dashboard de métricas para clientes IMPKT (Finn, 2026-03-05)
```

---

## Implementación técnica

### Detección de nuevo material

**Opción elegida: Scheduled task con polling cada 15 minutos**

Se configura via CronCreate:
```
cron: */15 * * * *
prompt: Revisa ideas/inbox/ por nuevo material. Si hay archivos nuevos, ejecuta el flujo de procesamiento completo (extracción → evaluación → aprobación/descarte → actualización de index.md).
recurring: true
```

**Alternativa manual:** Gabriel puede escribir `procesar ideas` y el sistema ejecuta inmediatamente sin esperar el siguiente polling.

**Alternativa considerada y descartada: Git hook**
- Requiere que Gabriel haga git add + commit por cada archivo depositado
- Falla si Gabriel arrastra archivos por GUI
- No hay forma de rastrear URLs copiadas en archivos .txt

### Extracción de contenido

| Tipo | Herramienta | Estado |
|---|---|---|
| URL genérica | WebFetch | Funcional |
| Repo de GitHub | gh api + WebFetch del README | Funcional |
| Video YouTube | Transcript via ytdl-org (pendiente) | Pendiente |
| Archivo .md/.txt | Read tool | Funcional |
| Archivo .pdf | PdfReader en Python (pendiente) | Pendiente |

**Nota sobre video:** La extracción de transcript de video requiere resolver la integración con Whisper o un servicio de transcription. Esto se marca como feature pendiente en la fase de implementación.

### Evaluación automática

La evaluación usa el modelo activo (MiniMax M2.7 o Claude según disponibilidad) con un prompt estructurado que pide los cuatro scores y el análisis. Prompt típico:

```
Evalúa la siguiente idea para IMPKT, agencia digital para PyMEs en México.
Servicio: [lista de 11 servicios]
Leads: Mila (marketing), Lena (outreach), Sofia (sales), Finn (production), Nova (client comms)
ICP: PyMEs 5-100 empleados, México, presencia digital débil

[contenido extraído]

Devuelve: relevancia (1-10), implementabilidad (1-10), roi (1-10), diferenciacion (1-10),
promedio, lead asignado, razón de asignación, por qué es útil, plan de implementación
```

### Actualización del index

Cada fase del flujo termina actualizando `index.md` de forma atómica:
1. Leer index.md actual
2. Modificar en memoria
3. Escribir index.md de vuelta

Para evitar race conditions si el scheduled task corre重叠 con una ejecución manual, se usa un archivo de lock: `.processing-lock` creado al inicio y eliminado al final.

---

## Responsabilidades de Gabriel

| Acción | Frecuencia | Tipo |
|---|---|---|
| Depositar material en `ideas/inbox/` | Cuando encuentre algo útil | Manual |
| Revisar ideas aprobadas en `ideas/approved/` | Semanal | Manual |
| Revisar implementación terminada en `ideas/implemented/` | Semanal | Manual |
| Aprobar implementación de ideas de alto impacto | Por notificación | Gate de aprobación |

**Gate de aprobación:** Ideas con `promedio >= 9` o que requieran inversión > $2,000 USD en herramientas/servicios requieren aprobación explícita de Gabriel antes de pasar a Festival. Las demás se ejecutan automáticamente.

---

## Rollos del sistema (automatizados)

1. **Detectar** nuevo material en inbox
2. **Extraer** contenido estructurado
3. **Evaluar** con scoring en 4 dimensiones
4. **Decidir** aprobar o descartar
5. **Planear** pasos de implementación si se aprueba
6. **Asignar** al lead correcto
7. **Crear** task en Festival
8. **Actualizar** index.md en cada paso
9. **Notificar** a Gabriel cuando hay ideas nuevas aprobadas (especialmente las que necesitan gate)

---

## Estado actual vs estado objetivo

| Componente | Estado actual | Estado objetivo |
|---|---|---|
| Estructura de carpetas `ideas/{inbox,processing,approved,implemented,discarded}` | Creada (vacía) | Funcional con contenido |
| `ideas/index.md` | No existe | Actualizado en cada ciclo |
| Flujo de procesamiento | No existe | Ejecutable automáticamente |
| Scheduled task de detección | No existe | Configurado, corriendo cada 15 min |
| Extracción de URLs | No existe | Funcional via WebFetch |
| Extracción de repos GitHub | No existe | Funcional via gh + WebFetch |
| Evaluación automática | No existe | Prompt estructurado funcional |
| Integración con Festival | No existe | Tasks creadas al aprobar |
| Gate de aprobación para ideas de alto impacto | No existe | Implementado con flag en frontmatter |
| Notificación a Gabriel (Telegram) | No existe | Mensaje en cada aprobación |

---

## Roadmap de implementación

### Fase 1: Fundamentos (semana 1)
- Crear `ideas/index.md` con estructura inicial
- Escribir script de procesamiento en Bash/Python que:
  - Detecta archivos nuevos en inbox
  - Extrae contenido de URLs con WebFetch
  - Genera el archivo de idea en processing/
- Configurar scheduled task de polling
- Probar con 3-5 ideas de ejemplo

### Fase 2: Evaluación (semana 2)
- Implementar prompt de evaluación estructurada
- Integrar scoring con 4 dimensiones
- Implementar decisión de aprobación/descarte
- Escribir justificación de descarte automáticamente

### Fase 3: Asignación y Festival (semana 3)
- Mapear cada idea aprobada a un lead (Mila/Lena/Sofia/Finn/Nova)
- Generar task de Festival automáticamente
- Actualizar index.md con estado
- Implementar gate de aprobación para alto impacto

### Fase 4: Notificación y refinamiento (semana 4)
- Conectar notificación a Gabriel por Telegram (canal ya existente de OpenClaw)
- Definir formato del mensaje de notificación
- Revisar falsos positivos/negativos del scoring
- Ajustar thresholds según retroalimentación de Gabriel

---

## Notas para Gabriel

- **No necesitas formatiar nada** antes de depositar. Un enlace, un copy-paste, un PDF — el sistema se adapta.
- **Si algo se descarta**, puedes reclamar y pedir re-evaluación. Escribe `revisar idea [ID]` y el sistema la vuelve a evaluar con contexto adicional que tú le des.
- **Las ideas aprobadas no se implementan sin tu visto bueno** si son de alto impacto (score >= 9 o costo > $2,000). El sistema te notifica y espera.
- **Revisa el index.md semanalmente** — ahí está el resumen de todo lo que ha entrado, qué se hizo y qué se rechazó.
