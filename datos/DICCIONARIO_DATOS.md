# Datos sintéticos y contrato comercial

Origen: generador determinista `scripts/generar_demo.py`. Ninguna empresa, cliente,
oficina o transacción real. 360 registros, 2025/2026, enero-octubre; tres canales,
dos líneas/familias y tres oficinas ficticias. Familia Preparados ficticios en KG;
Packs ficticios en UN. No contiene datos personales ni precios internos.

| Columna | Tipo y significado |
|---|---|
| ano | Cuatro dígitos; año del registro |
| mes | Entero 1..12 |
| canal | Texto obligatorio hasta 80 caracteres |
| linea | Texto obligatorio hasta 80 caracteres |
| familia | Texto obligatorio hasta 100 caracteres |
| oficina | Texto obligatorio hasta 80 caracteres |
| unidad_ump | KG (kilogramos) o UN (unidades) |
| facturacion_real_clp | Venta positiva o cero en CLP |
| facturacion_meta_clp | Meta CLP; vacío significa ausente, nunca cero |
| volumen_real_ump | Volumen no negativo, en la unidad de la fila |
| volumen_meta_ump | Meta en la misma unidad; vacío significa ausente |

UTF-8 con BOM opcional, comas como delimitador, punto decimal, sin separador de
miles ni notación científica. Máximo 15 dígitos enteros y 6 decimales, 2 MiB por
archivo y 10.000 filas. El límite HTTP incluye 64 KiB adicionales para el multipart.
Se acepta el mismo conjunto exacto de columnas en otro orden. Columnas adicionales
o duplicadas, filas vacías/mal formadas, NaN, infinito y negativos se rechazan.

Grano único: ano|mes|canal|linea|familia|oficina|unidad_ump. Duplicados se rechazan
con referencias de línea. Se aplica Unicode NFC y trim exterior, informando cambios.
No se cambia mayúsculas ni espacios interiores. Caracteres de control se rechazan.
Colisiones tras normalización se rechazan; no se agregan silenciosamente.

## Cálculo y cobertura

Moneda única CLP. Decimal con contexto local de 50 dígitos; no redondear sumandos.
Presentación ROUND_HALF_UP: CLP entero, porcentajes y volúmenes a un decimal.
KG/1.000 produce TON solo para presentación; el valor original permanece en KG.
No existe volumen total combinado KG+UN.

El año base puede carecer de metas sin afectar la comparación de ventas. Las metas
vacías actuales son una excepción documentada al esquema estricto: la suma disponible
se rotula parcial y no produce brecha ni cumplimiento del agregado afectado.
Real/meta se divide después de sumar, nunca se promedian porcentajes individuales.
Meta cero produce cumplimiento N/C y brecha real-meta válida si la cobertura existe.

La cobertura se comprueba por cada combinación de dimensiones/unidad y mes para
ambos años. El universo de combinaciones proviene de los dos años seleccionados.
Una ausencia no equivale a cero. La comparación total se invalida ante cualquier
mes/grupo ausente; se informa la lista de meses con cobertura común, sin recalcular
silenciosamente otro período. Base cero explícita y cobertura completa permite
diferencia absoluta; porcentaje N/C/Nuevo. Sin base observada, N/C.

Se rechazan meses futuros; el mes actual advierte que podría no estar cerrado.
Sin datos seleccionados se devuelve error recuperable. Un único año permite mostrar
KPIs actuales y N/C interanual; el selector identifica el año base sin datos.

Ranking por dimensión: brecha ascendente, solo negativas; participación sobre suma
de brechas negativas brutas de esa misma partición, no sobre brecha neta. Si algún
grupo de la partición no es comparable, su participación se invalida.
El top por canal, línea, familia y oficina se superpone: nunca sumarlos entre sí.

## Límites de interpretación

Datos ya agregados, sin devoluciones ni notas de crédito. No hay evidencia sobre
precios, promociones, competencia, demanda o stock. No hay pronósticos, causalidad,
rentabilidad, ticket o clientes únicos. La presencia de una fila no prueba que un
mes esté cerrado ni que el universo comercial original esté completo.
