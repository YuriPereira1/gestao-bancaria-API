from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Banco(Base):
    __tablename__ = "contas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    numero_conta: Mapped[int] = mapped_column(nullable=False)
    saldo: Mapped[float] = mapped_column(nullable=False)
