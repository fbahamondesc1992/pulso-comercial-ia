# Prompts del producto

`analista_v1.md`: línea base funcional con rol, esquema, referencias, cifras mediante
marcadores, unidades, abstención y límites causales. No está deliberadamente degradada.

`analista_v2.md`: refuerza jerarquía frente a datos, prioridad por magnitud de brecha,
crecimiento vs. cumplimiento, brecha neta vs. negativa bruta, no sumar particiones,
estados N/C, abstención y acciones explícitas de investigación.

Ambas se cargan literalmente por `cargar_prompt`; no hay copia oculta en app.py.
`ANALYST_PROMPT_VERSION=v1|v2` selecciona la versión; v2 es la selección técnica para el MVP tras la evaluación final: 10/10 frente
a 9/10 de v1, con dos reintentos. Sin reintento, 8/10 frente a 9/10. No es superioridad
estadística general; revisión humana de la nueva muestra pendiente. Rollback: seleccionar v1 y reiniciar el servicio.
Se registra SHA256 del archivo en cada evaluación y versión en la respuesta web.
Un reintento añade una instrucción fija de corrección y no incorpora salida inválida.

Contrato: cifras únicamente como `{{F001}}`, siempre con ID existente y citado.
Python expande el marcador a nombre del indicador, cifra y unidad. Una cifra literal,
incluso plausible, se rechaza conservadoramente por no asegurar correspondencia
inequívoca. No se transforma el LLM en calculadora. El texto interpretativo sí es
generativo cuando se llama al proveedor real. El modo mock no cuenta como IA.

Proveedor preparado: OpenAI Responses API, `gpt-6.1-sol`, reasoning.effort=low,
max_output_tokens=1800, timeout=20 s, SDK max_retries=0, store=false, sin tools.
Conexión real en la cuenta comprobada con HTTP 200 y respuesta OK. No se promete determinismo.
El identificador publicado no ofrece un snapshot fechado distinto en la página
consultada: registrar también el modelo que retorna cada respuesta.

El diagnóstico usa hasta 45 hechos: total, volumen por unidad y top dos brechas
por cada dimensión. No se envían CSV ni etiquetas arbitrarias en producción: alias.
GS-07 conserva intencionalmente la etiqueta maliciosa sintética para evaluar la
segunda barrera, el prompt, además de la protección de alias de producción.

Fuentes oficiales consultadas el 12-11-2026:
- https://developers.openai.com/api/docs/models/gpt-6.1-sol
- https://developers.openai.com/api/docs/guides/structured-outputs

Ver `docs/MEJORA_PROMPTS.md`: evaluación G1 real autorizada hasta USD 2 acumulados.
Los prompts v1/v2 se preservan sin cambios durante la comparación. Servicio Standard,
prompt_cache_options.ttl=30m; no usa el parámetro de retención anterior incompatible.

Estado vigente fase 18: F4 cerrado por aprobación global explícita del usuario;
selección técnica v2 confirmada para el MVP. Evidencia 18_cierre_f4_inicio_f6.json.
Los campos individuales históricos no se rellenan ni alteran. F6 en preparación,
G3 pendiente, disponibilidad solicitada hasta 30-11-2026 (Chile). Ver PLAN_F6.md
en docs/.
