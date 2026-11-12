import pytest
from validador_csv import leer_csv, ErrorCSV, MAX_BYTES, COLUMNAS
from tests.conftest import fila, csv_bytes


def test_valido_bom_y_meta_vacia():
    ds = leer_csv(b"\xef\xbb\xbf" + csv_bytes([fila(meta=None)]))
    assert ds.filas[0]["facturacion_meta_clp"] is None
    assert ds.advertencias


@pytest.mark.parametrize("campo,valor", [("mes", "13"), ("mes", "1.0"), ("ano", "26"), ("unidad_ump", "TON"),
    ("canal", ""), ("oficina", "x"*81), ("familia", "a\x01b"),
    *[(k, v) for k in COLUMNAS[7:] for v in ("NaN", "Infinity", "-1", "1,2", "1e4", "1"*16)]])
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
    rows = [fila(familia=f"F{i}") for i in range(10_000)]
    assert len(leer_csv(csv_bytes(rows)).filas) == 10_000
    with pytest.raises(ErrorCSV, match="10.000"):
        leer_csv(csv_bytes(rows + [fila(familia="Extra")]))
