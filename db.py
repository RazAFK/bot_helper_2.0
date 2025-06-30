from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Mapped, mapped_column, scoped_session
import sqlalchemy
from datetime import datetime, timezone
from typing import List

DB_URL = 'sqlite:///database.db'
engine = create_engine(DB_URL, echo=True)
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

JoinTS = Table(
    "joinedTS",
    Base.metadata,
    Column("u_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("s_id", Integer, ForeignKey("subjects.id"), primary_key=True) 
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    clas: Mapped[int] = mapped_column(Integer, nullable=False)
    registration_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    warn: Mapped[int] = mapped_column(Integer, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_teacher: Mapped[int] = mapped_column(Integer, nullable=False)#0 - не препод, 1 - не подтверждённый препод, 2 - подтверждённый препод
    busy: Mapped[int] = mapped_column(Integer, nullable=False)#0 - не занят, 1 - занят как ученик, 2 - занят как препод, 12 - занят и как препод и как ученик


    subjects: Mapped[List["Subject"]] = relationship(
        secondary=JoinTS,
        back_populates='users',
        cascade='save-update, merge',
        lazy='select'

    )


class Subject(Base):
     __tablename__ = 'subjects'
     
     id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, nullable=False)
     subject: Mapped[str] = mapped_column(String, unique=True, nullable=False)

     users: Mapped[List["User"]] = relationship(
        secondary=JoinTS,
        back_populates='subjects',
        viewonly=True
    )


def create_db_and_tables() -> None:
	Base.metadata.create_all(engine)
      

def add_user(user_id, username, name, clas, warn=0, is_admin=0, is_teacher=0, busy=0):
    with Session() as session:  # Автоматический remove() при выходе
        new_user = User(
            id=user_id,
            username=username,
            name=name,
            clas=clas,
            warn=warn,
            is_admin=is_admin,
            is_teacher=is_teacher,
            busy=busy
            )
        session.add(new_user)
        session.commit()
        print(f"Пользователь {name} добавлен")

def add_subject(subj):
    with Session() as session:  # Автоматический remove() при выходе
        new_subject = Subject(subject=subj)
        session.add(new_subject)
        session.commit()
        print(f"Предмет {subj} добавлен")


def add_join(user_id, subject_id):
    with Session() as session:
        user = session.get(User, user_id)
        subj = session.get(Subject, subject_id)
        user.subjects.append(subj)
        session.commit()
        print(f"Связь между пользователем: {user.name} и предметом {user.subjects} добавлена")

create_db_and_tables()
try:
    add_subject('english')
    #add_user(54321, None, 'Raz', 10)
    add_join(54321, 3)
    print('arr')
except sqlalchemy.exc.IntegrityError:
    print('unic fail')