"""Proveedor real opt-in, referencias verificables y cifras insertadas por Python."""
import hashlib
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError
from schemas import InformeIA
from indicadores import formato, LABELS

ROOT = Path(__file__).resolve().parent
MODEL = "gpt-6.1-sol"
MAX_PAYLOAD_BYTES = 32_000
MAX_PROMPT_BYTES = 12_000
TOKEN = re.compile(r"\{\{(F\d{3})\}\}")
URL = re.compile(r"https?://|www\.|mailto:|[\w.+-]+@[\w.-]+\.[a-z]{2,}", re.I)
CAUSA = re.compile(r"\b(debido a|causad[oa] por|se debe a|producto de|a causa de|explicad[oa] por|por (?:el |la |los |las )?(?:precio|stock|promoci|competencia))", re.I)
CAUSAL_TEMA = re.compile(r"\b(precios?|stock|quiebre|competencia|promociones?|demanda)\b", re.I)
NUM_PALABRA = re.compile(r"\b(cien|ciento|doscientos|trescientos|cuatrocientos|quinientos|mil|mill[oó]n|millones|por ciento)\b", re.I)


class ErrorIA(ValueError):
    def __init__(self, codigo, mensaje="No fue posible generar un análisis verificable", intentos=None):
        super().__init__(mensaje)
        self.codigo = codigo
        self.intentos = intentos or []


@dataclass
class RespuestaProveedor:
    texto: str
    modelo: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    request_id: str | None = None
    estado: str = "completed"


