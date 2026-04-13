#!/usr/bin/env python3
"""
IMPKT Lead Research Tool
Investiga un prospecto dado su URL o nombre de negocio.
Uso: python research.py --name "Restaurante La Casa"
"""

import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess

WORKSPACE = Path("C:/Users/oscar/impkt")
RESEARCH_DIR = WORKSPACE / "pipeline" / "research"


def fetch_url(url: str) -> str:
    """Fetch URL content using curl."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "--max-time", "15", "--user-agent",
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
             url],
            capture_output=True, text=True, timeout=20
        )
        return result.stdout[:5000]
    except Exception as e:
        return f"ERROR fetching {url}: {e}"


def extract_name(text: str) -> str:
    """Extract business name from page title or text."""
    title_match = re.search(r'<title>([^<]+)</title>', text, re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', text, re.IGNORECASE)
    if h1_match:
        return h1_match.group(1).strip()
    return "Nombre no identificado"


def extract_social(text: str) -> list:
    """Extract social media links."""
    social = []
    patterns = {
        "Instagram": r'instagram\.com/[\w.]+',
        "Facebook": r'facebook\.com/[\w.]+',
        "LinkedIn": r'linkedin\.com/[\w./]+',
        "Twitter/X": r'(twitter\.com|x\.com)/[\w.]+',
    }
    for name, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            social.append(f"{name}: https://{matches[0]}")
    return social


def extract_contact(text: str) -> dict:
    """Extract contact information."""
    contact = {}

    # Email
    email_match = re.search(r'[\w.-]+@[\w.-]+\.\w+', text)
    if email_match:
        contact['email'] = email_match.group(0)

    # Phone
    phone_match = re.search(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        contact['phone'] = phone_match.group(0)

    # WhatsApp
    wa_match = re.search(r'wa\.me/\d+|whatsapp\.com/[\w./]+', text, re.IGNORECASE)
    if wa_match:
        contact['whatsapp'] = f"https://{wa_match.group(0)}"

    return contact


def evaluate_presence(url: str, text: str) -> dict:
    """Evaluate the digital presence of the business."""
    text_lower = text.lower()
    presence = {}

    presence['has_website'] = True  # We fetched it so it exists
    presence['has_contact_form'] = 'contact' in text_lower or 'formulario' in text_lower
    presence['has_prices'] = '$' in text or 'precio' in text_lower or 'menu' in text_lower
    presence['has_social'] = any(s in text_lower for s in ['instagram', 'facebook', 'linkedin', 'twitter'])
    presence['has_whatsapp'] = 'whatsapp' in text_lower or 'wa.me' in text_lower
    presence['has_seo'] = 'google' in text_lower or 'seo' in text_lower or 'business' in text_lower

    # Check if mobile-friendly (basic)
    presence['has_mobile_viewport'] = 'viewport' in text_lower
    presence['is_https'] = url.startswith('https')

    return presence


def identify_opportunities(presence: dict) -> list:
    """Identify what IMPKT can offer based on gaps."""
    opportunities = []
    if not presence.get('has_whatsapp'):
        opportunities.append("WhatsApp Automation — atencion 24/7 y conversion")
    if not presence.get('has_contact_form'):
        opportunities.append("Formulario de contacto + Landing Page")
    if not presence.get('has_social'):
        opportunities.append("Social Media — generar presencia digital")
    if not presence.get('has_seo'):
        opportunities.append("SEO Local — aparecer en Google cuando busquen en su zona")
    if not presence.get('has_prices'):
        opportunities.append("Catalogo digital o menu online")
    if not presence.get('is_https'):
        opportunities.append("SSL + HTTPS — seguridad y SEO")
    if not presence.get('has_mobile_viewport'):
        opportunities.append("Optimizacion mobile — sitio no preparado para celulares")
    return opportunities


def generate_slug(name: str) -> str:
    """Generate a URL-safe slug from business name."""
    slug = re.sub(r'[^\w\s-]', '', name.lower())
    slug = re.sub(r'[\s]+', '-', slug)
    return slug[:50]


def research_prospect(name: str, url: str = None) -> Path:
    """Research a prospect and save report."""
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

    slug = generate_slug(name)
    text = ""

    if url:
        print(f"Fetching {url}...")
        text = fetch_url(url)
    else:
        # Search for the business online
        print(f"No URL provided. Searching for '{name}'...")
        search_text = f"Business: {name}"
        text = search_text

    business_name = extract_name(text) if text else name
    contact = extract_contact(text)
    social = extract_social(text)
    presence = evaluate_presence(url or "", text)
    opportunities = identify_opportunities(presence)

    # Calculate a simple score
    score = sum([
        presence.get('has_website', False) * 10,
        presence.get('has_contact_form', False) * 15,
        presence.get('has_prices', False) * 10,
        presence.get('has_social', False) * 15,
        presence.get('has_whatsapp', False) * 20,
        presence.get('is_https', False) * 5,
        presence.get('has_mobile_viewport', False) * 10,
        presence.get('has_seo', False) * 15,
    ])

    report = f"""# Research: {business_name}

**Fecha:** {datetime.now().strftime('%Y-%m-%d')}
**URL:** {url or 'No proporcionada'}
**Slug:** {slug}
**Lead score:** {score}/100

---

## Contacto

| Campo | Valor |
|-------|-------|
| Email | {contact.get('email', 'No encontrado')} |
| Telefono | {contact.get('phone', 'No encontrado')} |
| WhatsApp | {contact.get('whatsapp', 'No encontrado')} |

---

## Redes Sociales

{chr(10).join(f'- {s}' for s in social) if social else 'No se encontraron redes sociales'}

---

## Analisis de Presencia Digital

| Aspecto | Estado |
|---------|--------|
| Sitio web | {'Si' if presence.get('has_website') else 'No'} |
| HTTPS | {'Si' if presence.get('is_https') else 'No'} |
| Formulario de contacto | {'Si' if presence.get('has_contact_form') else 'No'} |
| Precios en linea | {'Si' if presence.get('has_prices') else 'No'} |
| Redes sociales | {'Si' if presence.get('has_social') else 'No'} |
| WhatsApp | {'Si' if presence.get('has_whatsapp') else 'No'} |
| SEO visible | {'Si' if presence.get('has_seo') else 'No'} |
| Mobile-friendly | {'Si' if presence.get('has_mobile_viewport') else 'No'} |

---

## Oportunidades para IMPKT

{chr(10).join(f'{i+1}. {o}' for i, o in enumerate(opportunities)) if opportunities else 'Ninguna oportunidad identificada — el negocio parece estar bien cubierto digitalmente.'}

---

## Score

**{score}/100** — {'Alta prioridad' if score < 40 else 'Media prioridad' if score < 70 else 'Baja prioridad'}

"""

    filepath = RESEARCH_DIR / f"{slug}.md"
    filepath.write_text(report, encoding="utf-8")
    return filepath


def parse_args():
    parser = argparse.ArgumentParser(description='Research de prospectos IMPKT')
    parser.add_argument('--name', required=True, help='Nombre del negocio')
    parser.add_argument('--url', default=None, help='URL del sitio web (opcional)')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    filepath = research_prospect(args.name, args.url)
    print(f"[OK] Research guardado: {filepath}")
