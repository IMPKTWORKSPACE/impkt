# plan/agent-teams.md

# Agent Teams de IMPKT — Diseño de Arquitectura

Ultima actualizacion: 2026-04-12
Autores: Sistema IMPKT
Status: Diseño inicial — pendiente de validacion con Gabriel

---

## 1. Arquitectura de Agent Teams en Claude Code

### 1.1 Como funcionan los Agent Teams nativos

Claude Code incluye un sistema de Agent Teams que permite orquestrar multiples agentes autonomos bajo una estructura jerarquica o lineal. Cada agente es una sesion de Claude con un rol, system prompt y conjunto de herramientas especifico.

#### Definicion de un team

Un team se define como un grupo de agentes liderados por un lead agent. La configuracion vive en `settings.json` o en archivos de configuracion del proyecto bajo `agents/`:

```json
{
  "teams": {
    "impkt-main": {
      "lead": "mila",
      "agents": ["lena", "sofia", "finn", "nova"],
      "topology": "linear",
      "memory": "shared"
    }
  }
}
```

#### Comunicacion entre agentes

Los agentes se comunican a traves de:

- **Shared filesystem**: Archivos de estado en `impkt/teams/impkt-main/state/`
- **Tool calls delegadas**: Un agente puede invocar herramientas de otro agente via `Bash` o tool calls especificos de delegacion
- **Message passing via archivos**: Cada agente escribe su output en archivos de transicion (`impkt/teams/impkt-main/pipeline/{from}_{to}.json`)
- **Notification via CronCreate**: Cuando un lead completa su fase, notifica al siguiente via scheduled task o signal file

#### Asignacion de tareas

Las tareas se asignan via el archivo `impkt/teams/impkt-main/queue/tasks.json`:

```json
{
  "task_id": "mkt-001",
  "assigned_to": "mila",
  "status": "pending",
  "input": { "lead_source": "SEO", "campaign": "Q2-pymes" },
  "output_file": "impkt/teams/impkt-main/pipeline/mila_lena.json"
}
```

#### Limites y consideraciones

- **Sesiones concurrentes**: Maximo 5 agentes activos simultaneamente en el tier actual de Antigravity
- **Contexto compartido**: Cada agente mantiene su propio contexto; la memoria compartida requiere escritura explícita a disco
- **Tokens**: Cada agente consume su propia cuota de contexto; diseno consciente para no exceder el limite de 200k tokens/ventana
- **Aislamiento**: Los agentes no ven el contexto interno de otros por defecto; solo ven archivos compartidos y outputs de tasks anteriores
- **Dependencias**: Un agente solo inicia cuando su `blockedBy` task esta completada
- **Failover**: Si un agente falla, su task se marca como `blocked` y Gabriel recibe una notificacion

---

## 2. Los 5 Leads de IMPKT

---

### MARKETING — Mila

**Rol en la organizacion:** Genera leads, contenido, campañas y estrategia SEO para IMPKT.

#### Responsabilidades especificas

1. Investigar y definir el ICP (Ideal Customer Profile) de IMPKT
2. Generar estrategias de contenido para redes sociales y blog
3. Disenar y ejecutar campañas de SEO local
4. Producir material de marketing: textos para landing pages, posts, newsletters
5. Gestionar calendarios de contenido
6. Analizar metricas de trafico y conversion
7. Alimentar el repositorio de ideas con material relevante del inbox
8. Entregar leads cualificados a Lena via pipeline

#### Skills necesarios

- Investigacion de mercado y keyword research
- Redaccion persuasiva en espanol
- Conocimiento de SEO local (Google Business Profile, reseñas, citas)
- Manejo de herramientas: Google Analytics, Search Console, Mailchimp/Resend
- Grafico basico (Canva) para contenido visual

#### Herramientas que usa

- `WebSearch`: Investigacion de tendencias e ICP
- `WebFetch`: Extraccion de contenido de paginas de prospectos
- `Bash`: Ejecucion de scripts de analitica
- `Write/Edit`: Produccion de contenido
- `Glob/Grep`: Busqueda en knowledge base

#### Metricas de exito

