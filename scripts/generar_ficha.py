"""Ficha de una página. Mantener pendientes explícitos hasta completar F4/F6/F7."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
INK=colors.HexColor('#12252B')
GREEN=colors.HexColor('#22705A')
GRAY=colors.HexColor('#53616B')


def generar():
    output=ROOT/'docs/FICHA_NEGOCIO.pdf'
    styles={
        'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=28,leading=31,textColor=INK,spaceAfter=8),
        'sub':ParagraphStyle('sub',fontName='Helvetica',fontSize=11,leading=15,textColor=GRAY,spaceAfter=12),
        'head':ParagraphStyle('head',fontName='Helvetica-Bold',fontSize=10,leading=13,textColor=GREEN,spaceBefore=13,spaceAfter=5),
        'body':ParagraphStyle('body',fontName='Helvetica',fontSize=9.2,leading=13,textColor=INK,spaceAfter=5),
        'small':ParagraphStyle('small',fontName='Helvetica',fontSize=7.3,leading=10,textColor=GRAY,spaceAfter=4),
        'cell':ParagraphStyle('cell',fontName='Helvetica',fontSize=9,leading=12,textColor=INK),
    }
    def p(text,style='body'):return Paragraph(text,styles[style])
    story=[p('PULSO COMERCIAL IA','title'),p('De una planilla de ventas a una explicación ejecutiva verificable.','sub'),
           p('<b>FICHA DE NEGOCIO · 12 NOV 2026 · VERSIÓN LOCAL</b><br/>IA real, publicación, repositorio y video: pendientes de sus siguientes etapas.','small')]
    for title,text in [
        ('CLIENTE Y PROBLEMA','Gerencias comerciales y dueños de pymes distribuidoras o mayoristas. Las ventas y metas dispersas en planillas consumen tiempo y facilitan comparaciones incorrectas. El pagador propuesto es la empresa o el equipo comercial.'),
        ('SOLUCIÓN Y VALOR DIFERENCIAL','CSV ficticio, indicadores exactos, filtros y brechas por canal, línea y oficina. Un LLM redacta la lectura ejecutiva sobre hechos con IDs. La rapidez es una hipótesis de valor aún no medida; la trazabilidad permite revisar la evidencia de cada hallazgo.'),
        ('ROL CENTRAL DE LA IA','Python calcula y valida; la IA interpreta; el usuario decide. OpenAI Responses API, modelo candidato <b>gpt-5.6-terra</b>, prompts v1/v2 y diez casos. La validación local usa mocks; <b>no hay mejora real medida todavía</b>. Las cifras se insertan desde hechos, no desde cálculos del modelo.'),
        ('MODELO DE INGRESOS','Hipótesis: suscripción SaaS B2B mensual por empresa/equipo o cupo de análisis, con demo gratuita. Precio y disposición a pagar pendientes de validación. Sin cobros ni clientes pagadores declarados.'),
    ]:story += [p(title,'head'),p(text)]
    story += [p('COSTO OPERATIVO ESTIMADO · USD / MES','head')]
    data=[[p('<b>Escenario</b>','cell'),p('<b>IA</b>','cell'),p('<b>Cloud / otros</b>','cell'),p('<b>Total</b>','cell')],
          [p('100 análisis','cell'),p('2,51','cell'),p('0,07 + 2,00','cell'),p('<b>4,58</b>','cell')],
          [p('1.000 análisis','cell'),p('25,08','cell'),p('0,71 + 2,00','cell'),p('<b>27,79</b>','cell')]]
    table=Table(data,colWidths=[175,80,150,106])
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E4F1EB')),('BACKGROUND',(0,1),(-1,-1),colors.HexColor('#F4F7F6')),
                               ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#B7CEC2'))]))
    story += [table,Spacer(1,7),p('Supuestos: 6.000 tokens de entrada, 900 de salida; USD 2/12 por millón, respectivamente; 10% de reintentos. Cloud Run Santiago: 1 vCPU, 0,5 GiB, 20 s activos y ocho requests por análisis, sin free tier. Otros: provisión hipotética de USD 2/mes para builds, imagen, secretos, logs y tráfico; no es tarifa ni tope garantizado. Sin impuestos. <b>Estimación, no gasto incurrido.</b>','small'),
              p('LÍMITES Y ESTADO DE ENTREGA','head'),p('Solo datos ficticios; análisis descriptivo, sin causalidad ni pronósticos. Dependencia del proveedor y riesgo de consumo público. Los límites locales son volátiles; cuotas, alertas y secretos cloud aún no están configurados. URL pública y GitHub: <b>PENDIENTES</b>. Video: <b>NO GRABADO</b>.'),
              p('FUENTES Y TRAZABILIDAD','head'),p('<link href="https://developers.openai.com/api/docs/models/gpt-5.6-terra" color="#22705A">OpenAI: modelo y tarifas</link> · <link href="https://cloud.google.com/run/pricing" color="#22705A">Google Cloud Run: tarifas por región</link> · Consulta: 12-11-2026.<br/>Cálculos, supuestos y limitaciones ampliados en docs/COSTOS_Y_LIMITACIONES.md.','small')]
    def footer(canvas,doc):
        canvas.setStrokeColor(colors.HexColor('#C9D5D0'));canvas.line(42,40,553,40)
        canvas.setFont('Helvetica',7);canvas.setFillColor(GRAY)
        canvas.drawString(42,27,'Proyecto final · Advanced Prompt Engineering · Universidad Adolfo Ibáñez')
        canvas.drawRightString(553,27,'Ficha preliminar / 1')
    doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=52,
                          title='Pulso Comercial IA | Ficha de negocio',author='Pulso Comercial IA')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    pages=len(PdfReader(output).pages)
    if pages!=1:raise RuntimeError(f'La ficha tiene {pages} páginas, debe tener exactamente una.')
    print(output, '· 1 página comprobada')


if __name__=='__main__':generar()
