## 🏦 Banking Management API

A FastAPI + SQLAlchemy + PostgreSQL API, ready to run using Docker.

---

## 📋 Prerequisites

- Docker and Docker Compose (included in recent Docker versions)

No local installation of Python or PostgreSQL is required.

## ⚙️ Setup


Clone the repository:

`git clone git@github.com:YuriPereira1/gestao-bancaria-API.git`

```
cd gestao_bancaria_api
```

Copy the example environment variables file:

`cp .env.example .env`

Start the containers using Docker Compose:

`docker compose up --build`

Access the API documentation in your browser:

http://0.0.0.0:8000/docs


## ⚠️ Notes

If the database port 5432 is already in use on your host machine, you can remove the port exposure from the `docker-compose.yml` file.

To reset the database (remove all data), run:

`docker compose down -v`


To stop the containers without removing volumes:

`docker compose down`


To stop all running Docker containers on your system:

`docker stop $(docker ps -q)`
