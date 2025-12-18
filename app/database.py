import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    logging.error("ERRO: a variável de ambiente DATABASE_URL não está definida!")
    sys.exit(1)

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
