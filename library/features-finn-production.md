# Features para FINN — Production / Builder

**Fecha:** 2026-04-13
**Agente:** Finn (PRODUCTION)

---

## Stack para construir

Finn usa Claude Code como herramienta principal de build. No necesita plugins especiales
para código — los tiene todos nativos.

---

## Plugins evaluados

| Plugin | Disponible | Instalado | Para que sirve | Como se instala |
|--------|-----------|-----------|---------------|----------------|
| frontend-design | SI (built-in skill) | NO | Produccion de frontend diferenciado, no genérico-IA | Skill — se activa automatico en tareas frontend |
| code-review | SI (marketplace) | NO | QA de código con agentes paralelo | `claude plugin install code-review` |
| feature-dev | SI (marketplace) | NO | Workflow 7-fases de desarrollo | `claude plugin install feature-dev` |
| commit-commands | SI (marketplace) | NO | Git workflow automatizado | `claude plugin install commit-commands` |
| security-guidance | NO (marketplace) | N/A | No existe como plugin — se replica con hooks PreToolUse | Ver hooks en features-global.md |

**Recomendado para Finn:**
- `frontend-design` — CRITICO (built-in, se activa automatico)
- `code-review` — INSTALAR (QA antes de entregar proyectos)
- `commit-commands` — INSTALAR (workflow git profesional)
- `feature-dev` — INSTALAR (proyectos complejos)

---

## MCPs evaluados

| MCP | Disponible | Para que sirve | API keys | Instalacion |
|-----|-----------|---------------|----------|-------------|
| filesystem | SI | Mejor acceso a archivos del proyecto | Ninguna | `npx -y @modelcontextprotocol/server-filesystem [path]` |
| git | SI | Versionar proyectos, branches | Ninguna | `uvx mcp-server-git --repository [path]` |
| sqlite | SI (archivado) | DB local para tracking de proyectos | Ninguna | `uvx mcp-server-sqlite` |
| playwright | NO | No existe — usar puppeteer (archivado) o ver alternativas | Ninguna | No disponible |
| supabase | NO | No existe MCP oficial — usar cliente Python | Ninguna | No disponible — instalar via pip |

**Recomendado para Finn:**
- `filesystem` MCP — UTIL para navegar proyectos grandes
- `sqlite` MCP — UTIL para tracking de tareas de proyecto
- Cliente Supabase via pip — para backend de proyectos

---

## Herramientas para Vercel deploy

**Vercel CLI:**
```bash
npm install -g vercel
npx vercel --help
```

**Token de Vercel:** Ya tiene cuenta con credenciales (se verifico en FASE 1).

**Workflow propuesto:**
1. Finn termina proyecto en `projects/[cliente]/`
2. `npx vercel` desde el directorio del proyecto
3. Vercel detecta framework automaticamente (Next.js, Vite, etc.)
4. Deploy a URL temporal → URL final

---

## Generador de proposals PDF

**Ver:** `tools/proposal-generator/` — se construira en FASE 5

Para Finn, el PDF proposal NO es su responsabilidad directa — Sofia lo genera.
Finn recibe el deal y ejecuta.

---

## QA Visual

**Problema:** No hay Playwright oficial de MCP.

**Alternativas:**
1. **Screenshot via curl:** `curl -s "https://api.apiflash.com/v1/urltofile?access_key=...&url=..."`
2. **Puppeteer MCP (archivado):** `npx -y @modelcontextprotocol/server-puppeteer` (abre navegador real)
3. **Browser agent de Antigravity:** Si existe, usar para QA visual

**Recomendacion:** Postergar hasta que se verifique si Antigravity Browser agent existe.

---

## Resumen de installation para Finn

| Accion | Prioridad | Comando/Nota |
|--------|-----------|--------------|
| frontend-design skill | Critica | Built-in — automatico |
| code-review plugin | Alta | `claude plugin install code-review` |
| commit-commands plugin | Alta | `claude plugin install commit-commands` |
| feature-dev plugin | Media | `claude plugin install feature-dev` |
| filesystem MCP | Media | `npx -y @modelcontextprotocol/server-filesystem` |
| sqlite MCP | Media | `uvx mcp-server-sqlite` |
| Vercel CLI | Critica | `npm install -g vercel` |
| Supabase client | Alta | `pip install supabase` |

---

## Dependencias pendientes (para Gabriel)

- Credenciales Vercel (verificar que el login funciona: `npx vercel login`)
- API key para screenshot (apiflash o similar) si se necesita QA visual automatico
