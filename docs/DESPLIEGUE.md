# Despliegue vigente

Plan aprobado conservado sin cambios en [PLAN_F6.md](PLAN_F6.md).
El historial de preparación, bloqueos y cambios está en BITACORA_ENTREGA.md.
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

## Operación

Para usar gcloud local: `source .venv/activar-gcloud.sh`. La configuración y
credenciales se conservan en .venv/gcloud-config, excluidas de Git.
Ante un error del proveedor, conservar dashboard y mostrar error controlado.
Para detener consumo IA, actualizar AI_ENABLED=false en el mismo servicio.
No eliminar recursos antes del 30-11-2026; retirada posterior por autorización.
