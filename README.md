# Pulso Comercial IA

Copiloto ejecutivo de ventas: **Python calcula y valida; el LLM interpreta; el usuario decide.**

Estado al 12-11-2026: MVP local verificado; publicación GitHub autorizada G2.
Repositorio creado: https://github.com/fbahamondesc1992/pulso-comercial-ia
URL de la aplicación: **PENDIENTE**. Evaluación IA y video: **PENDIENTES**.
La clave anterior devolvió 401; el usuario la reemplazó. La nueva todavía no fue
probada porque también seleccionó `gpt-6.1-sol` y pidió revisar primero su presupuesto.
El código conserva `gpt-5.6-terra` hasta completar esa revisión/migración; no usar
`AI_ENABLED=true` con el nuevo modelo antes de adaptar parámetros y tarifas.
G3 sigue pendiente. Ver [revisión del modelo](docs/REVISION_MODELO_GPT61_SOL.md).

![Dashboard local con datos ficticios](evidencias/11_demo_local_1440.png)

## Cliente, problema y negocio

Para dueños y gerencias comerciales de pymes distribuidoras/mayoristas que consolidan
ventas y metas en planillas. La carga manual dificulta comparar períodos y detectar
brechas. El producto reúne indicadores verificables y una explicación ejecutiva con
evidencia. La promesa «de una planilla a una explicación en minutos» es una hipótesis
de valor, no una medición de productividad.

La IA aporta síntesis y preguntas de investigación, con referencias a cifras del motor.
La diferenciación es la trazabilidad y la separación entre cálculo e interpretación.
Monetización propuesta: SaaS B2B mensual por empresa/equipo o cupo de análisis; demo
gratuita. No hay precio validado, clientes pagadores demostrados ni cobros implementados.
Escenarios operativos: [costos y limitaciones](docs/COSTOS_Y_LIMITACIONES.md).

## Ejecutar localmente

Requiere Python 3.12. No usar el Python 3.9 del sistema inspeccionado.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python app.py
```

Abrir http://127.0.0.1:8080. La app escucha solo localmente en este modo.
En el entorno ya preparado bastan el último comando y el navegador.
No se requiere credencial para usar datos, filtros y KPIs.

1. Pulsar «Probar con datos de demostración» o cargar un CSV ficticio.
2. Seleccionar años, meses y dimensiones; aplicar filtros.
3. Revisar cobertura, metas, volumen por unidad y rankings.
4. Solicitar IA cuando el servicio esté autorizado y habilitado.
5. Expandir evidencia de cada hallazgo y revisar fórmula, período, unidad e ID.

Sin configuración de IA aparece un error recuperable y un **Resumen automático sin IA**.
No se simula una respuesta real. Al cambiar filtros se invalida el análisis previo.

## Configuración

`.env.example` contiene solo nombres y valores de ejemplo. Al ejecutar directamente
`.venv/bin/python app.py`, se carga el `.env` local sin sobrescribir variables del
proceso ni interpolar expresiones. Importar la app en pytest o Gunicorn no carga .env.
En local configurar variables en el proceso, nunca copiar una clave al chat, código o
comandos guardados. En producción referenciar Secret Manager.

| Variable | Valor inicial / efecto |
|---|---|
| PORT | 8080 |
| AI_ENABLED | false; requiere activación expresa después de G1 |
| OPENAI_API_KEY | Solo servidor, nunca frontend ni repositorio |
| AI_MODEL | gpt-5.6-terra; disponibilidad en cuenta pendiente |
| ANALYST_PROMPT_VERSION | v2, candidata sin mejora real medida |
| AI_TIMEOUT_SECONDS | 20 por intento, máximo admitido 30 |
| AI_MAX_OUTPUT_TOKENS | 1800, rango admitido 256..2400 |
| AI_REQUESTS_PER_IP_HOUR | 5 por proceso |
| AI_REQUESTS_GLOBAL_HOUR | 30 por proceso |

## Datos y metodología

`datos/demo_ventas.csv`: 360 filas ficticias, enero-octubre 2025/2026, tres canales,
dos líneas/familias, tres oficinas, KG y UN. Regenerable con
`.venv/bin/python scripts/generar_demo.py`.
Contrato completo: [diccionario](datos/DICCIONARIO_DATOS.md).

Facturación y meta son sumas Decimal; brecha=real-meta; cumplimiento=sum(real)/sum(meta).
YoY compara mismos meses con cobertura comprobada a nivel de grano. Ausencias no son
ceros; meta parcial invalida tasas/brecha afectadas. CLP entero y porcentajes con un
decimal, ROUND_HALF_UP al mostrar. KG y UN separados; KG/1000 a TON en presentación.
Las participaciones de brecha usan negativas brutas de una sola dimensión.

## Arquitectura y estructura

```text
Navegador: archivo en memoria + filtros
  → Flask / validador_csv.py
  → indicadores.py (Decimal y cobertura)
  → dashboard + hechos con IDs
  → analista_ia.py + prompts versionados + OpenAI
  → Pydantic / referencias / política numérica / restricciones
  → explicación o error seguro
