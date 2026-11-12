# Correcciones locales del evaluador · 12-11-2026

Actualización de revisión (fase 15): 23 respuestas examinadas por el asistente,
149 pruebas sin red y controles adicionales para afirmaciones añadidas a hipótesis
y estados incompletos del proveedor. Ver [revisión semántica](REVISION_SEMANTICA.md).
Revisión humana y repetición final siguen pendientes; sin gasto API nuevo.


Alcance solicitado: punto 1 del plan de cierre. Sin llamadas a OpenAI, sin nueva
evaluación del modelo y sin cambio de prompts, golden set, datos ni reglas de KPI.
Los resultados originales de fase 13 permanecen intactos.

## Cambios

- El validador de causalidad analiza cláusulas. Reconoce negaciones directas de
  atribución con una gramática acotada; no usa la presencia global de «no hay datos»
  para permitir afirmaciones posteriores en el mismo campo.
- Admite una explicación de incomparabilidad interanual por cobertura solo si el
  payload contiene evidencia estructurada de base total con cobertura parcial.
  No permite atribuir una caída comercial a esa limitación.
- Una acción de investigación no habilita afirmaciones en otra oración o tras un
  contraste. Las referencias, cifras y causas explícitas siguen verificándose.
- El criterio KG/UN reconoce la unidad física de cumplimiento_ump en dimension.unidad_ump,
  aunque el valor se exprese en %. Exige dos unidades válidas efectivamente citadas;
  mencionar KG/UN sin evidencia no basta. Se rechazan datos nulos/no comparables,
  la misma unidad repetida y métricas monetarias usadas como evidencia de volumen.
- Las frases prohibidas del golden set distinguen una negación directa al inicio
  de una cláusula. «No representa cumplimiento perfecto» no afirma cumplimiento.
  Una segunda afirmación positiva o una doble negación siguen fallando.

Se identifican por separado revisión 2 del validador y revisión 2 de criterios;
no son nuevas versiones de los prompts. El evaluador registra ambos identificadores
para futuras corridas comparables. El nuevo script revalidar_evidencia.py solo lee
salidas sintéticas guardadas, verifica hashes de payload/prompt y genera otro archivo.

## Pruebas y resultados locales

`.venv/bin/python -m pytest -q`: **139 pruebas aprobadas**, con red bloqueada.
Incluyen negaciones, causas inventadas después de una negación, acciones con
aseveraciones añadidas, explicación de cobertura sin respaldo, porcentajes por
unidad, evidencia ausente y mezcla numérica en un total UMP. Se revalidan además
las 23 respuestas históricas y se comprueba que ninguna antes aceptada regrese.

| Lectura de los diez casos por prompt | v1 | v2 |
|---|---:|---:|
| Evaluación real original con reglas anteriores | 8/10 | 7/10 |
| Revalidación offline de respuestas existentes con reglas corregidas | 9/10 | 10/10 |

La fila offline toma el primer intento ya observado que acepta el validador actual.
No genera respuestas alternativas ni estima qué habría pasado en otra llamada.
Es una prueba de regresión del evaluador, **no una mejora nueva medida del prompt**,
ni una repetición independiente ni revisión humana. La evaluación de fase 13 sigue
siendo el resultado experimental original. GS-05/v1 continúa fallando por falta de
las referencias interanuales exigidas: no se relajó ese criterio para mejorar el puntaje.

Evidencias: 14_pytest.txt, 14_revalidacion_final.json y 14_integridad.json.
14_revalidacion_offline.json es el paso intermedio que todavía detectaba como
prohibida la negación «no representa cumplimiento perfecto»; se conserva, no se reemplaza.
Docker actualizado/verificado: 14_docker_build.txt y 14_docker_verificacion.json.

## Límites y pendientes

La gramática es conservadora y no comprende todo el español. Puede rechazar una
negación válida expresada de otra forma o no detectar una afirmación implícita.
La cobertura de referencias KG/UN no certifica por sí sola toda la interpretación
semántica; las prohibiciones numéricas/textuales siguen siendo controles parciales.
Se conserva la necesidad de revisión humana y una evaluación final con ambos
prompts bajo las mismas reglas antes de declarar calidad o elegir un ganador.

Costo API nuevo: USD 0. El registro presupuestario de fase 13 permanece sin cambios.
Dashboard con IA deshabilitada; sin despliegue. Cambios de esta fase conservados
localmente para revisión, sin nuevo commit ni push.
