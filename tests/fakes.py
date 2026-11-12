import json
from analista_ia import RespuestaProveedor


def informe_valido(payload):
    ids = [h["id"] for h in payload["hechos"] if h["estado"] == "valido" and h["valor"] is not None]
    return {"resumen_ejecutivo": "Los hechos permiten una lectura descriptiva." if ids else "La evidencia es insuficiente para un diagnóstico.",
            "hallazgos": [{"titulo": "Resultado observado", "descripcion": "Conviene revisar este indicador: {{"+ids[0]+"}}.", "evidencia_ids": [ids[0]], "nivel": "informativo"}] if ids else [],
            "acciones_sugeridas": [{"accion": "Revisar el detalle del período.", "evidencia_ids": [ids[0]], "categoria": "investigacion"}] if ids else [],
            "limitaciones": ["No se dispone de información causal."]}


class ProveedorFalso:
    real = False
    def __init__(self, respuestas=None):
        self.respuestas = list(respuestas or [])
        self.calls = []

    def generar(self, sistema, payload, correccion=False):
        self.calls.append((sistema, payload, correccion))
        result = self.respuestas.pop(0) if self.respuestas else informe_valido(payload)
        if isinstance(result, Exception):
            raise result
        return RespuestaProveedor(result if isinstance(result, str) else json.dumps(result), "FAKE-SIN-IA", 0, 0)