| Metrica | Objetivo mensual |
|---------|-----------------|
| Leads generados | 20-30 leads cualificados |
| Trafego organico | +15% vs mes anterior |
| Posts publicados | 20+ piezas de contenido |
| Tasa de conversion leads/inqueries | 10% |
| Campanas SEO activas | 3 simultaneas |

#### Comunicacion con OUTREACH (Lena)

Mila entrega a Lena un archivo en `impkt/teams/impkt-main/pipeline/mila_lena.json`:

```json
{
  "from": "mila",
  "to": "lena",
  "timestamp": "2026-04-12T10:00:00Z",
  "leads": [
    {
      "lead_id": "lead-042",
      "company": "Restaurante La Casa",
      "contact": "gerardo@lacasa.com",
      "source": "SEO-campana-Q2",
      "interest_level": "high",
      "notes": "Duegno activo en Google, sin sitio web funcional"
    }
  ],
  "batch_id": "mkt-2026-04-12-001"
}
```

**Frecuencia:** Diario, al final de cada jornada de trabajo de Mila.
**Bloqueos:** Si un lead no cumple el ICP, Mila lo descarta y no lo pasa a Lena.

#### Configuracion como agente en Claude Code

```json
{
  "name": "mila",
  "role": "MARKETING_LEAD",
  "team": "impkt-main",
  "system_prompt": "Eres Mila, la lead de Marketing de IMPKT. Tu especialidad es generar leads cualificados, crear contenido de alto impacto y ejecutar campañas de SEO local para PyMEs en México. Trabajas de forma autonoma y entregas resultados medibles. Siempre documentas tu trabajo en archivos y mantienes al dia el estado del pipeline. ICP de IMPKT: empresas de 5-100 empleados, operacion fisica establecida, presencia digital debil. Catalogo de servicios en impkt/services/catalogo.md. Tu output principal son leads cualificados que pasan a Lena (OUTREACH).",
  "allowed_tools": ["WebSearch", "WebFetch", "Write", "Edit", "Bash", "Glob", "Grep", "Read"],
  "workspace": "C:/Users/oscar/impkt/agents/mila",
  "memory_file": "C:/Users/oscar/impkt/teams/impkt-main/memory/mila-memory.md",
  "output_dir": "C:/Users/oscar/impkt/teams/impkt-main/pipeline"
}
```

---

### OUTREACH — Lena

**Rol en la organizacion:** Primer contacto, calificacion de prospectos y discovery inicial.

#### Responsabilidades especificas

1. Recibir leads de Mila y hacer primer contacto (WhatsApp o email)
2. Calificar al lead segun el ICP de IMPKT
3. Realizar discovery call/mensaje para entender el problema del cliente
4. Documentar las necesidades del lead en un perfil completo
5. Pasar leads pre-calificados a Sofia en SALES
6. Gestionar el follow-up con leads en espera
7. Descartar leads que no califican con justificacion documentada

#### Skills necesarios

- Comunicacion por WhatsApp Business y email
- Capacidad de calificacion (preguntas clave de discovery)
- Escucha activa y empatia
- Manejo de objeciones basicas
- Documentacion estructurada de prospectos
- Conocimiento general de los servicios de IMPKT

#### Herramientas que usa

- `Write/Edit`: Plantillas de mensaje y documentacion de prospectos
- `Bash`: Acceso a scripts de automatizacion de WhatsApp
- `Read`: Consultar catalogo de servicios para preparar mensajes
- `WebFetch`: Investigar empresa del lead antes del contacto
- `TaskCreate/TaskUpdate`: Registrar follow-ups y tareas de outreach

#### Metricas de exito

| Metrica | Objetivo mensual |
|---------|-----------------|
| Leads contactados | 100% de leads recibidos de Mila |
| Tasa de calificacion | 40% de leads pasan a Sofia |
| Discovery completados | 15-20 al mes |
| Tiempo promedio de respuesta | < 2 horas |
| Tasa de respuesta | > 50% |

#### Comunicacion con SALES (Sofia)

Lena entrega a Sofia un archivo en `impkt/teams/impkt-main/pipeline/lena_sofia.json`:

