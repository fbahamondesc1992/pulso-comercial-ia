# GPT-6.1 Sol: revisión de tarifas y presupuesto

**Actualización vigente:** el usuario autorizó USD 3 y posteriormente redujo el
tope a **USD 2 acumulados** para preservar USD 3 del saldo declarado al profesor.
La propuesta de USD 7 de abajo queda como antecedente, NO es el límite autorizado.
Adaptación local realizada; conexión HTTP 200 verificada. Se conserva reserva
completa de fallos sin uso conocido y se liquida cada respuesta con uso reportado
a USD 2,50 de entrada/10 de salida por millón, de forma conservadora.
El registro persistente y los resultados están en la fase 13.

Fecha: 12-11-2026. Seleccionado expresamente por el usuario, quien pidió revisar
primero tarifas y presupuesto. No se ejecutaron llamadas con la nueva clave.
El código y la ficha PDF anterior conservan GPT-5.6 Terra; la migración queda
pendiente del cierre de esta revisión. AI_ENABLED permanece false.

## Compatibilidad y tarifa comprobadas

OpenAI documenta Responses API y Structured Outputs para `gpt-6.1-sol`.
No admite reasoning.effort=none: usar low para este flujo inicial.
Tarifa Standard por millón de tokens: entrada USD 2, salida USD 10,
lectura de caché USD 0,10 y escritura de caché USD 2,50.
No se usará Fast, Ultrafast, contexto largo, residencia regional ni herramientas.
La disponibilidad efectiva en esta cuenta no está comprobada.

Fuentes oficiales consultadas:
- https://developers.openai.com/api/docs/models/gpt-6.1-sol
- https://developers.openai.com/api/docs/pricing?latest-pricing=standard
- https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#migration-quickstart

## Presupuesto propuesto: USD 7 acumulados, no adicionales

Se conserva la reserva de USD 0,1416 y el intento de conexión anterior rechazado.
El fallo local por discrepancia de modelo no realizó ninguna llamada y no descuenta
otro intento. Quedan hasta 39 intentos dentro del máximo acumulado de 40.

Nueva reserva por intento: 60.000 tokens de entrada a USD 2,50/millón
(cubre conservadoramente escritura de caché) y 1.800 tokens de salida a USD 10/millón:

`60.000 × 2,50 / 1.000.000 + 1.800 × 10 / 1.000.000 = USD 0,168`.

Reserva acumulada máxima: `0,1416 + 39 × 0,168 = USD 6,6936`, dentro de USD 7.
Es una reserva de planificación, no consumo observado ni garantía contractual.
Los tokens de razonamiento consumen el mismo límite de salida.

Alcance: una prueba de conexión, seguida solo si pasa por diez casos con v1 y diez
con v2, con hasta 38 intentos de evaluación restantes. Máximo un reintento por caso,
sin reintentos automáticos del SDK. Si se agota el saldo, conservar resultados
parciales y detenerse. No incluye repetición final ni uso público del dashboard.

La prueba usaría salida máxima de 512 tokens, low, texto sintético y sin tools.
Se reserva prudentemente el mismo importe por intento. Evaluación: 1.800 tokens,
timeout de 20 segundos, store=false. Una respuesta truncada o timeout se reportará;
no se elevarán límites automáticamente. No se garantizan veinte casos completados.

## Estimación operativa comparativa

Con el supuesto anterior de 6.000 tokens de entrada y 900 de salida totales:
USD 0,021 por intento Standard sin escritura de caché; USD 0,024 si toda la entrada
se valoriza conservadoramente como escritura. Con 10% de reintentos: USD 0,0231
a USD 0,0264 por análisis. No son mediciones reales ni garantías de latencia.

Manteniendo los supuestos cloud anteriores, 100 análisis/mes serían USD 4,38–4,71;
1.000 serían USD 25,81–29,11. Incluyen la provisión hipotética de USD 2/mes ya
documentada; no son nuevas tarifas cloud verificadas ni autorización de despliegue.

## Cambios preparados para la siguiente etapa

1. Cambiar el modelo por defecto y reasoning a low en proveedor y prueba de conexión.
2. Actualizar tarifas, reserva y metadatos del evaluador; fijar servicio Standard.
3. Actualizar pruebas del contrato SDK, configuración de ejemplo y documentación.
4. Verificar todo sin red antes de usar la clave; conservar .env excluido.
5. Ejecutar conexión y, si pasa, la evaluación dentro del saldo acumulado anterior.

La ejecución espera aprobación del alcance revisado. Fundamento: AGENTS.md G1
exige presupuesto, modelo y alcance previamente presentados; además el usuario
solicitó revisar estos valores antes de usar el nuevo modelo. G2 ya está autorizado.
