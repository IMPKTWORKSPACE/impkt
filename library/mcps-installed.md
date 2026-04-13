# MCPs Instalados

**Fecha:** 2026-04-13

---

## MCPs configurados

**Archivo:** `C:\Users\oscar\impkt\.claude\mcp.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/oscar/impkt"]
    },
    "fetch": {
      "command": "python",
      "args": ["-m", "mcp_server_fetch"]
    },
    "git": {
      "command": "python",
      "args": ["-m", "mcp_server_git", "--repository", "C:/Users/oscar/impkt"]
    }
  }
}
```

---

## Metodo de instalacion

Los MCPs se instalaron via pip/npm porque uvx no esta disponible:

```bash
# fetch y git
pip install mcp-server-fetch mcp-server-git

# filesystem (via npx)
npx -y @modelcontextprotocol/server-filesystem [path]
```

---

## MCPs instalados

| MCP | Status | Para que sirve | API keys |
|-----|--------|---------------|----------|
| filesystem | Configurado | Acceso mejorado a archivos del workspace | Ninguna |
| fetch | Configurado | Web fetching para research | Ninguna |
| git | Configurado | Git operations avanzadas | Ninguna |

---

## MCPs NO disponibles

| MCP | Razon |
|-----|-------|
| sqlite | Archivado — no instalado por simplicidad (filesystem + JSON funciona) |
| playwright | No existe en official repo — usar puppeteer (archivado) |
| supabase | No existe official MCP — usar cliente Python |
| github | Archivado — requiere GitHub PAT (token disponible) |

---

## Verificacion

Despues de reiniciar Claude Code:
```
/mcp tools
```

Debe listar las herramientas de los 3 MCPs instalados.

---

## Pending

- Verificar que los MCPs funcionan en la proxima sesion de Claude Code
- Si filesystem MCP tiene problemas con npx, cambiar a script Python
