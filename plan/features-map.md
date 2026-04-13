# features-map.md — Mapa de Features Nativas para IMPKT

**Fecha:** 2026-04-12
**Estado:** Documento de plan — requiere validación de Gabriel
**Base:** Auditoría completa de OpenClaw (`audit/verdict.md`) + evaluación de plataforma

---

## Features de Claude Code (el executor)

Claude Code es la CLI que corre dentro de Antigravity. Es el executor principal del sistema IMPKT.

---

### Core Tools

#### Read / Write / Edit / MultiEdit

**Descripcion:** Operaciones directas sobre el filesystem local.

| Operacion | Tool | Uso en IMPKT |
|-----------|------|-------------|
| Leer archivo completo o porcion | `Read` | Auditoria, review de configs, lectura de estado |
| Escribir archivo nuevo | `Write` | Crear artifacts, generar codigo, escribir resultados |
| Reemplazar texto exacto | `Edit` | Modificar configs, aplicar cambios puntuals |
| Reemplazo multiple | `MultiEdit` | Refactoring grande, remplace global |

**¿La necesitamos?** Sí — absoluto.
**Para que parte de IMPKT:** Todo el sistema opera sobre archivos. Finn (PRODUCTION) construye landing pages, sitios, automatizaciones. Mila (MARKETING) genera contenido. Nova (CLIENT COMMS) maneja documentación.
**Configuracion:** Ninguna — nativo de Claude Code. Solo seguir `token-rules.md` para no leer archivos completos innecesariamente.
**Limitaciones:** No hay sistema de locking — dos agentes escribiendo el mismo archivo es un problema. Regla: un solo agente por archivo a la vez.

---

#### Bash

**Descripcion:** Terminal bash completa via Git Bash (`C:\Program Files\Git\bin\bash.exe`). Ejecuta scripts, comandos de sistema, npm, git.

**¿La necesitamos?** Sí — absoluto.
**Para que parte de IMPKT:**
- Instalacion de dependencias (`npm install`, `npx ruflo@latest init`)
- Git operations (commits, pushes)
- Ejecucion de scripts de deployment (Vercel CLI, etc.)
- Ghost Runtime management (containers efimeros)
- Verificacion de estado del sistema

**Configuracion:**
```bash
# Verificar que bash funciona
bash --version

# Git ya inicializado en C:\Users\oscar\impkt
git status

# Para scripts .sh, usar bash no cmd
bash system/festival/impkt-migration/run.sh
```

**Limitaciones:**
- En Windows, `bash` es Git Bash — no es un Linux completo
- Docker no disponible (restringido por Antigravity sandboxing)
- Las variables de entorno NO persisten entre sesiones — configurar por sesion
- Sesiones largas pueden caer (~12h max) — guardar estado en disco antes de cada milestone

---

#### Glob / Grep

**Descripcion:** Busqueda de archivos por patron (`Glob`) y busqueda de contenido por regex (`Grep`).

**¿La necesitamos?** Sí — para navegacion y auditoria.
**Para que parte de IMPKT:**
- Encontrar archivos de configuracion (`.json`, `.md`)
- Buscar patterns en codigo (funciones, variables, imports)
- Auditoria de archivos del vault de OpenClaw
- Verificar existencia de archivos generados

**Configuracion:** Ninguna — nativos.
**Limitaciones:** `Glob` sobre `**/*.md` puede ser lento en vaults grandes de Obsidian. Usar `head_limit` en `Grep` para no saturar contexto.

---

#### WebFetch / WebSearch

**Descripcion:**
- `WebFetch`: GET a una URL, convierte HTML a markdown, procesa con modelo
- `WebSearch`: Busqueda web con modelo (usa la API del executor actual)

**¿La necesitamos?** Sí — para investigacion y validacion.
**Para que parte de IMPKT:**
- **Mila (MARKETING):** Investigar tendencias, analizar competencia, extraer informacion de paginas
- **Lena (OUTREACH):** Validar empresas objetivo, investigar prospectos
- **Finn (PRODUCTION):** Documentacion de APIs, verificar URLs de clientes
- **Repositorio de Ideas:** Extraer contenido de links depositados por Gabriel en `ideas/inbox/`

**Configuracion:**
- `WebFetch`: Solo requiere URL válida. No requiere API key adicional si ya funciona la conexion.
- `WebSearch`: Verificar que la API key de MiniMax soporta busqueda web o si se necesita Perplexity API separada.

**Limitaciones:**
- Autenticacion requerida para URLs privadas (Google Docs, Confluence, etc.)
- Rate limiting posible en busquedas frecuentes
- WebFetch sigue redirects pero informar si cambia de host

---

### Skills System

