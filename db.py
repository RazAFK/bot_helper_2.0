from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Mapped, mapped_column

DB_URL = 'sqlite:///db/database.db'
engine = create_engine(DB_URL, echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)



def create_db_and_tables() -> None:
	Base.metadata.create_all(engine)