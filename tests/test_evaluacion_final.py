import json
from decimal import Decimal

import pytest

from analista_ia import ErrorIA
from scripts.evaluar_prompts import Presupuesto, main


def test_limite_acumulado_conserva_consumo_y_no_admite_intento_67(tmp_path):
    path = tmp_path / 'presupuesto.json'
    budget = Presupuesto(66, '2', path, '0.5843775', 26)
    for _ in range(40):
        budget.reservar()
        budget.liquidar(1000, 100)
    with pytest.raises(ErrorIA, match='presupuesto'):
        budget.reservar()
    budget.close()
    saved = json.loads(path.read_text())
    assert saved['llamadas'] == 66
    assert Decimal(saved['comprometido_usd']) == Decimal('0.5843775') + 40 * Decimal('0.0035')
    with pytest.raises(ValueError, match='ampliar'):
        Presupuesto(67, '2', path)


@pytest.mark.parametrize('extra', [['--max-llamadas', '67'], ['--tope-usd', '3']])
def test_cli_rechaza_ampliaciones_no_autorizadas_antes_del_proveedor(monkeypatch, tmp_path, extra):
    monkeypatch.setattr('sys.argv', ['evaluar_prompts.py', '--modo', 'real',
        '--autorizacion', 'AUTORIZO EVAL IA', '--tope-usd', '2',
        '--max-llamadas', '66', '--estado-presupuesto', str(tmp_path / 'saldo.json'), *extra])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 2
    assert not (tmp_path / 'saldo.json').exists()
