"""Prueba real opt-in: una llamada breve, sin CSV, sin tools y sin reintentos."""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import dotenv_values
from openai import OpenAI, APIStatusError, APIConnectionError, APITimeoutError
from analista_ia import MODEL

CODIGOS_SEGUROS = {
    "invalid_api_key", "insufficient_quota", "rate_limit_exceeded", "model_not_found",
    "unsupported_parameter", "invalid_request_error", "billing_hard_limit_reached",
    "permission_denied", "account_deactivated", "organization_deactivated",
}


def probar(client, model=MODEL):
    """Solo publica una respuesta si es exactamente OK; errores nunca contienen el body."""
    record = {"fecha_utc": datetime.now(timezone.utc).isoformat(), "modelo_solicitado": model,
              "endpoint": "https://api.openai.com/v1/responses", "intentos_maximos": 1,
              "max_output_tokens": 32, "store": False, "resultado": "NO_EJECUTADO"}
    start = time.monotonic()
    try:
        response = client.responses.create(
            model=model, input="Responde únicamente OK.", reasoning={"effort": "none"},
            max_output_tokens=32, store=False,
        )
        ok = response.status == "completed" and response.output_text.strip() == "OK"
        record.update(resultado="CONEXION_OK" if ok else "RESPUESTA_NO_ESPERADA",
                      http_status=200, respuesta="OK" if ok else "OMITIDA", modelo_devuelto=response.model)
        if response.usage:
            entrada, salida = response.usage.input_tokens, response.usage.output_tokens
            record.update(input_tokens=entrada, output_tokens=salida,
                          costo_estimado_usd=str((Decimal(entrada)*2 + Decimal(salida)*12)/1_000_000))
    except APIStatusError as exc:
        code = getattr(exc, "code", None)
        record.update(resultado="RECHAZADO_POR_PROVEEDOR", http_status=exc.status_code,
                      codigo=code if isinstance(code, str) and code in CODIGOS_SEGUROS else "codigo_no_publicado",
                      costo_estimado_usd=None)
    except APITimeoutError:
        record.update(resultado="TIMEOUT", costo_estimado_usd=None)
    except APIConnectionError:
        record.update(resultado="ERROR_CONEXION", costo_estimado_usd=None)
    except Exception:
        record.update(resultado="ERROR_LOCAL_CONTROLADO", costo_estimado_usd=None)
    record["latencia_ms"] = round((time.monotonic()-start)*1000)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ejecutar", action="store_true")
    parser.add_argument("--salida", default="evidencias/10_conexion_ia.json")
    args = parser.parse_args()
    if not args.ejecutar:
        print("NO EJECUTADO. --ejecutar requiere autorización real de gasto registrada.")
        return
    path = Path(args.salida)
    if path.exists():
        parser.error("La evidencia ya existe; no se sobrescribe ni se repite automáticamente la llamada.")
    config = dotenv_values(ROOT / ".env", interpolate=False)
    key = config.get("OPENAI_API_KEY")
    model = config.get("AI_MODEL", MODEL)
    if not key:
        parser.error("No hay credencial en el .env local.")
    if model != MODEL:
        parser.error("El modelo no coincide con el presupuesto aprobado.")
    # Destino oficial fijo, sin redirección por OPENAI_BASE_URL ni proxies del entorno.
    import httpx2
    with OpenAI(api_key=key, base_url="https://api.openai.com/v1", timeout=20, max_retries=0,
                http_client=httpx2.Client(trust_env=False, timeout=20)) as client:
        result = probar(client, model)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(result, ensure_ascii=False))
    if result["resultado"] != "CONEXION_OK":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
