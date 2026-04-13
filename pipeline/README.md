# Pipeline README

## Estructura de comunicación entre leads

```
Gabriel
  ↓
Mila (MARKETING) → genera leads
  ↓ [pipeline/mila-to-lena/]
Lena (OUTREACH) → califica, discovery
  ↓ [pipeline/lena-to-sofia/]
Sofia (SALES) → cierra deals
  ↓ [pipeline/sofia-to-finn/]
Finn (PRODUCTION) → construye, entrega
  ↓ [pipeline/finn-to-nova/]
Nova (CLIENT COMMS) → onboardea, retiene
  ↓ [feedback a Gabriel]
```

## Formato de archivos JSON

Cada archivo en el pipeline tiene:
- Formato: `YYYY-MM-DD/[lead-or-deal-id].json`
- Contenido: JSON con metadata del lead/deal + notas
- Estado: se mueven entre carpetas según avanzan o se descartan

## Reglas del pipeline

1. Cada lead/deal tiene su propio archivo JSON
2. Cuando se pasa al siguiente lead, crear nuevo archivo en la carpeta destino
3. El archivo original se mueve a la carpeta destination (no se duplica)
4. Si se descarta, mover a `archive/` o `lost/` con razón

## Dónde encontrar qué

| Carpeta | Qué contiene | Quién lo usa |
|---|---|---|
| `pipeline/mila-to-lena/` | Leads sin contactar | Lena |
| `pipeline/lena-to-sofia/` | Leads calificados | Sofia |
| `pipeline/sofia-to-finn/` | Deals cerrados, listos para build | Finn |
| `pipeline/finn-to-nova/` | Proyectos completados | Nova |
| `pipeline/archive/` | Leads no calificados (por si regresan) | Lena |
| `pipeline/lost/` | Deals perdidos | Sofia |
| `support/tickets/` | Issues técnicos de clientes | Finn + Nova |
| `sales/` | Dashboard y metrics de ventas | Sofia |
| `production/projects/` | Proyectos completados | Finn |
| `clients/` | Info de clientes activos | Nova |