# Matriz de cumplimiento · 12-11-2026

Alcance actual: G0/G2 completos; G1 vigente hasta USD 2 acumulados.
Conexión real GPT-6.1 Sol HTTP 200 y veinte casos evaluados (diez por prompt).
V1: 80% y v2: 70% de casos con criterios automáticos cumplidos; sin mejora positiva.
Compromiso conservador total USD 0,5843775; billing no consultado.
GitHub público; despliegue G3, revisión humana, video y ficha final pendientes.
No asigna puntaje ni aprobación comercial/académica.
VERIFICADO significa evidencia concreta dentro del alcance señalado, no una promesa.
Se preservan las 27 filas de la sección 14 del prompt.

| Código | Requisito | Evidencia concreta | Estado | Comentario / limitación |
|---|---|---|---|---|
| NEG-01 | Cliente, problema y diferenciación | README.md; docs/FICHA_NEGOCIO.pdf | VERIFICADO | Definición documentada; negocio no validado comercialmente |
| NEG-02 | IA central y genuina | analista_ia.py; evidencias/13_evaluacion_real.json | EN_PROCESO | LLM real evaluado; falta flujo real en producción |
| NEG-03 | Modelo de ingresos | README.md; ficha PDF | VERIFICADO | Hipótesis SaaS B2B; no declara ventas |
| NEG-04 | Costos mensuales sustentados | docs/COSTOS_Y_LIMITACIONES.md; evidencias/13_resumen_evaluacion.json | EN_PROCESO | Escenarios 100/1.000 actualizados a GPT-6.1 Sol; falta trasladarlos a ficha PDF final |
| SW-01 | App funcional y responsive | evidencias/11_demo_local_1440.png; 11_demo_local_375.png; 11_revision_navegador.json | EN_PROCESO | Local verificado; HTTPS público pendiente |
| SW-02 | Flujo principal sin login | scripts/verificar_ui.cjs; evidencias/11_revision_navegador.json | EN_PROCESO | Contextos limpios sin login; falta incógnito en URL pública |
| SW-03 | CSV, filtros y errores | tests/test_csv.py; test_app.py; 11_revision_navegador.json | VERIFICADO | 2 MiB/10.000 filas, filtros, error controlado; no exige API real |
| SW-04 | KPIs exactos y unidades | tests/test_indicadores.py; datos/DICCIONARIO_DATOS.md | VERIFICADO | Seis oráculos, cobertura, Decimal, ponderación y KG/UN |
| SW-05 | IA real activa en URL pública | evidencias/13_conexion_ia_corregida.json | BLOQUEADO | Conexión local verificada; falta autorización y despliegue G3 con IA activa |
| PE-01 | PROMPT_MAESTRO.md raíz | Archivo íntegro; hash en evidencias/01_plan_aprobado.md; 12_github_publicado.json | VERIFICADO | Igual al original y versionado en repositorio público |
| PE-02 | Reglas del agente | AGENTS.md; evidencias/10_autorizacion_g1.md | VERIFICADO | G0/G1/G2 documentados; G1 ajustado a USD 2 acumulados; G3 pendiente |
| PE-03 | Prompts de sistema versionados | prompts/analista_v1.md; analista_v2.md; 12_github_publicado.json | VERIFICADO | Dos versiones y carga literal comprobadas; ambas versionadas en Git |
| PE-04 | Golden set 5+, objetivo 8–10 | golden_set/casos_analista.json; tests/test_golden_set.py | VERIFICADO | Diez casos reproducibles; evaluación real es PE-05 |
| PE-05 | Mejora medida v1/v2 | docs/MEJORA_PROMPTS.md; evidencias/13_evaluacion_real.json | EN_PROCESO | Comparación real: 80% v1 vs 70% v2; regresión de 10 pp. Falsos positivos, revisión humana y repetición final pendientes |
| PE-06 | Cálculo y validación fuera LLM | indicadores.py; schemas.py; test_analista_ia.py | VERIFICADO | Contratos/IDs/marcadores; verificación semántica no exhaustiva |
| PE-07 | Inyección, abstención e incertidumbre | GS-05/06/07/09/10; suite local | EN_PROCESO | GS-07/10 cumplen criterios automáticos reales; revisión semántica humana pendiente, casos de cobertura/unidad por corregir |
| DEV-01 | README completo | README.md | EN_PROCESO | Uso, arquitectura, negocio y controles completos; URLs reales pendientes |
| DEV-02 | Docker reproducible | Dockerfile con digest; requirements.txt; evidencias/13_docker_build.txt; 13_docker_verificacion.json | VERIFICADO | Imagen Linux amd64 con adaptador GPT-6.1 Sol; salud/demo 200 y usuario 10001; .env excluido |
| DEV-03 | Repositorio accesible al profesor | evidencias/12_github_publicado.json; 06_github_url.txt | VERIFICADO | Público, HTTP 200 sin autenticación, README íntegro y SHA local/remoto iguales |
| DEV-04 | URL HTTPS pública | NO EJECUTADO | BLOQUEADO | Falta G3; localhost no cuenta |
| DEV-05 | Secretos fuera repo/historial/imagen | evidencias/12_github_publicado.json; 12_auditoria_indice.json; 11_docker_verificacion.json | VERIFICADO | Índice e historial completo auditados antes de push; imagen sin clave; revisión por patrones y coincidencia local, no garantía universal |
| DEV-06 | Secreto en plataforma | docs/DESPLIEGUE.md | BLOQUEADO | Solo diseño; falta configurar referencia a secreto con G3 |
| DEV-07 | Control de gasto cloud y API | docs/COSTOS_Y_LIMITACIONES.md; tests/test_golden_set.py; test_app.py | EN_PROCESO | Presupuesto persistente del evaluador comprobado hasta USD 2; no protege endpoint público; cuotas/alertas cloud pendientes |
| DEV-08 | Health y flujo posdespliegue | Salud/dashboard locales comprobados | BLOQUEADO | Prueba pública todavía no ejecutada; requiere G3/G1 |
| COM-01 | Video real máximo 3 min | docs/VIDEO_GUION.md | EN_PROCESO | Guion 180 s; VIDEO NO GRABADO |
| COM-02 | Ficha PDF una página | docs/FICHA_NEGOCIO.pdf; evidencias/09_ficha_negocio.png | EN_PROCESO | Una página y revisión visual verificadas; ficha histórica con modelo anterior; actualizar costos, resultados y URLs |
| COM-03 | Evidencias honestas y bitácora | evidencias/; docs/BITACORA_ENTREGA.md | VERIFICADO | Distingue mock, local, pendiente y producción no ejecutada |

Pauta: negocio 20, software 25, prompt engineering 25, despliegue 20 y comunicación 10.
No se declara PROYECTO COMPLETO: faltan IA pública, mejora positiva/revisión final,
control de gasto público, video y ficha final. La pauta PDF requiere cuatro entregables
y aplica nota máxima 4,0 si falta un requisito mínimo; no se otorga una nota aquí.