**Descripcion:** Un skill en Claude Code es un archivo `SKILL.md` que define comportamiento especializado del agente para una tarea especifica. Se invoca automaticamente cuando el tema coincide o manualmente via `/skill-name`.

**¿Como funciona un skill?**
1. El skill es un archivo `.md` con estructura definida: proposito, instrucciones, patterns, limites
2. Se coloca en un directorio reconocible por Claude Code (configurable en `settings.json`)
3. El agente lo detecta automaticamente o se invoca manualmente
4. El skill modifica el comportamiento del agente para esa tarea sin cambiar el modelo

**Skills que IMPKT YA tiene:**
```
C:\Users\oscar\impkt\tools\graphify\
  graphify-out/         # Output de la ultima ejecucion
  run-graphify.py       # Script de ejecucion
```

**Skills que IMPKT necesita crear:**

| Skill | Ubicacion | Proposito | Prioridad |
|-------|-----------|-----------|-----------|
| `coding-agent` | `skills/coding-agent.md` | Patrones de pair programming, PTY vs no-PTY, background execution | Alta |
| `self-improving` | `system/self-improving/SKILL.md` | Framework de mejora continua (migrado de OpenClaw asset #10) | Alta |
| `deployment` | `skills/deployment.md` | Despliegue a Vercel, verificacion post-deploy, rollback | Media |
| `content-generator` | `skills/content-generator.md` | Generacion de contenido de marketing (blog posts, social, SEO) | Media |
| `proposal-builder` | `skills/proposal-builder.md` | Construir propuestas comerciales automaticamente | Media |

**Configuracion del directorio de skills:**
```json
// En settings.json de Claude Code
{
  "skills": {
    "directories": [
      "C:/Users/oscar/impkt/skills",
      "C:/Users/oscar/impkt/system/self-improving"
    ]
  }
}
```

**Limitaciones:**
- Los skills no son agentes separados — viven dentro del contexto del agente activo
- No hay skill marketplace — todo es custom
- La deteccion automatica por tema puede fallar — verificar invocacion manual

---

### Hooks System

**Descripcion:** Los hooks permiten ejecutar prompts automaticos antes o despues del uso de tools. Se configuran en `settings.json`.

**¿Como funciona?**
```
Tool call → PreToolUse hook (prompt se ejecuta antes) → Tool ejecuta
Tool call → PostToolUse hook (prompt se ejecuta despues) → Tool resultado
```

**¿La necesitamos?** Sí — parcialmente.
**Para que parte de IMPKT:**
- **PreToolUse hook (ya tiene graphify):** Graphify está instalado como hook que corre antes de ciertas tools. Verificar estado actual.
- **PostToolUse hook (nuevo):** Logging automatico de cada operacion — equivalente al `command-logger` de OpenClaw.
- **Session-memory hook (nuevo):** Cada N tool calls, escribir resumen de contexto a `system/state.md` — evita perder estado entre sesiones.

**Configuracion propuesta para `settings.json`:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "graphify-check",
        "prompt": "Before using Read/Write/Edit on .md files in knowledge/, run: python C:/Users/oscar/impkt/tools/graphify/run-graphify.py. After the tool call, incorporate any new links found into the graph."
      }
    ],
    "PostToolUse": [
      {
        "name": "command-logger",
        "prompt": "After every Bash or Write tool call, append a one-line summary with timestamp to system/cache/command-log.md."
      },
      {
        "name": "session-memory",
        "prompt": "After every 10 tool calls, write current context summary to system/state.md: last action completed, next action pending, any errors encountered."
      }
    ]
  }
}
```

**Estado actual:** Graphify hook existe pero el estado de activacion es incierto — verificar con `mcp__ide__getDiagnostics` o revisando settings.json directamente.

**Limitaciones:**
- Hooks en `settings.json` requieren reinicio de sesion para activarse
- Si el prompt del hook es muy largo, consume tokens adicionales en cada tool call
- No hay hook nativo para "cada N minutos" — solo por tool calls

---

### MCP (Model Context Protocol)

**Descripcion:** Protocolo para conectar Claude Code con servidores externos que proveen tools o datos adicionales. Similar a un plugin system pero standarizado.

**¿Hay MCP servers configurados?** No hay evidencia de MCP servers activos en la configuracion actual de IMPKT. El vault de OpenClaw no tiene configuracion MCP documentada.

**MCP servers potenciales para IMPKT:**

| Server | Proposito | Viabilidad |
|--------|-----------|------------|
| **Obsidian MCP** | Leer/escribir notas de Obsidian directamente | Alta — Obsidian ya está instalado |
| **Filesystem MCP** | Acceso controlado a archivos fuera del workspace | Media — ya tenemos filesystem nativo |
| **GitHub MCP** | Issues, PRs, repositorios | Baja — IMPKT no usa GitHub para proyectos |
| **Slack/Discord MCP** | Notificaciones | Pendiente — segun necesidad de Gabriel |

**Obsidian como MCP server (prioridad media):**
- Obsidian tiene plugin oficial de MCP (`obsidian-mcp`)
- Permitiria a Claude Code leer/escribir notas de conocimiento directamente
- Requiere: instalar plugin en Obsidian + configurar `mcp_servers` en settings.json
- Beneficio: graphify ya hace link mapping — con MCP podriamos hacer mas

**Configuracion pendiente:**
```json
// En settings.json
{
  "mcpServers": {
    "obsidian": {
      "command": "obsidian-mcp",
      "args": ["--vault", "C:/Users/oscar/impkt"]
    }
  }
}
```

**Limitaciones:**
- Obsidian MCP plugin puede requerir configuracion adicional
- No todos los plugins de Obsidian son compatibles con MCP
- Cada MCP server adicional consume recursos

---

### Agent Teams

**Descripcion:** Sistema nativo de Claude Code para crear y orquestar multiples agentes que trabajan en paralelo o secuencia. Cada agente es una sesion con su propio contexto, y el lead agent los coordina.

**¿Como funciona?**
1. Un lead agent define tasks y las asigna a agents hijos
2. Los agents hijos operan en paralelo o secuencia
3. El lead agent agrega resultados y toma decisiones
4. Comunicacion entre agentes via mensajes o archivos compartidos

**Arquitectura de 5 leads (ya definida en CLAUDE.md):**

```
MARKETING (Mila)
  Responsabilidad: Genera leads, contenido, campañas, SEO
  Tareas tipo: Blog posts, social media, campañas outreach, SEO local
  Herramientas: WebSearch, content-generator skill, writing tools

