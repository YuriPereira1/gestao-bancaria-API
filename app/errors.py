from dataclasses import dataclass


class ErrorTransferencia:
    pass


class ErrorPostTransferencia(ErrorTransferencia):
    pass


class ErrorConta:
    pass


class ErrorPostConta(ErrorConta):
    pass


@dataclass
class SaldoInsuficiente(ErrorPostTransferencia):
    mensagem: str


@dataclass
class ErrorContaNaoExiste(ErrorPostTransferencia):
    mensagem: str
