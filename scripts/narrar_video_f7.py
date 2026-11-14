"""Añade locución local honesta al recorrido público, sin usar proveedor IA."""
import json
import subprocess
import sys
from pathlib import Path
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'evidencias/32_recorrido_publico_duracion_pauta_sin_ia.webm'
TARGET=ROOT/'evidencias/33_recorrido_publico_narrado.mp4'
TMP=ROOT/'.venv/narracion-f7';TMP.mkdir(exist_ok=True)
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
SEGMENTS=[
 (0,12,"Pulso Comercial IA responde a un problema frecuente: las ventas, las metas y los resultados quedan dispersos en planillas. La gerencia necesita detectar brechas sin confundir cumplimiento con crecimiento."),
 (13,25,"Esta es la aplicación pública. Entramos sin iniciar sesión y usamos solo datos ficticios de demostración. El archivo comercial de una empresa no forma parte de esta grabación."),
 (27,45,"El motor de Python valida el archivo, calcula con Decimal y presenta facturación real, meta, cumplimiento, brecha y variación interanual. La meta se compara con las ventas del mismo período."),
 (47,65,"El gráfico muestra la evolución mensual. Para comparar años, Pulso exige los mismos meses y cobertura suficiente. Cuando falta información, muestra no comparable en vez de completar con ceros."),
 (67,83,"En Dónde mirar aparecen las mayores brechas negativas por canal. Su participación usa la suma de brechas negativas de esa dimensión. No sumamos rankings de canales con los de líneas."),
 (85,99,"Los volúmenes se mantienen separados por unidad. Kilogramos pueden mostrarse como toneladas; las unidades físicas se presentan por su cuenta. Nunca se suma kilogramaje con unidades."),
 (101,113,"El botón de análisis usa un modelo real para interpretar hechos ya calculados. En esta toma no lo activo: preservamos el cupo docente y no fingimos una respuesta nueva."),
 (115,123,"La arquitectura es sencilla: Flask recibe el CSV en memoria, un validador revisa el contrato y Python calcula indicadores trazables con identificadores."),
 (125,139,"Después, un prompt versionado guía al modelo. La respuesta se valida contra el esquema y sus referencias antes de mostrarla. Probamos las versiones uno y dos con diez casos reales, con resultados documentados."),
 (141,160,"Aplicamos un filtro y el panel recalcula los indicadores. Pulso es una hipótesis de servicio por suscripción para pequeñas empresas. El análisis es descriptivo: no demuestra causas ni reemplaza decisiones humanas. El código y la ficha están publicados en GitHub."),
]
def duration(file):
 r=subprocess.run([FFMPEG,'-i',str(file)],capture_output=True,text=True)
 import re
 m=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',r.stderr)
 if not m:raise RuntimeError(f'No duration for {file.name}')
 return int(m[1])*3600+int(m[2])*60+float(m[3])
files=[]
for i,(start,end,text) in enumerate(SEGMENTS,1):
 f=TMP/f'segmento_{i:02}.aiff'
 subprocess.run(['say','-v','Paulina','-r','205','-o',str(f),'--',text],check=True)
 sec=duration(f)
 files.append(f)
 print(json.dumps({'segmento':i,'inicio':start,'fin':end,'voz_segundos':round(sec,2),'cabe':sec<=end-start},ensure_ascii=False),flush=True)
 # Los tramos se revisan juntos antes de mezclar; los solapamientos leves se corrigen.
if '--prepare' in sys.argv:sys.exit(0)
inputs=[];filters=[];labels=[]
for i,((start,_,_),f) in enumerate(zip(SEGMENTS,files),1):
 inputs.extend(['-i',str(f)])
 filters.append(f'[{i}:a]adelay={start*1000}|{start*1000},aresample=44100[a{i}]')
 labels.append(f'[a{i}]')
filters.append(''.join(labels)+f'amix=inputs={len(labels)}:duration=longest:dropout_transition=0,apad[aout]')
cmd=[FFMPEG,'-y','-i',str(SOURCE),*inputs,'-filter_complex',';'.join(filters),'-map','0:v','-map','[aout]','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(TARGET)]
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode:raise RuntimeError(r.stderr[-2000:])
print(json.dumps({'video':str(TARGET),'duracion':duration(TARGET),'bytes':TARGET.stat().st_size},ensure_ascii=False))