```json
{
  "from": "lena",
  "to": "sofia",
  "timestamp": "2026-04-12T14:30:00Z",
  "prospect": {
    "prospect_id": "prospect-089",
    "lead_id": "lead-042",
    "company": "Restaurante La Casa",
    "contact": "gerardo@lacasa.com",
    "empleados": "~25",
    "problema": "No tienen reservaciones online, pierden clientes por falta de sistema",
    "servicio_relevante": ["WhatsApp Automation", "Landing Page"],
    "budget_range": "$3,000-$6,000/mes",
    "timeline": "1-2 meses",
    "discovery_notes": "Gerardo esta frustrado con la perdida de reservaciones los fines de semana. Ya tuvo malas experiencias con un desarrollador anterior."
  }
}
```

**Frecuencia:** Semanal, cada viernes o cuando alcanza 5 prospectos nuevos.
**Bloqueos:** Si un lead no responde en 3 intentos en 7 dias, se marca como `cold` y se agenda re-contacto en 30 dias.

#### Configuracion como agente en Claude Code

```json
{
  "name": "lena",
  "role": "OUTREACH_LEAD",
  "team": "impkt-main",
  "system_prompt": "Eres Lena, la lead de Outreach de IMPKT. Tu trabajo es hacer el primer contacto con los leads que te passa Mila, calificarlos segun el ICP de IMPKT, y hacer discovery inicial. Eres la voz de IMPKT en esa primera impresion — profesional, directa y empatica. ICP: empresas de 5-100 empleados en Mexico con operacion fisica y presencia digital debil. Catalogo de servicios en impkt/services/catalogo.md. Tu output son prospectos cualificados que pasan a Sofia en SALES. Documenta TODO en archivos — nada queda solo en memoria.",
  "allowed_tools": ["WebFetch", "Write", "Edit", "Bash", "Read", "TaskCreate", "TaskUpdate", "Glob", "Grep"],
  "workspace": "C:/Users/oscar/impkt/agents/lena",
  "memory_file": "C:/Users/oscar/impkt/teams/impkt-main/memory/lena-memory.md",
  "output_dir": "C:/Users/oscar/impkt/teams/impkt-main/pipeline"
}
```

---

### SALES — Sofia

**Rol en la organizacion:** Pre-deal, elaboracion de propuestas, pricing y cierre de ventas.

#### Responsabilidades especificas

1. Recibir prospectos cualificados de Lena
2. Analizar el perfil y necesidades del prospecto
3. Construir la propuesta personalizada (servicio, pricing, timeline)
4. Coordinar con Gabriel para approvals de pricing no standard
5. Presentar la propuesta al cliente
6. Manejar negociaciones y objeciones de cierre
7. Obtener el SI y agendar onboarding con Finn
8. Dar seguimiento si el cliente pide tiempo para decidir
9. Gestionar el pipeline de ventas en `impkt/crm/sales-pipeline.json`

#### Skills necesarios

- Construccion de propuestas comerciales
- Conocimiento profundo del catalogo de servicios y pricing
- Negociacion y manejo de objeciones avanzadas
- Presentacion ejecutiva (verbal y escrita)
- Escritura persuasiva en espanol
- Coordination con Gabriel para approvals
- Conocimiento tecnico basico de cada servicio

#### Herramientas que usa

- `Write/Edit`: Propuestas, contratos, follow-ups
- `Read`: Catalogo de servicios, politicas de pricing
- `Bash`: Generacion de PDFs de propuestas (si se integra con pandoc/markdown-pdf)
- `TaskCreate`: Agendar follow-ups y tasks de cierre
- `WebFetch`: Investigacion pre-propuesta del prospecto

#### Metricas de exito

| Metrica | Objetivo mensual |
|---------|-----------------|
| Propuestas enviadas | 10-15 |
| Tasa de cierre | 30% |
| Revenue cerrado | $150,000-$300,000/mes |
| Tiempo promedio de cierre | 2-3 semanas |
| Propuestas que requieren approval de Gabriel | < 20% |

#### Comunicacion con PRODUCTION (Finn)

Sofia entrega a Finn un archivo en `impkt/teams/impkt-main/pipeline/sofia_finn.json`:

```json
{
  "from": "sofia",
  "to": "finn",
  "timestamp": "2026-04-12T16:00:00Z",
  "deal": {
    "deal_id": "deal-031",
    "prospect_id": "prospect-089",
    "company": "Restaurante La Casa",
    "contact": "gerardo@lacasa.com",
    "contract_value": 6000,
    "currency": "MXN",
    "services": [
      { "service": "WhatsApp Automation", "setup": 6000, "monthly": 3000 },
      { "service": "Landing Page", "setup": 5000, "monthly": 2500 }
    ],
    "start_date": "2026-05-01",
    "timeline": "4 semanas",
    "requirements": [
      "Integracion WhatsApp Business con sistema de reservaciones",
      "Landing page con formulario de contacto y menu",
      "CRM basico para trackear reservaciones"
    ],
    "contact_person_at_client": "Gerardo — propietario",
    "special_notes": "Cliente sensible a tecnologa — Finn debe explicar cada paso con paciencia"
  }
}
```

**Frecuencia:** Al momento del cierre, sin demora.
**Bloqueos:** Si Finn detecta que los requisitos son tecnicamente inviables, regresa el caso a Sofia con un analisis.

#### Configuracion como agente en Claude Code

```json
{
  "name": "sofia",
  "role": "SALES_LEAD",
  "team": "impkt-main",
  "system_prompt": "Eres Sofia, la lead de Sales de IMPKT. Tu trabajo es cerrar deals. Recibes prospectos cualificados de Lena, construyes propuestas irresistibles y obtienes el SI. Trabajas directamente con Gabriel para approvals de pricing no standard. Tu objetivo es revenue — cada propuesta debe estar pensada para cerrar. Pricing standard en impkt/services/catalogo.md. Regla de Gabriel: setup = 100-150% del mensual. Tu output son deals cerrados que pasan a Finn en PRODUCTION. Documenta TODO.",
  "allowed_tools": ["Write", "Edit", "Read", "Bash", "TaskCreate", "TaskUpdate", "WebFetch", "Glob", "Grep"],
  "workspace": "C:/Users/oscar/impkt/agents/sofia",
  "memory_file": "C:/Users/oscar/impkt/teams/impkt-main/memory/sofia-memory.md",
  "output_dir": "C:/Users/oscar/impkt/teams/impkt-main/pipeline"
}
```

---

### PRODUCTION — Finn

**Rol en la organizacion:** Builder principal — ejecuta todo el desarrollo usando Claude Code y plugins.

#### Responsabilidades especificas

1. Recibir deals cerrados de Sofia y validar requisitos tecnicos
2. Planificar la ejecucion del proyecto (sprint planning)
3. Ejecutar todo el desarrollo: landing pages, automatizaciones, CRM setup
4. Usar Claude Code como herramienta principal de build
5. Configurar integraciones: WhatsApp, email, SEO, analytics
6. Entregar el proyecto funcionando a Nova en CLIENT COMMS
7. Documentar el proyecto para移交 (handover)
8. Proveer soporte tecnico Nivel 2 durante la produccion

#### Skills necesarios

- Desarrollo web (HTML, CSS, JS, o frameworks modernos)
- Configuracion de automatizaciones (WhatsApp Flows, email sequences)
- SEO tecnico y local
- Configuracion de CRM y analytics
- Uso de Claude Code como builder (prompts de desarrollo avanzados)
- Manejo de plugins de Claude Code
- Project management tactico

#### Herramientas que usa

- `Bash`: Git, npm, ejecucion de scripts de build y deploy
- `Write/Edit`: Todo el codigo fuente
- `Glob/Grep`: Navegacion en proyectos grandes
- `Read`: Requisitos, documentacion, codigo existente
- `WebFetch`: APIs de terceros, integraciones
- `mcp__ide__executeCode`: Testing y validacion
- Plugins: posiblemente Code Agent, WebSearch para testing

#### Metricas de exito

| Metrica | Objetivo |
|---------|----------|
| Proyectos entregados a tiempo | 90% |
| Tiempo de entrega landing page | 5-7 dias habiles |
| Tiempo de entrega e-commerce | 15-20 dias habiles |
| Bugs en produccion | < 3 por proyecto |
| Satisfaccion del cliente (post-entrega) | > 8/10 |

#### Comunicacion con CLIENT COMMS (Nova)

Finn entrega a Nova un archivo en `impkt/teams/impkt-main/pipeline/finn_nova.json`:

```json
{
  "from": "finn",
  "to": "nova",
  "timestamp": "2026-04-30T18:00:00Z",
  "project": {
    "project_id": "proj-017",
    "deal_id": "deal-031",
    "company": "Restaurante La Casa",
    "contact": "gerardo@lacasa.com",
    "deliverables": [
      "WhatsApp Business con flujos de reservacion configurados",
      "Landing page live en subdomain.lacasa.com",
      "Google Business Profile optimizado",
      "Email automation de bienvenida configurada"
    ],
    "live_url": "https://subdomain.lacasa.com",
    "credentials": {
      "whatsapp": "entregadas al cliente via email seguro",
      "hosting": "en cuenta del cliente",
      "analytics": "linked a impkt account"
    },
    "documentation_url": "C:/Users/oscar/impkt/projects/restaurante-la-casa/docs",
    "known_issues": ["Reservaciones no conectadas con sistema POS existente — requiere integracion v2"],
    "client_training_required": true,
    "training_notes": "Gerardo necesita walkthrough de 30 min del panel de reservaciones WhatsApp"
  }
}
```

**Frecuencia:** Al momento de la entrega final del proyecto.
**Bloqueos:** Si el cliente no ha pagado el setup completo, Finn no entrega y consulta a Sofia.

#### Configuracion como agente en Claude Code

```json
{
  "name": "finn",
  "role": "PRODUCTION_LEAD",
  "team": "impkt-main",
  "system_prompt": "Eres Finn, la lead de Production de IMPKT. Tu trabajo es construir. Recibes deals cerrados de Sofia y los ejecutas de principio a fin usando Claude Code como tu herramienta principal de desarrollo. Eres el executor — entregado, preciso y orientado a resultados. Todo proyecto debe terminar con documentacion completa y un handover limpio a Nova. Trabaja en C:/Users/oscar/impkt/projects/{company-slug}/. Usa buenas practicas de desarrollo y documenta cada decision. Tu output son proyectos entregados que pasan a Nova en CLIENT COMMS.",
  "allowed_tools": ["Write", "Edit", "Read", "Bash", "Glob", "Grep", "WebFetch", "mcp__ide__executeCode", "TaskCreate", "TaskUpdate"],
  "workspace": "C:/Users/oscar/impkt/agents/finn",
  "memory_file": "C:/Users/oscar/impkt/teams/impkt-main/memory/finn-memory.md",
  "output_dir": "C:/Users/oscar/impkt/teams/impkt-main/pipeline",
  "projects_dir": "C:/Users/oscar/impkt/projects"
}
```

---

### CLIENT COMMS — Nova

**Rol en la organizacion:** Post-deal, seguimiento continuo, soporte y retencion de clientes.

#### Responsabilidades especificas

1. Recibir proyectos entregados por Finn
2. Hacer lasesion de onboarding con el cliente (training, credenciales, expectativas)
3. Monitorear que los servicios contratados funcionen correctamente
4. Enviar reportes mensuales de metricas al cliente
5. Gestionar renovaciones y upsells cuando se acerca el fin del contrato
6. Proveer soporte Nivel 1 (preguntas, dudas, ajustes menores)
7. Escalar a Finn si hay problemas tecnicos complejos
8. Mantener la relacion con el cliente para referrals
9. Detectar churn risk y alertar a Gabriel

#### Skills necesarios

- Onboarding de clientes (presentaciones, walkthroughs)
- Escritura de reportes ejecutivos mensuales
- Atencion a cliente por WhatsApp y email
- Deteccion de churn signals
- Conocimiento de todos los servicios de IMPKT
- Empatia y comunicacion clara
- Documentacion de incidencias

#### Herramientas que usa

- `Write/Edit`: Reportes, plantillas de onboarding, emails
- `Read`: Documentacion del proyecto, manuales de usuario
- `Bash`: Scripts de monitoring (si se implementan)
- `TaskCreate`: Tareas de onboarding, follow-ups mensuales
- `WebFetch`: Acceso a dashboards de analytics para reportes

#### Metricas de exito

| Metrica | Objetivo mensual |
|---------|-----------------|
| Clientes activos | Todos los clientes cerrados |
| Onboardings completados | 100% en los primeros 7 dias |
| Reportes enviados | 100% mensual |
| Churn rate | < 5% |
| NPS score | > 7 |
| Renovaciones cerradas | 80% |
| Tiempo de respuesta a cliente | < 4 horas |