OUTREACH (Lena)
  Responsabilidad: Primer contacto, calificación, discovery
  Tareas tipo: Research de prospectos, primers de contacto, qualification
  Herramientas: WebFetch, company research, email patterns

SALES (Sofia)
  Responsabilidad: Pre-deal, propuestas, pricing, cierre
  Tareas tipo: Proposals, pricing calculator, objection handling
  Herramientas: Proposal-builder skill, pricing rules de CLAUDE.md

PRODUCTION (Finn)
  Responsabilidad: Builder — landing pages, sitios, e-commerce, automatización
  Tareas tipo: Desarrollo web, CRM setup, WhatsApp automation, email automation
  Herramientas: Claude Code, Bash, deployment skills, coding-agent skill

CLIENT COMMS (Nova)
  Responsabilidad: Post-deal, seguimiento, soporte
  Tareas tipo: Status updates, bug reports, satisfaction surveys, renewals
  Herramientas: Communication patterns, issue tracking, relationship memory
```

**Configuracion de Agent Teams en IMPKT:**

```
plan/agent-teams.md  ← Documento completo de configuracion (por crear)
system/
  agents/
    mila/     # Workspace de Mila (MARKETING lead)
    lena/     # Workspace de Lena (OUTREACH lead)
    sofia/    # Workspace de Sofia (SALES lead)
    finn/     # Workspace de Finn (PRODUCTION lead)
    nova/     # Workspace de Nova (CLIENT COMMS lead)
  shared/     # Memorias compartidas entre leads
```

**Como invocar un team:**
```
/team mila,lena,sofia,finn,nova
  task: Ejecutar campana de marketing completa para cliente XYZ
  context: [datos del cliente]
```

**Limitaciones:**
- Agent Teams en Claude Code tiene limits de contexto compartidos
- Cada agente hijo hereda limits de la sesion padre
- No hay persistencia automatica entre agentes — deben escribir a archivos compartidos
- La sintaxis exacta de `/team` y su comportamiento requiere verificacion con la version actual de Claude Code (v2.1.104 segun self-check.md)

---

### Sub-agents

**Descripcion:** Uso de `TaskCreate`/`TaskGet`/`TaskUpdate` para crear tareas atomicas que pueden ejecutarse en paralelo. A diferencia de Agent Teams, los sub-agents son tareas, no agentes con contexto propio.

**¿La necesitamos?** Sí — para workloads paralelos.
**Para que parte de IMPKT:**
- Campañas de marketing con multiples deliverables simultáneos
- Research de multiples prospectos al mismo tiempo
- Testing paralelo de diferentes configs
- Festival tasks que pueden ejecutarse simultaneamente

**Configuracion:**
```
TaskCreate → define una tarea
TaskUpdate (status: in_progress) → reclama la tarea
[Ejecuta el trabajo]
TaskUpdate (status: completed) → marca como done
```

**Limitaciones:**
- Los sub-agents no tienen contexto propio — heredan del agente padre
- No hay "spawn agent" nativo en Claude Code — las tareas se ejecutan secuencialmente a menos que se use Agent Teams
- El limite real es el contexto de la sesion padre

---

### Git Tools

**Descripcion:** Integracion nativa de git via Bash + tools de Git especificas de Claude Code (`Commit`, `Branch`, `Checkout`, etc.).

**¿La necesitamos?** Sí — para versionamiento y collaboration.
**Para que parte de IMPKT:**
- Versionar el workspace de IMPKT (`C:\Users\oscar\impkt` ya tiene git inicializado)
- Mantener branches para features/experimentos
- Desplegar via git (Vercel se conecta a git)
- Backup del estado del sistema

**Configuracion:**
```bash
# Estado actual
cd C:/Users/oscar/impkt
git status  # Ya inicializado

