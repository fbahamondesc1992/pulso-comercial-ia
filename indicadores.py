"""Fuente única de cifras. No hay imputación ni agregación de unidades heterogéneas."""
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP, localcontext
from zoneinfo import ZoneInfo

from schemas import Filtros
from validador_csv import DIMENSIONES, Dataset

D = Decimal
ZERO = D(0)
LABELS = {
    "real": "Facturación real", "meta": "Meta facturación", "brecha": "Brecha facturación",
    "cumplimiento": "Cumplimiento de meta", "base": "Facturación año base",
    "yoy_clp": "Variación interanual CLP", "yoy_pct": "Variación interanual %",
    "volumen_real": "Volumen real", "volumen_meta": "Meta volumen", "cumplimiento_ump": "Cumplimiento UMP",
    "brecha_negativa_bruta": "Brecha negativa bruta", "participacion_bruta": "Participación en brechas negativas brutas",
}
FORMULAS = {
    "real": "sum(real)", "meta": "sum(meta)", "base": "sum(real año base)",
    "brecha": "real - meta", "cumplimiento": "sum(real) / sum(meta) * 100",
    "yoy_clp": "real actual - real base (mismos meses)", "yoy_pct": "(real actual / real base - 1) * 100",
    "volumen_real": "sum(volumen real de una unidad)", "volumen_meta": "sum(volumen meta de una unidad)",
    "cumplimiento_ump": "sum(volumen real) / sum(volumen meta) * 100",
    "brecha_negativa_bruta": "max(0, -brecha)",
    "participacion_bruta": "brecha negativa del grupo / suma de brechas negativas de la misma dimensión * 100",
}


def formato(valor, unidad="CLP"):
    if valor is None:
        return "N/C"
    decimal = D(valor)
    precision = D("1") if unidad == "CLP" else D("0.1")
    with localcontext() as ctx:
        ctx.prec = max(50, len(decimal.as_tuple().digits) + 2)
        redondeado = decimal.quantize(precision, rounding=ROUND_HALF_UP)
    if redondeado == 0:
        redondeado = abs(redondeado)
    texto = f"{redondeado:,.{0 if unidad == 'CLP' else 1}f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"${texto}" if unidad == "CLP" else f"{texto} {unidad}"


def metrica(valor, unidad="CLP", estado="valido"):
    return {"valor": str(valor) if valor is not None else None, "unidad": unidad,
            "estado": estado, "texto": formato(valor, unidad)}


def _suma(rows, campo):
    return sum((r[campo] for r in rows if r[campo] is not None), ZERO)


def _key(row):
    return tuple(row[d] for d in (*DIMENSIONES, "unidad_ump"))


def _agregado(rows, filtros):
    meses = set(filtros.meses)
    actual = [r for r in rows if r["ano"] == filtros.ano_actual and r["mes"] in meses]
    base = [r for r in rows if r["ano"] == filtros.ano_base and r["mes"] in meses]
    claves = {_key(r) for r in rows}
    esperados = {(key, m) for key in claves for m in meses}
    slots_a = {(_key(r), r["mes"]) for r in actual}
    slots_b = {(_key(r), r["mes"]) for r in base}
    completo_a = bool(esperados) and slots_a == esperados
    completo_b = bool(esperados) and slots_b == esperados
    comparable = completo_a and completo_b
    meses_comparables = [m for m in sorted(meses) if claves and
                         all((k, m) in slots_a and (k, m) in slots_b for k in claves)]
    real = _suma(actual, "facturacion_real_clp") if actual else None
    real_base = _suma(base, "facturacion_real_clp") if base else None
    metas = [r["facturacion_meta_clp"] for r in actual]
    meta_ok = bool(actual) and all(v is not None for v in metas)
    meta = sum((v for v in metas if v is not None), ZERO) if any(v is not None for v in metas) else None
    brecha = real - meta if meta_ok else None
    estado_meta = ("valido" if completo_a else "cobertura_parcial") if meta_ok else "meta_parcial_no_comparable"
    result = {
        "real": metrica(real, estado="valido" if completo_a else "cobertura_parcial"),
        "base": metrica(real_base, estado="valido" if completo_b else "cobertura_parcial"),
        "meta": metrica(meta, estado=estado_meta),
        "brecha": metrica(brecha, estado=estado_meta),
        "cumplimiento": metrica(real / meta * 100 if meta_ok and meta > 0 else None, "%",
                                 estado_meta if meta_ok and meta > 0 else "meta_cero" if meta_ok else estado_meta),
        "yoy_clp": metrica(real - real_base if comparable else None, estado="valido" if comparable else "no_comparable"),
        "yoy_pct": metrica((real / real_base - 1) * 100 if comparable and real_base > 0 else None, "%",
                            "valido" if comparable and real_base > 0 else "nuevo" if comparable and real > 0 else "no_comparable"),
        "meses_comparables": meses_comparables,
        "meses_actuales": sorted({r["mes"] for r in actual}),
        "meses_base": sorted({r["mes"] for r in base}),
        "volumen": {},
    }
    for unit in sorted({r["unidad_ump"] for r in rows}):
        a = [r for r in actual if r["unidad_ump"] == unit]
        unit_keys = {_key(r) for r in rows if r["unidad_ump"] == unit}
        unit_complete = all((k, m) in slots_a for k in unit_keys for m in meses)
        vr = _suma(a, "volumen_real_ump") if a else None
        vm = _suma(a, "volumen_meta_ump") if any(r["volumen_meta_ump"] is not None for r in a) else None
        ok = bool(a) and all(r["volumen_meta_ump"] is not None for r in a)
        unit_status = "valido" if unit_complete else "cobertura_parcial"
        result["volumen"][unit] = {
            "volumen_real": metrica(vr, unit, "valido" if unit_complete else "cobertura_parcial"),
            "volumen_meta": metrica(vm, unit, unit_status if ok else "meta_parcial_no_comparable"),
            "cumplimiento_ump": metrica(vr / vm * 100 if ok and vm > 0 else None, "%", unit_status if ok and vm > 0 else "no_comparable"),
            "presentacion": formato(vr / 1000, "TON") if unit == "KG" and vr is not None else formato(vr, unit),
        }
    return result


