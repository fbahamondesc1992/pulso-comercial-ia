# Prompts del producto

`analista_v1.md`: línea base funcional con rol, esquema, referencias, cifras mediante
marcadores, unidades, abstención y límites causales. No está deliberadamente degradada.

`analista_v2.md`: refuerza jerarquía frente a datos, prioridad por magnitud de brecha,
crecimiento vs. cumplimiento, brecha neta vs. negativa bruta, no sumar particiones,
estados N/C, abstención y acciones explícitas de investigación.

Ambas se cargan literalmente por `cargar_prompt`; no hay copia oculta en app.py.
`ANALYST_PROMPT_VERSION=v1|v2` selecciona la versión; v2 es la candidata local,
NO una ganadora medida. Rollback: seleccionar v1 y reiniciar el servicio.
Se registra SHA256 del archivo en cada evaluación y versión en la respuesta web.
Un reintento añade una instrucción fija de corrección y no incorpora salida inválida.

Contrato: cifras únicamente como `{{F001}}`, siempre con ID existente y citado.
Python expande el marcador a nombre del indicador, cifra y unidad. Una cifra literal,
incluso plausible, se rechaza conservadoramente por no asegurar correspondencia
inequívoca. No se transforma el LLM en calculadora. El texto interpretativo sí es
generativo cuando se llama al proveedor real. El modo mock no cuenta como IA.

Proveedor preparado: OpenAI Responses API, `gpt-5.6-terra`, reasoning.effort=none,
max_output_tokens=1800, timeout=20 s, SDK max_retries=0, store=false, sin tools.
La disponibilidad en la cuenta NO se ha comprobado. No se promete determinismo.
El identificador publicado no ofrece un snapshot fechado distinto en la página
consultada: registrar también el modelo que retorna cada respuesta.

El diagnóstico usa hasta 45 hechos: total, volumen por unidad y top dos brechas
por cada dimensión. No se envían CSV ni etiquetas arbitrarias en producción: alias.
GS-07 conserva intencionalmente la etiqueta maliciosa sintética para evaluar la
segunda barrera, el prompt, además de la protección de alias de producción.

Fuentes oficiales consultadas el 12-11-2026:
- https://developers.openai.com/api/docs/models/gpt-5.6-terra
- https://developers.openai.com/api/docs/guides/structured-outputs

Ver `docs/MEJORA_PROMPTS.md`: G1 anterior recibido; evaluación real pendiente de
revisión de presupuesto/migración al nuevo modelo solicitado GPT-6.1 Sol.
Estas especificaciones corresponden al adaptador actual, todavía sin migrar.
