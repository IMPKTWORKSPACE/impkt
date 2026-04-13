# Proposal Generator — IMPKT

Genera propuestas comerciales en PDF con branding IMPKT.

## Instalacion

```bash
pip install fpdf2
```

## Uso

```bash
python tools/proposal-generator/generate_proposal.py \
  --business "Restaurante La Casa" \
  --contact "Gerardo Martinez" \
  --industry "Restaurante" \
  --location "Monterrey, NL" \
  --problem "Pierden reservaciones por falta de sistema online" \
  --package landing \
  --setup 5000 \
  --monthly 2500 \
  --months 6 \
  --timeline "3 semanas" \
  --output-dir proposals
```

## Paquetes disponibles

| Flag | Nombre |
|------|--------|
| `landing` | Landing Page |
| `corporativo` | Sitio Corporativo |
| `ecommerce` | E-commerce |
| `seo` | SEO Local |
| `social` | Social Media |
| `whatsapp` | WhatsApp Automation |
| `email` | Email Automation |
| `automatizacion` | Automatizacion Integral |
| `full` | Paquete Integral |

## Output

PDF guardado en `proposals/IMPKT-Propuesta-[PAQUETE]-[NEGOCIO]-[FECHA].pdf`
