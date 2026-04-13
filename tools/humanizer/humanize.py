#!/usr/bin/env python3
"""
IMPKT Content Humanizer
Post-procesa texto generado por IA para que suene natural.
Uso: python humanize.py "Tu texto aqui"
"""

import re
import sys

# Frases genericas de IA a eliminar o reemplazar
GENERIC_PHRASES = [
    (r'en el mundo actual', ''),
    (r'es importante destacar', ''),
    (r'en conclusion', 'En resumen'),
    (r'por otro lado', 'asi mismo'),
    (r'en primer lugar', ''),
    (r'ademas', ''),
    (r'asimismo', ''),
    (r'de igual manera', ''),
    (r'no obstante', 'sin embargo'),
    (r'sin embargo', ''),
    (r'es necesario mencionar', ''),
    (r'en cuanto a', 'sobre'),
    (r'con respecto a', 'sobre'),
    (r'relativo a', 'sobre'),
    (r'ai\.', 'IA.'),
    (r'artificial intelligence', 'inteligencia artificial'),
    (r'\bademas\b', ''),
    (r' cabe destacar', ''),
    (r'\bvale la pena\b', ''),
    (r'en este sentido', ''),
    (r'para ello', ''),
    (r'de tal manera', ''),
    (r'ahora bien', ''),
]

# Patrones que indican texto generico de IA
AI_PATTERNS = [
    r'estamos comprometidos',
    r'comprometidos con',
    r'brindamos soluciones',
    r'soluciones innovadoras',
    r'lideres en',
    r'gracias por su confianza',
    r'confiar en nosotros',
    r'no dude en contactarnos',
    r'estamos a sus ordenes',
]

# Marcadores de texto de IA a revisar
WATCH_WORDS = [
    'sin duda', 'indudablemente', 'cabe remarquear',
    'resulta fundamental', 'resulta necesario', 'es preciso',
    'se hace imperativo', 'no se puede negar',
]


def humanize(text: str) -> str:
    """Transforma texto generico de IA en texto natural."""

    # 1. Eliminar frases genericas
    for pattern, replacement in GENERIC_PHRASES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # 2. Eliminar espacios multiples causados por removals
    text = re.sub(r'\s+', ' ', text)

    # 3. Hacer que las transiciones sean mas naturales
    text = re.sub(r'\. +(\w)', lambda m: f'. {m.group(1).lower()}', text)

    # 4. Eliminar frases de opening genericas
    openings = [
        r'^Buenos dias,?\s*',
        r'^Buenas tardes,?\s*',
        r'^Buenas noches,?\s*',
        r'^Estimado cliente,?\s*',
        r'^Querido cliente,?\s*',
    ]
    for pattern in openings:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # 5. Cortar si empieza con "Es un placer" o similar
    text = re.sub(r"^es un placer[\s,]+", '', text, flags=re.IGNORECASE)
    text = re.sub(r"^me complace[\s,]+", '', text, flags=re.IGNORECASE)
    text = re.sub(r"^con mucho gusto[\s,]+", '', text, flags=re.IGNORECASE)

    # 6. Eliminar watch words si aparecen multiples veces
    for word in WATCH_WORDS:
        count = len(re.findall(rf'\b{re.escape(word)}\b', text, re.IGNORECASE))
        if count > 1:
            text = re.sub(rf'\b{re.escape(word)}\b', '', text, flags=re.IGNORECASE)

    # 7. Limpiar comas redundantes antes de puntos
    text = re.sub(r',\s*,', ',', text)
    text = re.sub(r',\s*\.', '.', text)
    text = re.sub(r'\.\s*\.', '.', text)

    # 8. Trim final
    text = text.strip()

    return text


def main():
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = sys.stdin.read()

    result = humanize(text)
    print(result)


if __name__ == '__main__':
    main()
