# Matriz de cumplimiento · 13-11-2026

Alcance actual: G0/G2 recibidos; G1 vigente hasta USD 2 y 66 intentos acumulados.
Evaluación final real completa: v1 9/10, v2 10/10; +10 pp después de reintentos.
V1 usó 10 llamadas y v2 12; al primer intento, 9/10 y 8/10 respectivamente.
Revisión asistida de las 22 respuestas; dos falsos positivos residuales del filtro.
Selección técnica v2; cierre humano global recibido en fase 18. La aprobación global
previa se conserva y no se traslada a respuestas nuevas. Suite: 155 pruebas sin red.
Compromiso conservador acumulado USD 1,1850625 (incluye reserva pública USD 0,336). Consola OpenAI mostró USD 0,51;
no equivale al registro conservador ni acredita saldo disponible.
G3 ejecutado: URL e IA pública comprobadas por HTTP. Validación visual, video y ficha final pendientes.
No asigna puntaje ni aprobación comercial/académica.
VERIFICADO significa evidencia concreta dentro del alcance señalado, no una promesa.
Se preservan las 27 filas de la sección 14 del prompt.

| Código | Requisito | Evidencia concreta | Estado | Comentario / limitación |
|---|---|---|---|---|
| NEG-01 | Cliente, problema y diferenciación | README.md; docs/FICHA_NEGOCIO.pdf | VERIFICADO | Definición documentada; negocio no validado comercialmente |
| NEG-02 | IA central y genuina | evidencias/21_ia_real_publica.json | VERIFICADO | LLM real en endpoint público, tres hallazgos; prueba visual pendiente |
| NEG-03 | Modelo de ingresos | README.md; ficha PDF | VERIFICADO | Hipótesis SaaS B2B; no declara ventas |
| NEG-04 | Costos mensuales sustentados | docs/COSTOS_Y_LIMITACIONES.md; evidencias/13_resumen_evaluacion.json | EN_PROCESO | Escenarios 100/1.000 actualizados a GPT-6.1 Sol; falta trasladarlos a ficha PDF final |
| SW-01 | App funcional y responsive | evidencias/11_demo_local_1440.png; 11_demo_local_375.png; 11_revision_navegador.json | EN_PROCESO | Local verificado; HTTPS público pendiente |
| SW-02 | Flujo principal sin login | scripts/verificar_ui.cjs; evidencias/11_revision_navegador.json | EN_PROCESO | Contextos limpios sin login; falta incógnito en URL pública |
| SW-03 | CSV, filtros y errores | tests/test_csv.py; test_app.py; evidencias/22_upload_publico.json | VERIFICADO | 2 MiB/10.000 filas; regresión multipart corregida; 5.088 filas ficticias HTTP 200 público y excesos rechazados |
| SW-04 | KPIs exactos y unidades | tests/test_indicadores.py; datos/DICCIONARIO_DATOS.md | VERIFICADO | Seis oráculos, cobertura, Decimal, ponderación y KG/UN |
| SW-05 | IA real activa en URL pública | evidencias/21_ia_real_publica.json; 21_cloud_run_ia_activa.json | VERIFICADO | GPT-6.1-Sol v2 HTTP 200, origen ia_real; falta recorrido desde botón en navegador |
| PE-01 | PROMPT_MAESTRO.md raíz | Archivo íntegro; hash en evidencias/01_plan_aprobado.md; 12_github_publicado.json | VERIFICADO | Igual al original y versionado en repositorio público |
| PE-02 | Reglas del agente | AGENTS.md; evidencias/10_autorizacion_g1.md | VERIFICADO | G0/G1/G2 documentados; G1 ajustado a USD 2 y 66 intentos acumulados; evidencia 17_autorizacion_y_preflight.json; G3 recibido: evidencia 19_autorizacion_g3.json |
| PE-03 | Prompts de sistema versionados | prompts/analista_v1.md; analista_v2.md; 12_github_publicado.json | VERIFICADO | Dos versiones y carga literal comprobadas; ambas versionadas en Git |
| PE-04 | Golden set 5+, objetivo 8–10 | golden_set/casos_analista.json; tests/test_golden_set.py | VERIFICADO | Diez casos reproducibles; evaluación real es PE-05 |
| PE-05 | Mejora medida v1/v2 | docs/EVALUACION_FINAL.md; evidencias/17_evaluacion_real_final.json | VERIFICADO | 90% v1 vs 100% v2 con reintentos; +10 pp en esta muestra. Primer intento: 90% vs 80%. Cierre humano global aprobado; no superioridad estadística general |
| PE-06 | Cálculo y validación fuera LLM | indicadores.py; schemas.py; test_analista_ia.py | VERIFICADO | Contratos/IDs/marcadores; validador revisión 3 y 155 tests; verificación semántica no exhaustiva |
| PE-07 | Inyección, abstención e incertidumbre | GS-05/06/07/09/10; evidencias/17_revision_semantica_asistente.json; 18_cierre_f4_inicio_f6.json | VERIFICADO | Casos reales repetidos; revisión asistida sin inyección obedecida ni mezcla observadas. Cierre humano global aprobado; dos falsos positivos de causalidad recuperados con reintento |
| DEV-01 | README completo | README.md; docs/DESPLIEGUE.md | VERIFICADO | URL real, uso y límites actualizados; publicación documental pendiente |
| DEV-02 | Docker reproducible | Dockerfile con digest; requirements.txt; evidencias/15_docker_build.txt; 15_docker_verificacion.json | VERIFICADO | Imagen Linux amd64 con validador corregido; salud/demo 200 y usuario 10001; .env excluido |
| DEV-03 | Repositorio accesible al profesor | evidencias/16_github_publicado.json; 06_github_url.txt | VERIFICADO | Correcciones 98199c0 publicadas; HTTP 200 sin autenticación, README íntegro y SHA local/remoto iguales |
| DEV-04 | URL HTTPS pública | evidencias/07_url_publica.txt; 21_http_publico_sin_ia.json | EN_PROCESO | HTTPS sin autenticación verificado por HTTP; incógnito visual pendiente |
| DEV-05 | Secretos fuera repo/historial/imagen | evidencias/16_auditoria_indice.json; 16_github_publicado.json; 15_docker_verificacion.json | VERIFICADO | Índice e historial completo auditados antes de push; imagen sin clave; revisión por patrones y coincidencia local, no garantía universal |
| DEV-06 | Secreto en plataforma | evidencias/21_secreto_iam.json; 21_cloud_run_ia_activa.json | VERIFICADO | Versión 1 fijada, secretAccessor exclusivo de runtime sobre el secreto |
| DEV-07 | Control de gasto cloud y API | evidencias/21_presupuesto_cloud.json; 21_confirmacion_cupo_docente.json; 21_presupuesto_validacion.json | VERIFICADO | CLP 4900 alertas 50/80/100, no corte; OpenAI USD 5 aplicado confirmado, demora posible; contadores volátiles |
| DEV-08 | Health y flujo posdespliegue | evidencias/21_http_publico_sin_ia.json; 21_ia_real_publica.json | EN_PROCESO | Health/demo/IA reales por HTTP aprobados; capturas y flujo visual público pendientes |
| COM-01 | Video real máximo 3 min | docs/VIDEO_GUION.md | EN_PROCESO | Guion 180 s; VIDEO NO GRABADO |
| COM-02 | Ficha PDF una página | docs/FICHA_NEGOCIO.pdf; evidencias/09_ficha_negocio.png | EN_PROCESO | Una página y revisión visual verificadas; ficha histórica con modelo anterior; actualizar costos, resultados y URLs |
| COM-03 | Evidencias honestas y bitácora | evidencias/21_*; docs/BITACORA_ENTREGA.md | VERIFICADO | Distingue HTTP de navegador, reserva de consumo, e historial de avances |

Pauta: negocio 20, software 25, prompt engineering 25, despliegue 20 y comunicación 10.
No se declara PROYECTO COMPLETO: falta validación visual pública, video y ficha final. La pauta PDF requiere cuatro entregables
y aplica nota máxima 4,0 si falta un requisito mínimo; no se otorga una nota aquí.

Estado vigente fase 21: F4 cerrado. F6 desplegado con IA activa y HTTP verificado.
Herramienta de navegador no disponible: faltan 375/1440 px, incógnito, capturas y
flujo visual de evidencia/errores. Se conservan 27 requisitos. Disponibilidad
autorizada hasta 30-11-2026. No se atribuye aprobación académica ni puntaje.
