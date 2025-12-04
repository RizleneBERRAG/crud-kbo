from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fichier SQLite dans le dossier data/
DATABASE_URL = "sqlite:///./data/kbo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dépendance FastAPI : fournir une session DB à chaque requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
