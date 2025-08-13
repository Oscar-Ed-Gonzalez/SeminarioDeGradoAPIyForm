from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Cambia aquí para PostgreSQL, por ejemplo:
# DATABASE_URL = "postgresql+psycopg://user:pass@localhost:5432/rosdb"
DATABASE_URL = "postgresql+psycopg2://postgres:contrasena123@localhost:5432/ros_db"

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()