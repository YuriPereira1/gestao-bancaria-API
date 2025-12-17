from decimal import Decimal
from sqlalchemy import Integer, Numeric, Identity
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Banco(Base):
    __tablename__ = "contas"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True)
    numero_conta: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    saldo: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
