"""Ingesta en memoria, grano único y números acotados sin floats."""
import csv
import io
import re
import unicodedata
from dataclasses import dataclass
from decimal import Decimal

MAX_BYTES = 8 * 1024 * 1024
MAX_ROWS = 30_000
DIMENSIONES = ("canal", "linea", "familia", "oficina")
GRANO = ("ano", "mes", *DIMENSIONES, "unidad_ump")
COLUMNAS = (*GRANO, "facturacion_real_clp", "facturacion_meta_clp", "volumen_real_ump", "volumen_meta_ump")
NUMERO = re.compile(r"-?\d{1,15}(?:\.\d+)?\Z", re.ASCII)


class ErrorCSV(ValueError):
    pass


@dataclass(frozen=True)
class Dataset:
    filas: list[dict]
    advertencias: list[str]


def leer_csv(contenido: bytes, nombre: str = "datos.csv") -> Dataset:
    if not nombre.lower().endswith(".csv"):
        raise ErrorCSV("Selecciona un archivo con extensión .csv.")
    if not contenido or not contenido.strip():
        raise ErrorCSV("El archivo está vacío.")
    if len(contenido) > MAX_BYTES:
        raise ErrorCSV("El CSV supera el máximo de 8 MiB.")
    try:
        texto = contenido.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ErrorCSV("Usa un CSV UTF-8, separado por comas o punto y coma.") from exc
    if "\x00" in texto:
        raise ErrorCSV("El archivo contiene caracteres nulos.")
    try:
        # Elegir por la cabecera, nunca por valores o etiquetas de las filas.
        cabecera_coma = next(csv.reader(io.StringIO(texto, newline=""), strict=True))
        separador = ";" if len(cabecera_coma) == 1 else ","
        reader = csv.reader(io.StringIO(texto, newline=""), delimiter=separador, strict=True)
        cabecera = next(reader)
        if len(set(cabecera)) != len(cabecera):
            raise ErrorCSV("Hay columnas duplicadas en la cabecera.")
        if set(cabecera) != set(COLUMNAS):
            raise ErrorCSV("Las columnas deben coincidir con el ejemplo descargable: " + ", ".join(COLUMNAS))
        filas, vistos, cambios = [], {}, 0
        for values in reader:
            linea = reader.line_num
            if len(filas) >= MAX_ROWS:
                raise ErrorCSV("El CSV supera el máximo de 30.000 filas.")
            if len(values) != len(cabecera):
                raise ErrorCSV(f"Línea {linea}: cantidad de columnas incorrecta.")
            row = dict(zip(cabecera, values))
            if not re.fullmatch(r"[1-9][0-9]{3}", row["ano"]):
                raise ErrorCSV(f"Línea {linea}: año debe tener cuatro dígitos.")
            if not re.fullmatch(r"[0-9]{1,2}", row["mes"]) or not 1 <= int(row["mes"]) <= 12:
                raise ErrorCSV(f"Línea {linea}: mes debe estar entre 1 y 12.")
            row["ano"], row["mes"] = int(row["ano"]), int(row["mes"])
            for campo in DIMENSIONES:
                original = row[campo]
                limpio = unicodedata.normalize("NFC", original).strip()
                if not limpio or len(limpio) > (100 if campo == "familia" else 80):
                    raise ErrorCSV(f"Línea {linea}: {campo} vacío o demasiado largo.")
                if any(unicodedata.category(c).startswith("C") for c in limpio):
                    raise ErrorCSV(f"Línea {linea}: {campo} contiene caracteres de control.")
                cambios += int(original != limpio)
                row[campo] = limpio
            if row["unidad_ump"] not in ("KG", "UN"):
                raise ErrorCSV(f"Línea {linea}: unidad_ump debe ser KG o UN.")
            for campo in COLUMNAS[7:]:
                valor = row[campo]
                # Cada dialecto tiene una sola convención decimal, sin miles.
                canonico = valor.replace(",", ".") if separador == ";" else valor
                decimal_incorrecto = "." in valor if separador == ";" else "," in valor
                if valor == "" and "meta" in campo:
                    row[campo] = None
                elif decimal_incorrecto or not NUMERO.fullmatch(canonico) or (canonico.startswith("-") and "meta" in campo):
                    decimal = "coma decimal" if separador == ";" else "punto decimal"
                    raise ErrorCSV(f"Línea {linea}: {campo} requiere un número finito con {decimal} y máximo 15 enteros. Negativos solo en valores reales; sin miles ni notación científica.")
                else:
                    row[campo] = Decimal(canonico)
            clave = tuple(row[k] for k in GRANO)
            if clave in vistos:
                raise ErrorCSV(f"Grano duplicado en líneas {vistos[clave]} y {linea}, incluida la normalización de espacios/Unicode.")
            vistos[clave] = linea
            filas.append(row)
    except (csv.Error, StopIteration) as exc:
        raise ErrorCSV("CSV mal formado o sin cabecera válida.") from exc
    if not filas:
        raise ErrorCSV("El CSV no contiene filas con métricas calculables.")
    avisos = [f"Se normalizaron espacios exteriores o Unicode NFC en {cambios} etiquetas."] if cambios else []
    if len({r["ano"] for r in filas}) < 2:
        avisos.append("Solo hay un año: no existe comparación interanual.")
    return Dataset(filas, avisos)
