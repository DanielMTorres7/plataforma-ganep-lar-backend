from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# Configuração do banco de dados
DATABASE_URL = "postgresql://RPA:Ganep1175@localhost/GanepLar"  # SQLite (ou use PostgreSQL/MySQL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

__all__ = ['SessionLocal', 'Session', 'text']