# Workflow propuesto:
# - main: codigo productivo
# - feature/*: experiments y nuevas features
# - No hacer force push a main
# - Commits descriptivos con Co-Authored-By
```

**Workflow propuesto para IMPKT:**
1. Cada milestone completado → commit en branch feature/migration-X
2. Validacion de Gabriel → merge a main
3. Main siempre debe compilar/funcionar (no commits rotos)

**Limitaciones:**
- Git credentials no persisten entre sesiones de Antigravity
- Si el remote (GitHub/GitLab) no está configurado, solo funciona local
- Credential helper puede requerir configuracion adicional

---

### Scheduled Tasks

**Descripcion:** Sistema de cron jobs nativo de Claude Code via `CronCreate`/`CronList`/`CronDelete`. Programa prompts para ejecutarse en horario.

**¿La necesitamos?** Sí — para automation de tareas recurrentes.
**Para que parte de IMPKT:**
- Verificaciones periodicas de estado de proyectos
- Reportes semanales para Gabriel (via Telegram si OpenClaw sigue conectado)
- Heartbeat del sistema (que el sistema "despierte" periodicamente y verifique cosas)
- Monitoreo de campaigns en ejecucion

**Configuracion pendiente:**
```json
// Ejemplo — verificar cada dia a las 9am
CronCreate:
  cron: "0 9 * * *"
  prompt: "Leer system/state.md, verificar si hay tareas pendientes de Festival. Si hay, reportar a Gabriel via Telegram."
  recurring: true

// Ejemplo — reminder semanal de status
CronCreate:
  cron: "0 9 * * 1"
  prompt: "Generar resumen semanal: campanhas activas, leads nuevos, estado de proyectos. Escribir en knowledge/weekly-reports/YYYY-WXX.md"
  recurring: true
```

**Estado:** No configurado aún. Se configura en TAREA 3 (Ejecutar Migración).

**Limitaciones:**
- Los cron jobs viven solo en la sesion de Claude Code — se borran cuando la sesion termina
- No hay persistencia de cron jobs entre sesiones a menos que se use `durable: true`
- DURATION max de 7 dias para recurring jobs — luego auto-expire

---

### Plugins

**Descripcion:** Claude Code soporta plugins que extienden su funcionalidad. El "Artifact system" es una built-in feature que permite generar y mostrar artefactos interactivos (HTML, SVG, React components).

**¿La necesitamos?** Parcialmente.
**Para que parte de IMPKT:**
- **Artifact system:** Muy util para Finn (PRODUCTION) generando prototipos de landing pages, demos de UI, visualizaciones de datos para proposals de Sofia
- **Otros plugins:** Requiere evaluacion caso por caso

**Artifact system (prioridad media):**
```
 artifact: landing-page-prototype
   type: html
   content: <!DOCTYPE html>...
   description: Prototipo de landing page para cliente XYZ
```
- Se genera codigo interactivo que se puede compartir
- Ideal para mostrar a clientes antes de desarrollar
- No requiere deployment — se puede compartir como link

**Limitaciones:**
- Los artifacts son efimeros — no se guardan automaticamente en el filesystem
- Para guardar, hay que escribir el contenido a un archivo explicitamente
- Plugin ecosystem de Claude Code es limitado comparado con VS Code

---

## Features de Antigravity (el sandbox)

Antigravity es la plataforma agéntica de Google donde corre Claude Code. Provee infraestructura adicional.

---

### Ghost Runtimes

**Descripcion:** Containers efimeros (similar a Docker pero gestionado por Antigravity) para testing y validación sin afectar el sistema host.

**¿La necesitamos?** Sí — para testing de calidad.
**Para que parte de IMPKT:**
- Testing de codigo nuevo antes de deployar a produccion
- Verificar que scripts funcionan en ambiente limpio
- Probar instalaciones de dependencias sin contaminar el workspace
- A/B testing de diferentes configs

**Configuracion:** No hay CLI directa — se accede desde la interfaz de Antigravity. Buscar "Ghost Runtime" o "Container" en el panel de Antigravity.

**Estado:** No utilizado aún — configurar en TAREA 3.

**Limitaciones:**
- Ephemeral por naturaleza — no guardar estado importante ahi
- Pueden terminate sin aviso si la sesion de Antigravity se cierra
- No hay acceso directo desde bash — es una feature de la interfaz

---

### Browser Agent

**Descripcion:** Agente de browser con Chromium headless para navegacion web automatizada y verificacion visual.

**¿La necesitamos?** Sí — para verificacion funcional y visual.
**Para que parte de IMPKT:**
- **Finn (PRODUCTION):** Verificar que landing pages se ven correctamente post-deploy, check de formularios, validacion de SEO on-page
- **Mila (MARKETING):** Verificar que campañasemail se renderizan bien
- **Lena (OUTREACH):** Verificar que las paginas de los prospectos existen y tienen el contenido esperado

**Configuracion:** Buscar "Browser agent" o "Headless browser" en Antigravity. Generalmente se invoca con un comando o desde el panel de agentes.

**Estado:** No configurado/utilizado aún.

**Limitaciones:**
- No es 100% deterministico — paginas con JS heavy pueden comportarse diferente
- Timeout en paginas lentas
- Requiere permisos de red adecuados

---

### Agent Manager

**Descripcion:** Interface de Antigravity para gestionar agentes activos, ver sus estados, recursos, y logs.

**¿La necesitamos?** Sí — para supervision.
**Para que parte de IMPKT:**
- Ver cuales agentes leads (Mila, Lena, Sofia, Finn, Nova) estan activos
- Monitorear uso de recursos
- Kill agents que se queden colgados

**Configuracion:** Panel de Antigravity — generalmente en la seccion "Agents" o "Runtime".

**Limitaciones:**
- No hay CLI — es puramente interfaz grafica
- Los logs pueden ser verbosos — filtrar por agent name o tipo

---

### Planning / Fast / UI Agents (Gemini)

**Descripcion:** Agentes nativos de Gemini disponibles en Antigravity para tareas especificas. Planning agent para descomponer tareas complejas. Fast agent para tareas rapidas. UI agent para tareas de interfaz.

**¿La necesitamos?** Evaluación pendiente.
**Para que parte de IMPKT:**
- Podrian ayudar con planning de campañas complejas o arquitecturas de sitio
- El Fast agent podria servir como "primer contacto" rapido para inquiries

**Estado:** No evaluado aún — depende de la interfaz de Antigravity.

**Limitaciones:**
- Son agentes Gemini, no Claude — al usarlos se sale del stack de MiniMax/Claude
- Costo adicional potencial si no estan incluidos en el plan de Antigravity
- La coordinacion entre agentes Gemini y Claude Code requiere investigacion

---

### Deployment Scripts

**Descripcion:** Scripts de deployment pre-configurados para GCP (Google Cloud Platform) integrados con Antigravity.

**¿La necesitamos?** No para el MVP.
**Para que parte de IMPKT:** Deployment a produccion de proyectos web de clientes.
**Porque no ahora:**
- Los proyectos web de IMPKT (landing pages, sitios corporativos) usan Vercel, no GCP
- Vercel se conecta via git, no necesita GCP scripts
- GCP seria relevante solo si IMPKT expande a servicios cloud mas complejos
- Gabriel no ha mencionado GCP como requerimiento

**Revaluar cuando:** IMPKT tenga necesidad de servicios cloud de Google (Cloud Run, BigQuery, etc.)

---

### Artifact System (de Antigravity)

**Descripcion:** Compartido con la seccion de Plugins de Claude Code — sistema de generacion de artefactos interactivos. Antigravity puede mejorar esto con visualizacion en browser.

**Descripcion:** Igual que en Claude Code — generado por el modelo, mostrado como artefacto interactivo.

**Limitaciones:** Ver seccion Plugins.

---

## Features de RUFLO (orquestación)

RUFLO es el orquestador de agentes de npm (`ruflo@latest`). Es la capa de orquestacion decisions por Gabriel.

**Nota:** RUFLO se instala en TAREA 3. Esta seccion documenta que existe y se evalua post-instalacion.

---

### Swarm Topologies

**Descripcion:** RUFLO soporta multiple topologies de enjambre de agentes.

| Topologia | Descripcion | Caso de uso en IMPKT |
|-----------|-------------|---------------------|
| `mesh` | Todos los agentes se comunican con todos | Brainstorming de equipo completo |
| `hierarchical` | Lider comunica a subordinados | 5 leads directing sub-agents |
| `star` | Central hub + spokes | Un agente coordinando todo |
| `ring` | Cada agente habla con su vecino | Pipeline de produccion secuencial |

**¿La necesitamos?** Parcialmente.
**Topologia propuesta:** `hierarchical` para IMPKT — los 5 leads coordinan, pero RUFLO se evalua post-instalacion.

**Configuracion (post-instalacion):**
```bash
npx ruflo@latest topology set hierarchical
npx ruflo@latest team add mila --role marketing
npx ruflo@latest team add lena --role outreach
# etc.
```

**Limitaciones:** RUFLO no está instalado aún — esta feature depende de instalacion exitosa.

---

### Q-Learning Router

**Descripcion:** RUFLO incorpora Q-Learning para que el router aprenda automaticamente cual modelo usar para cada tipo de tarea, basandose en costos, velocidad, y calidad.

**¿La necesitamos?** No — por ahora.
**Porque no:**
- No hay training data acumulado todavia (IMPKT esta comenzando)
- El routing ya esta definido en CLAUDE.md (MiniMax M2.7 default, Claude Sonnet para premium)
- Q-Learning toma tiempo en converger — no hay datos para entrenar
- El overhead de mantener Q-Learning no justifica el beneficio actual

**Revaluar cuando:** IMPKT tenga 100+ sesiones acumuladas con diferentes modelos y se pueda hacer A/B testing real.

---

### Memory System (de RUFLO)

**Descripcion:** RUFLO tiene su propio sistema de memoria persistente entre sesiones.

**¿La necesitamos?** Evaluación pendiente.
**Porque no por ahora:**
- IMPKT ya tiene su propio sistema de memoria (system/state.md, system/memory.md, system/self-improving/)
- Agregar otra capa de memoria puede causar inconsistencias
- Primero establecer el sistema de memoria de IMPKT antes de añadir capas adicionales

**Revaluar cuando:** El sistema de memoria nativo de IMPKT resulte insuficiente para la carga de trabajo.

---

### 100+ Agent Types

**Descripcion:** RUFLO viene con un catalogo extenso de tipos de agentes pre-configurados (code-writer, researcher, analyst, etc.).

**¿La necesitamos?** Parcialmente — como referencia.
**Para que parte de IMPKT:** Los 100+ agent types de RUFLO pueden servir como inspiracion para definir los sub-roles de cada lead. Por ejemplo:
- Finn (PRODUCTION) combina: code-writer, tester, deployment-engineer
- Mila (MARKETING) combina: content-writer, seo-specialist, social-media-manager

**Configuracion:** No implementar todos — solo los que IMPKT necesite.

**Limitaciones:** Cada agent type consumes recursos. No todos son necesarios para el scope actual de IMPKT.

---

### Skills System (de RUFLO)

**Descripcion:** RUFLO tiene su propio skill system, separado del skill system de Claude Code.

**¿La necesitamos?** Evaluación posterior.
**Porque no por ahora:**
- El skill system de Claude Code es suficiente para el MVP
- Mantener dos sistemas de skills同步 es overhead
- RUFLO skills son para cuando RUFLO se use activamente como orquestador

**Revaluar cuando:** RUFLO se convierta en el orquestador principal (actualmente Claude Code es el executor directo).

---

### Hooks (de RUFLO)

**Descripcion:** Hooks internos de RUFLO para automatizar acciones basadas en eventos del orquestador.

**¿La necesitamos?** No — todavía no.
**Porque no:**
- Los hooks de Claude Code (PreToolUse, PostToolUse) son suficientes
- RUFLO hooks requieren que RUFLO esté activo y corriendo
- Por ahora IMPKT opera directamente con Claude Code, no con RUFLO como orchestrator

**Revaluar cuando:** Gabriel decida usar RUFLO como orchestrator principal en lugar de Claude Code directo.

---

## Features de Obsidian + Graphify

---

### Graphify

**Descripcion:** Herramienta que analiza archivos markdown y detecta/crea links entre articulos, construyendo un grafo de conocimiento. Instalado en `C:\Users\oscar\impkt\tools\graphify\`.

**Estado:** Instalado. Verificado en `system/self-check.md`.

**¿La necesitamos?** Sí — para knowledge mapping.
**Para que parte de IMPKT:**
- Mapear conexiones entre notas de conocimiento (estrategia, procesos, clientes)
- Identificar gaps en la base de conocimiento (notas huérfanas, sin incoming links)
- Visualizar como crece el conocimiento de IMPKT

**Configuracion verificada:**
```bash
cd C:/Users/oscar/impkt
python tools/graphify/run-graphify.py
```

Output en: `C:\Users\oscar\impkt\graphify-out\`

**Limitaciones:**
- Solo analiza archivos .md — no extrae contenido de otros formatos
- No detecta semantic similarity — solo syntactic links (`[[wiki-links]]` y `[text](url)`)
- El grafo es tan bueno como los links que se crean manualmente

---

### Obsidian Vault

**Descripcion:** Obsidian es el editor de notas con backlinks y graph view. El vault de IMPKT está en `C:\Users\oscar\impkt` (el directorio raíz ya tiene `.obsidian/`).

**¿La necesitamos?** Sí — como base de conocimiento de IMPKT.
**Para que parte de IMPKT:**
- Notas de clientes, campañas, estrategias
- Documentación de procesos internos
- Repositorio de ideas (integrado con `ideas/` directory)
- Base de conocimiento para cada lead agent

**Estructura propuesta:**
```
C:\Users\oscar\impkt\
  knowledge/
    clients/         # Notas por cliente
    campaigns/        # Campañas activas y pasadas
    processes/       # Procesos internos documentados
    strategies/       # Decisiones estratégicas
  ideas/
    inbox/           # Material sin procesar de Gabriel
    approved/         # Ideas aprobadas
    implemented/      # Ideas ya ejecutadas
    discarded/        # Descartadas con justificación
  .obsidian/         # Config de Obsidian (ya existe)
