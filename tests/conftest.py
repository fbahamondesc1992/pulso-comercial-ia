import io
import csv
import socket
from decimal import Decimal
import pytest
from validador_csv import COLUMNAS, Dataset


@pytest.fixture(autouse=True)
def sin_red(monkeypatch):
    def prohibido(*args, **kwargs):
        raise AssertionError("La suite local no permite red ni consumo de API.")
    monkeypatch.setattr(socket.socket, "connect", prohibido)
    monkeypatch.setattr(socket, "create_connection", prohibido)


def fila(ano=2026, mes=1, real="1200000", meta="1500000", **extras):
    row = dict(zip(COLUMNAS, (ano, mes, "Canal A", "Línea A", "Familia A", "Oficina A", "KG",
                              Decimal(real), Decimal(meta) if meta is not None else None, Decimal("1000"), Decimal("1250"))))
    row.update(extras)
    return row


def dataset(real="1200000", meta="1500000", base="1000000"):
    return Dataset([fila(real=real, meta=meta), fila(ano=2025, real=base, meta=None)], [])


def csv_bytes(rows=None, headers=COLUMNAS):
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows if rows is not None else [fila()])
    return out.getvalue().encode()
