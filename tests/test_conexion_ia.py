from types import SimpleNamespace
from scripts.probar_conexion_ia import probar


def test_conexion_usa_solo_texto_sintetico_y_un_intento():
    calls = []
    def create(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(status="completed", output_text="OK", model="modelo-prueba",
                               usage=SimpleNamespace(input_tokens=12, output_tokens=1))
    r = probar(SimpleNamespace(responses=SimpleNamespace(create=create)))
    assert r["resultado"] == "CONEXION_OK"
    assert r["costo_estimado_usd"] == "0.000036"
    assert len(calls) == 1 and calls[0]["store"] is False
    assert calls[0]["max_output_tokens"] == 32
    assert "tools" not in calls[0]


def test_error_no_filtra_excepcion():
    def create(**kwargs):
        raise RuntimeError("contenido privado no publicable")
    r = probar(SimpleNamespace(responses=SimpleNamespace(create=create)))
    assert r["resultado"] == "ERROR_LOCAL_CONTROLADO"
    assert "contenido privado" not in str(r)
