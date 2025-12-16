from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from . import crud
from .schemas import Conta, CriarConta, Transferencia
from .database import get_db

router = APIRouter()


@router.post("/conta/", response_model=Conta, status_code=status.HTTP_201_CREATED)
def criar_conta(conta: CriarConta, db: Session = Depends(get_db)):
    return crud.criar_conta(db, conta)


@router.get(
    "/conta/{numero_conta}", response_model=Conta, status_code=status.HTTP_200_OK
)
def get_conta(numero_conta: int, db: Session = Depends(get_db)):
    return crud.get_conta(db, numero_conta)


@router.post("/transacao/", response_model=Conta, status_code=status.HTTP_200_OK)
def transferir(transferencia: Transferencia, db: Session = Depends(get_db)):
    return crud.transacao_bancaria(db, transferencia)
