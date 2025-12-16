from fastapi import Query
from pydantic import BaseModel, ConfigDict
from typing import Annotated, Literal


class ContaBase(BaseModel):
    numero_conta: int
    saldo: float = 0.0


class CriarConta(ContaBase):
    pass


class Conta(ContaBase):
    model_config = ConfigDict(from_attributes=True)


class Transferencia(BaseModel):
    numero_conta: int
    tipo_transferencia: Literal["P", "D", "C"]
    valor: float
