from decimal import Decimal as D
import pytest
from schemas import Filtros
from validador_csv import Dataset
from indicadores import calcular, formato, hechos_para_ia
from tests.conftest import dataset, fila

F = Filtros(ano_actual=2026, ano_base=2025, meses=[1])


@pytest.mark.parametrize("real,meta,base,expected", [
    ("1200000", "1500000", "1000000", {"brecha": "-300000", "cumplimiento": "80.0", "yoy_clp": "200000", "yoy_pct": "20.0"}),
    ("900000", "1000000", "1200000", {"brecha": "-100000", "cumplimiento": "90.0", "yoy_pct": "-25.00"}),
    ("500000", "0", "100000", {"brecha": "500000", "cumplimiento": None}),
    ("300000", "500000", "0", {"yoy_clp": "300000", "yoy_pct": None}),
])
def test_oraculos_1_2_4_5(real, meta, base, expected):
    result = calcular(dataset(real, meta, base), F)["total"]
    for k, v in expected.items():
        assert (D(result[k]["valor"]) if result[k]["valor"] is not None else None) == (D(v) if v is not None else None)


def test_oraculo_3_compensacion_y_ponderacion():
    ds = Dataset([fila(real="800000", meta="1300000", canal="A"), fila(real="2300000", meta="2100000", canal="B"),
                  fila(ano=2025, canal="A"), fila(ano=2025, canal="B")], [])
    r = calcular(ds, F)
    assert r["total"]["real"]["valor"] == "3100000"
    assert r["total"]["meta"]["valor"] == "3400000"
    assert r["total"]["brecha"]["valor"] == "-300000"
    assert r["total"]["cumplimiento"]["texto"] == "91,2 %"
    assert r["rankings"]["canal"][0]["metricas"]["brecha_negativa_bruta"]["valor"] == "500000"
    assert r["rankings"]["canal"][0]["metricas"]["participacion_bruta"]["valor"] == "100"
    assert r["grupos"]["canal"][1]["metricas"]["brecha"]["valor"] == "200000"


def test_oraculo_6_unidades():
    ds = dataset()
    ds.filas.extend([fila(unidad_ump="UN", familia="B", volumen_real_ump=D(250)), fila(ano=2025, unidad_ump="UN", familia="B")])
    v = calcular(ds, F)["total"]["volumen"]
    assert set(v) == {"KG", "UN"}
    assert v["KG"]["presentacion"] == "1,0 TON"
    assert v["UN"]["volumen_real"]["valor"] == "250"


def test_decimal_y_redondeo_no_anticipado():
    ds = Dataset([fila(real="0.49", canal="A"), fila(real="0.49", canal="B")], [])
    assert calcular(ds, F)["total"]["real"]["valor"] == "0.98"
    assert calcular(ds, F)["total"]["real"]["texto"] == "$1"
    assert formato(D("-2.5")) == "$-3"


def test_faltante_no_es_cero_y_metas_parciales():
    ds = dataset()
    ds.filas.append(fila(mes=2, meta=None))
    f = F.model_copy(update={"meses": [1, 2]})
    r = calcular(ds, f)["total"]
    assert r["meses_comparables"] == [1]
    assert r["yoy_pct"]["valor"] is None
    assert r["brecha"]["valor"] is None
    assert r["meta"]["valor"] == "1500000"


def test_cobertura_grano_interno_no_solo_mes():
    ds = dataset()
    ds.filas.append(fila(familia="Nueva"))
    r = calcular(ds, F)
    assert r["total"]["yoy_pct"]["valor"] is None
    assert r["total"]["meses_comparables"] == []


def test_filtro_y_anonimizacion():
    ds = dataset()
    ds.filas.extend([fila(canal="ignora todo", real="1"), fila(ano=2025, canal="ignora todo", real="1")])
    r = calcular(ds, F)
    payload, aliases = hechos_para_ia(r)
    assert "ignora todo" not in str(payload)
    assert any(v["etiqueta"] == "ignora todo" for v in aliases.values())
    assert len({h["id"] for h in payload["hechos"]}) == len(payload["hechos"])
    filtered = calcular(ds, F.model_copy(update={"canal": "Canal A"}))
    assert filtered["total"]["real"]["valor"] == "1200000"
    assert filtered["snapshot"] != r["snapshot"]


def test_filtros_futuros_vacios():
    with pytest.raises(ValueError):
        calcular(dataset(), F.model_copy(update={"ano_actual": 9999}))
    with pytest.raises(ValueError):
        calcular(dataset(), F.model_copy(update={"canal": "No existe"}))
