from typing import Literal, Annotated
from pydantic import BaseModel, ConfigDict, Field


class ContaBase(BaseModel):
    numero_conta: Annotated[
        int, Field(..., ge=0, description="Numero da conta bancária")
    ]
    saldo: Annotated[float, Field(..., ge=0, description="Saldo da conta bancária")]


class CriarConta(ContaBase):
    pass


class Conta(ContaBase):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        json_schema_extra={"numero conta": 1, "saldo": 100.0},
    )


class Transferencia(BaseModel):
    numero_conta: Annotated[
        int, Field(..., ge=0, description="Numero da conta bancária")
    ]
    tipo_transferencia: Annotated[
        Literal["P", "D", "C"],
        Field(
            ..., description="Tipo de transferência bancária, Pix, Débito ou Crédito"
        ),
    ]
    valor: Annotated[float, Field(..., gt=0, description="Valor da transfêrencia")]
