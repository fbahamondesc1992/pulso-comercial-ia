# Autorización de conexión y evaluación IA

Fecha del chat: 12-11-2026, America/Santiago.
El usuario respondió «AUTORIZA EVAL IA» y pidió guardar la credencial facilitada
por el docente en el env del producto y hacer un test de conexión simple.
Se interpreta su instrucción explícita como autorización G1, sin exigir repetir
la fórmula gramatical anterior. No se transcribe aquí la credencial.

Presupuesto previamente presentado: OpenAI gpt-5.6-terra, máximo 40 intentos y USD 6
para la primera batería. La conexión breve consume un intento de ese alcance;
quedan como máximo 39 para la batería. Si la conexión falla, detener las llamadas
dependientes y documentar el bloqueo técnico. G2/G3 no autorizados.

La clave queda solo en .env (0600), excluido de Git/Docker. AI_ENABLED=false
mantiene deshabilitado el gasto libre desde el dashboard; la prueba puntual es
explícita y no altera ese interruptor. Se recomendó rotar la clave compartida en chat.
