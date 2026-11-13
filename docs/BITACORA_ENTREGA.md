# Bitácora verificable

Fecha del trabajo: 12-11-2026, America/Santiago. Los registros técnicos pueden usar UTC.
Objetivo académico: entrega 13-11-2026, 23:59 Chile. Estado general: **MVP LOCAL**.

## F0 · lectura y autorización

Leído íntegramente el prompt de 657 líneas y PDF de una página. Directorio inicial:
solo ambos documentos, sin código, Git ni dependencias. Se presentó plan completo y
se detuvo. Usuario respondió `APROBADO PLAN`; transcripción en 01_plan_aprobado.md.
No se recibió G1, G2 ni G3. No se han realizado llamadas pagadas, commits ni despliegue.
PROMPT_MAESTRO.md es copia exacta del original, SHA256:
`03a85687663a728e5d7ab75fa841a28c5ce868bb613d78b75083f9b53c6156a8`.

## F1 · datos y cálculos

Creado entorno .venv con Python 3.12.15. Dependencias locales directas/transitivas
fijadas. Dataset sintético de 360 filas y diccionario. Motor Decimal/cobertura.
Primera ejecución: 51 pruebas pasaron y dos fallaron por un fixture que intentaba
reasignar un atributo de dataclass frozen; corregido el fixture, 53 pasaron.
Los seis oráculos numéricos, cobertura y unidades están probados.

## F2 · aplicación local

Flask, frontend responsive, filtros, gráfico, rankings, volúmenes y salud. La subida
multipart usa BytesIO; no se persiste el archivo. Pruebas reales de navegador a 375
y 1440 px: sin desbordes ni excepciones JS, filtros coherentes, CSV inválido controlado,
link de salto por teclado y respaldo sin IA claramente identificado.
Evidencias 02_demo_local_*.png y 02_revision_navegador.json. Capturas revisadas visualmente.
Chromium instalado exclusivamente bajo .venv para la verificación local.

Docker inicialmente inactivo. Se inició Docker Desktop, se construyó para Linux amd64
y se comprobó Gunicorn en 127.0.0.1:8081. Base fijada a digest después de resolverla.
Registro de build en 03_docker_build.txt y comprobaciones en 03_docker_verificacion.json.
El contenedor utiliza UID 10001 y AI_ENABLED=false; no contiene clave de API.
No se publicaron puertos fuera de loopback ni recursos cloud.

## F3 · integración IA sin gasto

SDK oficial, Responses API, Pydantic, prompts físicos v1/v2, referencias y cifras
mediante marcadores. Sin tools, almacenamiento del proveedor desactivado y reintento
acotado. Etiquetas externas pasan a alias antes del proveedor.
Tras añadir el paquete tests se detectaron imports de fixtures incompatibles; se
corrigieron. Suite ampliada: 88 pruebas pasaron antes del cierre documental.
Resultado final y comando conservados en 03_pytest.txt y 03_pytest.xml.
Red bloqueada en pytest; los tests del adaptador SDK usan un cliente falso.

Documentación oficial consultada: GPT-4.1 mini y GPT-5 mini figuraban deprecados;
se preparó GPT-5.6 Terra con salida estructurada y reasoning none. Acceso de cuenta
no probado. No se afirma validez de un prompt frente al modelo hasta F4 real.

## F4 · infraestructura de evaluación lista; ejecución real bloqueada

Diez casos y evaluador por versión, métricas, hashes, criterios y revisión humana.
20 ejecuciones fake completadas, sin API: 04_golden_set_mock.json/.csv.
Las tasas fake son solo diagnóstico del evaluador. Costo real de IA en esta tarea: cero
llamadas; no se presenta factura ni consumo medido del proveedor.
Presupuesto conservador de primera batería: 40 intentos, reserva máxima USD 5,664,
tope solicitado USD 6. Requiere autorización literal AUTORIZO EVAL IA.

## F5/F7 · documentación local anticipada

