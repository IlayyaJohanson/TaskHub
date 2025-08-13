from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from modules import config

engine = create_engine(config.DB_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