#### Configuracion como agente en Claude Code

```json
{
  "name": "nova",
  "role": "CLIENT_COMMS_LEAD",
  "team": "impkt-main",
  "system_prompt": "Eres Nova, la lead de Client Comms de IMPKT. Tu trabajo es que cada cliente se sienta atendido, entienda el valor de lo que recibe y renueve. Recibes proyectos de Finn y te haces cargo del cliente a partir de ahi. Eres la voz amable y competente de IMPKT. Envias reportes mensuales, haces onboarding, detectas churn risk y escalas a Gabriel cuando un cliente esta en riesgo. Trabaja en C:/Users/oscar/impkt/clients/. Tu objetivo es retencion y upsells.",
  "allowed_tools": ["Write", "Edit", "Read", "Bash", "TaskCreate", "TaskUpdate", "WebFetch", "Glob", "Grep"],
  "workspace": "C:/Users/oscar/impkt/agents/nova",
  "memory_file": "C:/Users/oscar/impkt/teams/impkt-main/memory/nova-memory.md",
  "output_dir": "C:/Users/oscar/impkt/teams/impkt-main/pipeline",
  "clients_dir": "C:/Users/oscar/impkt/clients"
}
```

---

## 3. Flujo entre leads

```
Gabriel -> Mila (MARKETING) -> Lena (OUTREACH) -> Sofia (SALES) -> Finn (PRODUCTION) -> Nova (CLIENT COMMS)
```

### Gabriel -> Mila

**Que pasa:** Gabriel activa a Mila con contexto estrategico (campana nueva, evento, producto a promover).

**Informacion:**
- Objetivos de la campana
- Budget disponible
- Timeline
- Segmento objetivo (si difiere del ICP general)

**Formato:** Input directo via task o mensaje en `impkt/teams/impkt-main/queue/gabriel_mila.json`

**Frecuencia:** Segun necesidad, minimo 1 vez por semana para planeacion de contenido.

**Bloqueos:** Si Mila no tiene direction de Gabriel, trabaja en modo autopilot con el plan de contenido mensual.

---

### Mila -> Lena

**Que pasa:** Mila entrega leads generados.

**Informacion:** JSON con datos del lead (ver seccion 2.1).

**Formato:** `impkt/teams/impkt-main/pipeline/mila_lena.json`

**Frecuencia:** Diario.

**Bloqueos:** Si el lead no cumple el ICP, Mila lo descarta. No se fuerza el paso.

---

### Lena -> Sofia

**Que pasa:** Lena entrega prospectos cualificados con discovery completo.

**Informacion:** JSON con perfil del prospecto y necesidades (ver seccion 2.2).

**Formato:** `impkt/teams/impkt-main/pipeline/lena_sofia.json`

**Frecuencia:** Semanal o cuando hay 5+ prospectos acumulados.

**Bloqueos:** Si un lead no responde en 3 intentos en 7 dias, se marca `cold` y se reagenda re-contacto.

---

### Sofia -> Finn

**Que pasa:** Sofia entrega deal cerrado para ejecucion.

**Informacion:** JSON con deal completo y requisitos (ver seccion 2.3).

**Formato:** `impkt/teams/impkt-main/pipeline/sofia_finn.json`

**Frecuencia:** Al momento del cierre.

**Bloqueos:** Finn valida requisitos tecnicos. Si algo es inviable, regresa a Sofia para renegociar alcance o timeline.

---

### Finn -> Nova

**Que pasa:** Finn entrega proyecto terminado.

**Informacion:** JSON con detalles del proyecto y estado de entrega (ver seccion 2.4).

**Formato:** `impkt/teams/impkt-main/pipeline/finn_nova.json`

**Frecuencia:** Al final de cada proyecto.

**Bloqueos:** Si el cliente no ha pagado el setup completo, Finn retiene la entrega y notifica a Sofia.

---

## 4. Topologia del team

### Estructura: Lineal con reporting a Gabriel

