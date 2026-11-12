"""Generador determinista de ventas ficticias; no fuentes corporativas."""
import csv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validador_csv import COLUMNAS


def generar(destino):
    with Path(destino).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        writer.writeheader()
        for ano in (2025, 2026):
            for mes in range(1, 11):
                for ci, canal in enumerate(("Tradicional", "Supermercado", "Foodservice")):
                    for oi, oficina in enumerate(("Oficina Norte", "Oficina Centro", "Oficina Sur")):
                        for li, (linea, familia, unidad) in enumerate((("Alimentos", "Preparados ficticios", "KG"), ("Insumos", "Packs ficticios", "UN"))):
                            base = 1_400_000 + ci * 420_000 + oi * 220_000 + li * 180_000 + mes * 65_000
                            factor = (93, 115, 108)[ci] + (2 if oi == 1 else 0) - li * 3
                            real = base if ano == 2025 else base * factor // 100
                            meta = "" if ano == 2025 else base * 112 // 100
                            writer.writerow(dict(zip(COLUMNAS, (ano, mes, canal, linea, familia, oficina, unidad,
                                real, meta, real // (4000 if unidad == "KG" else 8000), "" if ano == 2025 else meta // (4000 if unidad == "KG" else 8000)))))


if __name__ == "__main__":
    generar(Path(__file__).resolve().parents[1] / "datos/demo_ventas.csv")
