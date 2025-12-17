from typing import Literal
from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal
from . import schemas, models, errors


def get_conta(
    db: Session, numero_conta: int
) -> models.Banco | errors.ErrorContaNaoExiste:
    query = select(models.Banco).where(models.Banco.numero_conta == numero_conta)
    db_conta = db.execute(query).scalars().first()
    if not db_conta:
        return errors.ErrorContaNaoExiste()
    return db_conta


def criar_conta(
    db: Session, usuario: schemas.CriarConta
) -> models.Banco | errors.ErrorConta:
    db_usuario = models.Banco(**usuario.model_dump())
    verificar_id_banco = get_conta(db, db_usuario.numero_conta)
    if isinstance(verificar_id_banco, models.Banco):
        return errors.ErrorContaJaExiste()
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def get_taxa(tipo: Literal["P", "D", "C"]) -> float:
    if tipo == "C":
        return 0.05
    if tipo == "D":
        return 0.03
    return 0.0


def transacao_bancaria(
    db: Session, transferencia: schemas.Transferencia
) -> models.Banco | errors.ErrorExecucao:
    db_conta = get_conta(db, transferencia.numero_conta)
    if isinstance(db_conta, errors.ErrorContaNaoExiste):
        return db_conta
    taxa = get_taxa(transferencia.tipo_transferencia)
    valor_descontar = transferencia.valor * Decimal(taxa + 1)
    if db_conta.saldo < valor_descontar:
        return errors.ErrorSaldoInsuficiente()
    db_conta.saldo -= valor_descontar
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta
