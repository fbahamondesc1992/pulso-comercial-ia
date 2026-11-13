import pytest
from validador_csv import leer_csv, ErrorCSV, MAX_BYTES, MAX_ROWS, COLUMNAS
from tests.conftest import fila, csv_bytes


def test_valido_bom_y_meta_vacia():
    ds = leer_csv(b"\xef\xbb\xbf" + csv_bytes([fila(meta=None)]))
    assert ds.filas[0]["facturacion_meta_clp"] is None
    assert ds.advertencias


@pytest.mark.parametrize("campo,valor", [("mes", "13"), ("mes", "1.0"), ("ano", "26"), ("unidad_ump", "TON"),
    ("canal", ""), ("oficina", "x"*81), ("familia", "a\x01b"),
    *[(k, v) for k in COLUMNAS[7:] for v in ("NaN", "Infinity", "1,2", "1e4", "1"*16)],
    ("facturacion_meta_clp", "-1"), ("volumen_meta_ump", "-1")])
def test_campos_invalidos(campo, valor):
    with pytest.raises(ErrorCSV):
        leer_csv(csv_bytes([fila(**{campo: valor})]))


@pytest.mark.parametrize("raw", [b"", b"   ", b"\xff", b"a,b\n1,2", b"a,a\n1,2", b"\x00", b"a"*(MAX_BYTES+1)])
def test_archivos_invalidos(raw):
    with pytest.raises(ErrorCSV):
        leer_csv(raw)


def test_tipo_filas_cabecera_y_duplicados():
    with pytest.raises(ErrorCSV, match="extensión"):
        leer_csv(csv_bytes(), "x.xlsx")
    with pytest.raises(ErrorCSV, match="líneas 2 y 3"):
        leer_csv(csv_bytes([fila(), fila()]))
    with pytest.raises(ErrorCSV):
        leer_csv(csv_bytes() + b"1,2,3\n")
    with pytest.raises(ErrorCSV):
        leer_csv((",".join(COLUMNAS)+"\n").encode())


def test_normalizacion_visible_colision_y_mayusculas():
    ds = leer_csv(csv_bytes([fila(canal=" Canal "), fila(canal="CANAL")]))
    assert ds.filas[0]["canal"] == "Canal"
    assert ds.advertencias
    with pytest.raises(ErrorCSV, match="duplicado"):
        leer_csv(csv_bytes([fila(canal="Canal"), fila(canal=" Canal ")]))


def test_limite_filas():
    rows = [fila(familia=f"F{i}") for i in range(MAX_ROWS)]
    assert len(leer_csv(csv_bytes(rows)).filas) == MAX_ROWS
    with pytest.raises(ErrorCSV, match="30.000"):
        leer_csv(csv_bytes(rows + [fila(familia="Extra")]))


def csv_chileno(rows):
    import csv
    import io
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=COLUMNAS, delimiter=";")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8-sig")


def test_chileno_equivalencia_exacta_y_textos():
    from decimal import Decimal
    normal = fila(real="1234.560001", meta=None, canal='Canal, "A"; Sur',
                  volumen_real_ump=Decimal("0.000001"), volumen_meta_ump=Decimal("0"))
    chileno = {k: str(v).replace('.', ',') if isinstance(v, Decimal) else v for k, v in normal.items()}
    assert leer_csv(csv_chileno([chileno])).filas == leer_csv(csv_bytes([normal])).filas


@pytest.mark.parametrize("valor", ["1.234,56", "1.23", "1,2,3", "NaN", "Infinity", "1e4", "1"*16])
def test_chileno_no_admite_ambiguos_ni_invalidos(valor):
    with pytest.raises(ErrorCSV, match="coma decimal"):
        leer_csv(csv_chileno([fila(facturacion_real_clp=valor)]))


def test_chileno_duplicados_y_filas_malformadas():
    with pytest.raises(ErrorCSV, match="duplicado"):
        leer_csv(csv_chileno([fila(), fila()]))
    with pytest.raises(ErrorCSV, match="cantidad de columnas"):
        leer_csv(csv_chileno([fila()]) + b"1;2;3\n")


def test_devoluciones_y_precision_chilena():
    from decimal import Decimal
    entrada = fila(facturacion_real_clp="-1,123456789012345678901", volumen_real_ump="-0,000000001",
                   facturacion_meta_clp="2,000000000000001", volumen_meta_ump="0,0000000001")
    datos = leer_csv(csv_chileno([entrada])).filas[0]
    assert datos["facturacion_real_clp"] == Decimal("-1.123456789012345678901")
    assert datos["volumen_real_ump"] == Decimal("-0.000000001")
    assert datos["facturacion_meta_clp"] == Decimal("2.000000000000001")


def test_metas_negativas_chilenas_rechazadas():
    for campo in ("facturacion_meta_clp", "volumen_meta_ump"):
        with pytest.raises(ErrorCSV, match="Negativos solo"):
            leer_csv(csv_chileno([fila(**{campo: "-1,2"})]))