def opciones(dataset):
    return {"anos": sorted({r["ano"] for r in dataset.filas}),
            "meses_por_ano": {str(y): sorted({r["mes"] for r in dataset.filas if r["ano"] == y}) for y in {r["ano"] for r in dataset.filas}},
            **{d: sorted({r[d] for r in dataset.filas}) for d in DIMENSIONES}}


def filtros_iniciales(dataset):
    hoy = datetime.now(ZoneInfo("America/Santiago")).date()
    anos = sorted({r["ano"] for r in dataset.filas if r["ano"] <= hoy.year})
    if not anos:
        raise ValueError("El archivo solo contiene años futuros.")
    actual = 2026 if 2025 in anos and 2026 in anos else anos[-1]
    base = 2025 if actual == 2026 and 2025 in anos else max((y for y in anos if y < actual), default=actual - 1)
    meses = sorted({r["mes"] for r in dataset.filas if r["ano"] == actual and (actual < hoy.year or r["mes"] <= hoy.month)})
    if not meses:
        raise ValueError("No hay meses actuales calculables.")
    return Filtros(ano_actual=actual, ano_base=base, meses=meses)


def calcular(dataset: Dataset, filtros: Filtros):
    with localcontext() as ctx:
        # La suma de importes netos conserva todos los decimales de entrada.
        max_digitos = max(len(v.as_tuple().digits) for r in dataset.filas for v in
                          (r["facturacion_real_clp"], r["facturacion_meta_clp"],
                           r["volumen_real_ump"], r["volumen_meta_ump"]) if v is not None)
        ctx.prec = max(50, max_digitos + len(str(len(dataset.filas))) + 2)
        return _calcular(dataset, filtros)


