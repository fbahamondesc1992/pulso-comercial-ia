"""Fixtures sintéticos y reconstrucción de hechos usando el motor real."""
import csv
import io
import json
import re
from pathlib import Path
from indicadores import calcular, hechos_para_ia
from schemas import Filtros
from validador_csv import COLUMNAS, leer_csv

ROOT = Path(__file__).resolve().parents[1]
CRITERIOS_VERSION = "2"


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


def unidad_de_volumen(hecho):
    """Identifica la unidad física incluso cuando el valor citado es un porcentaje."""
    if hecho["estado"] != "valido" or hecho["valor"] is None:
        return None
    unidad = hecho["dimension"].get("unidad_ump")
    if unidad not in ("KG", "UN"):
        return None
    if hecho["indicador"] == "cumplimiento_ump" and hecho["unidad"] == "%":
        return unidad
    if hecho["indicador"] in ("volumen_real", "volumen_meta") and hecho["unidad"] == unidad:
        return unidad
    return None


def sin_afirmaciones_prohibidas(informe, prohibiciones):
    textos = [informe['resumen_ejecutivo'], *informe['limitaciones']]
    textos += [text for h in informe['hallazgos'] for text in (h['titulo'], h['descripcion'])]
    textos += [a['accion'] for a in informe['acciones_sugeridas']]
    for frase in prohibiciones:
        # Solo se excluye la mención directamente negada al inicio de una cláusula.
        # No se borra toda la oración ni se permite una segunda afirmación positiva.
        negacion = re.compile(
            r'(^|[.!?;\n]\s*)no (?:representa|implica|significa|es|equivale a|corresponde interpretarlo como) '
            r'(?:un |el )?' + re.escape(frase) + r'\b', re.I)
        for texto in textos:
            resto = negacion.sub(lambda m: m.group(1), texto.strip())
            if frase.casefold() in resto.casefold():
                return False
    return True


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
        pruebas["unidades_separadas"] = {"KG", "UN"} <= {unidad_de_volumen(h) for h in citados}
    pruebas["sin_frases_prohibidas"] = sin_afirmaciones_prohibidas(informe, caso["prohibiciones"])
    return pruebas
