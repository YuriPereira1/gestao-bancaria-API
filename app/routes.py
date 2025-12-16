from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from . import crud, errors
from .schemas import Conta, CriarConta, Transferencia
from .database import get_db

router = APIRouter()


@router.post("/conta/", response_model=Conta, status_code=status.HTTP_201_CREATED)
def criar_conta(conta: CriarConta, db: Session = Depends(get_db)):
    crud_response = crud.criar_conta(db, conta)
    if isinstance(crud_response, errors.ErrorContaJaExiste):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Conta já existe!"
        )
    return crud_response


@router.get(
    "/conta/{numero_conta}", response_model=Conta, status_code=status.HTTP_200_OK
)
def get_conta(numero_conta: int, db: Session = Depends(get_db)):
    crud_response = crud.get_conta(db, numero_conta)
    if isinstance(crud_response, errors.ErrorContaNaoExiste):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não existe!"
        )
    return crud_response


@router.post("/transacao/", response_model=Conta, status_code=status.HTTP_200_OK)
def transferir(transferencia: Transferencia, db: Session = Depends(get_db)):
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
