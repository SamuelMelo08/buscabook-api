from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Url do banco de dads
DATABASE_URL = 'sqlite:///base.db'

#Criação de uma conexão com o banco
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Função para pegar uma seção
def get_session():

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