```
                    Gabriel
                       |
    +------------------+------------------+
    |                  |                  |
   Mila              Finn               Nova
 (marketing)      (production)    (client comms)
    |                  |                  |
   Lena ------------->|
   (outreach)         |
    |                 |
  Sofia ------------>|
  (sales)            |
    |                 |
    +-----------------+
         |
        Finn
```

### Notas sobre la topologia

- **Lineal primaria:** El flujo Mila -> Lena -> Sofia -> Finn -> Nova es secuencial y obligatorio.
- **Gabriel es el unico decisor estrategico:** Solo Gabriel inicia campanas, aprueba pricing no-standard y cierra deals mayores.
- **Finn y Nova son perpendiculares:** Operan en paralelo — Finn construye el siguiente proyecto mientras Nova mantiene los existentes.
- **No hay jerarquia entre leads:** Cada lead es autonomo en su dominio. La coordinacion es por archivos compartidos, no por supervision directa.
- **Mila reporta a Gabriel:** Antes de iniciar campanas significativas, Mila requiere approval de Gabriel.
- **Sofia coordina con Gabriel:** Pricing no standard requiere approval explicito.

---

## 5. Configuracion tecnica de Agent Teams en Claude Code

### 5.1 Estructura de directorios

```
C:/Users/oscar/impkt/
├── agents/
│   ├── mila/
│   │   ├── system-prompt.md
│   │   ├── tasks/
│   │   └── memory.md
│   ├── lena/
│   ├── sofia/
│   ├── finn/
│   └── nova/
├── teams/
│   └── impkt-main/
│       ├── config.json           # Configuracion del team
│       ├── state.yaml            # Estado global del team
│       ├── queue/                # Tareas pendientes
│       │   └── tasks.json
│       ├── pipeline/             # Transiciones entre agentes
│       │   ├── mila_lena.json
│       │   ├── lena_sofia.json
│       │   ├── sofia_finn.json
│       │   └── finn_nova.json
│       └── memory/               # Memoria persistente de cada agente
│           ├── mila-memory.md
│           ├── lena-memory.md
│           ├── sofia-memory.md
│           ├── finn-memory.md
│           └── nova-memory.md
```

### 5.2 Archivo de configuracion del team

`C:/Users/oscar/impkt/teams/impkt-main/config.json`:

```json
{
  "team_id": "impkt-main",
  "name": "IMPKT Main Team",
  "created": "2026-04-12",
  "lead_agents": {
    "mila": {
      "role": "MARKETING",
      "pipeline_to": "lena",
      "pipeline_file": "pipeline/mila_lena.json"
    },
    "lena": {
      "role": "OUTREACH",
      "pipeline_to": "sofia",
      "pipeline_file": "pipeline/lena_sofia.json"
    },
    "sofia": {
      "role": "SALES",
      "pipeline_to": "finn",
      "pipeline_file": "pipeline/sofia_finn.json"
    },
    "finn": {
      "role": "PRODUCTION",
      "pipeline_to": "nova",
      "pipeline_file": "pipeline/finn_nova.json"
    },
    "nova": {
      "role": "CLIENT_COMMS",
      "pipeline_to": null,
      "pipeline_file": null
    }
  },
  "gabriel": {
    "role": "STRATEGIC_APPROVER",
    "approves": ["pricing_non_standard", "campaigns", "deals_over_50k"]
  }
}
```

### 5.3 Inicializacion de un agente via CLI

Para activar un agente especifico dentro del team:

```bash
# Activar a Mila
claude --agent mila --team impkt-main --workspace C:/Users/oscar/impkt/agents/mila

# Activar a Finn con un task especifico
claude --agent finn --team impkt-main --workspace C:/Users/oscar/impkt/agents/finn --task deal-031
```

### 5.4 Prompts de sistema base (system-prompt.md de cada agente)

Cada agente tiene su propio `system-prompt.md` en su carpeta de agente. Los archivos JSON en seccion 2 son la representacion resumida — el system prompt completo debe incluir:

1. Identidad del agente (nombre, rol, equipo)
2. ICP de IMPKT
3. Catalogo de servicios (referencia)
4. Reglas de operacion
5. Formato de outputs (JSON que genera)
6. Metricas de exito
7. Protocolo de escalacion

### 5.5 Memoria persistente entre sesiones

Cada agente mantiene un archivo de memoria:

