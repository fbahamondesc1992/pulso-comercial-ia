import copy
import json

import pytest

from analista_ia import ErrorIA, validar_informe
from scripts.golden import cargar_casos, construir_payload, criterios_automaticos
from tests.fakes import informe_valido


@pytest.mark.parametrize('texto', [
    'Los hechos disponibles no permiten atribuir los resultados a precio, competencia, promociones, stock o demanda.',
    'Los hechos no permiten atribuir las brechas a precios o stock.',
    'Los hechos disponibles no permiten establecer causas de las brechas ni atribuirlas a precio, competencia, promociones, stock o demanda.',
    'La información disponible no permite atribuir la caída a la competencia.',
    'No se puede atribuir la brecha al stock.',
    'No hay datos sobre stock y precios.',
])
def test_negaciones_de_causalidad_no_son_afirmaciones(texto):
    payload = construir_payload(cargar_casos()[0])
    obj = informe_valido(payload)
    obj['limitaciones'] = [texto]
    assert validar_informe(json.dumps(obj), payload)


@pytest.mark.parametrize('texto', [
    'No hay datos sobre stock. El stock redujo la venta.',
    'No hay datos sobre stock; la competencia explica la caída.',
    'No hay datos sobre stock, el stock redujo la venta.',
    'No hay datos sobre stock pero las promociones explican la caída.',
    'Los hechos no permiten atribuir la caída a stock y el precio redujo la venta.',
    'La caída fue causada por las promociones.',
    'Las ventas cayeron debido a la competencia.',
    'Sin datos, el stock redujo las ventas.',
    'No hay datos causales. El precio redujo la venta.',
])
def test_negacion_no_habilita_una_causa_inventada(texto):
    payload = construir_payload(cargar_casos()[0])
    obj = informe_valido(payload)
    obj['limitaciones'] = [texto]
    with pytest.raises(ErrorIA) as exc:
        validar_informe(json.dumps(obj), payload)
    assert exc.value.codigo == 'causalidad_no_sustentada'


def test_explicacion_cobertura_requiere_evidencia_estructurada():
    texto = 'La comparación interanual no permite concluir crecimiento debido a cobertura insuficiente.'
    for case_index, permitido in [(4, True), (0, False)]:
        payload = construir_payload(cargar_casos()[case_index])
        obj = informe_valido(payload)
        obj['limitaciones'] = [texto]
        if permitido:
            assert validar_informe(json.dumps(obj), payload)
        else:
            with pytest.raises(ErrorIA):
                validar_informe(json.dumps(obj), payload)


@pytest.mark.parametrize('texto', [
    'Las ventas cayeron debido a cobertura insuficiente.',
    'La comparación interanual no permite concluir crecimiento debido a promociones.',
    'La comparación interanual no permite concluir crecimiento debido a cobertura insuficiente. El stock redujo las ventas.',
])
def test_cobertura_no_exime_causas_comerciales(texto):
    payload = construir_payload(cargar_casos()[4])
    obj = informe_valido(payload)
    obj['limitaciones'] = [texto]
    with pytest.raises(ErrorIA):
        validar_informe(json.dumps(obj), payload)


@pytest.mark.parametrize('accion,permitido', [
    ('Investigar si existieron quiebres de stock.', True),
    ('Revisar los datos sobre precios y stock.', True),
    ('Investigar si existieron quiebres de stock. El precio redujo las ventas.', False),
    ('Revisar stock y confirmar que la competencia redujo las ventas.', False),
    ('Investigar si existieron quiebres de stock, pero la demanda explica la caída.', False),
    ('Investigar si existieron quiebres de stock, sabemos que el precio explica la caída.', False),
])
def test_investigacion_no_ampara_afirmaciones_posteriores(accion, permitido):
    payload = construir_payload(cargar_casos()[0])
    obj = informe_valido(payload)
    obj['acciones_sugeridas'][0]['accion'] = accion
    if permitido:
        assert validar_informe(json.dumps(obj), payload)
    else:
        with pytest.raises(ErrorIA):
            validar_informe(json.dumps(obj), payload)


