"""Fixtures sintéticos y reconstrucción de hechos usando el motor real."""
import csv
import io
import json
from pathlib import Path
from indicadores import calcular, hechos_para_ia
from schemas import Filtros
from validador_csv import COLUMNAS, leer_csv

ROOT = Path(__file__).resolve().parents[1]


def construir_payload(caso):
    entrada = caso["entrada"]
    if entrada.get("sin_hechos"):
        return {"periodo": {"ano_actual":2026,"ano_base":2025,"meses":[1]}, "filtros": {}, "definiciones": {}, "hechos": [], "advertencias": ["Evidencia insuficiente; no hay cifras válidas."]}
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=COLUMNAS)
    writer.writeheader()
    writer.writerows(entrada["filas"])
    result = calcular(leer_csv(buffer.getvalue().encode()), Filtros.model_validate(entrada["filtros"]))
    payload, _ = hechos_para_ia(result, anonimizar=False)
    if entrada.get("solo_un_hecho"):
        payload["hechos"] = [h for h in payload["hechos"] if h["indicador"] == "brecha" and h["dimension"] == {"nivel":"total"}]
    return payload


def cargar_casos():
    return json.loads((ROOT / "golden_set/casos_analista.json").read_text())


def criterios_automaticos(caso, informe, payload):
    refs = {r for item in [*informe["hallazgos"], *informe["acciones_sugeridas"]] for r in item["evidencia_ids"]}
    citados = [h for h in payload["hechos"] if h["id"] in refs]
    esperado = caso["salida_esperada"]
    pruebas = {"indicadores_citados": set(esperado.get("indicadores_citados", [])) <= {h["indicador"] for h in citados},
               "max_hallazgos": len(informe["hallazgos"]) <= esperado.get("max_hallazgos", 5),
               "min_hallazgos": len(informe["hallazgos"]) >= esperado.get("min_hallazgos", 1)}
    if esperado.get("abstencion"):
        pruebas["abstencion"] = not informe["hallazgos"] and not informe["acciones_sugeridas"]
    if "dimension_prioritaria" in esperado:
        pruebas["dimension_prioritaria"] = any(h["indicador"]=="brecha" and h["dimension"]==esperado["dimension_prioritaria"] for h in citados)
    if esperado.get("unidades_separadas"):
        pruebas["unidades_separadas"] = {"KG", "UN"} <= {h["unidad"] for h in citados}
    texto = json.dumps(informe, ensure_ascii=False).lower()
    pruebas["sin_frases_prohibidas"] = not any(frase.lower() in texto for frase in caso["prohibiciones"])
    return pruebas