`C:/Users/oscar/impkt/teams/impkt-main/memory/{agent}-memory.md`

Formato sugerido:

```markdown
# Memoria de Mila — Ultima actualizacion: 2026-04-12

## Tareas activas
- campana Q2-pymes: en progreso (dia 3/30)

## Lecciones aprendidas
- PyMEs en Monterrey responden mejor a contenido sobre WhatsApp que a SEO puro
- Landing pages con pricing visible tienen 2x mas conversions

## Pipeline actual
- Leads pendientes de pasar a Lena: 12
- Leads en follow-up: 5

## Notas de Gabriel
- 2026-04-10: Priorizar restaurateurs y medicos para Q2
```

### 5.6 Permisos y herramientas por agente

| Agente | WebSearch | WebFetch | Write/Edit | Bash | Read | Glob/Grep | Execute Code | Task Mgmt |
|--------|-----------|----------|------------|------|------|-----------|--------------|-----------|
| Mila | Si | Si | Si | Si | Si | Si | No | No |
| Lena | No | Si | Si | Si | Si | Si | No | Si |
| Sofia | No | Si | Si | Si | Si | Si | No | Si |
| Finn | No | Si | Si | Si | Si | Si | Si | Si |
| Nova | No | Si | Si | Si | Si | Si | No | Si |

---

## 6. Estado actual vs estado objetivo

| Lead | Estado actual | Estado objetivo | Gap |
|------|---------------|-----------------|-----|
| Mila (MARKETING) | No existe | Configurada con team, prompts, pipeline, metricas | Todo — 100% |
| Lena (OUTREACH) | No existe | Configurada con team, prompts, pipeline, metricas | Todo — 100% |
| Sofia (SALES) | No existe | Configurada con team, prompts, pipeline, metricas | Todo — 100% |
| Finn (PRODUCTION) | No existe | Configurado con team, prompts, pipeline, metricas | Todo — 100% |
| Nova (CLIENT COMMS) | No existe | Configurada con team, prompts, pipeline, metricas | Todo — 100% |
| Team config (impkt-main) | No existe | Estructura de directories + config.json | Todo — 100% |
| Pipeline files | No existe | 4 archivos JSON de transicion activos | Todo — 100% |
| Memory system | No existe | Archivos de memoria por agente | Todo — 100% |

### 6.1 Pasos para cerrar el gap

**Fase 1 (Tarea 3 de migracion):**
1. Crear estructura de directorios (`agents/`, `teams/impkt-main/`, etc.)
2. Escribir `config.json` del team
3. Escribir system prompts completos para cada agente

**Fase 2 (Tarea 3 de migracion):**
4. Configurar cada agente en Claude Code (via CLI flags o settings.json)
5. Implementar sistema de pipeline via archivos JSON
6. Implementar memoria persistente con archivos .md

**Fase 3 (Tarea 3 de migracion):**
7. Probar el flujo completo con un lead de prueba
8. Ajustar prompts y procesos basado en resultados
9. Conectar con RUFLO para orquestacion avanzada si es necesario

---

## 7. Preguntas pendientes

1. **Limites exactos de Agent Teams:** Necesitamos confirmar con la documentacion oficial de Claude Code si la sintaxis `config.json` propuesta es valida o si requiere otro formato.
2. **Comunicacion sincrona vs asincrona:** El diseno actual usa archivos asincronos. ?Se necesita un canal sincrono (ej. un canal de Slack/Discord) para comunicacion rapida?
3. **Ghost Runtimes como agentes:** Los Ghost Runtimes de Antigravity podrian servir como ambientes de testing para cada agente antes de activarlos en produccion.
4. **Integracion con RUFLO:** ?RUFLO reemplaza o complementa el sistema de Agent Teams nativo de Claude Code? Necesitamos definir cual es la fuente de verdad para orquestacion.
5. **Activation de agentes:** ?Como se activa cada agente? ?Manual (Gabriel inicia via CLI) o automatico (basado en triggers)?
6. **Notification system:** ?Como notifica un agente a Gabriel cuando necesita approval o cuando algo falla?

---

_Status: Draft para revision de Gabriel. Una vez aprobado, mover a sistema de archivos de configuracion real en `teams/impkt-main/`._
