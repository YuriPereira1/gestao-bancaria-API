from typing import Literal
from pydantic import BaseModel, ConfigDict


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
