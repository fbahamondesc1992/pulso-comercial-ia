# Experimento v1 vs. v2

Actualización G2/modelo: nueva clave guardada por el usuario; todavía no probada.
Se seleccionó GPT-6.1 Sol y se solicitó revisar primero sus tarifas/presupuesto.
Ver [revisión vigente](REVISION_MODELO_GPT61_SOL.md). Los importes y el 401 descritos
más abajo corresponden al alcance anterior de GPT-5.6 Terra. No se ejecutaron
nuevas llamadas pagadas ni evaluación.


Estado: **NO EJECUTADO CON IA REAL**. El archivo `evidencias/04_golden_set_mock.json`
prueba únicamente el evaluador y los contratos con un cliente falso. No demuestra
calidad semántica de un modelo ni una mejora de prompts.

Actualización 12-11-2026: G1 autorizado. La prueba única de conexión devolvió HTTP
401 `invalid_api_key`; ver `evidencias/10_conexion_ia.json`. La batería se detuvo
antes de comenzar, sin confundir este fallo de credencial con un resultado del prompt.
Se requiere reemplazar la clave por una válida; no renovar la aprobación de gasto
ya concedida mientras se mantengan el modelo, alcance y saldo autorizado.

## Diseño

Diez escenarios en `golden_set/casos_analista.json`. Los casos numéricos reconstruyen
el CSV y calculan hechos con el motor real; sus oráculos se contrastan en pytest.
GS-09 limita el payload a un solo hecho válido; GS-10 carece de hechos y exige abstención.
Modelo, parámetros, casos, contexto, esquema y validadores idénticos en ambas versiones.
Se conserva el hash del payload para comprobar igualdad. La API puede variar entre
ejecuciones: una corrida por caso no permite concluir significancia estadística.

V2 agrega prioridad comercial, tratamiento de denominadores y cobertura, separación
de particiones, jerarquía y restricciones de hipótesis. V1 ya es una base funcional.
Las diferencias se revisan en los archivos; la elección actual de v2 es provisional.

## Ejecución

```bash
.venv/bin/python scripts/evaluar_prompts.py
.venv/bin/python scripts/evaluar_prompts.py --modo mock --salida evidencias/04_mock_nueva_corrida.json
```

El primer comando solo presenta el plan. El segundo no consume API. El evaluador
no sobrescribe resultados existentes. Una ejecución real exige autorización G1
documentada, `AI_ENABLED=true`, credencial configurada fuera del repositorio,
`--modo real --autorizacion 'AUTORIZO EVAL IA' --tope-usd 6 --max-llamadas 40`
y una ruta diferente, por ejemplo `evidencias/04_real_inicial.json`.
Esos argumentos son controles operativos, no reemplazan el permiso del usuario.

## Medición y lectura

| Indicador real | v1 | v2 | Diferencia pp |
|---|---|---|---|
| JSON válido por intento | PENDIENTE | PENDIENTE | PENDIENTE |
| Esquema válido por intento | PENDIENTE | PENDIENTE | PENDIENTE |
| Casos con criterios automáticos cumplidos | PENDIENTE | PENDIENTE | PENDIENTE |
| Hallazgos con referencias válidas | PENDIENTE | PENDIENTE | PENDIENTE |
| Casos correctos tras revisión humana | PENDIENTE | PENDIENTE | PENDIENTE |

Objetivos de aceptación: cero cifras sin respaldo, cero instrucciones maliciosas
obedecidas, cero afirmaciones causales no sustentadas. Los detectores automáticos
son conservadores e incompletos; un contador en cero no acredita ausencia semántica.
Los rechazos por cifras cuentan respuestas detectadas, no todas las posibles cifras
de una salida; puede haber fallos anteriores de esquema que impidan medirlas.

Por caso se guardan fecha UTC, prompt/hash, modelo, contexto/hash, salidas sintéticas,
intentos, validaciones, latencia, tokens y costo si existe uso reportado. Se registran
fallos previos al reintento y resultados finales. La evidencia se escribe tras cada
caso para conservar resultados parciales. Un presupuesto agotado detiene la batería;
la matriz reporta los casos realmente ejecutados, no una batería completa ficticia.

Revisión humana: contrastar cada frase con su evidencia, verificar prioridad,
distinguir hechos e hipótesis, verificar incertidumbre y comprobar inyección.
Registrar revisor, fecha, decisión, justificación y caso en un archivo separado que
referencie el hash del resultado original; conservar el resultado crudo inmutable.
Los campos de revisión humana permanecen null/PENDIENTE hasta esa revisión.

Si v2 no mejora o regresa, informar el resultado. Una nueva iteración requiere
presupuesto disponible y conserva las versiones evaluadas. Antes del cierre se
repite la batería completa: no declarar mejora por tests deterministas o mocks.
