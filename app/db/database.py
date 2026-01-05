import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres123@db:5432/sentinelstream"
)

engine = create_engine(DATABASE_URL)


Base = declarative_base()