```

**Limitaciones:**
- Obsidian corre localmente — no es accesible desde Antigravity directamente
- MCP server de Obsidian no está configurado todavía (ver seccion MCP)

---

### Wiki Mode

**Descripcion:** Navegacion por articulos usando `[[wiki-links]]` — al hacer click en un link se abre el archivo.

**¿La necesitamos?** Sí — para navegar el conocimiento.
**Como se usa:**
1. Escribir nota con `[[nombre-del-articulo]]`
2. Obsidian detecta que no existe y ofrece crearla
3. Asi se construye el grafo progresivamente

**Configuracion:** Ya viene默认 en Obsidian. Solo asegurar que `settings.json` de Obsidian tiene `wikiLinks: true`.

---

### MCP Server (Obsidian)

**Descripcion:** Obsidian tiene un plugin MCP oficial que permite a herramientas externas (como Claude Code) leer y escribir notas.

**¿La necesitamos?** Evaluación pendiente — prioridad media.
**Beneficio potencial:**
- Claude Code podria escribir notas de reuniones automaticamente
- Actualizar estado de campaigns en Obsidian desde Claude Code
- Leer notas de clientes mientras hace trabajo de production

**Como configurar (cuando se implemente):**
1. Instalar plugin `obsidian-mcp` en Obsidian (Community plugins)
2. Configurar `mcpServers` en settings.json de Claude Code
3. Testear lectura/escritura de una nota dummy

**Limitaciones:** Ver seccion MCP — mismo analisis.

---

## Matriz de Decisión

| Feature | Plataforma | Necesaria | Decision | Prioridad | Estado |
|---------|-----------|-----------|---------|-----------|--------|
| Read/Write/Edit | Claude Code | Sí | Implementar | Crítica | Nativa |
| Bash | Claude Code | Sí | Implementar | Crítica | Nativa |
| Glob/Grep | Claude Code | Sí | Implementar | Alta | Nativa |
| WebFetch/WebSearch | Claude Code | Sí | Implementar | Alta | Nativa |
| Skills (custom) | Claude Code | Sí | Implementar | Alta | Por crear |
| Hooks (PreToolUse) | Claude Code | Sí | Ya configurado (graphify) | Alta | Verificar |
| Hooks (PostToolUse) | Claude Code | Sí | Implementar | Alta | Por configurar |
| Agent Teams | Claude Code | Sí | Diseñar e implementar | Alta | Por hacer |
| Sub-agents | Claude Code | Sí | Implementar | Alta | Nativo disponible |
| Git tools | Claude Code | Sí | Implementar | Alta | Ya inicializado |
| Scheduled tasks | Claude Code | Sí | Implementar | Media | Por configurar |
| Artifact system | Claude Code | Sí | Usar | Media | Nativo |
| MCP (Obsidian) | Claude Code | Parcial | Evaluar post-MVP | Media | Por evaluar |
| Ghost Runtimes | Antigravity | Sí | Usar para testing | Media | Por usar |
| Browser agent | Antigravity | Sí | Usar para verificación | Media | Por usar |
| Agent Manager | Antigravity | Sí | Supervisión | Media | Por usar |
| Planning/Fast/UI agents | Antigravity | No | Descartar por ahora | Baja | N/A |
| Deployment scripts (GCP) | Antigravity | No | Descartar (Vercel en su lugar) | Baja | N/A |
| Swarm topologies | RUFLO | Parcial | Instalar, no usar aún | Baja | Por instalar |
| Q-Learning router | RUFLO | No | Descartar (sin training data) | Baja | N/A |
| Memory system | RUFLO | No | Descartar (tenemos propio) | Baja | N/A |
| 100+ agent types | RUFLO | Parcial | Referencia, no implementar | Baja | Por evaluar |
| Skills (RUFLO) | RUFLO | No | Descartar por ahora | Baja | N/A |
| Hooks (RUFLO) | RUFLO | No | Descartar por ahora | Baja | N/A |
| Graphify | Obsidian | Sí | Mantener instalado | Alta | Instalado |
| Obsidian vault | Obsidian | Sí | Usar como KB principal | Alta | Ya es vault |
| Wiki mode | Obsidian | Sí | Usar para navegación | Alta | Nativo |
| Obsidian MCP | Obsidian | Parcial | Evaluar post-MVP | Media | Por evaluar |

---

## Configuraciones Pendientes por Hacer

Esta es la lista completa de configuraciones que deben ejecutarse en TAREA 3 para activar cada feature.

### Críticas (antes del primer workflow)

| # | Configuracion | Ubicacion | Comando/Tool | Dependencias |
|---|--------------|-----------|--------------|-------------|
| 1 | Crear `skills/` directory | `C:\Users\oscar\impkt\skills\` | Bash mkdir | Ninguna |
| 2 | Crear skill `coding-agent.md` | `skills/coding-agent.md` | Write | Copiar de OpenClaw asset #5 |
| 3 | Crear skill `deployment.md` | `skills/deployment.md` | Write | Basado en Vercel docs |
| 4 | Crear skill `content-generator.md` | `skills/content-generator.md` | Write | Basado en Mila's needs |
| 5 | Crear skill `proposal-builder.md` | `skills/proposal-builder.md` | Write | Basado en pricing de CLAUDE.md |
| 6 | Configurar PostToolUse hooks | `settings.json` | Edit (update-config skill) | Ninguna |
| 7 | Crear directorios de memoria | `system/self-improving/`, `system/proactivity/` | Bash mkdir | Ninguna |
| 8 | Crear `knowledge/` structure | `knowledge/clients/`, `knowledge/campaigns/`, `knowledge/processes/` | Bash mkdir | Ninguna |
| 9 | Inicializar RUFLO | En workspace root | Bash: `npx ruflo@latest init --wizard` | Node.js/npm disponible |

### Medias (primer mes de operación)

| # | Configuracion | Ubicacion | Comando/Tool | Dependencias |
|---|--------------|-----------|--------------|-------------|
| 10 | Configurar Scheduled Tasks (heartbeat) | Claude Code session | CronCreate | Ninguna |
| 11 | Integrar Graphify con Hooks | `settings.json` + `run-graphify.py` | Edit | Graphify hook existente |
| 12 | Evaluar Obsidian MCP | Obsidian + settings.json | Skill: update-config | Plugin obsidian-mcp instalado |
| 13 | Probar Ghost Runtime | Antigravity UI | Interfaz | Ninguna |
| 14 | Crear workspaces para 5 leads | `system/agents/mila/`, etc. | Bash mkdir | Agent Teams diseñado |
| 15 | Documentar Agent Teams config | `plan/agent-teams.md` | Write | Depende de #14 |

### Bajas (post-MVP, cuando IMPKT crezca)

| # | Configuracion | Dependencias |
|---|--------------|-------------|
| 16 | Evaluar RUFLO como orchestrator activo | #9 completado |
| 17 | Q-Learning router si hay data suficiente | 100+ sesiones acumuladas |
| 18 | Planning/Fast/UI agents de Gemini | Prueba de necesidad |
| 19 | GCP deployment scripts | Necesidad de Google Cloud |

---

## Resumen Ejecutivo

**IMPKT usa un stack delgado:** Claude Code como executor directo + Antigravity como sandbox + Obsidian como KB + Graphify como link mapper.

**Lo que SÍ usamos:**
- Core tools (Read/Write/Bash/Grep) — fundamento del sistema
- Skills system — especializado por rol (Finn, Mila, etc.)
- Hooks — graphify + command-logger + session-memory
- Agent Teams — 5 leads en arquitetura jerárquica
- Scheduled Tasks — heartbeat y reportes
- Ghost Runtimes + Browser agent — testing y verificación

**Lo que NO usamos (todavía):**
- RUFLO como orchestrator activo (se instala pero no se usa hasta tener más carga)
- Q-Learning router (sin training data)
- GCP deployment (Vercel es suficiente)
- Gemini native agents (no hay necesidad demostrada)

**Lo que se reevalúa post-MVP:**
- Obsidian MCP server
- RUFLO como orchestrator principal
- Q-Learning cuando haya data

El sistema es deliberadamente simple al inicio. Cada capa adicional se justifica solo cuando la complejidad del negocio lo demande.