README, reglas del agente, diccionario, metodología, costos, matriz y guion preparados.
Ficha PDF preliminar de una página, renderizada y revisada visualmente; conserva
pendientes reales. Poppler produjo avisos de caché de fuentes durante renderizado,
pero finalizó y se inspeccionó el PNG; no hay texto cortado ni páginas adicionales.
Auditoría pip-audit: sin vulnerabilidades conocidas en las dependencias de ejecución
consultadas (05_dependencias_audit.json); no es garantía absoluta de seguridad.
Revisión de secretos por patrones y contexto de imagen documentada; Git todavía no
existe, por lo que no hay historial auditable ni hash de commit.

## Pendientes que impiden cerrar

- G1, credencial de servidor y primera evaluación real; revisión humana y comparación.
- Repetición final de evaluación dentro de presupuesto autorizado.
- G2: propietario/repositorio/visibilidad, commit/push y acceso docente.
- G3: proyecto cloud, facturación, cuotas, secretos/IAM, despliegue HTTPS e IA real.
- Cuotas/alertas configuradas con evidencia; estado actual: NO CONFIGURADAS.
- Video real ≤180 s; estado: NO GRABADO.
- URLs finales, ficha y README finales, comprobación incógnito pública.

No se declara PROYECTO COMPLETO. La próxima puerta es G1; F5 local se adelantó para
que la aprobación de gasto sea sobre un resultado concreto ya revisable.

## Verificación final local

Suite final: **90 passed**, comando `.venv/bin/python -m pytest -q
--junitxml=evidencias/03_pytest.xml`. Sin red y sin llamadas pagadas.
`pip check`: no dependencias rotas. Escáner local: sin hallazgos tras corregir
un falso positivo que confundía la línea posterior a una API key vacía.
Se añadió prueba de regresión para ese caso y rechazo de informes sin hallazgos
cuando sí existen hechos válidos. Docker se reconstruyó tras el último cambio.
La interfaz queda disponible en http://127.0.0.1:8081 mediante el contenedor
`pulso-local-g0`, ligado solo a loopback. No equivale a URL pública.

## Actualización G1 · configuración y prueba de conexión

El usuario autorizó explícitamente «AUTORIZA EVAL IA», proporcionó una credencial
del docente y pidió guardarla en env y hacer una prueba simple. Se conservó la
autorización sin exigir repetir la fórmula gramatical. Registro sin credencial:
`evidencias/10_autorizacion_g1.md`. Alcance previo: máximo USD 6 y 40 intentos.

Se creó .env con modo 0600, excluido por .gitignore y por la lista de inclusión
.dockerignore. No se copió la clave a código, evidencias, imagen ni comandos shell.
Se añadió python-dotenv 1.2.4 al entorno virtual y requirements.txt; app.py carga
.env solo al iniciarse directamente, no al importarse en pytest/Gunicorn.
AI_ENABLED permanece false en el producto; la prueba puntual usa la clave sin
habilitar el gasto libre desde el dashboard. Se recomendó rotar la clave expuesta.

Se ejecutó `scripts/probar_conexion_ia.py --ejecutar`: una petición a Responses,
modelo gpt-5.6-terra, salida máxima 32 tokens, timeout 20 s y cero reintentos SDK.
Resultado real: **HTTP 401, invalid_api_key**, rechazo de OpenAI en 720 ms.
No hubo texto generado ni tokens/consumo reportados. No se asigna un costo inventado.
Evidencia sin secretos: `evidencias/10_conexion_ia.json`.

La batería de evaluación no comenzó. Bloqueo técnico: reemplazo de credencial;
G1 ya está autorizado. Esta prueba consume un intento del alcance máximo, por lo
que restan como máximo 39; cualquier nueva conexión se contabiliza también.
La imagen local anterior sigue sin credencial y con IA deshabilitada; no se reinició
ni publicó para esta prueba. La dependencia nueva aún debe incorporarse al rebuild.

