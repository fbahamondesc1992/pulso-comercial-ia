# Preparación de publicación (NO EJECUTADA)

## G2 GitHub

Antes de `AUTORIZO GITHUB`: revisar archivos, diff y secretos; acordar propietario,
nombre y visibilidad. Recomendación: repositorio público solo con código/datos ficticios.
No hay Git inicializado ni commits. La aprobación G0 no permite commits/push.
Tras G2: inicializar, revisar staging, commit y push normal; registrar URL/hash y
comprobar acceso docente. No force push, credenciales en remote ni cambios ajenos.

## G3 Cloud Run

Región candidata `southamerica-west1`, verificada en la documentación de ubicaciones;
capacidad, permisos y cuota de la cuenta todavía no comprobados. CLI `gcloud` no
disponible en PATH durante F0. Resolver una herramienta adecuada o indicar pasos de consola.

Antes de crear recursos: identificar proyecto y facturación autorizados; presentar
tarifas por SKU, reserva de operación, alcance IAM y recursos concretos. Confirmar
que presupuesto/alertas no se confunden con un límite duro. Verificar cuota real del
proveedor y reservar cupo para el docente. No ampliar acceso o gasto automáticamente.

Configuración propuesta: contenedor Linux compatible con Cloud Run, puerto PORT,
1 vCPU/512 MiB, concurrencia 4, min-instances 0, max-instances 1, timeout HTTP 65 s,
Gunicorn un worker/cuatro threads. No asumir que max-instances garantiza gasto duro.
Imagen local en Apple Silicon requiere verificar plataforma linux/amd64 para despliegue;
el build local por sí solo no prueba compatibilidad con producción.

Cuenta de servicio exclusiva para la app. Acceso Secret Manager únicamente al secreto
necesario, sin roles amplios de editor. API key mediante referencia a versión del
secreto. Nunca pegar valor en comandos, historial, capturas o repositorio.
Habilitar acceso público solo dentro de `AUTORIZO DESPLIEGUE` y sin permisos excesivos.

No se incluye un comando aparentemente listo con IDs ficticios. Cuando se conozcan
proyecto, imagen por digest, identidad y secreto, verificar sintaxis vigente y presentar
el comando concreto sin valores secretos antes de G3.

## Verificación pública

Incógnito: HTTPS → demo → métricas → solicitud IA → referencias expandidas. Debe
probarse IA real, no fallback. Verificar móvil/escritorio y /health. Guardar revisión,
digest, URL, metadatos no sensibles y consumo. La llamada real requiere también saldo G1.
Capturas de presupuestos/cuotas: ocultar números de cuenta y secretos, sin inventarlas.

## Operación y retirada

Registrar ventana de acceso durante corrección. Si se agota cupo, el dashboard sigue
disponible y explica el error. No afirmar entrega completa si IA no está operativa.
Tras autorización de cierre: deshabilitar IA, retirar servicio y recursos exclusivos;
verificar imágenes/secretos/logs remanentes y gasto. No eliminar recursos compartidos.

Fuentes consultadas 12-11-2026:
- https://docs.cloud.google.com/run/docs/locations
- https://docs.cloud.google.com/run/docs/configuring/services/secrets
- https://docs.cloud.google.com/billing/docs/how-to/budgets
- https://cloud.google.com/run/pricing
