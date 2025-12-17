from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.database import get_db, Base
from app.schemas import Conta

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

connection = engine.connect()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def get_client_with_db():
    Base.metadata.create_all(bind=connection)

    client = TestClient(app)
    yield client

    Base.metadata.drop_all(bind=connection)


def test_criar_conta(client: TestClient):
    resposta = client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

    assert resposta.status_code == status.HTTP_201_CREATED
    data = Conta.model_validate(resposta.json())

    assert data.numero_conta == 1
    assert data.saldo == 100.0

    assert isinstance(data.numero_conta, int)
    assert isinstance(data.saldo, float)


def test_nao_pode_criar_conta_duas_vezes(client: TestClient):
    adicionado_ao_banco = client.post(
        "/conta/", json={"numero_conta": 1, "saldo": 100.0}
    )

    resposta = client.post("/conta/", json={"numero_conta": 1, "saldo": 200.0})

    assert resposta.status_code == status.HTTP_400_BAD_REQUEST
    data = Conta.model_validate(adicionado_ao_banco.json())

    assert data.saldo == 100.0


def test_pegar_conta(client: TestClient):
    client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

    numero_conta = 1
    resposta = client.get(f"/conta/{numero_conta}")

    assert resposta.status_code == status.HTTP_200_OK

    data = Conta.model_validate(resposta.json())

    assert data.numero_conta == 1
    assert data.saldo == 100.0

    assert isinstance(data.numero_conta, int)
    assert isinstance(data.saldo, float)


def test_erro_acessar_conta_inexistente(client: TestClient):
    resposta = client.get("/conta/1")

    assert resposta.status_code == status.HTTP_404_NOT_FOUND


def test_saldo_insuficiente(client: TestClient):
    client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

    resposta = client.post(
        "/transacao/",
        json={"numero_conta": 1, "tipo_transferencia": "P", "valor": 110.0},
    )

    assert resposta.status_code == status.HTTP_400_BAD_REQUEST


class TestCadaTipoTransferencia:
    def test_pix(self, client: TestClient):
        client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

        resposta = client.post(
            "/transacao/",
            json={"numero_conta": 1, "tipo_transferencia": "P", "valor": 100.0},
        )

        assert resposta.status_code == status.HTTP_200_OK

        data = Conta.model_validate(resposta.json())

        assert data.saldo == 0

    def test_debito(self, client: TestClient):
        client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

        resposta = client.post(
            "/transacao/",
            json={"numero_conta": 1, "tipo_transferencia": "D", "valor": 90.0},
        )

        assert resposta.status_code == status.HTTP_200_OK

        data = Conta.model_validate(resposta.json())

        assert data.saldo == pytest.approx(7.3)  # type: ignore[arg-type]

    def test_credito(self, client: TestClient):
        client.post("/conta/", json={"numero_conta": 1, "saldo": 100.0})

        resposta = client.post(
            "/transacao/",
            json={"numero_conta": 1, "tipo_transferencia": "C", "valor": 90.0},
        )

        assert resposta.status_code == status.HTTP_200_OK

        data = Conta.model_validate(resposta.json())

        assert data.saldo == pytest.approx(5.5)  # type: ignore[arg-type]