Validación de esta actualización: 92 pruebas aprobadas sin red; evidencia en
10_pytest_configuracion.txt/.xml. Comprobación de permisos/exclusiones y búsqueda
de la clave exacta fuera de .env: cero exposiciones en archivos del proyecto
inspeccionados; registro seguro en 10_configuracion_segura.json.

## Continuación autorizada: cierre de pendientes locales y paquete G2

El usuario indicó «Procede con el resto». Se avanzó sobre el trabajo local autorizado
y se preparó la publicación para aprobación final, sin inferir visibilidad ni habilitar
recursos externos. No se repitió la llamada de IA: .env no cambió desde el rechazo 401.
G1 permanece autorizado; G2 y G3 no han sido concedidos con su alcance concreto.

Se actualizó la imagen con python-dotenv, sin incorporar .env. Docker se encontraba
detenido y se inició antes de construir. Build Linux amd64 y ejecución con UID 10001
verificados; health y dashboard 200, IA deshabilitada 503 esperado. Evidencias
11_docker_build.txt y 11_docker_verificacion.json. La auditoría actualizada no encontró
vulnerabilidades conocidas: 11_dependencias_audit.json.

Se corrigió la recuperación del frontend: un CSV nuevo inválido ya no conserva cifras
del dataset anterior, y los controles quedan deshabilitados durante la carga para
evitar carreras. Navegador a 375/1440 px verificado; 11_revision_navegador.json y
capturas 11_demo_local_*.png. Suite: 96 pruebas aprobadas sin red (11_pytest.txt/.xml).

Se preparó un empaquetador por lista explícita y pruebas de exclusión de .env, symlinks
y patrones de secretos. El ZIP incluye manifiesto por archivo; su verificación
externa se registra en entrega/VERIFICACION_PAQUETE.json. No incluye la credencial
ni el PDF original del curso. No se utiliza un zip indiscriminado del directorio.

GitHub: el conector confirmó cuenta fbahamondesc1992; la búsqueda del nombre propuesto
pulso-comercial-ia no arrojó repositorio. Propuesta concreta en docs/REVISION_PUBLICACION.md:
crear repositorio público y rama main con commit inicial normal, solo después de G2.
Sin commits, pushes, despliegue, IAM, alertas cloud ni grabación de video final.

## Fase 12: G2 autorizado y revisión del nuevo modelo

El usuario autorizó GitHub para el repositorio público acordado y reemplazó la
clave local. La CLI confirmó fbahamondesc1992; creó el repositorio público
https://github.com/fbahamondesc1992/pulso-comercial-ia. Sin force push ni G3.

El preflight de conexión se detuvo antes de crear el cliente porque AI_MODEL
cambió a gpt-6.1-sol. No hubo nueva llamada ni cargo medido. El usuario confirmó
ese modelo y pidió revisar tarifas/presupuesto primero. Revisión oficial y propuesta
de USD 7 acumulados, 40 intentos totales en REVISION_MODELO_GPT61_SOL.md.
El código conserva GPT-5.6 Terra hasta finalizar la revisión y migración; IA apagada.

Suite vigente: 96 pruebas aprobadas sin red, 12_pytest.txt. Publicación por lista
explícita con auditoría de índice y todos los objetos Git, incluso huérfanos.
.gitattributes conserva bytes exactos para evitar normalizar CSV y alterar hashes.
El ZIP de fase 11 y la ficha PDF se conservan como entregables históricos locales,
con modelo anterior y pendientes de publicación visibles. El README indica el estado
vigente; no se presenta esa ficha como documento final de entrega.

Publicación verificada: https://github.com/fbahamondesc1992/pulso-comercial-ia, público, rama main,
SHA inicial 879bfdba8c37da8ae5db0a6bdff6060557af44c4 idéntico local/remoto.
HTTP 200 sin autenticación y README remoto idéntico. Auditoría completa: 104 objetos
Git, cero hallazgos. Evidencia 12_github_publicado.json. No hubo llamadas OpenAI
nuevas, migración del adaptador ni despliegue cloud.

