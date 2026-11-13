# Costos y límites · 12-11-2026

## Autorización vigente

El usuario declaró una carga de USD 5 y limitó la prueba de conexión y evaluación a
**USD 2 acumulados**, para reservar USD 3 al profesor. Este límite sustituye USD 3
inicialmente autorizado y la propuesta no aprobada de USD 7. No se verificó el saldo
real de billing. G3 y consumo público siguen sin autorizar; AI_ENABLED=false.

Modelo seleccionado: `gpt-6.1-sol`, Responses API, reasoning low, servicio Standard,
store=false, sin herramientas, caché con TTL de 30 minutos. No se utilizan Fast,
Ultrafast, residencia regional ni contexto largo. Salida máxima: 512 tokens en
conexión y 1.800 en evaluación, incluidos tokens de razonamiento; timeout 20 s.

## Precios y estimación operativa

Precios oficiales por millón de tokens: entrada USD 2; salida USD 10; lectura de
caché USD 0,10; escritura con TTL 30m USD 2,50. La escritura usa esa tarifa total,
no un recargo adicional. Consulta oficial el 12-11-2026:
- https://developers.openai.com/api/docs/models/gpt-6.1-sol
- https://developers.openai.com/api/docs/pricing?latest-pricing=standard
- https://developers.openai.com/api/docs/guides/prompt-caching

Supuesto por intento: 6.000 tokens de entrada y 900 de salida totales.
Costo estimado sin escritura: USD 0,021; valorando toda la entrada como escritura:
USD 0,024. Con 10% de reintentos: USD 0,0231–0,0264 por análisis. No son mediciones
reales ni tarifas garantizadas. Los descuentos de lectura no se presuponen.

Cloud Run Santiago: 1 vCPU, 512 MiB, min=0, max=1, concurrencia=4. Supuestos aún no
configurados: 20 s activos y ocho requests/análisis, sin free tier. Tarifas consultadas
previamente: CPU USD 0,0000336/vCPU-s, memoria USD 0,0000035/GiB-s y USD 0,40/millón
requests. Evidencia: 05_fuente_cloud_run.json. Compute estimado: USD 0,0007102/análisis.
Provisión hipotética adicional: USD 2/mes para builds, imagen, secretos, logs y tráfico.
No es una tarifa ni un tope; falta concretar recursos antes de G3.

| Análisis/mes | IA estimada | Compute/HTTP | Provisión otros | Total USD |
|---|---:|---:|---:|---:|
| 100 | 2,31–2,64 | 0,07102 | 2,00 | 4,38–4,71 |
| 1.000 | 23,10–26,40 | 0,71020 | 2,00 | 25,81–29,11 |

Sin impuestos, cambio CLP, créditos ni descuentos. Fuentes cloud:
https://cloud.google.com/run/pricing y https://docs.cloud.google.com/run/docs/locations.
La ficha PDF de fase 09 conserva el escenario histórico de GPT-5.6 Terra; esta hoja
sustituye sus estimaciones para el modelo actual. No se presenta la ficha como final.

## Control acumulado de la evaluación

Antes de cada intento se reserva USD 0,168: 60.000 tokens de entrada × 2,50/millón
más 1.800 de salida × 10/millón. La entrada reservada es una cota conservadora por
bytes UTF-8 más margen de esquema/framing, no una medición de tokens. Se verificó
que cada payload, prompt y esquema del golden set más 8.192 bytes queda bajo 60.000.

Cuando OpenAI reporta uso válido, se reemplaza esa reserva por su valoración superior:
entrada × USD 2,50/millón + salida × USD 10/millón. Los errores sin uso reportado
mantienen íntegra la reserva; no se les atribuye costo cero. Las respuestas incompletas
conservan tokens y estado de fallo. El costo estándar simple del informe es una
estimación, no factura; el compromiso conservador del registro controla el límite.

Registro persistente: entrega/13_presupuesto_ia.json, exclusivo mediante bloqueo de
archivo, escrito antes de la llamada y tras liquidar. Un reinicio no reinicia saldo;
una reserva interrumpida se conserva. Copia vigente publicable en evidencias/17_presupuesto_final.json; la copia de fase 13 se conserva.
El contador incluye intentos previos y limita el total a 66, según la ampliación G1
expresa para hasta 40 intentos adicionales a los 26 anteriores. Si no alcanza para la
siguiente reserva, se detiene. No se reintentan automáticamente errores del proveedor.
La batería se detiene si el proveedor no está disponible, evitando repetir fallos de
configuración. La validación de contenido permite como máximo un reintento por caso.

