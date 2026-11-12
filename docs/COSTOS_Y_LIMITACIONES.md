# Costos y límites · estimación, no gasto observado

Actualización G2/modelo: nueva clave guardada por el usuario; todavía no probada.
Se seleccionó GPT-6.1 Sol y se solicitó revisar primero sus tarifas/presupuesto.
Ver [revisión vigente](REVISION_MODELO_GPT61_SOL.md). Los importes y el 401 descritos
más abajo corresponden al alcance anterior de GPT-5.6 Terra. No se ejecutaron
nuevas llamadas pagadas ni evaluación.


Fecha de consulta: 12-11-2026. Moneda: USD; sin IVA, conversión a CLP, créditos ni
descuentos por caché. No se realizó ninguna llamada pagada ni despliegue.

Actualización de conexión: G1 autorizado; se realizó un intento real rechazado con
HTTP 401 `invalid_api_key`, sin generación ni datos de uso reportados. El costo del
intento no se inventa (null en evidencia). Se conserva prudentemente una reserva de
USD 0,1416 del alcance presentado y se descuenta un intento de los 40 autorizados.
La batería permanece sin ejecutar hasta disponer de una credencial válida.

## Modelo y API

OpenAI `gpt-5.6-terra` declara soporte de Responses API y salidas estructuradas.
Precio estándar publicado: USD 2 por millón de tokens de entrada, USD 12 de salida.
Se propone reasoning.effort=none y salida máxima 1.800 tokens. Cuenta, saldo,
disponibilidad y límites efectivos: NO VERIFICADOS.
Fuente: https://developers.openai.com/api/docs/models/gpt-5.6-terra

Hipótesis para una consulta típica: 6.000 tokens de entrada y 900 de salida.
Son supuestos de planificación, NO mediciones del modelo. El payload demo observado
tiene 13.258 bytes UTF-8 antes de los últimos ajustes de advertencias; no equivalen
a tokens. Prompt, esquema y framing también consumen entrada.

Costo por intento típico = (6.000 × 2 + 900 × 12) / 1.000.000 = USD 0,0228.
Con 10% de consultas que requieren un segundo intento: USD 0,02508 por análisis.
Como máximo se realizan dos intentos, no un bucle ilimitado.

## Infraestructura propuesta

Cloud Run, Santiago `southamerica-west1`, facturación por solicitudes, 1 vCPU,
512 MiB, min-instances=0, max-instances=1, concurrencia=4 y un worker con cuatro
threads. Valores propuestos, NO configurados. Región presente en documentación.

Tarifas de Santiago extraídas de su tabla oficial: CPU activa USD 0,0000336 por
vCPU-segundo; memoria activa USD 0,0000035 por GiB-segundo; USD 0,40 por millón
de requests. Fragmento y región conservados en `evidencias/05_fuente_cloud_run.json`.
Supuesto conservador de carga ligera: 20 segundos activos por análisis, memoria
0,5 GiB y ocho solicitudes HTTP por análisis, sin compartir tiempos concurrentes.
No se aplica free tier: puede estar consumido por otros proyectos de la cuenta.

Compute/requests por análisis = 20 × (0,0000336 + 0,5 × 0,0000035)
+ 8 × 0,40 / 1.000.000 = USD 0,0007102.

Se añade una **provisión hipotética de USD 2/mes** para builds, almacenamiento de
imagen, secretos, logs, tráfico y arranques adicionales. No es una tarifa oficial
ni una garantía de cobertura: reemplazarla por el cálculo por SKU/uso antes de G3.

| Escenario mensual | IA con 10% reintentos | Compute/HTTP | Provisión otros | Total estimado |
|---|---:|---:|---:|---:|
| 100 análisis | 2,50800 | 0,07102 | 2,00 | **4,58 USD** |
| 1.000 análisis | 25,08000 | 0,71020 | 2,00 | **27,79 USD** |

No son un precio de venta, un tope duro ni una factura. Variaciones en duración,
tráfico, tokens, abuso o configuración pueden elevarlos. La suscripción B2B y su
precio son hipótesis por validar; el MVP no realiza cobros.

Fuentes cloud:
- https://cloud.google.com/run/pricing
- https://docs.cloud.google.com/run/docs/locations
- https://docs.cloud.google.com/billing/docs/how-to/budgets
- https://docs.cloud.google.com/run/docs/configuring/services/secrets

## Propuesta G1: primera evaluación

Diez casos × dos prompts = 20 llamadas iniciales; máximo 40 intentos con reintentos.
Reserva conservadora por intento: 60.000 tokens entrada y 1.800 salida = USD 0,1416.
Máximo reservado de la batería: USD 5,664. **Solicitar tope USD 6, máximo 40 intentos.**
La cota de entrada usa un token por byte más margen para esquema/framing, deliberadamente
superior al contexto admitido. No es una estimación de uso típico. Cada llamada reserva
ese importe antes de ejecutarse, sin liberarlo tras un fallo de uso desconocido.
El presupuesto se controla dentro de una ejecución; reiniciar el script no crea permiso
para otra batería. Consultar gasto anterior y saldo de autorización antes de reejecutar.
El escenario típico de 20 llamadas sería USD 0,456, pero su consumo real se medirá.

Esta propuesta NO autoriza la repetición final ni la prueba de producción; deben
incluirse en una ampliación de presupuesto o una autorización posterior explícita.
El cambio de modelo exige revalidar tarifas y parámetros.

## Restricciones de abuso y privacidad

AI_ENABLED=false por defecto; una clave por sí sola no habilita llamadas.
SDK sin reintentos automáticos; validación con máximo un reintento; timeout de 20 s
por intento; payload 32.000 bytes; prompt 12.000 bytes; máximo 45 hechos.
El límite acepta 5 solicitudes IA por IP y hora, 30 globales por hora y proceso;
cada solicitud puede generar dos intentos. remote_addr no confía en headers externos:
detrás del proxy puede agrupar usuarios. No equivale a identificación individual.
Se elimina el estado vencido para acotar memoria. Restart, nuevos workers o instancias
reinician/separan contadores: **no son un tope duradero de gasto**.

No hay CORS abierto; se exige header de aplicación y Origin compatible. Esto reduce
uso cruzado desde navegadores, no bloquea clientes HTTP deliberados.
Configurar cuota/límite efectivo del proveedor si está disponible; documentar su
ausencia si no. Configurar alertas cloud y comprobar si existen spend caps aplicables
al servicio/cuenta. Una alerta de presupuesto no detiene por sí misma el consumo.
Ninguna alerta, cuota o secreto cloud está configurado todavía.

El CSV se mantiene solo en memoria del navegador y petición. Flask usa BytesIO para
multipart, sin spool a disco. Etiquetas enviadas al modelo son alias; esto no convierte
datos sensibles en datos autorizados. Usar exclusivamente datos ficticios. El reporte
no determina causalidad, predicción ni aprobación comercial.