## Fase 13: GPT-6.1 Sol, evaluación real y ajuste de presupuesto

El usuario autorizó USD 3 y luego redujo a USD 2 para conservar USD 3 de una carga
de USD 5 declarada para el profesor. Billing no consultado. Dashboard sin IA activa.
Se adaptó reasoning low, Standard, endpoint oficial fijo y cliente sin proxies del
entorno. La primera conexión recibió 400; se detectó incompatibilidad de in_memory
y se cambió a prompt_cache_options.ttl=30m según documentación. Segunda: HTTP 200,
OK, 11 tokens de entrada y 5 de salida. Se preservaron ambas evidencias y reservas.

Se incorporó presupuesto persistente exclusivo por archivo con reservas previas a
cada llamada y liquidación conservadora del uso reportado. Los fallos sin uso
conservan toda su reserva; no se imputó costo cero. Las respuestas incompletas
conservan tokens. Un fallo de proveedor detiene la batería.

Suite: 100 pruebas aprobadas sin red. Docker reconstruido Linux amd64, usuario 10001,
salud/dashboard 200 e IA 503 deshabilitada; imagen sin credenciales. El primer intento
de reinicio encontró el nombre aún retenido por auto-remove; tras completarse la
retirada se inició y verificó el contenedor correcto. Evidencias 13_docker_*.

Evaluación real: 20 casos, 23 intentos (10 v1 y 13 v2), 60.668/12.303 tokens.
V1 80% frente a v2 70%, sin mejora. Falsos positivos de causalidad y limitación de
criterio KG/UN descritos en MEJORA_PROMPTS.md; sin modificar la corrida original ni
marcar revisión asistida como humana. Compromiso acumulado USD 0,5843775, incluye
USD 0,3096 de reservas históricas desconocidas. Saldo del límite: USD 1,4156225.
No se ejecutó repetición final, no se habilitó servicio público ni se gastó más.

Se releyó la pauta Proyecto_Final_Advanced_Prompt_Engineering.pdf y se contrastó
con el prompt maestro. El informe de brechas distingue implementación, despliegue,
validación y entregables; la fecha de entrega es 13-11-2026 a las 23:59 de Chile.

## Fase 14: correcciones locales solicitadas del punto 1

Se acotaron por cláusula las excepciones de negación causal, se exigió cobertura
parcial estructurada para explicar incomparabilidad y se limitó el alcance de
acciones de investigación. Se corrigió el criterio KG/UN para reconocer porcentajes
de cumplimiento por unidad física. La revalidación reveló otro falso positivo en
la prohibición literal de «cumplimiento perfecto» dentro de una negación directa;
se corrigió manteniendo rechazo de afirmaciones positivas y dobles negaciones.

Se añadieron 39 pruebas de regresión/adversarias: total 139 aprobadas sin red.
Nuevo script revalidar_evidencia.py verifica hashes, conserva datos/prompts y no
llama al proveedor. Resultado final offline 9/10 v1 y 10/10 v2 sobre las mismas
23 respuestas observadas; no es una mejora nueva del prompt ni revisión humana.
La prueba intermedia queda conservada. GS-05/v1 sigue sin cumplir referencias.

14_integridad.json verifica igualdad con HEAD de prompts, golden set, demo, motor,
evaluación y presupuesto originales. Registro persistente sin cambios, cero llamadas
y costo API nuevo USD 0. Dashboard deshabilitado. No se realizó repetición real,
no se cambió el prompt por defecto y no se desplegó ni publicó esta fase.

## Fase 15: revisión semántica asistida y técnica local