```

`app.py`: rutas y seguridad HTTP; `schemas.py`: contratos; `templates`/`static`: UI;
`datos`: demo/diccionario; `prompts`: sistema v1/v2; `golden_set`: diez casos;
`scripts`: evaluación y verificación; `tests`: regresión; `docs`: metodología y entrega;
`evidencias`: resultados reales y pendientes claramente rotulados.

No hay base de datos. Cada petición vuelve a validar y calcular el archivo. Nunca se
confía en KPIs enviados por el navegador. El snapshot vincula informe/dataset/filtros.
El proveedor recibe solo agregados con alias; no recibe el CSV original.
La prosa de IA usa marcadores de hechos; Python inserta cifras y unidades. Las reglas
semánticas automáticas no garantizan por sí solas que toda interpretación sea correcta.

Rutas: `GET /`, `GET /health`, `GET /demo.csv`, `POST /api/dashboard`,
`POST /api/analisis`. Las APIs requieren `X-Pulso-Request: 1`; no admiten CORS público.
`/health` no llama al proveedor y un 200 no certifica que la IA esté disponible.

## Pruebas y evaluación

```bash
.venv/bin/python -m pytest -q
.venv/bin/python scripts/evaluar_prompts.py
.venv/bin/python scripts/evaluar_prompts.py --modo mock --salida evidencias/04_mock_nueva_corrida.json
```

Prueba puntual autorizada: `.venv/bin/python scripts/probar_conexion_ia.py --ejecutar`.
Lee la clave de .env, realiza un intento con 32 tokens máximos de salida y no imprime
el cuerpo de errores ni la credencial. No sobrescribe evidencia existente; para una
clave reemplazada usar una nueva ruta `--salida`. El rechazo histórico corresponde a la clave anterior; la nueva no fue probada.
AI_ENABLED=false conserva deshabilitado el gasto desde el dashboard.

Pytest bloquea red. Golden set con cliente falso verifica infraestructura, no calidad
de IA. [Protocolo y comparación pendiente](docs/MEJORA_PROMPTS.md).
La evaluación real necesita `AUTORIZO EVAL IA` y presupuesto explícito.
El script conserva resultados por caso, se detiene antes de superar su reserva y no
sobrescribe evidencias. Repetirlo no renueva una autorización de gasto.

Prueba de navegador: `node scripts/verificar_ui.cjs`, con Playwright disponible;
`PLAYWRIGHT_MODULE_PATH` permite señalar la instalación y `PLAYWRIGHT_BROWSERS_PATH`
su Chromium. Los binarios de esta revisión se instalaron dentro de `.venv`.
La revisión verifica demo, filtros, errores, fallback y ausencia de desbordes a 375/1440.
No acredita experiencia móvil en dispositivo físico ni producción.

## Docker y despliegue

```bash
docker build -t pulso-comercial-ia:local .
docker run --rm -p 127.0.0.1:8081:8080 -e PORT=8080 pulso-comercial-ia:local
curl -i http://127.0.0.1:8081/health
```

El 8081 evita colisión con el servidor local 8080. El contenedor utiliza Gunicorn,
un worker/cuatro threads y usuario sin privilegios. `.dockerignore` es una lista de
inclusión de archivos de ejecución. La imagen no incluye evidencia, tests ni secretos.
Estado efectivo del build: consultar [bitácora](docs/BITACORA_ENTREGA.md).

Publicación planificada en Cloud Run Santiago, HTTPS sin login, solo después de G3.
No ejecutar publicación antes de revisar [preparación de despliegue](docs/DESPLIEGUE.md).
G2 recibido: repositorio público creado. La auditoría de secretos precede a cada push.

## Seguridad, actualización y límites

CSV en memoria, máximo 2 MiB/10.000 filas; no se aceptan pickle/eval ni comandos.
Escaping por textContent/Jinja; CSP sin scripts externos/inline; cabeceras defensivas.
Sin logs de archivos/prompts privados; errores no exponen stack traces ni credenciales.
Auditar con `.venv/bin/python -m pip_audit -r requirements.txt` y revisión de secretos
antes de publicar. La auditoría reporta vulnerabilidades conocidas en la fecha, no
ausencia absoluta de vulnerabilidades. Versiones directas/transitivas fijadas; para
actualizar, resolver en entorno aislado, revisar cambios y repetir suite/auditoría/build.
La base Docker quedó fijada a versión y digest verificado durante el build local.

Contadores de solicitudes son volátiles por proceso. No garantizan gasto máximo.
Alertas cloud, cuotas del proveedor, Secret Manager y acceso docente siguen pendientes.
MVP sin login, ERP, persistencia, usuarios, RAG, pronósticos, precios ni datos reales.

## Entrega y apagado

- [Matriz completa](docs/MATRIZ_CUMPLIMIENTO.md), [bitácora](docs/BITACORA_ENTREGA.md).
- [Ficha de negocio PDF](docs/FICHA_NEGOCIO.pdf): versión local con pendientes visibles.
- [Guion de video](docs/VIDEO_GUION.md): no sustituye grabación real.
- URL pública: PENDIENTE; video: NO GRABADO. GitHub enlazado al inicio.

Detener local: Ctrl+C en el proceso Flask/Gunicorn. Contenedor: detener su ID con
`docker stop ID`; se elimina al usar --rm. No borrar imágenes ni recursos ajenos.
En cloud, mantener la app durante corrección; tras fecha acordada, deshabilitar IA y
retirar servicio/revisiones, imágenes, secretos y recursos propios con autorización.
Verificar facturación residual de almacenamiento/logs; detener la app no elimina todo costo.

## Paquete local para revisión

`.venv/bin/python scripts/preparar_entrega.py` genera
`entrega/Pulso_Comercial_IA_MVP_LOCAL.zip` con lista explícita, manifiesto SHA256
y revisión de credenciales. `.env`, entornos, caches y PDF original del curso
quedan fuera. La carpeta entrega está excluida de Git.

[Registro de publicación](docs/REVISION_PUBLICACION.md): G2 autorizado para
fbahamondesc1992/pulso-comercial-ia, público. Despliegue pendiente de G3.
El ZIP anterior representa el cierre local previo a G2; su manifiesto fecha ese estado.

Actualización local: 96 pruebas sin red, imagen Linux amd64 con python-dotenv,
salud/dashboard 200, revisión responsive y recuperación de CSV inválido.
Evidencias de esta versión en `evidencias/11_*`.
