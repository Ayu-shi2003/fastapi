from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

# Percent-encode special characters in password
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__= "users"

    id =Column(Integer,primary_key=True)
    name=Column(String)
    age=Column(Integer)

# Create all tables
Base.metadata.create_all(engine)