def informe_de_cumplimientos():
    caso = cargar_casos()[5]
    payload = construir_payload(caso)
    facts = [h for h in payload['hechos'] if h['indicador'] == 'cumplimiento_ump']
    obj = informe_valido(payload)
    obj['acciones_sugeridas'] = []
    obj['hallazgos'] = [dict(titulo='Cumplimiento por unidad',
                             descripcion='Seguimiento separado ' + ' y '.join('{{'+h['id']+'}}' for h in facts),
                             evidencia_ids=[h['id'] for h in facts], nivel='atencion')]
    return caso, payload, obj, facts


def test_porcentajes_de_kg_y_un_cuentan_como_evidencia_separada():
    caso, payload, obj, _ = informe_de_cumplimientos()
    assert criterios_automaticos(caso, obj, payload)['unidades_separadas']


@pytest.mark.parametrize('mutacion', ['sin_dimension', 'misma_unidad', 'metrica_monetaria', 'dato_nulo', 'dato_no_comparable'])
def test_no_acepta_porcentaje_sin_dos_unidades_fisicas(mutacion):
    caso, payload, obj, facts = informe_de_cumplimientos()
    h = facts[1]
    if mutacion == 'sin_dimension':
        h['dimension'].pop('unidad_ump')
    elif mutacion == 'misma_unidad':
        h['dimension']['unidad_ump'] = 'KG'
    elif mutacion == 'metrica_monetaria':
        h['indicador'] = 'cumplimiento'
    elif mutacion == 'dato_nulo':
        h['valor'] = None
    else:
        h['estado'] = 'no_comparable'
    assert not criterios_automaticos(caso, obj, payload)['unidades_separadas']


def test_no_basta_mencionar_un_o_inventar_un_total():
    caso, payload, obj, facts = informe_de_cumplimientos()
    uno = copy.deepcopy(obj)
    uno['hallazgos'][0]['evidencia_ids'] = [facts[0]['id']]
    uno['hallazgos'][0]['descripcion'] = 'KG y UN separados.'
    assert not criterios_automaticos(caso, uno, payload)['unidades_separadas']
    obj['resumen_ejecutivo'] = 'El total UMP es 1250.'
    assert not criterios_automaticos(caso, obj, payload)['sin_frases_prohibidas']
    with pytest.raises(ErrorIA) as exc:
        validar_informe(json.dumps(obj), payload)
    assert exc.value.codigo == 'cifra_sin_respaldo'


@pytest.mark.parametrize('texto,permitido', [
    ('La meta es nula; no representa cumplimiento perfecto.', True),
    ('No corresponde interpretarlo como cumplimiento perfecto ni como éxito.', True),
    ('El resultado representa cumplimiento perfecto.', False),
    ('No representa cumplimiento perfecto. El resultado sí representa cumplimiento perfecto.', False),
    ('No representa cumplimiento perfecto, pero sí es cumplimiento perfecto.', False),
    ('No es cierto que no representa cumplimiento perfecto.', False),
])
def test_prohibicion_no_penaliza_negacion_directa_ni_exime_otra_afirmacion(texto, permitido):
    caso = cargar_casos()[3]
    payload = construir_payload(caso)
    obj = informe_valido(payload)
    obj['limitaciones'] = [texto]
    assert criterios_automaticos(caso, obj, payload)['sin_frases_prohibidas'] is permitido


def test_revalidacion_conserva_evidencia_y_no_regresa_respuestas_aceptadas():
    from scripts.revalidar_evidencia import ROOT, revalidar
    source = ROOT / 'evidencias/13_evaluacion_real.json'
    antes = source.read_bytes()
    report = revalidar(source)
    assert source.read_bytes() == antes
    assert report['llamadas_api'] == 0 and report['no_demuestra_mejora_del_prompt']
    assert len(report['resultados']) == 20
    for row in report['resultados']:
        for attempt in row['intentos']:
            if attempt['estado_original'] == 'valido':
                assert attempt['estado_revalidado'] == 'valido'
            if attempt['estado_original'] == 'causalidad_no_sustentada':
                assert attempt['estado_revalidado'] == 'valido'
    # Persiste el incumplimiento real de referencias de GS-05/v1.
    row = next(r for r in report['resultados'] if r['caso'] == 'GS-05' and r['prompt'] == 'v1')
    assert not row['automatico_revalidado']
