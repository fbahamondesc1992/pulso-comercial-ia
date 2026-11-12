# Matriz de cumplimiento · 12-11-2026

Alcance actual: implementación local aprobada G0 y autorización G1 recibida.
La conexión real fue rechazada: HTTP 401 `invalid_api_key` (10_conexion_ia.json).
Nueva clave aún no probada: cambio a gpt-6.1-sol en revisión de presupuesto.
G2 recibido y repositorio público creado; push se documenta al verificarlo. No hay despliegue.
No asigna puntaje ni aprobación comercial/académica.
VERIFICADO significa evidencia concreta dentro del alcance señalado, no una promesa.
Se preservan las 27 filas de la sección 14 del prompt.

| Código | Requisito | Evidencia concreta | Estado | Comentario / limitación |
|---|---|---|---|---|
| NEG-01 | Cliente, problema y diferenciación | README.md; docs/FICHA_NEGOCIO.pdf | VERIFICADO | Definición documentada; negocio no validado comercialmente |
| NEG-02 | IA central y genuina | analista_ia.py; pruebas con cliente falso | EN_PROCESO | Pendiente LLM real en producción |
| NEG-03 | Modelo de ingresos | README.md; ficha PDF | VERIFICADO | Hipótesis SaaS B2B; no declara ventas |
| NEG-04 | Costos mensuales sustentados | docs/COSTOS_Y_LIMITACIONES.md; evidencias/05_fuente_cloud_run.json | VERIFICADO | Escenarios 100/1.000 con tarifas y supuestos; provisión otros explícita, no gasto observado |
| SW-01 | App funcional y responsive | evidencias/11_demo_local_1440.png; 11_demo_local_375.png; 11_revision_navegador.json | EN_PROCESO | Local verificado; HTTPS público pendiente |
| SW-02 | Flujo principal sin login | scripts/verificar_ui.cjs; evidencias/11_revision_navegador.json | EN_PROCESO | Contextos limpios sin login; falta incógnito en URL pública |
| SW-03 | CSV, filtros y errores | tests/test_csv.py; test_app.py; 11_revision_navegador.json | VERIFICADO | 2 MiB/10.000 filas, filtros, error controlado; no exige API real |
| SW-04 | KPIs exactos y unidades | tests/test_indicadores.py; datos/DICCIONARIO_DATOS.md | VERIFICADO | Seis oráculos, cobertura, Decimal, ponderación y KG/UN |
| SW-05 | IA real activa en URL pública | evidencias/10_conexion_ia.json | BLOQUEADO | Clave anterior rechazada; nueva clave/modelo pendientes de prueba y presupuesto. Falta G3 |
| PE-01 | PROMPT_MAESTRO.md raíz | Archivo íntegro; hash en evidencias/01_plan_aprobado.md y bitácora | EN_PROCESO | Igual al original; G2 recibido, versionado en preparación |
| PE-02 | Reglas del agente | AGENTS.md; evidencias/10_autorizacion_g1.md | VERIFICADO | G0/G1/G2 documentados; nuevo modelo requiere revisión de G1; G3 pendiente |
| PE-03 | Prompts de sistema versionados | prompts/analista_v1.md; analista_v2.md; README.md | EN_PROCESO | Dos versiones físicas y carga literal verificadas; Git en preparación con G2 autorizado |
| PE-04 | Golden set 5+, objetivo 8–10 | golden_set/casos_analista.json; tests/test_golden_set.py | VERIFICADO | Diez casos reproducibles; evaluación real es PE-05 |
| PE-05 | Mejora medida v1/v2 | docs/MEJORA_PROMPTS.md; evidencias/10_conexion_ia.json | BLOQUEADO | Cambio a GPT-6.1 Sol en revisión de presupuesto; nueva clave no probada. Ninguna mejora declarada |
| PE-06 | Cálculo y validación fuera LLM | indicadores.py; schemas.py; test_analista_ia.py | VERIFICADO | Contratos/IDs/marcadores; verificación semántica no exhaustiva |
| PE-07 | Inyección, abstención e incertidumbre | GS-05/06/07/09/10; suite local | EN_PROCESO | Controles locales pasan; comportamiento del modelo real pendiente |
| DEV-01 | README completo | README.md | EN_PROCESO | Uso, arquitectura, negocio y controles completos; URLs reales pendientes |
| DEV-02 | Docker reproducible | Dockerfile con digest; requirements.txt; evidencias/11_docker_build.txt; 11_docker_verificacion.json | VERIFICADO | Imagen Linux amd64 actualizada con python-dotenv; salud/demo 200 y usuario 10001; .env excluido |
| DEV-03 | Repositorio accesible al profesor | docs/REVISION_PUBLICACION.md | EN_PROCESO | G2 recibido, repositorio público creado; push y acceso al contenido en verificación |
| DEV-04 | URL HTTPS pública | NO EJECUTADO | BLOQUEADO | Falta G3; localhost no cuenta |
| DEV-05 | Secretos fuera repo/historial/imagen | .gitignore; .dockerignore; evidencias/05_secretos_local.json; 03_docker_verificacion.json | EN_PROCESO | Revisión local e imagen; paquete por lista explícita sin clave; historial no existe, repetir antes de push |
| DEV-06 | Secreto en plataforma | docs/DESPLIEGUE.md | BLOQUEADO | Solo diseño; falta configurar referencia a secreto con G3 |
| DEV-07 | Control de gasto cloud y API | docs/COSTOS_Y_LIMITACIONES.md; tests/test_golden_set.py; test_app.py | EN_PROCESO | Reserva evaluador y límites locales probados; cuotas/alertas cloud sin configurar |
| DEV-08 | Health y flujo posdespliegue | Salud/dashboard locales comprobados | BLOQUEADO | Prueba pública todavía no ejecutada; requiere G3/G1 |
| COM-01 | Video real máximo 3 min | docs/VIDEO_GUION.md | EN_PROCESO | Guion 180 s; VIDEO NO GRABADO |
| COM-02 | Ficha PDF una página | docs/FICHA_NEGOCIO.pdf; evidencias/09_ficha_negocio.png | EN_PROCESO | Una página y revisión visual verificadas; ficha preliminar con URLs pendientes |
| COM-03 | Evidencias honestas y bitácora | evidencias/; docs/BITACORA_ENTREGA.md | VERIFICADO | Distingue mock, local, pendiente y producción no ejecutada |

Pauta: negocio 20, software 25, prompt engineering 25, despliegue 20 y comunicación 10.
No se declara PROYECTO COMPLETO mientras falten IA real pública, repo, evaluación y video.
