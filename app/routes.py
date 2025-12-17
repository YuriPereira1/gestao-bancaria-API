from typing import Annotated
from fastapi import APIRouter, Depends, Path, status, HTTPException, Body
from sqlalchemy.orm import Session
from . import crud, errors
from .schemas import Conta, CriarConta, Transferencia
from .database import get_db

router = APIRouter()

tags_metadata = [
    {
        "name": "Conta",
        "description": "Operações relacionadas as contas.",
    },
    {"name": "Transação", "description": "Operações de transação de conta."},
]


@router.post(
    "/conta/",
    response_model=Conta,
    status_code=status.HTTP_201_CREATED,
    tags=["Conta"],
    summary="Cria conta",
    description="Rota para criar conta.",
)
async def criar_conta(
    conta: Annotated[CriarConta, Body()], db: Session = Depends(get_db)
):
    crud_response = crud.criar_conta(db, conta)
    if isinstance(crud_response, errors.ErrorContaJaExiste):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Conta já existe!"
        )
    return crud_response


@router.get(
    "/conta/{numero_conta}",
    response_model=Conta,
    status_code=status.HTTP_200_OK,
    tags=["Conta"],
    summary="Pega conta",
    description="Busca e retorna uma conta pelo seu id.",
)
async def get_conta(
    numero_conta: Annotated[int, Path()],
    db: Session = Depends(get_db),
):
    crud_response = crud.get_conta(db, numero_conta)
    if isinstance(crud_response, errors.ErrorContaNaoExiste):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não existe!"
        )
    return crud_response


@router.post(
    "/transacao/",
    response_model=Conta,
    status_code=status.HTTP_200_OK,
    tags=["Transação"],
    summary="Transfere saldo",
    description="Subtrai valor transferido da conta selecionada, "
    "jutamente com taxas de tranferência.",
)
async def transferir(
    transferencia: Annotated[Transferencia, Body()], db: Session = Depends(get_db)
):
    crud_response = crud.transacao_bancaria(db, transferencia)
    if isinstance(crud_response, errors.ErrorContaNaoExiste):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não existe!"
        )
    if isinstance(crud_response, errors.ErrorSaldoInsuficiente):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente!"
        )
    return crud_response