Inicio de la batería: tres intentos de conexión acumulados y compromiso USD 0,3096775:
USD 0,1416 reservado por el 401 histórico, USD 0,168 por el 400 de migración sin uso,
y USD 0,0000775 como valoración superior de la conexión válida (11 entrada/5 salida).
La documentación detectó que in_memory no era compatible con este modelo; se usó
prompt_cache_options.ttl=30m. La conexión válida respondió OK. Ningún fallo se oculta.

La ampliación autorizó la comparación final completa de fase 17, ya ejecutada: 22
intentos nuevos, 48 acumulados. Valoración superior nueva USD 0,264685; compromiso
acumulado USD 0,8490625 y margen USD 1,1509375 del límite de USD 2. No habilita
tráfico público ni gastar el margen automáticamente. El saldo real del proveedor
puede diferir por otros usos de la misma cuenta; billing no consultado.

## Límites de operación y privacidad

Límites locales de dashboard: 5 solicitudes/IP/h y 30 globales/h por proceso; cada
solicitud puede requerir dos intentos. Reinicios o nuevos workers reinician contadores:
no son un tope persistente para la demo pública. El presupuesto persistente descrito
arriba protege el evaluador, no el endpoint público. Antes de habilitar pruebas del
profesor se debe acotar el gasto del servicio y definir cómo usará el saldo reservado.

CSV ficticios exclusivamente, conservados en memoria; nunca se guardan uploads.
El proveedor recibe agregados con alias, no el CSV. Evidencias de evaluación contienen
solo casos y respuestas sintéticos. Secretos excluidos de Git, imagen y logs.
No hay cuotas, alertas, secretos cloud ni despliegue configurados. Las alertas de gasto
por sí solas no detienen consumo: https://docs.cloud.google.com/billing/docs/how-to/budgets.

## Fase 21 · publicación real del 13-11-2026

URL: https://pulso-comercial-ia-njsqy6x3ka-tl.a.run.app
Primera revisión sin IA: `pulso-comercial-ia-00001-lmv`; revisión activa:
`pulso-comercial-ia-00002-2gq`, 100% del tráfico. Imagen aprobada subida desde Docker
local; digest `sha256:725063e85c319ce0473374f0fab18dea720fabed47386fcf8122daa3b93af7e8`.
No se utilizó Cloud Build ni se reconstruyó la imagen.

Cloud Run: Santiago, CPU 1, memoria 512 MiB, concurrencia 1, mínimos 0, máximos
servicio/revisión 1, timeout 65 s, CPU por solicitud. Secreto `pulso-openai-key:1`,
acceso solo de `pulso-runtime` mediante secretAccessor sobre ese secreto.
Presupuesto verificado CLP 4900, exclusivo del proyecto, alertas 50/80/100%; no es
corte de gasto. Límite OpenAI USD 5 aplicado, gasto USD 0,51 y pertenencia de clave
confirmados por el usuario; autoriza al docente todo el cupo restante. No se cambió
el límite global ni el de otros proyectos. Fuente: 21_confirmacion_cupo_docente.json.

HTTP anónimo: inicio/health/demo/dashboard 200; protección de cabecera 403 y fuente
inválida 400. La primera revisión devuelve IA deshabilitada 503. Segunda revisión:
una solicitud pública real, HTTP 200, GPT-6.1-Sol, prompt v2, tres hallazgos,
26,969 s; IDs y snapshot válidos. Revisión asistida del texto sin causas afirmadas
ni suma de dimensiones superpuestas; conserva limitaciones. No equivale a aprobación humana.

Se reservaron dos intentos potenciales por USD 0,336 antes de activar y probar.
El endpoint no devuelve tokens ni número de intentos internos: reserva íntegra
conservada, 50 intentos contabilizados conservadoramente (48 anteriores y 2
potenciales), compromiso USD 1,1850625 de USD 2. No afirmar 50 llamadas observadas
ni USD 0,336 de consumo real. Registro previo preservado; evidencia 21_presupuesto_*.
Suite local: 152 passed en 0,62 s, sin red; no se modificó código de aplicación.

**F6 sigue EN_PROCESO:** falta recorrido visual en navegador incógnito a 375/1440,
capturas reales, expansión de evidencia y comprobación visual del error de cuota.
Herramienta de navegador no disponible; las pruebas HTTP no sustituyen esa evidencia.
F7: video real y actualización de ficha PDF aún pendientes.
