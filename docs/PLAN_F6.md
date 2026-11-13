# F6 · plan de despliegue para revisión

Estado: preparación local; G3 no recibido. F4 cerrado por el usuario (evidencia 18).
Disponibilidad solicitada hasta el 30-11-2026, inclusive, hora de Chile. No se programa
borrado automático: retirada posterior por decisión del usuario. No hay proyecto
dedicado a Pulso. Se verificó acceso autenticado y una cuenta de facturación con
estado visible «Cuenta pagada». Sus identificadores se conservan solo en entrega/
(excluido de Git). Vincular el proyecto nuevo a esa cuenta requiere G3. No existe URL pública.

## Recursos y alcance propuestos

| Recurso | Configuración propuesta |
|---|---|
| Proyecto dedicado | Nombre Pulso Comercial IA; ID candidato pulso-comercial-ia-uai-2026, disponibilidad no comprobada |
| Región | southamerica-west1 (Santiago); confirmar cuota y SKU en el proyecto nuevo |
| Artifact Registry | Un repositorio Docker regional pulso; imagen amd64 desplegada por digest |
| Cloud Run | Un servicio pulso-comercial-ia, puerto 8080, 1 vCPU, 512 MiB |
| Escalamiento | Facturación por solicitud, mínimo 0, máximo de servicio 1 y de revisión 1; concurrencia 1; timeout 65 s |
| Identidad de ejecución | Una cuenta pulso-runtime sin claves descargables |
| Secret Manager | Un secreto pulso-openai-key, versión numérica fijada en el despliegue |
| Aplicación | Modelo gpt-6.1-sol, prompt v2, 1.800 tokens, timeout proveedor 20 s; un reintento máximo |
| Tráfico | HTTPS público sin login, acceso desde navegador; sin dominio comprado |

No se propone base de datos, VPC, balanceador separado ni persistencia de CSV.
Primera revisión cloud con IA deshabilitada; activación solo tras verificar gasto y
credencial. La clave se transfiere por entrada estándar o interfaz segura a Secret
Manager, nunca como literal en comando, captura, repositorio o imagen.

## Ejecución y permisos

1. El usuario inicia sesión en Google Cloud y completa los requisitos de facturación
   y pago de su cuenta. No se solicitan datos bancarios por chat.
2. Bajo G3, crear el proyecto dedicado y asociar la cuenta de facturación elegida.
   Si el ID candidato está ocupado, acordar el ID real antes de seguir.
3. Usar Google Cloud Shell, que evita instalar gcloud globalmente en este equipo.
   Inspeccionar identidad, proyecto, facturación, organización y políticas aplicables.
4. Habilitar Cloud Run, Artifact Registry y Secret Manager. Preferir la imagen local
   ya verificada; si se requiere Cloud Build, presupuestar y autorizar ese recurso
   adicional antes de usarlo. No subir todo el workspace como contexto de compilación.
5. Operador de despliegue: permisos de administración de Cloud Run, creación del
   repositorio y secreto, creación de cuenta de servicio y permiso para utilizarla;
   habilitación de APIs solo donde sea necesario. No otorgar Owner/Editor a la app.
   Las acciones de creación y vínculo de facturación requieren permisos del usuario.
6. Cuenta pulso-runtime: roles/secretmanager.secretAccessor únicamente sobre el
   secreto pulso-openai-key. La lectura de imagen usa las identidades administradas
   de Cloud Run; no conceder acceso amplio a la cuenta runtime.
7. Registrar imagen por digest remoto, revisión, configuración efectiva e IAM. Usar
   --no-invoker-iam-check para el acceso público si las políticas lo permiten; no
   relajar una política de organización si lo impide.

La sintaxis de deploy fue consultada en la documentación oficial. No se genera un
comando ejecutable con IDs o digest inventados. Tras conocer los identificadores,
el comando debe incluir --project, --region, --image por digest, --service-account,
--cpu=1, --memory=512Mi, --port=8080, --min=0, --max=1, --max-instances=1,
--concurrency=1, --timeout=65, --cpu-throttling y la referencia numérica al secreto.
Verificar esas opciones en Cloud Shell antes de ejecutarlas.

## Gasto y protección del cupo docente

