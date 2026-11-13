import io
import json
from pathlib import Path
import pytest
from app import create_app, LimiteDemo
from tests.fakes import ProveedorFalso
from tests.conftest import csv_bytes, fila

HEADERS = {"X-Pulso-Request": "1"}


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "false")
    return create_app({"TESTING": True}).test_client()


def test_rutas_y_salud(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").json["status"] == "ok"
    assert client.get("/demo.csv").status_code == 200
    assert client.get("/no-existe").status_code == 404
    assert "frame-ancestors 'none'" in client.get("/").headers["Content-Security-Policy"]


def test_demo_y_filtros(client):
    r = client.post("/api/dashboard", data={"fuente": "demo"}, headers=HEADERS)
    assert r.status_code == 200
    assert r.json["filas"] == 360
    assert r.json["total"]["yoy_pct"]["estado"] == "valido"
    filters = r.json["filtros"]
    filters["canal"] = "Tradicional"
    s = client.post("/api/dashboard", data={"fuente": "demo", "filtros": json.dumps(filters)}, headers=HEADERS)
    assert s.status_code == 200
    assert s.json["snapshot"] != r.json["snapshot"]
    assert s.json["filas"] == 120


def test_upload_y_escaping(client):
    raw = csv_bytes([fila(canal='<img src=x onerror=alert(1)>')])
    r = client.post("/api/dashboard", data={"fuente": "archivo", "archivo": (io.BytesIO(raw), "test.csv")}, headers=HEADERS)
    assert r.status_code == 200
    assert "<img" in r.json["opciones"]["canal"][0]
    assert "<img" not in str(r.json["hechos"])
    # El navegador usa textContent; nunca innerHTML para contenido recibido.
    assert "innerHTML" not in Path("static/app.js").read_text()


@pytest.mark.parametrize("data", [{}, {"fuente":"demo","filtros":"{"}, {"fuente":"demo","filtros":'{"ano_actual":2026}'},
                                 {"fuente":"archivo","archivo":(io.BytesIO(b"bad"),"x.csv")}])
def test_invalido_no_500(client, data):
    assert client.post("/api/dashboard", data=data, headers=HEADERS).status_code == 400


def test_csrf_y_limite_tamano(client):
    assert client.post("/api/dashboard", data={"fuente":"demo"}).status_code == 403
    assert client.post("/api/dashboard", data={"fuente":"demo"}, headers={**HEADERS,"Origin":"https://otro.test"}).status_code == 403
    r = client.post("/api/dashboard", data={"fuente":"archivo","archivo":(io.BytesIO(b"x"*2_200_000),"x.csv")}, headers=HEADERS)
    assert r.status_code == 413


def test_ia_deshabilitada_y_snapshot(client):
    r = client.post("/api/dashboard", data={"fuente":"demo"}, headers=HEADERS)
    assert client.post("/api/analisis", data={"fuente":"demo","snapshot":"bad"}, headers=HEADERS).status_code == 409
    a = client.post("/api/analisis", data={"fuente":"demo","snapshot":r.json["snapshot"]}, headers=HEADERS)
    assert a.status_code == 503
    assert a.json["codigo"] == "ia_deshabilitada"
    assert a.json["respaldo"]["origen"] == "sin_ia"


def test_flujo_ia_fake_y_cupo():
    fake = ProveedorFalso()
    app = create_app({"TESTING":True}, proveedor=fake)
    app.extensions["limite_demo"] = LimiteDemo(por_ip=1)
    client = app.test_client()
    r = client.post("/api/dashboard", data={"fuente":"demo"}, headers=HEADERS)
    form = {"fuente":"demo","snapshot":r.json["snapshot"]}
    a = client.post("/api/analisis", data=form, headers=HEADERS)
    assert a.status_code == 200
    assert a.json["origen"] == "simulacion_prueba"
    assert len(fake.calls) == 1
    assert "Tradicional" not in json.dumps(fake.calls[0][1])
    assert client.post("/api/analisis", data=form, headers=HEADERS).status_code == 429
    assert len(fake.calls) == 1


def test_archivo_grande_sigue_en_memoria():
    from app import PeticionEnMemoria
    req = PeticionEnMemoria.from_values()
    stream = req._get_file_stream(1_000_000,"text/csv","a.csv")
    assert isinstance(stream, io.BytesIO)


@pytest.mark.parametrize("filas", [1000, 5088])
def test_csv_multipart_mayor_64k_dentro_del_limite(client, filas):
    from tests.conftest import fila, csv_bytes
    contenido = csv_bytes([fila(familia=f"Familia sintetica {i}") for i in range(filas)])
    assert 64 * 1024 < len(contenido) < 2 * 1024 * 1024
    r = client.post("/api/dashboard", data={"fuente": "archivo", "archivo":
        (io.BytesIO(contenido), "sintetico.csv")}, headers=HEADERS)
    assert r.status_code == 200


def test_campo_formulario_excesivo_rechazado(client):
    r = client.post("/api/dashboard", data={"fuente": "demo", "filtros": "x" * (128 * 1024 + 1)},
                    content_type="multipart/form-data", headers=HEADERS)
    assert r.status_code == 413


def test_limite_global():
    limit = LimiteDemo(por_ip=5,global_hora=2)
    assert limit.admitir("a") and limit.admitir("b")
    assert not limit.admitir("c")