class ProveedorOpenAI:
    real = True

    def __init__(self, model=None, timeout=20, max_output_tokens=1800, sdk_client=None):
        # Ni una credencial presente habilita gasto por sí sola.
        if os.getenv("AI_ENABLED", "false").lower() != "true":
            raise ErrorIA("ia_deshabilitada", "La IA real aún no está habilitada. Los indicadores siguen disponibles.")
        if not os.getenv("OPENAI_API_KEY") and sdk_client is None:
            raise ErrorIA("sin_clave", "Falta configurar la credencial de IA en el servidor.")
        if not 1 <= timeout <= 30 or not 256 <= max_output_tokens <= 2400:
            raise ValueError("Límites de IA fuera del rango permitido.")
        from openai import OpenAI
        import httpx2
        self.client = sdk_client or OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1",
            timeout=timeout, max_retries=0,
            http_client=httpx2.Client(trust_env=False, timeout=timeout))
        self.model = model or os.getenv("AI_MODEL", MODEL)
        self.timeout = timeout
        self.max_output_tokens = max_output_tokens

    def generar(self, sistema, payload, correccion=False):
        # Sin tools, historial, CSV, almacenamiento de respuesta ni base_url del usuario.
        response = self.client.responses.create(
            model=self.model,
            input=[{"role": "system", "content": sistema}, {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            text={"format": {"type": "json_schema", "name": "informe_comercial", "strict": True, "schema": InformeIA.model_json_schema()}},
            reasoning={"effort": "low"}, max_output_tokens=self.max_output_tokens,
            store=False, service_tier="default", prompt_cache_options={"ttl": "30m"},
        )
        usage = response.usage
        return RespuestaProveedor(response.output_text, response.model,
            usage.input_tokens if usage else None, usage.output_tokens if usage else None,
            getattr(response, "_request_id", None), response.status)


def cargar_prompt(version):
    if version not in ("v1", "v2"):
        raise ErrorIA("version_invalida", "La versión del prompt no es válida.")
    text = (ROOT / "prompts" / f"analista_{version}.md").read_text(encoding="utf-8")
    if len(text.encode()) > MAX_PROMPT_BYTES:
        raise ErrorIA("prompt_demasiado_largo")
    return text


def validar_informe(raw, payload):
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ErrorIA("json_invalido") from exc
    try:
        informe = InformeIA.model_validate(parsed)
    except ValidationError as exc:
        raise ErrorIA("schema_invalido") from exc
    hechos = {h["id"]: h for h in payload["hechos"]}
    all_refs = {ref for item in [*informe.hallazgos, *informe.acciones_sugeridas] for ref in item.evidencia_ids}
    if not all_refs <= hechos.keys():
        raise ErrorIA("ids_invalidos")
    validos = {k for k, h in hechos.items() if h["estado"] == "valido" and h["valor"] is not None}
    if not validos and (informe.hallazgos or informe.acciones_sugeridas):
        raise ErrorIA("requiere_abstencion")
    if validos and not informe.hallazgos:
        raise ErrorIA("hallazgo_sin_evidencia")

    def texto_seguro(text, refs, permitir_hipotesis=False):
        tokens = set(TOKEN.findall(text))
        if not tokens <= refs:
            raise ErrorIA("ids_invalidos")
        limpio = TOKEN.sub("", text)
        # Política conservadora: cifras solo mediante tokens de hechos, nunca texto libre.
        # Se rechaza incluso una cifra plausible si su correspondencia semántica es ambigua.
        if re.search(r"\d|[{}]", limpio) or NUM_PALABRA.search(limpio):
            raise ErrorIA("cifra_sin_respaldo")
        if URL.search(limpio) or re.search(r"<[^>]+>", limpio):
            raise ErrorIA("contenido_externo")
        if CAUSA.search(limpio):
            raise ErrorIA("causalidad_no_sustentada")
        if CAUSAL_TEMA.search(limpio) and not permitir_hipotesis and not re.search(r"no (?:se dispone|hay|contamos)|sin (?:datos|informaci[oó]n)", limpio, re.I):
            raise ErrorIA("causalidad_no_sustentada")
        return tokens

    texto_seguro(informe.resumen_ejecutivo, all_refs)
    for h in informe.hallazgos:
        refs = set(h.evidencia_ids)
        texto_seguro(h.titulo, refs)
        tokens = texto_seguro(h.descripcion, refs)
        if not tokens or not tokens.intersection(validos):
            raise ErrorIA("hallazgo_sin_evidencia")
    for accion in informe.acciones_sugeridas:
        # Las hipótesis solo se admiten como investigación/pregunta, nunca afirmación causal.
        es_pregunta = bool(re.match(r"(?:Investigar|Revisar|Comprobar|Verificar|Explorar|Contrastar)\b", accion.accion, re.I))
        texto_seguro(accion.accion, set(accion.evidencia_ids), permitir_hipotesis=es_pregunta)
    for limitacion in informe.limitaciones:
        texto_seguro(limitacion, all_refs)
    return informe


def renderizar_informe(informe, payload):
    """Expande referencias con nombre de métrica, valor/unidad y ámbito. HTML nunca."""
    hechos = {h["id"]: h for h in payload["hechos"]}
    def sustituir(text):
        def expand(match):
            h = hechos[match.group(1)]
            valor = formato(h["valor"], h["unidad"]) if h["estado"] == "valido" else "N/C"
            return f"{LABELS[h['indicador']]}: {valor} [{h['id']}]"
        return TOKEN.sub(expand, text)
    result = informe.model_dump()
    result["resumen_ejecutivo"] = sustituir(result["resumen_ejecutivo"])
    for h in result["hallazgos"]:
        h["titulo"], h["descripcion"] = sustituir(h["titulo"]), sustituir(h["descripcion"])
    for a in result["acciones_sugeridas"]:
        a["accion"] = sustituir(a["accion"])
    result["limitaciones"] = [sustituir(x) for x in result["limitaciones"]]
    return result


def analizar(payload, proveedor, version="v2", observador=None, antes_llamada=None):
    if len(json.dumps(payload, ensure_ascii=False).encode()) > MAX_PAYLOAD_BYTES:
        raise ErrorIA("contexto_excesivo", "El contexto excede el límite de la demo. Reduce los filtros.")
    system = cargar_prompt(version)
    intentos = []
    for attempt in range(2):
        if antes_llamada:
            antes_llamada()
        start = time.monotonic()
        respuesta = None
        registro = {"intento": attempt + 1, "prompt": version, "prompt_sha256": hashlib.sha256(system.encode()).hexdigest()}
        try:
            # Corrección fija: nunca reinyectar respuesta inválida o datos no confiables al sistema.
            prompt = system + ("\nCorrección: la respuesta anterior no pasó las validaciones. Revisa el esquema, usa solo {{Fxxx}} para cifras, referencias válidas y abstente si falta evidencia." if attempt else "")
            respuesta = proveedor.generar(prompt, payload, correccion=bool(attempt))
            registro.update({"modelo": respuesta.modelo, "input_tokens": respuesta.input_tokens,
                             "output_tokens": respuesta.output_tokens, "request_id": respuesta.request_id})
            if respuesta.estado != "completed" or not respuesta.texto:
                raise ErrorIA("respuesta_incompleta")
            try:
                informe = validar_informe(respuesta.texto, payload)
                registro["estado"] = "valido"
            except ErrorIA as error:
                registro["estado"] = error.codigo
                raise
        except ErrorIA as error:
            registro.setdefault("estado", error.codigo)
        except Exception as exc:
            # No exponer excepciones del SDK, que pueden contener contexto o identificadores.
            registro["estado"] = "proveedor_no_disponible"
            from openai import APIStatusError
            if isinstance(exc, APIStatusError):
                registro["http_status"] = exc.status_code
                param = getattr(exc, "param", None)
                if param in ("model", "reasoning.effort", "max_output_tokens", "service_tier", "text.format.schema", "prompt_cache_options"):
                    registro["parametro"] = param
        registro["latencia_ms"] = round((time.monotonic() - start) * 1000)
        intentos.append(registro)
        if observador:
            observador(registro, respuesta.texto if respuesta else None)
        if registro["estado"] == "valido":
            return {"origen": "ia_real" if proveedor.real else "simulacion_prueba", "informe": renderizar_informe(informe, payload),
                    "estructurado": informe.model_dump(), "metadatos": {"prompt": version, "modelo": respuesta.modelo, "intentos": intentos}}
        if registro["estado"] in ("proveedor_no_disponible", "respuesta_incompleta"):
            break
    raise ErrorIA("analisis_no_verificable", intentos=intentos)


def resumen_local(resultado):
    total = resultado["total"]
    return {"origen": "sin_ia", "titulo": "Resumen automático sin IA",
            "texto": f"Facturación observada: {total['real']['texto']}. Meta: {total['meta']['texto']} ({total['meta']['estado']}). Brecha: {total['brecha']['texto']}. Revisa las advertencias de cobertura.",
            "snapshot": resultado["snapshot"]}