Propuesta de provisión para Google Cloud: **USD 5 para el período hasta 30/11**,
separados del saldo OpenAI. Es un presupuesto operativo propuesto, no precio fijo
ni garantía de gasto máximo. Alertas al 50%, 80% y 100%; no son un corte automático.
Revisar costos diariamente durante la ventana. No crear una automatización aún.

Cloud Run cobra CPU, memoria y solicitudes; escala a cero reduce tiempo ocioso.
Santiago figura en Tier 2. La tabla dinámica consultada no certifica el SKU efectivo
del proyecto: calcular el importe regional en la consola antes de aprobar ejecución.
No asumir costo cero ni trasladar tarifas de otra región. Considerar además tráfico,
logs, arranques, almacenamiento de imagen y secreto. Los límites de instancias no
son un límite financiero estricto.

Artifact Registry publica almacenamiento de USD 0,000136986 por GiB-h fuera de su
franquicia; 1 GiB durante 19 días equivale a unos USD 0,0625 antes de descuentos.
Una versión activa de secreto a USD 0,000082192/h equivale a unos USD 0,0375 en ese
plazo, más accesos fuera de franquicia. Son supuestos de planificación; el tamaño
comprimido real, franquicias compartidas, impuestos y moneda se verifican en la cuenta.

OpenAI dispone de límites efectivos por proyecto, con posible demora de aplicación.
El usuario confirma que puede administrarlos. Antes de habilitar IA:

- Comprobar el proyecto al que pertenece la clave y su gasto mensual real. No tocar
  límites globales ni recursos compartidos del docente sin alcance explícito.
- Activar Enforce a hard limit; una alerta sola no basta. Documentar valor, gasto
  acumulado de ese mes, margen y alertas. Un límite mensual no es un saldo adicional.
- Proponer un cupo de uso docente de USD 2,50 más USD 0,50 de margen dentro de los
  USD 3 reservados; ese margen no garantiza absorber cualquier sobrepaso por demora.
  El importe absoluto del límite depende del gasto mensual observado y del alcance
  exclusivo o compartido del proyecto. No inventarlo a partir del registro local.
- Reducir límites de la demo a 2 solicitudes/IP/h y 3 globales/h, concurrencia 1.
  Los contadores se reinician con el proceso y no sustituyen el límite del proveedor.
  El acceso público puede consumir el cupo antes que el profesor; vigilar disponibilidad.
- Proponer para la prueba pública hasta dos intentos de API y USD 0,336 adicionales,
  dentro del margen del tope de evaluación USD 2, sujetos a autorización expresa de
  ese nuevo alcance. No descontarlos de los USD 3 del docente. No se ejecutaron.

Si no se verifica un control efectivo en la cuenta, no activar la IA pública; presentar
una alternativa de control persistente antes de modificar arquitectura o crear recursos.

## Pruebas de aceptación y recuperación

Verificar /health, demo y upload inválido; abrir sin login en incógnito, a 375 y
1440 px. Generar un análisis real, revisar IDs/cifras y expansión de evidencia;
registrar costo, revisión, digest y capturas reales sin credenciales. Verificar
respuesta recuperable cuando falta clave o se supera cuota; el dashboard debe seguir.

Rollback: devolver tráfico a una revisión previamente verificada, sin duplicar el
servicio; ante gasto o error, deshabilitar IA y conservar el dashboard. Después de
la ventana, acordar retirada del servicio, versiones del secreto e imágenes exclusivos,
verificando costos remanentes. No retirar antes del cierre docente acordado.

## Pendientes para concretar G3

Acceso autenticado y cuenta pagada verificados en consola. Pendientes: ID definitivo, permisos efectivos,
tarifa regional, tamaño de imagen, identidad y versión del secreto; límite OpenAI y
gasto mensual verificados. La propuesta de USD 5 cloud y la prueba pública pagada no
están autorizadas todavía. No hay recursos externos creados por esta fase.

Fuentes oficiales consultadas el 12-11-2026:
- https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy
- https://cloud.google.com/run/pricing
- https://cloud.google.com/artifact-registry/pricing
- https://cloud.google.com/secret-manager/pricing
- https://developers.openai.com/api/docs/guides/spend-limits
