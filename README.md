## 🏦 Gestão Bancária API

API em FastAPI + SQLAlchemy + PostgreSQL, pronta para rodar via Docker.

## 📋 Pré-requisitos

Docker e Docker Compose (já vem com Docker recente)

Nenhuma instalação de Python ou PostgreSQL é necessária localmente.

## ⚙️ Setup

Clone o repositório:

`git clone git@github.com:YuriPereira1/gestao-bancaria-API.git`

```sh
cd gestao_bancaria_api
cp .env.example .env
```
Copie o arquivo de exemplo de variáveis de ambiente:

Suba os containers com Docker Compose:

`docker compose up --build`

Acesse a documentação da API no navegador:

http://0.0.0.0:8000/docs


## ⚠️ Observações

Caso o banco já esteja em uso na porta 5432 do host, você pode remover a exposição da porta do docker-compose.yml.

Se precisar resetar o banco (limpar dados), execute:

`docker compose down -v`


Para parar os containers sem remover volumes:

docker compose down


Se quiser parar todos os containers do Docker:

`docker stop $(docker ps -q)`