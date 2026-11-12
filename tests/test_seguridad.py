from scripts.auditar_secretos import PATRONES


def test_clave_vacia_no_captura_linea_siguiente():
    pattern=PATRONES['asignacion_api_key']
    assert not pattern.search('OPENAI_API_KEY=\nANALYST_PROMPT_VERSION=v2')
    assert pattern.search('OPENAI_API_KEY=' + 'valor_sintetico_para_prueba')
