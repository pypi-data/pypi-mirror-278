from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

DB_CONNECTION_STRING = os.environ.get('DB_CONNECTION_STRING', 'postgresql://dekel:dekel@127.0.0.1:5432/dominoscode')
engine = create_engine(DB_CONNECTION_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()

def get_db():
    database: Session = SessionLocal()
    try:
        yield database
    except Exception:
        raise Exception('Failed to connect to db')
    finally:
        database.close()
