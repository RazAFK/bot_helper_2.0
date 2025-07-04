from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime, Boolean, select
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
    Column("u_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("s_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True) 
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


    asked_themes: Mapped[List["Theme"]] = relationship(
        'Theme',
        back_populates="asking_user",
        foreign_keys="[Theme.u_id]",
        cascade="save-update, merge",
        passive_deletes=True
    )
    answered_themes: Mapped[List["Theme"]] = relationship(
        'Theme',
        back_populates="answering_user",
        foreign_keys="[Theme.t_id]",
        cascade="save-update, merge",
        passive_deletes=True
    )

    
    subjects: Mapped[List["Subject"]] = relationship(
        secondary=JoinTS,
        back_populates="users"
    )

    
class Theme(Base):
    __tablename__ = "themes"

    t_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True, nullable=False)
    u_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    s_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'), nullable=False)
    question: Mapped[str] = mapped_column(String, nullable=True)
    ask_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)#0 - начата, 1 - в работе, 2 - завершена

    answering_user: Mapped["User"] = relationship(
        back_populates="answered_themes",
        foreign_keys=[t_id]
    )
    asking_user: Mapped["User"] = relationship(
        back_populates="asked_themes",
        foreign_keys=[u_id]
    )
    subject: Mapped["Subject"] = relationship(
        back_populates="themes"
    )


class Subject(Base):
    __tablename__ = 'subjects'
     
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, nullable=False)
    subject: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    themes: Mapped[List["Theme"]] = relationship(
        back_populates="subject",
        cascade="save-update, merge",
        passive_deletes=True
    )
    
    # Связь с пользователями через ассоциативную таблицу
    users: Mapped[List["User"]] = relationship(
        secondary=JoinTS,
        back_populates="subjects"
    )


def create_db_and_tables():
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
        #user = session.get(User, user_id)
        user = session.scalar(select(User).where(User.id == user_id))
        subj = session.get(Subject, subject_id)
        user.subjects.append(subj)
        session.commit()
        print(f"Связь между пользователем: {user.name} и предметом {subj.subject} добавлена")

def del_user(user_id):
    with Session() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        session.delete(user)
        session.commit()
        print(f"Пользователь {user.name} удалён")

def add_theme(u_id, t_id, s_id, question=None):
    with Session() as session:
        #user = session.get(User, user_id)
        user = session.get(User, u_id)
        teacher = session.get(User, t_id)
        subject= session.get(Subject, s_id)
        theme = Theme(u_id=user.id, t_id=teacher.id, s_id=subject.id, question=question)
        session.add(theme) 
        session.commit()
        print(f"Тема {question} с пользователем {user.name} и преподавателем {teacher.name}, по предмету {subject.subject}")


create_db_and_tables()
try:
    #add_subject('english')
    #add_user(1, None, 'Raz', 10)
    #add_join(1, 3)
    #del_user(1)
    #add_theme(1, 2, 2, 'Goida')
    #add_join(2, 2)
    print('work')
except sqlalchemy.exc.IntegrityError:
    print('unic fail')