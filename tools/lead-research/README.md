# Lead Research — IMPKT

Investiga prospectos digitalmente para Outreach (Lena).

## Uso

```bash
python tools/lead-research/research.py --name "Restaurante La Casa" --url "https://restaurante.com"
python tools/lead-research/research.py --name "Veterinaria El Parque" --url "https://veterinariaelparque.com"
python tools/lead-research/research.py --name "Clinica Dental Sonrisa"  # sin URL — usa search
```

## Output

Archivo guardado en `pipeline/research/[slug].md` con:
- Contacto (email, telefono, WhatsApp)
- Redes sociales
- Analisis de presencia digital
- Oportunidades para IMPKT
- Lead score (0-100)

## Workflow de Lena

1. Recibe lead de Mila
2. Investiga con este script
3. Genera brief de prospecto
4. Pasa a Sofia con datos para propuesta