Se leyeron íntegramente las 23 respuestas de los veinte pares caso/prompt y se
contrastaron contra hechos reconstruidos. Sin contradicciones numéricas observadas,
inyección obedecida ni causalidad comercial afirmada. Dos observaciones v1: orden
del foco familiar GS-03 y falta de referencias interanuales GS-05. Registro individual
con hash, ubicación y justificación en 15_revision_semantica_asistente.json. No se
completó revisión humana ni se modificaron los campos humanos originales.

Se reprodujo y bloqueó una afirmación causal añadida a una acción «Investigar si…»
y se corrigió la revalidación offline para no rescatar JSON de una respuesta incompleta
o con fallo operativo. Validador revisión 3, criterios revisión 2, revalidador revisión 2.
149 tests aprobados sin red; revalidación conserva 9/10 v1 y 10/10 v2. Se reconstruye
y verifica el contenedor local. Sin nuevas llamadas ni consumo API, originales y
registro presupuestario intactos; sin commit/push, despliegue o cambio de prompt activo.

## Fase 16: aprobación humana y publicación de correcciones bajo G2

El usuario aprobó globalmente la revisión humana y solicitó expresamente auditar
y publicar las correcciones locales en el repositorio público existente, rama main.
La aceptación se registra con hashes en 16_aprobacion_revision_humana.json. No se
alteran respuestas, observaciones ni campos individuales del registro histórico.

Se ejecutó nuevamente `.venv/bin/python -m pytest -q`: 149 pruebas aprobadas en
0,60 s, sin red. Docker conserva la verificación de fase 15; no se declara un nuevo
build en esta fase documental y de publicación. Sin nuevas llamadas pagadas ni
cambios del presupuesto. La repetición real, G3, URL pública, video y ficha final
siguen pendientes. El resultado de publicación se documentará tras verificar GitHub.

Auditoría previa: 125 archivos del índice y 204 objetos Git inspeccionados, incluidos
objetos huérfanos, sin hallazgos por patrones ni coincidencia de la credencial local.
Originales y presupuesto conservados; las 27 filas de la matriz permanecen presentes.
Los reintentos de acceso a Git usaron la autorización G2 tras las restricciones de
red y escritura de .git del entorno; no se amplió el alcance de publicación.

Publicación completada: commit de correcciones
`98199c0f391d40a54b21c6b8ca266a24383ebfee`, push normal a origin/main.
SHA local/remoto iguales, repositorio HTTP 200 sin autenticación y README remoto
idéntico byte a byte. Auditoría posterior al commit: 126 archivos y 211 objetos,
sin hallazgos. Evidencia: 16_github_publicado.json, incorporada en un commit documental
posterior. No hubo llamadas a IA ni despliegue en esta fase.

## Fase 17: evaluación real final autorizada

El usuario autorizó hasta 40 intentos adicionales, 66 acumulados, conservando el
consumo previo y el tope total de USD 2. Se migró exclusivamente max_llamadas bajo
bloqueo del registro; copia previa y autorización en 17_presupuesto_antes.json y
17_autorizacion_y_preflight.json. Inicio: 26 intentos, USD 0,5843775 comprometidos.
Se verificaron las tarifas oficiales vigentes y se conservaron prompts, casos,
payloads y validador. El CLI acepta el límite autorizado y rechaza topes superiores
a USD 2. Suite previa: 152 pruebas aprobadas sin red. IA activa solo en el proceso
de evaluación, sin modificar .env ni habilitar el dashboard.

Corrida final completada: 20 pares caso/prompt, 22 llamadas nuevas, 48 intentos
acumulados. V1 9/10; v2 10/10 tras dos reintentos. En primer intento, 9/10 frente
a 8/10. GS-05/v1 omite referencias interanuales; GS-07/08 v2 reciben falsos positivos
de causalidad en negaciones legítimas y se recuperan con el único reintento permitido.
Se preservan rechazos, textos, tokens y costos; no se retocó el validador después.

