# Evaluación de prompts · estado vigente 12-11-2026

**Evaluación final real completada (fase 17): v1 9/10 y v2 10/10**, +10 puntos
porcentuales con el mismo evaluador corregido. V2 necesitó dos reintentos por falsos
positivos del filtro; al primer intento v1 obtiene 9/10 y v2 8/10. No se oculta ese
costo operativo. [Informe final](EVALUACION_FINAL.md) y evidencias `17_*`.

Selección técnica para el MVP: v2; no cambió el archivo ni el valor por defecto.
Revisión asistida de las 22 respuestas completada; humana de esta nueva muestra
pendiente. La aprobación de fase 16 corresponde a la corrida anterior. No se hereda.
Una corrida sintética pequeña no establece superioridad estadística general.

## Registro histórico preservado de fases 13–15

Los pendientes y métricas que siguen describen esas fases; para el estado actual,
consultar el informe final y MATRIZ_CUMPLIMIENTO.md.

# Evaluación real v1 vs. v2 · 12-11-2026

Actualización de revisión (fase 15): 23 respuestas examinadas por el asistente,
149 pruebas sin red y controles adicionales para afirmaciones añadidas a hipótesis
y estados incompletos del proveedor. Ver [revisión semántica](REVISION_SEMANTICA.md).
Revisión humana y repetición final siguen pendientes; sin gasto API nuevo.


**Actualización local posterior:** corregidos los falsos positivos y criterios de
unidad; ver [correcciones locales](CORRECCIONES_LOCALES.md). Revalidación offline:
v1 9/10 y v2 10/10. No sustituye la evaluación original de abajo (8/10 y 7/10),
no añade llamadas ni constituye mejora del prompt o repetición final.


Se completaron diez casos por versión con GPT-6.1 Sol, Responses API, reasoning low,
servicio Standard, caché TTL 30m, salida máxima 1.800 tokens, timeout 20 s y sin tools.
Se preservaron prompts, casos, payloads, esquema y validadores durante la comparación.
Los hashes de los payloads coinciden caso a caso. Evidencia original inmutable:
`evidencias/13_evaluacion_real.json` y su CSV; resumen en `13_resumen_evaluacion.json`.

## Resultado medido

| Métrica | v1 | v2 | Diferencia pp |
|---|---:|---:|---:|
| Casos evaluados | 10 | 10 | — |
| JSON válido por intento | 100% | 100% | 0 |
| Esquema válido por intento | 100% | 100% | 0 |
| Casos con todos los criterios automáticos cumplidos | 80% | 70% | -10 |
| Hallazgos con referencias existentes | 100% | 100% | 0 |
| Respuestas con cifras sin respaldo detectadas | 0 | 0 | 0 |
| Casos correctos tras revisión humana | PENDIENTE | PENDIENTE | — |

**V2 no mejoró en esta corrida.** No equivale a demostrar superioridad estadística de
v1: hay una sola corrida por caso y limitaciones del evaluador. La versión activa
por defecto continúa siendo la candidata v2; su selección final queda pendiente.
No se retocaron prompts ni validadores para alterar los resultados después de medir.

## Fallos y limitaciones del evaluador

- GS-05/v1: no citó los IDs de indicadores interanuales exigidos por el criterio,
  aunque expresó que no había comparabilidad por cobertura incompleta.
- GS-06/ambas: describieron separadamente kilogramos y unidades, pero citaron hechos
  de cumplimiento cuya unidad es %. La regla exige referencias con unidad KG y UN:
  el resultado automático no prueba por sí mismo una mezcla incorrecta de volúmenes.
- GS-01/v2 necesitó un reintento; GS-04/v2 y GS-05/v2 se rechazaron tras dos intentos
  por causalidad_no_sustentada. La inspección técnica del asistente detectó falsos
  positivos: el filtro rechaza negaciones de causalidad que nombran precio/stock,
  y también una explicación de falta de comparabilidad por cobertura insuficiente.
  Esto es un problema del validador, no evidencia de que el modelo afirmara esas causas.

Las observaciones anteriores son revisión técnica asistida, NO revisión humana.
Los campos humanos siguen null/PENDIENTE. GS-07 (inyección) y GS-10 (abstención)
cumplieron sus criterios automáticos en ambas versiones; falta contrastar semánticamente
las salidas y registrar revisor, fecha, decisión y justificación. Cero detecciones
numéricas no garantiza ausencia de todos los errores semánticos.

Corrección local identificada durante esta corrida (resuelta después en fase 14): distinguir negaciones/limitaciones de afirmaciones
causales y comprobar separación de unidades mediante dimensión y evidencia del
hecho, sin obligar a citar una métrica distinta. Mantener pruebas adversarias contra
causas inventadas, documentar cambio de evaluador y volver a comparar ambos prompts
en condiciones iguales. La evaluación original debe conservarse para trazabilidad.

## Consumo y alcance

23 intentos de evaluación (10 v1, 13 v2), 60.668 tokens de entrada y 12.303 de salida.
Estimación Standard simple: USD 0,244366; valoración superior incluyendo posible
escritura de caché: USD 0,2747000. No son importes de factura verificados.
Conexión válida: 11/5 tokens, USD 0,000072 estimados y USD 0,0000775 superiores.
Se mantienen USD 0,3096 reservados por dos fallos anteriores sin uso reportado.
Compromiso acumulado: **USD 0,5843775 de USD 2**; margen conservador no usado
USD 1,4156225. 26 intentos acumulados, contando conexiones.

No se consumió más al terminar la batería. La carga de USD 5 fue declarada por el
usuario; no se consultó billing. Los USD 3 destinados al profesor no se autorizaron
para evaluación adicional. El dashboard conserva AI_ENABLED=false.

## Estado académico

Existe evaluación real y comparación documentada, pero **no mejora positiva medida**.
Falta revisión humana, corregir los hallazgos del evaluador, seleccionar el prompt
final y repetir la batería completa antes de declarar cierre. La repetición final
no se ha ejecutado ni se presume autorizada por conservar saldo.
El archivo `04_golden_set_mock.json` sigue siendo exclusivamente prueba con cliente
falso, nunca evidencia de calidad real.

Estado vigente fase 18: F4 cerrado por aprobación global explícita del usuario;
selección técnica v2 confirmada para el MVP. Evidencia 18_cierre_f4_inicio_f6.json.
Los campos individuales históricos no se rellenan ni alteran. F6 en preparación,
G3 pendiente, disponibilidad solicitada hasta 30-11-2026 (Chile). Ver PLAN_F6.md
en docs/.
