"""Genera la ficha ejecutiva de una página con hipótesis y fuentes explícitas."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/FICHA_NEGOCIO.pdf'
navy=colors.HexColor('#102030'); teal=colors.HexColor('#087E83'); gray=colors.HexColor('#51616F')
styles={
 'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=19,leading=23,textColor=navy,spaceAfter=5),
 'sub':ParagraphStyle('sub',fontName='Helvetica',fontSize=9.3,leading=13,textColor=gray,spaceAfter=10),
 'h':ParagraphStyle('h',fontName='Helvetica-Bold',fontSize=9.3,leading=12,textColor=teal,spaceBefore=8,spaceAfter=2),
 'p':ParagraphStyle('p',fontName='Helvetica',fontSize=8.4,leading=12,textColor=navy,spaceAfter=3),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=7.1,leading=10,textColor=gray,spaceAfter=3),
}
def para(text,style='p'):return Paragraph(text,styles[style])
parts=[para('PULSO COMERCIAL IA','title'),para('Ficha de negocio | Proyecto final Advanced Prompt Engineering | 13 noviembre 2026','sub')]
def section(h,text):parts.extend([para(h,'h'),para(text)])
section('CLIENTE, PROBLEMA Y PROPUESTA','Gerencias comerciales y dueños de pymes distribuidoras o mayoristas que consolidan ventas y metas en planillas. Hipótesis de valor: pasar de un CSV a indicadores y una lectura ejecutiva verificable en minutos; el tiempo ahorrado no está medido.')
section('PRODUCTO E IA','Demo pública con CSV ficticio, filtros, facturación, metas, cumplimiento, brechas, evolución y ranking. Python valida y calcula con Decimal; GPT-6.1 Sol interpreta hechos con IDs; el usuario decide. El validador rechaza cifras sin respaldo y marca cobertura parcial. No se infieren causas ni se hacen pronósticos.')
section('MODELO DE INGRESOS','Hipótesis SaaS B2B: suscripción mensual por empresa/equipo o cupo de análisis, con demo gratuita. Precio, disposición a pagar e ingresos aún no validados; no existen cobros en el MVP.')
parts.append(para('COSTO OPERATIVO ESTIMADO (USD/MES)','h'))
data=[['Uso mensual','IA estimada','Cloud compute/HTTP','Otros supuestos','Total estimado'],['100 análisis','2,31-2,64','0,07','2,00','4,38-4,71'],['1.000 análisis','23,10-26,40','0,71','2,00','25,81-29,11']]
t=Table(data,colWidths=[83,83,112,91,102],hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),7.5),('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,1),(-1,-1),0.3,colors.HexColor('#D2DCE0'))]));parts.append(t)
parts.append(Spacer(1,5));parts.append(para('Supuestos: GPT-6.1 Sol Standard, 6.000 tokens de entrada y 900 de salida por intento; 10% de reintentos. Tarifas oficiales por millón: USD 2 entrada, USD 10 salida, USD 2,50 escritura de caché a 30 min. Cloud Run Santiago: 1 vCPU, 0,5 GiB, 20 s activos y ocho requests por análisis, sin free tier. “Otros” son provisión hipotética, no factura ni límite. Sin impuestos ni cambio CLP.','small'))
section('LÍMITES Y ESTADO','Solo datos ficticios en la entrega pública. CSV en memoria hasta 8 MiB/30.000 filas; no hay conectores, usuarios ni predicción. URL con IA real y secreto cloud activos; gasto y límites dependen del proveedor. Evaluación v1/v2 medida, sin afirmar mejora de v2. Prueba de un nuevo informe real tras la última corrección y video final pendientes.')
parts.append(para('App: https://pulso-comercial-ia-njsqy6x3ka-tl.a.run.app','small'))
parts.append(para('Código: https://github.com/fbahamondesc1992/pulso-comercial-ia','small'))
parts.append(para('Fuentes, consultadas 13-11-2026: https://developers.openai.com/api/docs/pricing ; https://cloud.google.com/run/pricing . Detalle de supuestos y gasto: docs/COSTOS_Y_LIMITACIONES.md. Los valores de la tabla son estimaciones, no gasto incurrido.','small'))
SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=32,title='Pulso Comercial IA - Ficha de negocio').build(parts)
print(OUT)
