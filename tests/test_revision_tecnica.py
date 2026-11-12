import json
from pathlib import Path

import pytest

from analista_ia import ErrorIA, validar_causalidad
from scripts.revalidar_evidencia import ROOT, revalidar


@pytest.mark.parametrize('texto', [
    'Investigar si hubo quiebres de stock, los precios causaron la caída.',
    'Revisar si hubo promociones y la competencia explica la caída.',
    'Comprobar si cambió la demanda, stock redujo las ventas.',
    'Investigar si cambió el stock, los precios claramente provocaron la caída.',
])
def test_hipotesis_no_absorbe_afirmacion_anadida(texto):
    with pytest.raises(ErrorIA) as exc:
        validar_causalidad(texto, permitir_hipotesis=True)
    assert exc.value.codigo == 'causalidad_no_sustentada'


@pytest.mark.parametrize('texto', [
    'Investigar si variaron los precios, stock o demanda.',
    'Revisar si hubo cambios en precios y promociones.',
    'Comprobar si los precios causaron la caída.',
])
def test_preguntas_sin_afirmacion_anadida_son_admitidas(texto):
    validar_causalidad(texto, permitir_hipotesis=True)


@pytest.mark.parametrize('estado', ['respuesta_incompleta', 'proveedor_no_disponible', 'estado_desconocido'])
def test_revalidacion_no_rescata_json_con_estado_operativo_fallido(tmp_path, estado):
    source = json.loads((ROOT / 'evidencias/13_evaluacion_real.json').read_text())
    row = source['resultados'][0]
    assert row['intentos'][0]['salida_cruda_sintetica']
    row['intentos'][0]['estado'] = estado
    source['resultados'] = [row]
    path = tmp_path / 'respuesta.json'
    path.write_text(json.dumps(source))
    result = revalidar(path)['resultados'][0]
    assert result['primer_intento_observado_aceptado'] is None
    assert result['automatico_revalidado'] is False
    assert result['intentos'][0]['estado_revalidado'] == estado