Uso nuevo: 58.674/11.800 tokens entrada/salida. Estimación Standard USD 0,235348;
valoración superior USD 0,264685. Compromiso acumulado USD 0,8490625; margen del
límite USD 1,1509375. Historial conciliado exactamente, sin consumo adicional posterior.
No se consultó billing. Selección técnica v2 por cobertura final y prioridad comercial,
con limitaciones de latencia/reintentos; muestra pequeña sin superioridad general.

Revisión asistida de 22 salidas vinculadas por hash y ubicación; humana nueva
pendiente, sin trasladar la aprobación de fase 16. Informe EVALUACION_FINAL.md,
resultados y conciliación en evidencias/17_*. Matriz actualizada en sus 27 requisitos.
No se desplegó ni se reconstruyó Docker: código de aplicación y prompts sin cambios.

## Fase 18: cierre F4 y preparación F6

El usuario da por cerrado F4 y solicita comenzar F6. Se registra aprobación global
vinculada por hash; se conservan observaciones y campos humanos individuales históricos.
Indica que no tiene proyecto Google Cloud, que administra gasto OpenAI y que requiere
disponibilidad hasta 30-11-2026. G3 aún no recibido.

No hay gcloud en PATH ni configuraciones locales de proyectos. No hay conector Cloud.
Docker 29.7.2 disponible; se verificó el contenedor existente amd64, usuario 10001,
salud/demo HTTP 200 e IA deshabilitada 503. Evidencia 18_docker_preflight.json.
No se ejecutó un nuevo build ni una llamada pagada. El alcance F6 se prepara en
PLAN_F6.md; creación de proyecto, facturación, IAM, recursos y URL pública pendientes.

El usuario confirma facturación habilitada. Lectura de consola: sesión autenticada y
cuenta con estado «Cuenta pagada». El proyecto visible pertenece a otro trabajo; no
se modificó ni se seleccionó como destino de Pulso. Identificadores privados solo en
entrega/18_contexto_cloud_privado.json (ignorado, permisos 0600). La cuenta observada
se propone para el proyecto nuevo, pendiente de G3; sin recursos ni cargos nuevos.

## Fase 19: G3 y avance parcial F6

G3 registrado con hash del plan aprobado. Consola confirmó proyecto dedicado, facturación
habilitada, APIs, repositorio regional y cuenta runtime. Se transfirió imagen local tras
bloqueos de clonación y descarga Docker; resultado de push no verificado. Presupuesto
de alertas específico creado; moneda pendiente de comprobar. OpenAI mostró límite
aplicado USD 5 y gasto USD 0,51, sin modificarlo ni ejecutar inferencias nuevas.

Retoma 13-11-2026: herramienta del navegador no disponible; gcloud ausente. No se
extraen credenciales del navegador ni se inventa éxito de comandos remotos. Registro
19_avance_f6.json y matriz actualizados. Plan aprobado y presupuesto IA preservados.
Pendientes: moneda del presupuesto cloud, push/digest, clave/proyecto/cupo, secreto,
Cloud Run, URL y pruebas públicas. F6 permanece abierto.

Verificación local de retoma: `.venv/bin/python -m pytest -q`, 152 passed en 0,67 s,
sin red; diff sin errores. Hash del plan preservado, ledger idéntico al cierre F4 y
27 filas de matriz conservadas. Sin nuevos commits/push en esta retoma.

## Configuración local de gcloud · 13-11-2026

SDK oficial 593.0.0 para macOS ARM64 instalado en `.venv/google-cloud-sdk`,
SHA256 contrastado con documentación oficial. `gcloud version` ejecutado correctamente.
Configuración aislada en `.venv/gcloud-config`, proyecto Pulso y región Santiago
seleccionados; Python `.venv/bin/python`. Ambos directorios excluidos de Git.
El bloqueo por ausencia del SDK está resuelto; falta que el usuario complete
`gcloud auth login` tras cargar `.venv/activar-gcloud.sh`. No se han ejecutado
aún las consultas cloud desde este SDK ni modificado recursos. Evidencia 20_gcloud_local.json.

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

## Fase 26 · cobertura de metas actuales · 13-11-2026

