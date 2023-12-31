from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
name = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')
host = os.getenv('DB_HOST')

SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
