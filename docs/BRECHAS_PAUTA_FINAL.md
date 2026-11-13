# Brechas frente al prompt maestro y la pauta final

**Estado vigente, fase 17:** comparación final real completada: v1 9/10 y v2 10/10
con reintentos. Selección técnica v2; 152 pruebas sin red. Quedan revisión humana
de las respuestas nuevas, dos falsos positivos residuales del filtro, G3 y protección
del gasto público, validación HTTPS, video real y ficha PDF definitiva. Ver
EVALUACION_FINAL.md. Los diagnósticos históricos que siguen no sustituyen este estado.


Actualización fase 16: validador y criterios corregidos, 149 pruebas aprobadas;
revisión asistida de 23 respuestas y aprobación humana global recibida. Se conservan
las observaciones v1. Repetición real final, selección de prompt y G3 pendientes.
Correcciones publicadas bajo G2: commit 98199c0; evidencia 16_github_publicado.json. El diagnóstico siguiente
es histórico (fases 13–14); los estados vigentes están en MATRIZ_CUMPLIMIENTO.md.


Actualización fase 14: correcciones locales del punto 1 realizadas y 139 pruebas
aprobadas. Revalidación de salidas guardadas 9/10 v1 y 10/10 v2, sin API. Sigue
pendiente la revisión semántica humana, selección final y repetición real comparable.
Ver CORRECCIONES_LOCALES.md; el diagnóstico original de abajo conserva contexto.


Revisión: 12-11-2026. Fuentes: PROMPT_MAESTRO.md íntegro y
Proyecto_Final_Advanced_Prompt_Engineering.pdf, una página. La pauta formal prevalece
sobre decisiones técnicas del prompt. No se asigna nota ni aprobación académica.

## Situación comprobada

Motor Decimal, validación CSV, separación KG/UN, filtros, dashboard responsive,
referencias, prompts v1/v2 y diez casos sintéticos implementados. Suite: 100 pruebas
sin red aprobadas. Docker build/run verificados. GitHub público y auditado.
Conexión real GPT-6.1 Sol correcta; comparación completa de veinte casos realizada.
No hay aplicación pública, revisión humana final ni video grabado. La ficha PDF es
preliminar y conserva el modelo/costos anteriores. No es un proyecto cerrado.

## Contraste con los cinco criterios de la pauta

| Criterio | Peso | Estado actual | Lo que falta para nivel excelente |
|---|---:|---|---|
| Idea de negocio | 20 | Cliente, problema, valor, ingresos y escenarios de costo documentados | Actualizar la ficha al modelo vigente, costos medidos/estimados diferenciados y enlaces reales |
| Software funcional | 25 | Flujo local, CSV, cálculos y UI verificados; modelo real evaluado por script | Corregir falsos positivos del validador; demostrar flujo completo desde navegador público, sin ayuda ni login |
| Prompt engineering | 25 | Maestro, reglas, prompts versionados y golden set de diez casos; comparación real | V2 no mejoró: 70% frente a 80% v1. Corregir evaluación, revisión humana, selección de prompt, iteración con mejora comprobada y repetición final |
| Despliegue y buenas prácticas | 20 | Repo público, Docker y auditorías implementados | HTTPS estable, secreto en plataforma, IAM mínimo, límite de gasto del servicio/proveedor, alertas cloud y pruebas posteriores |
| Comunicación | 10 | Guion de 180 segundos y ficha preliminar | Video real máximo tres minutos con demo pública; ficha final de una página y entrega en plataforma |

La pauta considera logrado el apartado de prompts estructurados y golden set sin
mejora demostrada, pero exige mejora medida para excelente. No se fuerza una mejora:
el prompt maestro permite presentar resultados honestos si la nueva versión regresa.

## Pendientes en orden de prioridad

1. **Corregir y cerrar IA.** Resolver falsos positivos ante negaciones de causalidad
   y explicación de cobertura. Revisar el criterio de unidades: citar cumplimiento
   KG/UN expresado en % no significa mezclar volúmenes. Añadir pruebas adversarias,
   congelar la nueva versión del evaluador y comparar ambos prompts en condiciones
   iguales. No reescribir los resultados de fase 13. Revisión humana semántica y
   selección de prompt final pendientes; repetición completa exigida por el maestro.
2. **Proteger el saldo destinado al profesor.** El evaluador ya tiene registro
   persistente hasta USD 2; el endpoint público no. Sus límites por proceso se
   reinician. Configurar límite/cuota efectiva del proveedor si existe, documentar
   restricciones reales y aplicar protección adicional verificable en el servicio.
   Preservar el cupo USD 3 indicado por el usuario. Una recarga o alerta no equivale
   a un límite de gasto. Billing no se ha consultado.
3. **Preparar y ejecutar despliegue.** Identificar proyecto Google Cloud, facturación,
   identidad de servicio, secreto y recursos; concretar costos/IAM/comandos para G3.
   Cloud Run es la elección del maestro; la pauta admite también plataformas
   equivalentes. Publicar solo después de AUTORIZO DESPLIEGUE dentro de ese alcance.
4. **Validación pública.** Incógnito, móvil 375 px y escritorio 1440 px: abrir HTTPS,
   cargar demo, filtrar, comprobar cifras, generar IA real y expandir evidencias.
   Comprobar /health, errores recuperables, versión desplegada y cuota de demo.
   Guardar capturas y metadatos reales sin secretos. El script del golden set no
   sustituye este recorrido desde navegador.
5. **Cerrar documentación y comunicación.** Ficha PDF de una página con GPT-6.1 Sol,
   costos 100/1.000, resultados/limitaciones y URLs reales. Actualizar README/matriz
   con producción. Grabar video máximo tres minutos: problema, demo en vivo y cómo
   se construyó; negocio y resultados medidos sin ocultar regresiones.
6. **Entregar y sostener disponibilidad.** Subir URL, repositorio, video y ficha a la
   plataforma del curso antes del viernes 13-11-2026, 23:59 de Chile. Verificar acceso
   y mantener la app y cupo del profesor durante la corrección; no apagar al entregar.

## Los cuatro entregables formales

| Entregable | Estado |
|---|---|
| URL pública del software funcionando | Falta |
| GitHub accesible con README, maestro, prompts y golden set | Disponible; incorporar evidencias de la fase 13 |
| Video demo real de máximo tres minutos | Falta grabación; hay guion |
| Ficha de negocio PDF de una página | Existe preliminar; falta actualización y cierre |

## Requisitos mínimos que condicionan la nota

La pauta fija nota máxima 4,0 si falta uno de estos mínimos: link público funcionando
al corregir, repo accesible, ninguna clave en el repo y al menos una función con IA
generativa. El repositorio y la exclusión de secretos están verificados. La función
IA existe y se evaluó realmente, pero falta demostrarla en la aplicación pública.
La ausencia actual de URL pública impide cumplir los mínimos de entrega.

## Alcance y autorizaciones

G0 y G2 recibidos; G1 actual limitado a USD 2 para la evaluación acordada. La fase 13
terminó con compromiso conservador USD 0,5843775, incluyendo reservas desconocidas;
no se efectuaron más llamadas. Hay USD 1,4156225 de margen del límite sin utilizar,
pero no se interpreta automáticamente como permiso para repetir la batería final.
G3 no recibido. Este diagnóstico no crea recursos, no amplía gasto y no despliega.

No faltan ERP, login, base de datos comercial, RAG, pronósticos, Kubernetes ni
microservicios: están expresamente fuera del MVP. Tampoco se requiere otro rediseño
visual para cerrar las brechas anteriores.
