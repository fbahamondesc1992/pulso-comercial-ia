import json
from types import SimpleNamespace
import pytest
from analista_ia import analizar, validar_informe, ErrorIA, ProveedorOpenAI, cargar_prompt
from indicadores import calcular, hechos_para_ia
from schemas import Filtros, InformeIA
from tests.fakes import ProveedorFalso, informe_valido
from tests.conftest import dataset


@pytest.fixture
def payload():
    return hechos_para_ia(calcular(dataset(), Filtros(ano_actual=2026, ano_base=2025, meses=[1])))[0]


def test_prompt_literal_y_cifras_por_python(payload):
    fake = ProveedorFalso()
    result = analizar(payload, fake, "v1")
    assert fake.calls[0][0] == cargar_prompt("v1")
    assert result["origen"] == "simulacion_prueba"
    assert "$1.200.000" in result["informe"]["hallazgos"][0]["descripcion"]
    assert "{{" not in result["informe"]["hallazgos"][0]["descripcion"]


@pytest.mark.parametrize("desc,codigo", [("Venta 1200000", "cifra_sin_respaldo"), ("Meta 80 %", "cifra_sin_respaldo"),
    ("Mil millones", "cifra_sin_respaldo"), ("Brecha {{F999}}", "ids_invalidos"),
    ("Cayó debido a promociones {{F001}}", "causalidad_no_sustentada"),
    ("El stock redujo la venta {{F001}}", "causalidad_no_sustentada"),
    ("Ver https://ejemplo.test {{F001}}", "contenido_externo"), ("<script>x</script>{{F001}}", "contenido_externo"),
    ("Todo está bien", "hallazgo_sin_evidencia")])
def test_rechazos_conservadores(payload, desc, codigo):
    obj = informe_valido(payload)
    obj["hallazgos"][0]["descripcion"] = desc
    with pytest.raises(ErrorIA) as e:
        validar_informe(json.dumps(obj), payload)
    assert e.value.codigo == codigo


def test_esquema_extra_ids_y_truncado(payload):
    obj = informe_valido(payload)
    obj["nuevo_kpi"] = 100
    with pytest.raises(ErrorIA, match="verificable"):
        validar_informe(json.dumps(obj), payload)
    with pytest.raises(ErrorIA) as e:
        validar_informe('{"x":', payload)
    assert e.value.codigo == "json_invalido"
    obj = informe_valido(payload)
    obj["hallazgos"][0]["evidencia_ids"] = ["F999"]
    with pytest.raises(ErrorIA) as e:
        validar_informe(json.dumps(obj), payload)
    assert e.value.codigo == "ids_invalidos"


def test_reintento_acotado_y_fallo(payload):
    fake = ProveedorFalso(["invalido", "invalido", informe_valido(payload)])
    with pytest.raises(ErrorIA) as e:
        analizar(payload, fake)
    assert len(fake.calls) == 2
    assert len(e.value.intentos) == 2
    assert fake.calls[1][2] is True


def test_fallo_sdk_sin_detalles_ni_reintento(payload):
    fake = ProveedorFalso([RuntimeError("SECRETO-NO-MOSTRAR")])
    with pytest.raises(ErrorIA) as e:
        analizar(payload, fake)
    assert "SECRETO" not in str(e.value)
    assert len(fake.calls) == 1


def test_abstencion(payload):
    payload["hechos"] = []
    result = analizar(payload, ProveedorFalso())
    assert result["informe"]["hallazgos"] == []
    assert result["informe"]["acciones_sugeridas"] == []


def test_no_aceptar_informe_vacio_con_hechos_validos(payload):
    obj=informe_valido(payload)
    obj["hallazgos"]=[]
    obj["acciones_sugeridas"]=[]
    with pytest.raises(ErrorIA):
        validar_informe(json.dumps(obj),payload)


def test_hipotesis_solo_investigacion(payload):
    obj = informe_valido(payload)
    obj["acciones_sugeridas"][0]["accion"] = "Investigar si existieron quiebres de stock."
    assert validar_informe(json.dumps(obj), payload)


def test_proveedor_opt_in_y_clave(monkeypatch):
    monkeypatch.delenv("AI_ENABLED", raising=False)
    with pytest.raises(ErrorIA) as e:
        ProveedorOpenAI()
    assert e.value.codigo == "ia_deshabilitada"
    monkeypatch.setenv("AI_ENABLED", "true")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ErrorIA) as e:
        ProveedorOpenAI()
    assert e.value.codigo == "sin_clave"


def test_contrato_sdk_sin_red(monkeypatch, payload):
    monkeypatch.setenv("AI_ENABLED", "true")
    captured = {}
    def create(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(status="completed", output_text=json.dumps(informe_valido(payload)), model="modelo-prueba", usage=SimpleNamespace(input_tokens=100, output_tokens=50))
    sdk = SimpleNamespace(responses=SimpleNamespace(create=create))
    real_adapter = ProveedorOpenAI(sdk_client=sdk)
    response = real_adapter.generar(cargar_prompt("v2"), payload)
    assert response.input_tokens == 100
    assert captured["store"] is False
    assert captured["text"]["format"]["schema"] == InformeIA.model_json_schema()
    assert captured["input"][0]["role"] == "system"
    assert "tools" not in captured


def test_prompt_path_y_contexto(payload):
    with pytest.raises(ErrorIA):
        cargar_prompt("../../.env")
    payload["advertencias"] = ["x"*40000]
    fake = ProveedorFalso()
    with pytest.raises(ErrorIA):
        analizar(payload, fake)
    assert not fake.calls
