from typing import Literal
from sqlalchemy import select
from sqlalchemy.orm import Session
from . import schemas, models, errors


def get_conta(db: Session, numero_conta: int) -> models.Banco | None:
    """
    Pega a conta bancária do usuário pelo ID fornecido.
    """
    query = select(models.Banco).where(models.Banco.numero_conta == numero_conta)
    return db.execute(query).scalars().first()


def criar_conta(db: Session, usuario: schemas.CriarConta) -> models.Banco | None:
    db_usuario = models.Banco(**usuario.model_dump())
    existe_usuario = get_conta(db, db_usuario.numero_conta)
    if existe_usuario:
        return None
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
) -> models.Banco | errors.ErrorPostTransferencia:
    db_conta: models.Banco | None = get_conta(db, transferencia.numero_conta)
    if db_conta is None:
        return errors.ErrorContaNaoExiste(mensagem="A conta não existe")
    taxa = get_taxa(transferencia.tipo_transferencia)
    valor_descontar = transferencia.valor * (taxa + 1)
    if db_conta.saldo < valor_descontar:
        return errors.SaldoInsuficiente(mensagem="Saldo insuficiente")
    db_conta.saldo -= valor_descontar
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta
