import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_INSTANCE = os.environ.get("DB_INSTANCE")

required_vars = ["DB_USER", "DB_PASSWORD", "DB_NAME","DB_INSTANCE"]
for var in required_vars:
    if not os.environ.get(var):
        raise ValueError(f"Environment variable {var} is missing")

connector = Connector()

# initialize SQLAlchemy connection pool with Connector
engine = create_engine(
    "mysql+pymysql://",
    creator=lambda: connector.connect(
        DB_INSTANCE,
        "pymysql",
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    ), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
