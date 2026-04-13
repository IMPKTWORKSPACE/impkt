#!/usr/bin/env python3
"""
IMPKT Proposal Generator
Genera propuestas comerciales en PDF con branding IMPKT.
Uso: python generate_proposal.py --business "Nombre" --contact "Contacto" --package landing --price 5000
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    print("ERROR: fpdf2 no instalado. Ejecuta: pip install fpdf2")
    sys.exit(1)


class IMPKTProposal(FPDF):
    def header(self):
        # Logo/barra superior
        self.set_fill_color(10, 10, 10)
        self.rect(0, 0, 210, 25, 'F')
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 7)
        self.cell(0, 10, 'IMPKT', ln=False)
        self.set_font('Helvetica', '', 9)
        self.set_xy(150, 8)
        self.cell(0, 5, 'Impacto medible, no promesas', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'IMPKT - Pagina {self.page_no()}', align='C')


def parse_args():
    parser = argparse.ArgumentParser(description='Generador de propuestas IMPKT')
    parser.add_argument('--business', required=True, help='Nombre del negocio')
    parser.add_argument('--contact', required=True, help='Nombre del contacto/decisor')
    parser.add_argument('--industry', default='PyME', help='Industria del negocio')
    parser.add_argument('--location', default='Mexico', help='Ciudad/Estado')
    parser.add_argument('--problem', default='', help='Problema principal del cliente')
    parser.add_argument('--package', required=True,
                        choices=['landing', 'corporativo', 'ecommerce', 'seo', 'social', 'whatsapp', 'email', 'automatizacion', 'full'],
                        help='Tipo de paquete')
    parser.add_argument('--setup', type=int, required=True, help='Costo de setup en MXN')
    parser.add_argument('--monthly', type=int, required=True, help='Costo mensual en MXN')
    parser.add_argument('--months', type=int, default=12, help='Meses de contrato (default 12)')
    parser.add_argument('--timeline', default='4 semanas', help='Timeline estimado')
    parser.add_argument('--output-dir', default='proposals', help='Directorio de output')
    parser.add_argument('--notes', default='', help='Notas adicionales')
    return parser.parse_args()


SERVICES = {
    'landing': {
        'name': 'Landing Page',
        'description': 'Pagina de inicio optimizada para conversion con diseno premium, SEO local y WhatsApp CTA.',
        'includes': [
            'Diseno UX/UI personalizado',
            'Optimizacion SEO local',
            'Integracion WhatsApp',
            'Meta tags y Open Graph',
            'Responsive (mobile-first)',
            'Formulario de contacto',
        ]
    },
    'corporativo': {
        'name': 'Sitio Corporativo',
        'description': 'Sitio web profesional con multiples secciones, blog y sistema de contacto.',
        'includes': [
            'Hasta 10 secciones personalizadas',
            'Diseno UX/UI profesional',
            'SEO avanzado',
            'Blog integrado',
            'Formularios avanzados',
            'Google Analytics',
        ]
    },
    'ecommerce': {
        'name': 'E-commerce',
        'description': 'Tienda en linea completa con catalogo, pagos y gestion de inventario.',
        'includes': [
            'Catalogo de productos',
            'Pasarela de pagos',
            'Carrito de compras',
            'Panel de administracion',
            'SEO para productos',
            'Integracionenvios',
        ]
    },
    'seo': {
        'name': 'SEO Local',
        'description': 'Estrategia integral de SEO local para Google Business Profile y posicionamiento organico.',
        'includes': [
            'Auditoria SEO completa',
            'Optimizacion Google Business',
            'Contenido SEO (4 articulos/mes)',
            'Backlinks locales',
            'Reseñas de Google',
            'Reporte mensual de metricas',
        ]
    },
    'social': {
        'name': 'Social Media',
        'description': 'Gestion de redes sociales con contenido estrategico y engagement.',
        'includes': [
            '20 posts/mes (diseno propio)',
            'Calendario de contenido',
            'Estrategia por plataforma',
            'Reporte de engagement',
            '2 ads campaigns/mes',
        ]
    },
    'whatsapp': {
        'name': 'WhatsApp Automation',
        'description': 'Automatizacion de WhatsApp Business para atencion y conversion.',
        'includes': [
            'Chatbot de atencion',
            'Respuestas automaticas',
            'Catalogode productos en WhatsApp',
            'Integracion CRM basica',
            'Dashboard de conversaciones',
        ]
    },
    'email': {
        'name': 'Email Automation',
        'description': 'Secuencias de email marketing para nurturing y conversion.',
        'includes': [
            'Setup de plataforma email',
            '3 secuencias automatizadas',
            'Templates personalizados',
            'Segmentacion de listas',
            'Reporte mensual',
        ]
    },
    'automatizacion': {
        'name': 'Automatizacion Integral',
        'description': 'Sistema completo de automatizacion para operaciones del negocio.',
        'includes': [
            'WhatsApp + Email automation',
            'CRM basico',
            'Dashboard de metricas',
            'Integracion de canales',
            'Training de uso',
        ]
    },
    'full': {
        'name': 'Paquete Integral',
        'description': 'Solucion digital completa para presencia y automatizacion.',
        'includes': [
            'Sitio web profesional',
            'SEO local',
            'WhatsApp Automation',
            'Email Marketing',
            'Social Media (10 posts/mes)',
            'CRM basico',
            'Reporting mensual',
        ]
    },
}


def format_mxn(amount):
    return f"${amount:,.0f} MXN".replace(',', '.')


def generate_proposal(args):
    service = SERVICES[args.package]
    total_contract = args.setup + (args.monthly * args.months)

    pdf = IMPKTProposal()
    pdf.set_auto_page_break(auto=True, margin=20)

    # === PAGINA 1: PORTADA ===
    pdf.add_page()
    pdf.ln(30)

    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(10, 10, 10)
    pdf.multi_cell(0, 10, f'Propuesta Comercial\n{service["name"]}', align='C')
    pdf.ln(10)

    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, f'Para: {args.business}\nContacto: {args.contact}\nIndustria: {args.industry}\nUbicacion: {args.location}', align='C')
    pdf.ln(15)

    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(10, 10, 10)
    pdf.cell(0, 10, f'Valor Total del Proyecto: {format_mxn(total_contract)}', align='C', ln=True)
    pdf.ln(5)

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f'Vigencia: {datetime.now().strftime("%B %d, %Y")}', align='C', ln=True)
    pdf.cell(0, 6, f'Timeline estimado: {args.timeline}', align='C', ln=True)

    pdf.ln(20)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(0, 5, '"Impacto medible, no promesas"\nSi no lo podemos medir, no te lo vendemos.', align='C')

    # === PAGINA 2: PROPUESTA ===
    pdf.add_page()

    # Problema / Solucion
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(10, 10, 10)
    pdf.cell(0, 10, 'Diagnostico y Propuesta de Valor', ln=True)
    pdf.ln(3)

    if args.problem:
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 6, f'Su negocio enfrenta el desafio de: {args.problem}')
        pdf.ln(5)

    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, service['description'])
    pdf.ln(8)

    # Que incluye
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(10, 10, 10)
    pdf.cell(0, 10, 'Que incluye el servicio:', ln=True)
    pdf.ln(2)

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(60, 60, 60)
    for item in service['includes']:
        pdf.set_x(15)
        pdf.cell(5, 6, chr(149), ln=False)  # bullet
        pdf.cell(0, 6, item, ln=True)
    pdf.ln(8)

    # Timeline
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(10, 10, 10)
    pdf.cell(0, 10, 'Timeline de Entrega', ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, f'{args.timeline} desde la aprobacion y pago del setup.', ln=True)
    pdf.ln(8)

    # Notas adicionales
    if args.notes:
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(10, 10, 10)
        pdf.cell(0, 10, 'Notas Adicionales', ln=True)
        pdf.ln(2)
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 6, args.notes)

    # === PAGINA 3: INVERSION ===
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(10, 10, 10)
    pdf.cell(0, 10, 'Estructura de Inversion', ln=True)
    pdf.ln(5)

    # Tabla de precios
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(100, 10, 'Concepto', border=1, fill=True, ln=False)
    pdf.cell(50, 10, 'Monto', border=1, fill=True, align='R', ln=True)

    pdf.set_font('Helvetica', '', 11)
    pdf.cell(100, 9, 'Setup (instalacion y configuracion)', border=1, ln=False)
    pdf.cell(50, 9, format_mxn(args.setup), border=1, align='R', ln=True)

    pdf.cell(100, 9, f'Mensualidad (primer {args.months} meses)', border=1, ln=False)
    pdf.cell(50, 9, format_mxn(args.monthly), border=1, align='R', ln=True)

    pdf.cell(100, 9, f'Meses de contrato', border=1, ln=False)
    pdf.cell(50, 9, str(args.months), border=1, align='R', ln=True)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(100, 10, 'TOTAL CONTRATO', border=1, fill=True, ln=False)
    pdf.cell(50, 10, format_mxn(total_contract), border=1, fill=True, align='R', ln=True)

    pdf.ln(12)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 5, f'Forma de pago: 50% al inicio, 50% a la entrega del proyecto.\nEl precio de setup incluye el primer mes de servicio.\nContrato minimo de {args.months} meses.')

    # === PAGINA 4: TERMINOS ===
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(10, 10, 10)
    pdf.cell(0, 10, 'Terminos y Condiciones', ln=True)
    pdf.ln(5)

    terms = [
        ('Duracion minima', f'El contrato tiene una duracion minima de {args.months} meses. Despues del periodo inicial, el contrato se renueva automaticamente de mes a mes.'),
        ('Contenido del cliente', 'El cliente es responsable de proporcionar todo el contenido (textos, imagenes, logos) en un maximo de 5 dias habiles tras aprobacion del brief.'),
        ('Cambios', 'Se incluyen hasta 2 rondas de cambios menores. Cambios mayores tienen costo adicional.'),
        ('Propiedad intelectual', 'Una vez pagado el 100% del proyecto, el cliente es propietario del sitio/webapp, incluyendo codigo fuente.'),
        ('Soporte tecnico', 'El soporte tecnico esta incluido durante el periodo del contrato. Issues criticos: respuesta en 24h. Issues menores: 48h.'),
        ('Garantia', 'Garantia de 30 dias para bugs de desarrollo. La garantia no cubre cambios de contenido ni nuevas funcionalidades.'),
        ('Datos y privacidad', 'IMPKT no almacena datos personales de los clientes finales del CONTRACTANTE. Cada proyecto es independiente.'),
    ]

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    for title, content in terms:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(10, 10, 10)
        pdf.cell(0, 7, f'{title}:', ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 5, content)
        pdf.ln(3)

    # === PAGINA FINAL ===
    pdf.add_page()

    pdf.ln(20)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(10, 10, 10)
    pdf.cell(0, 10, 'Proximo Paso', ln=True)
    pdf.ln(5)

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, f'Para comenzar el proyecto:\n\n1. Revisa y firma esta propuesta\n2. Realiza el pago del 50% de setup: {format_mxn(args.setup // 2)}\n3. Agendamos una llamada de kickoff\n\nTe esperamos.')
    pdf.ln(15)

    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(10, 10, 10)
    pdf.cell(0, 8, 'Contacto IMPKT', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, 'WhatsApp: 8115339022', ln=True)
    pdf.cell(0, 7, 'Web: impakt.mx (proximamente)', ln=True)

    pdf.ln(15)
    pdf.set_fill_color(10, 10, 10)
    pdf.rect(0, pdf.get_y(), 210, 2, 'F')

    # Save
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    slug = args.business.lower().replace(' ', '-').replace('_', '-')
    filename = f"IMPKT-Propuesta-{service['name'].replace(' ', '-')}-{slug}-{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = output_dir / filename
    pdf.output(str(filepath))
    return filepath


if __name__ == '__main__':
    args = parse_args()
    filepath = generate_proposal(args)
    print(f"[OK] Propuesta generada: {filepath}")
