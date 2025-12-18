from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.database import get_db, Base
from app.schemas import Conta

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/app_db_test"

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides.clear()
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)


def test_criar_conta(client: TestClient):  # pylint: disable=redefined-outer-name
    resposta = client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

    assert resposta.status_code == status.HTTP_201_CREATED
    data = Conta.model_validate(resposta.json())

    assert data.numero_conta == 1
    assert data.saldo == pytest.approx(100)  # type: ignore[arg-type]

    assert isinstance(data.numero_conta, int)
    assert isinstance(data.saldo, Decimal)


def test_nao_pode_criar_conta_duas_vezes(
    client: TestClient,
):  # pylint: disable=redefined-outer-name
    adicionado_ao_banco = client.post(
        "/conta/", json={"numero_conta": 1, "saldo": 100.0}
    )

    resposta = client.post("/conta/", json={"numero_conta": 1, "saldo": 200.0})

    assert resposta.status_code == status.HTTP_400_BAD_REQUEST
    data = Conta.model_validate(adicionado_ao_banco.json())

    assert data.saldo == 100


def test_pegar_conta(client: TestClient):  # pylint: disable=redefined-outer-name
    client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

    numero_conta = 1
    resposta = client.get(f"/conta/{numero_conta}")

    assert resposta.status_code == status.HTTP_200_OK

    data = Conta.model_validate(resposta.json())

    assert data.numero_conta == 1
    assert data.saldo == pytest.approx(100)  # type: ignore[arg-type]

    assert isinstance(data.numero_conta, int)
    assert isinstance(data.saldo, Decimal)


def test_erro_acessar_conta_inexistente(
    client: TestClient,
):  # pylint: disable=redefined-outer-name
    resposta = client.get("/conta/1")

    assert resposta.status_code == status.HTTP_404_NOT_FOUND


def test_saldo_insuficiente(client: TestClient):  # pylint: disable=redefined-outer-name
    client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

    resposta = client.post(
        "/transacao/",
        json={"numero_conta": 1, "tipo_transferencia": "P", "valor": 110.0},
    )

    assert resposta.status_code == status.HTTP_400_BAD_REQUEST


class TestCadaTipoTransferencia:
    def test_pix(self, client: TestClient):  # pylint: disable=redefined-outer-name
        client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

        resposta = client.post(
            "/transacao/",
            json={"numero_conta": 1, "tipo_transferencia": "P", "valor": 100.0},
        )

        assert resposta.status_code == status.HTTP_200_OK

        data = Conta.model_validate(resposta.json())

        assert data.saldo == pytest.approx(0)  # type: ignore

    def test_debito(self, client: TestClient):  # pylint: disable=redefined-outer-name
        client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

        resposta = client.post(
            "/transacao/",
            json={"numero_conta": 1, "tipo_transferencia": "D", "valor": 90.0},
        )

        assert resposta.status_code == status.HTTP_200_OK

        data = Conta.model_validate(resposta.json())

        assert data.saldo == pytest.approx(Decimal(7.3))  # type: ignore[arg-type]

    def test_credito(self, client: TestClient):  # pylint: disable=redefined-outer-name
        client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

        resposta = client.post(
            "/transacao/",
            json={"numero_conta": 1, "tipo_transferencia": "C", "valor": 90.0},
        )

        assert resposta.status_code == status.HTTP_200_OK

        data = Conta.model_validate(resposta.json())

        assert data.saldo == pytest.approx(5.5)  # type: ignore[arg-type]
