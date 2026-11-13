# Despliegue vigente

Plan aprobado conservado sin cambios en [PLAN_F6.md](PLAN_F6.md).
El historial de preparación, bloqueos y cambios está en BITACORA_ENTREGA.md.

## Fase 22 · corrección de carga multipart · 13-11-2026

El límite interno de formulario de 64 KiB rechazaba archivos válidos antes del
validador CSV. Se amplió a 128 KiB para admitir el bloque de lectura multipart y
su frontera; se conservan 2 MiB por archivo, 10.000 filas y el límite HTTP total.
Tres regresiones nuevas: cargas de 1.000/5.088 filas ficticias y campo de formulario
excesivo. Suite sin red: 155 passed en 0,87 s. Docker build linux/amd64 y carga
local de 441.670 bytes/5.088 filas: HTTP 200.

Revisión vigente `pulso-comercial-ia-00003-zjg`, 100% del tráfico. Digest:
`sha256:34edb0ba851c1fe5a0527f654d4629a20f838999aa607b0d909ebfb9ce2745ea`.
URL conservada. Pruebas públicas: health 200, CSV sintético 200, CSV 2 MiB+1
rechazado con 400 por el validador, petición 3 MiB rechazada con 413. La primera
comprobación esperaba 413 para ambos excesos y se corrigió esa expectativa;
no fue necesario otro cambio del producto. Evidencias: 22_upload_local.json y
22_upload_publico.json. Sin llamadas IA ni cambios en su ledger.

Archivo aportado preservado y excluido de Docker/Git; no enviado a nube ni IA.
El contrato CSV sigue exigiendo separador coma y punto decimal. F6 continúa
EN_PROCESO: recorrido visual público y capturas pendientes.

## Fase 21 · publicación inicial del 13-11-2026 (histórico)

URL: https://pulso-comercial-ia-njsqy6x3ka-tl.a.run.app
Primera revisión sin IA: `pulso-comercial-ia-00001-lmv`; revisión activa al cierre de fase 21:
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

## Operación

Para usar gcloud local: `source .venv/activar-gcloud.sh`. La configuración y
credenciales se conservan en .venv/gcloud-config, excluidas de Git.
Ante un error del proveedor, conservar dashboard y mostrar error controlado.
Para detener consumo IA, actualizar AI_ENABLED=false en el mismo servicio.
No eliminar recursos antes del 30-11-2026; retirada posterior por autorización.

## Fase 23 · CSV chileno · 13-11-2026

Se admite delimitador `;` con coma decimal y se mantiene delimitador `,` con punto
decimal. El dialecto se detecta por la cabecera; se conserva Decimal sin redondeo.
Se rechazan mezclas de dialectos, miles, negativos y más de 6 decimales conforme
al contrato vigente. Tests de equivalencia, textos con delimitadores entre comillas,
valores inválidos, duplicados y flujo HTTP: 167 passed en 0,90 s, sin red.

Build Docker linux/amd64 correcto. Revisión pública `pulso-comercial-ia-00004-fxk`,
100% tráfico, digest `sha256:4fe292b27809cbc2067ef283a34620f98ac3488b9de608d41b9cccc23175777a`.
Ambos formatos ficticios de 5.088 filas devolvieron HTTP 200 y respuestas iguales
localmente y en URL pública. Sin uso IA ni datos del usuario enviados. Evidencias
23_csv_chile_local.json y 23_csv_chile_publico.json.

El archivo del usuario, examinado solo localmente, aún falla en línea 5 por 7
decimales en facturacion_meta_clp; se observaron también 5 negativos en real CLP
y volumen real. No se redondeó ni alteró el archivo. F6 visual pendiente.

## Fase 24 · netos negativos y precisión de entrada · 13-11-2026

Facturación y volumen reales admiten negativos por devoluciones/ajustes; las metas
siguen no negativas. La ingesta conserva todos los decimales del CSV, con suma Decimal
y precisión de cálculo adaptada a la longitud de entrada; se redondea solo al mostrar.
Se agrega aviso de netos y de causalidad no verificable. El archivo aportado de
5.088 filas pasó validación local; quedó intacto y no se envió al servicio ni Git.

Suite sin red: 166 passed en 0,84 s. Build Docker linux/amd64 correcto.
Revisión `pulso-comercial-ia-00005-p4q`, 100% tráfico, digest
`sha256:9600e969f8d77f4dc9d9104c9b23df5f812a196d888f14f14a91b88984bcdc3a`.
Prueba pública con CSV ficticio: HTTP 200, valor negativo de 21 decimales conservado
y advertencia visible. Sin llamadas IA. Evidencia `evidencias/24_netos_publico.json`.
F6 sigue pendiente de recorrido visual/capturas.

## Fase 25 · límite CSV ampliado · 13-11-2026

Límite de filas aumentado a 30.000 y tamaño a 8 MiB en backend y frontend.
El margen multipart y el procesamiento en memoria se conservan. Prueba con 30.000
filas ficticias semicolon/coma decimal: 1.638.124 bytes, dashboard HTTP local 200,
30.000 filas, 0,71 s en cliente Flask; el tiempo no representa latencia pública.
Suite sin red: 166 passed en 1,11 s, incluidos límites 30.000/30.001 filas y
petición >8 MiB. Pendiente despliegue y verificación pública al registrar este paso.
Archivo aportado no enviado ni incluido en Git/imagen.

Despliegue verificado: revisión `pulso-comercial-ia-00006-f4z`, 100% tráfico;
digest `sha256:5c15a6f4a7700e4996c48af35c723257b16ca078ad6ddbb4443701920f6061cf`.
CSV ficticio chileno de 30.000 filas y 1.638.124 bytes: HTTP público 200,
4,38 s, 30.000 filas en respuesta. Sin IA. Evidencia `evidencias/25_limite_publico.json`.
F6 visual sigue pendiente.
