from dataclasses import dataclass


class Errors:
    pass


class ErrorExecucao(Errors):
    pass


class ErrorConta(ErrorExecucao):
    pass


@dataclass
class ErrorContaNaoExiste(ErrorConta):
    pass


@dataclass
class ErrorContaJaExiste(ErrorConta):
    pass


class ErrorSaldo(ErrorExecucao):
    pass


@dataclass
class ErrorSaldoInsuficiente(ErrorSaldo):
    pass
