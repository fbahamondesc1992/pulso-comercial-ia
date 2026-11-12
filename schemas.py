"""Contratos tipados; valores monetarios se serializan como cadenas exactas."""
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class Estricto(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Filtros(Estricto):
    ano_actual: int = Field(ge=1000, le=9999)
    ano_base: int = Field(ge=1000, le=9999)
    meses: list[Annotated[int, Field(ge=1, le=12)]] = Field(min_length=1, max_length=12)
    canal: str | None = Field(default=None, max_length=80)
    linea: str | None = Field(default=None, max_length=80)
    familia: str | None = Field(default=None, max_length=100)
    oficina: str | None = Field(default=None, max_length=80)

    @model_validator(mode="after")
    def coherencia(self):
        if self.ano_base >= self.ano_actual:
            raise ValueError("El año base debe ser anterior al año actual.")
        if len(set(self.meses)) != len(self.meses):
            raise ValueError("No repetir meses.")
        self.meses.sort()
        return self


Texto = Annotated[str, Field(min_length=1, max_length=700)]
Referencias = Annotated[list[Annotated[str, Field(pattern=r"^F[0-9]{3}$")]], Field(min_length=1, max_length=8)]


class Hallazgo(Estricto):
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: Texto
    evidencia_ids: Referencias
    nivel: Literal["atencion", "positivo", "informativo"]


class Accion(Estricto):
    accion: Texto
    evidencia_ids: Referencias
    categoria: Literal["investigacion", "seguimiento"]


class InformeIA(Estricto):
    resumen_ejecutivo: Texto
    hallazgos: list[Hallazgo] = Field(max_length=5)
    acciones_sugeridas: list[Accion] = Field(max_length=4)
    limitaciones: list[Texto] = Field(min_length=1, max_length=6)