Se separó la validez de metas actuales de la cobertura interanual. Si todas las
filas actuales presentes tienen meta, se calculan cumplimiento y brecha aunque
haya combinaciones que solo existen en el año base; el estado se rotula cobertura
parcial y se advierte expresamente el alcance. La variación interanual sigue N/C
sin cobertura completa. Ranking muestra brechas actuales sustentadas. La gráfica
muestra puntos calculados con nota de calidad en tabla y avisos. Prueba de regresión
con dataset ficticio base-extra; suite 167 passed en 1,09 s, sin red.

Diagnóstico del archivo aportado solo local: 77 filas actuales y 79 base para el
filtro de la captura; dos combinaciones solo en base, cero metas actuales vacías.
No se publicó ni transmitió el CSV ni sus cifras comerciales.

Revisión pública `pulso-comercial-ia-00007-qpv`, 100% del tráfico, digest
`sha256:6f7cf5fd32e5c4daf5ecb9af367519760dedeb68fe1c8e7c5479bea69a602857`.
Prueba HTTP pública con tres filas ficticias: cumplimiento 80%, brecha -20 CLP,
una fila de ranking, variación interanual N/C; evidencia
`evidencias/26_cobertura_publica.json`. Sin llamadas IA ni CSV del usuario.

## Fase 27 · evidencia IA N/C · 13-11-2026

Se reprodujo el fallo reportado: el validador permitía marcadores de hechos sin valor
si el hallazgo contenía otro marcador válido, y el renderizador convertía valores de
cobertura parcial en `N/C`. Ahora todos los marcadores usados deben referir hechos
numéricos con estado valido o cobertura_parcial; los valores parciales se muestran
con su cifra y aviso de alcance. Una cita de N/C invalida la respuesta e inicia el
reintento ya existente; si no hay informe verificable, se devuelve error recuperable.
El prompt v2 histórico permanece byte a byte para conservar la evidencia de evaluación.
Suite local 169 passed en 1,12 s, sin llamadas pagadas. Pendiente despliegue y prueba
pública con proveedor falso/flujo de dashboard; no se repetirá IA real por presupuesto.

Revisión pública `pulso-comercial-ia-00008-zzt`, 100% tráfico, digest
`sha256:b10f2cc79710446910289173bdf3afdc0e015b78894b6a6cd2a64adf1c0853ff`.
Health público HTTP 200. Evidencia `evidencias/27_validacion_publica.json`.
No se generó otro informe IA real: el cupo G3 de validación pública ya se contabilizó.

## Fase 28 · cierre humano F6 y apertura F7 · 13-11-2026

El usuario declara «Apruebo F6 que sigue». F6 queda cerrada por aprobación humana
con evidencia HTTP de URL/IA ya registrada y revisión vigente 00008-zzt. Este cierre
no certifica recorrido visual público en incógnito 375/1440, capturas públicas ni
un nuevo informe real tras la corrección del validador N/C. No se hizo nueva llamada
pagada. Evidencia de la decisión: `evidencias/28_aprobacion_f6.json`.

F7 queda abierta: actualizar ficha PDF de una página con modelo/costos/URL vigentes,
revisar guion y grabar video real de hasta 3 minutos, completar evidencias visuales
solo con demo ficticia y hacer auditoría final de repositorio, matriz y gasto.

## Fase 29 · F7 en ejecución · 13-11-2026

Ficha PDF final de una página con modelo y costos vigentes, enlaces reales y
fuentes oficiales; render PNG inspeccionado. HTTP público inicio/health/demo/dashboard
200 con demo ficticia. Herramienta de navegador/grabación ausente: capturas 375/1440,
incógnito y video real NO REALIZADOS. Guion final preparado. Auditoría GitHub
detectó repositorio PRIVATE; acceso anónimo pendiente de corregir bajo G2 público.
Evidencia 29_f7_estado.json. No se invocó IA pagada.