def _calcular(dataset, filtros):
    hoy = datetime.now(ZoneInfo("America/Santiago")).date()
    if filtros.ano_actual > hoy.year or (filtros.ano_actual == hoy.year and max(filtros.meses) > hoy.month):
        raise ValueError("No se pueden analizar meses futuros.")
    if filtros.ano_actual not in {r["ano"] for r in dataset.filas}:
        raise ValueError("El año actual no existe en el archivo.")
    rows = [r for r in dataset.filas if r["ano"] in (filtros.ano_actual, filtros.ano_base)
            and all(getattr(filtros, d) is None or r[d] == getattr(filtros, d) for d in DIMENSIONES)]
    if not any(r["ano"] == filtros.ano_actual and r["mes"] in filtros.meses for r in rows):
        raise ValueError("No hay datos para el período y los filtros seleccionados.")
    total = _agregado(rows, filtros)
    grupos, rankings = {}, {}
    # Una partición por dimensión; nunca se suman contribuciones entre particiones.
    for dim in (*DIMENSIONES, "canal_linea_oficina"):
        agrupados = defaultdict(list)
        for row in rows:
            key = (row["canal"], row["linea"], row["oficina"]) if dim == "canal_linea_oficina" else (row[dim],)
            agrupados[key].append(row)
        items = []
        for key, subset in sorted(agrupados.items()):
            dimension = dict(zip(("canal", "linea", "oficina"), key)) if dim == "canal_linea_oficina" else {dim: key[0]}
            items.append({"dimension": dimension, "metricas": _agregado(subset, filtros)})
        negativos = [x for x in items if x["metricas"]["brecha"]["valor"] is not None and D(x["metricas"]["brecha"]["valor"]) < 0]
        bruto = sum((-D(x["metricas"]["brecha"]["valor"]) for x in negativos), ZERO)
        todos_validos = all(x["metricas"]["brecha"]["valor"] is not None for x in items)
        for x in items:
            b = x["metricas"]["brecha"]["valor"]
            g = max(ZERO, -D(b)) if b is not None else None
            x["metricas"]["brecha_negativa_bruta"] = metrica(g, estado="valido" if g is not None else "no_comparable")
            x["metricas"]["participacion_bruta"] = metrica(g / bruto * 100 if g is not None and bruto > 0 and todos_validos else None, "%",
                                                           "valido" if g is not None and bruto > 0 and todos_validos else "no_comparable")
        grupos[dim] = items
        rankings[dim] = sorted(negativos, key=lambda x: (D(x["metricas"]["brecha"]["valor"]), str(x["dimension"])))[:5]
    avisos = list(dataset.advertencias)
    if any(r["facturacion_real_clp"] < 0 or r["volumen_real_ump"] < 0 for r in rows):
        avisos.append("Hay devoluciones o ajustes negativos en valores reales. Los indicadores muestran netos; el CSV no permite distinguir su causa ni separar ventas brutas de devoluciones.")
    if total["meses_comparables"] != filtros.meses:
        avisos.append("No comparable interanualmente: falta cobertura de uno o más grupos. Meses con cobertura completa en ambos años: " + (", ".join(map(str, total["meses_comparables"])) or "ninguno") + ". No se imputan ceros.")
    if total["meta"]["estado"] == "meta_parcial_no_comparable":
        avisos.append("Meta parcial/no comparable: no se calcula brecha ni cumplimiento del total afectado.")
    elif total["meta"]["estado"] == "cobertura_parcial":
        avisos.append("Cumplimiento y brecha calculados solo sobre las filas actuales presentes con meta; faltan combinaciones respecto de la base. No se imputan ventas ni metas.")
    for unidad, v in total["volumen"].items():
        if v["volumen_meta"]["estado"] == "meta_parcial_no_comparable":
            avisos.append(f"Meta de volumen {unidad} parcial/no comparable: no se calcula cumplimiento de esa unidad.")
    if filtros.ano_actual == hoy.year and hoy.month in filtros.meses:
        avisos.append("El mes en curso podría estar incompleto; la presencia de registros no certifica su cierre.")
    mensual = [{"mes": m, "metricas": _agregado(rows, filtros.model_copy(update={"meses": [m]}))} for m in filtros.meses]
    signature = hashlib.sha256(json.dumps({"filas": rows, "filtros": filtros.model_dump()}, sort_keys=True, default=str).encode()).hexdigest()
    return {"total": total, "grupos": grupos, "rankings": rankings, "mensual": mensual,
            "filtros": filtros.model_dump(), "advertencias": avisos, "opciones": opciones(dataset),
            "filas": len([r for r in rows if r["mes"] in filtros.meses]), "snapshot": signature}


def hechos_para_ia(resultado, anonimizar=True):
    """Máximo 45 hechos, top 2 por dimensión. Etiquetas arbitrarias quedan locales."""
    hechos, aliases = [], {}
    f = resultado["filtros"]
    periodo = {"ano_actual": f["ano_actual"], "ano_base": f["ano_base"], "meses": f["meses"]}

    def add(metrics, dimension, campos):
        for campo in campos:
            m = metrics[campo]
            dim = {}
            for k, v in dimension.items():
                if anonimizar and k in DIMENSIONES:
                    key = (k, v)
                    if key not in aliases:
                        aliases[key] = f"{k.upper()}_{sum(1 for a in aliases if a[0] == k) + 1:03d}"
                    dim[k] = aliases[key]
                else:
                    dim[k] = v
            hechos.append({"id": f"F{len(hechos)+1:03d}", "indicador": campo, "dimension": dim,
                           "valor": m["valor"], "unidad": m["unidad"], "periodo": periodo,
                           "formula": FORMULAS[campo], "estado": m["estado"]})
    add(resultado["total"], {"nivel": "total"}, ("real", "meta", "brecha", "cumplimiento", "base", "yoy_clp", "yoy_pct"))
    for unit, metrics in resultado["total"]["volumen"].items():
        add(metrics, {"nivel": "total", "unidad_ump": unit}, ("volumen_real", "volumen_meta", "cumplimiento_ump"))
    for dim in DIMENSIONES:
        for item in resultado["rankings"][dim][:2]:
            add(item["metricas"], item["dimension"], ("real", "meta", "brecha", "participacion_bruta"))
    # No se envía texto libre del archivo, ni siquiera en filtros/advertencias.
    payload = {"periodo": periodo, "filtros": {d: "filtrado" if f[d] else "todos" for d in DIMENSIONES},
               "definiciones": {"brecha": "real - meta", "variacion": "mismos meses entre años", "ranking": "top dos por dimensión; no sumar dimensiones superpuestas"},
               "hechos": hechos, "advertencias": resultado["advertencias"]}
    mapa = {alias: {"dimension": key[0], "etiqueta": key[1]} for key, alias in aliases.items()}
    return payload, mapa
