# Pulso Comercial IA

Leer PROMPT_MAESTRO.md; es la especificación del producto. Priorizar el MVP evaluable.
Python calcula y valida, el LLM interpreta, el usuario decide. No inventar cifras,
resultados, capturas, URLs, mejoras ni aprobaciones. Solo datos ficticios.

## Autorizaciones
- G0 APROBADO PLAN recibido en el chat el 12-11-2026: desarrollo local e instalación
  exclusivamente en .venv; pruebas con mocks. No constituye permiso para API pagada.
- G1 actualizado el 12-11-2026: GPT-6.1 Sol, conexión y evaluación hasta USD 2
  acumulados (incluye reserva anterior), máximo 66 intentos acumulados: 26 previos
  más hasta 40 adicionales para la evaluación final expresamente autorizada. Preservar USD 3
  del saldo declarado para el profesor. No habilita consumo público ni G3.
- G2 AUTORIZO GITHUB recibido el 12-11-2026: repositorio público
  fbahamondesc1992/pulso-comercial-ia, rama main, commits/push normales. No force push.
- G3 AUTORIZO DESPLIEGUE: recursos e IAM dentro del alcance autorizado.
- No delegar a subagentes sin petición expresa del usuario.

## Trabajo y verificación
Usar Python 3.12 y .venv/bin/python. Ejecutar .venv/bin/python -m pytest -q.
La suite prohíbe tráfico de red. No habilitar AI_ENABLED durante pruebas locales.
Preservar originales; sumar con Decimal, no mezclar KG y UN ni imputar faltantes.
Cargar literalmente prompts/analista_v1.md o analista_v2.md.
No guardar CSV subidos ni loggear texto del usuario, prompts privados o secretos.
Documentar cobertura, fallos y bloqueos; actualizar docs/MATRIZ_CUMPLIMIENTO.md.
Auditar secretos antes de GitHub, incluyendo historial cuando exista.
Docker: docker build -t pulso-comercial-ia:local .; docker run --rm -p 8080:8080
pulso-comercial-ia:local. Nunca declarar build probado si el motor no está activo.
Al finalizar una fase informar cambios, pruebas, evidencia, matriz y pendientes.
