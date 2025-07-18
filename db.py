import sqlalchemy
from sqlalchemy import create_engine, event, Column, Integer, String, ForeignKey, Table, DateTime, Boolean, select
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Mapped, mapped_column, scoped_session

from contextlib import contextmanager
from datetime import datetime, timezone
from typing import List
from log import log_error, log_info, InfoType

from settings.settings import *

DB_URL = 'sqlite:///database/database.db'
engine = create_engine(
    DB_URL,
    echo=dbecho, 
    pool_size=5, 
    connect_args={
        'check_same_thread': False,
        'timeout': 30
    }
    )
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
#tables
JoinTS = Table(
    "joinedTS",
    Base.metadata,
    Column("u_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("s_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True) 
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)
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

    t_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True, nullable=False, default=0)
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

#initialization
def create_db_and_tables():
	Base.metadata.create_all(engine)


@contextmanager
def db_session():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        Session.remove()
      
#adds(inserts)
def add_user(user_id, username, name, clas, warn=0, is_admin=0, is_teacher=0, busy=0):
    with db_session() as session:  # Автоматический remove() при выходе
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
        try:
            session.commit()
            log_info(f'user: {new_user.name}', InfoType.ADD)
            return True
        except Exception as ex:
            session.rollback()
            log_error(ex)
            return False

def add_subject(subj):
    with db_session() as session:  # Автоматический remove() при выходе
        new_subject = Subject(subject=subj)
        session.add(new_subject)
        try:
            session.commit()
            log_info(f'subject: {new_subject.subject}', InfoType.ADD)
            return True
        except Exception as ex:
            session.rollback()
            log_error(ex)
            return False

def add_join(user_id, subject_id):
    with db_session() as session:
        user = session.get(User, user_id)
        subj = session.get(Subject, subject_id)
        user.subjects.append(subj)
        try:
            session.commit()
            log_info(f'join between: {user.name} and {subj.subject}', InfoType.ADD)
            return True
        except Exception as ex:
            session.rollback()
            log_error(ex)
            return False
        
def add_theme(u_id, s_id, question=None):
    with db_session() as session:
        user = session.get(User, u_id)
        subject = session.get(Subject, s_id)
        theme = Theme(u_id=user.id, s_id=subject.id, question=question)
        session.add(theme)
        try:
            session.commit()
            log_info(f'theme with user: {user.name} on subject: {subject.subject}', InfoType.ADD)
            return True
        except Exception as ex:
            session.rollback()
            log_error(ex)
            return False

#update(updates)
def update(user_id, new_name):
    with db_session() as session:
        user = session.get(User, user_id)
        

#dels
def del_user(user_id):
    with db_session() as session:
        user = session.get(User, user_id)
        session.delete(user)
        try:
            session.commit()
            log_info(f'user: {user.name}', InfoType.DEL)
            return True
        except Exception as ex:
            session.rollback()
            log_error(ex)
            return False
        
def del_subject(subject_id):
    with db_session() as session:
        subject = session.get(Subject, subject_id)
        session.delete(subject)
        try:
            session.commit()
            log_info(f'subject: {subject.subject}', InfoType.DEL)
            return True
        except Exception as ex:
            session.rollback()
            log_error(ex)
            return False
        
def del_join(user_id, subject_id):
    with db_session() as session:
        user = session.get(User, user_id)
        subj = session.get(Subject, subject_id)
        user.subjects.remove(subj)
        try:
            session.commit()
            log_info(f'join between: {user.name} and {subj.subject}', InfoType.DEL)
            return True
        except Exception as ex:
            session.rollback()
            log_error(ex)
            return False

def del_asked_theme(user_id):
    with db_session() as session:
        theme = session.scalar(select(Theme).where(Theme.u_id == user_id and Theme.status == 0))
        user = session.get(User, user_id)
        session.delete(theme)
        try:
            session.commit()
            log_info(f'unanswered theme from user: {user.name}', InfoType.DEL)
            return True
        except Exception as ex:
            session.rollback()
            log_error(ex)
            return False


# try:
#     #add_subject('history')
#     #add_user(1, None, 'Raz', 10)
#     #add_join(1, 3)
#     #del_user(1)
#     #add_theme(1, 2, 2, 'Goida')
#     #add_join(2, 2)
#     print('work')
# except sqlalchemy.exc.IntegrityError:
#     print('unic fail')