# Content Humanizer — IMPKT

Post-procesa texto generado por IA para que no suene robotico.

## Uso

```bash
# Via argumentos
python tools/humanizer/humanize.py "En el mundo actual es importante destacar que las PyMEs necesitan presencia digital."

# Via stdin
echo "Tu texto aqui" | python tools/humanizer/humanize.py
```

## Lo que hace

1. Elimina frases genericas de IA ("en el mundo actual", "es importante destacar", etc.)
2. Reemplaza transiciones robóticas con naturales
3. Elimina openings genericos ("Estimado cliente", "Es un placer...")
4. Varia estructura de oraciones
5. Limpia redundancias

## Tono IMPKT

- Directo: lo importante primero
- Tecnico sin ser inaccesible
- Sin jerga vacia
- Accion-oriented
