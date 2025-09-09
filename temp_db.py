import sqlalchemy
from sqlalchemy import create_engine, event, Column, Integer, String, ForeignKey, Table, DateTime, Boolean, select, update
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Mapped, mapped_column, scoped_session

from contextlib import contextmanager
from datetime import datetime, timezone
from typing import List
from log import log_error, log_info, InfoType
from enum import Enum, auto

from settings.settings import *
from errors import *




DB_URL = 'sqlite:///database/temporary_database.db'
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
class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, nullable=False)
    sender: Mapped[int] = mapped_column(Integer, nullable=False)#0 - admin, 1 - teacher, 2 - student
    receiver: Mapped[int] = mapped_column(Integer, nullable=False)#0 - admin, 1 - teacher, 2 - student
    username: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    clas: Mapped[int] = mapped_column(Integer, nullable=False)
    registration_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    warn: Mapped[int] = mapped_column(Integer, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_teacher: Mapped[int] = mapped_column(Integer, nullable=False)#0 - не препод, 1 - не подтверждённый препод, 2 - подтверждённый препод
    busy: Mapped[int] = mapped_column(Integer, nullable=False)#0 - не занят, 1 - занят как ученик, 2 - занят как препод, 12 - занят и как препод и как ученик

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

#update(updates)
def rows_update(model, conditions, updates, max_rows=None):
    '''
    update
    
    conditions: for more complex conditions, use & as and, | as or \n
    '''
    with db_session() as session:
        try:
            # Проверяем количество затрагиваемых строк
            if max_rows is not None:
                count = session.query(model).filter(conditions).count()
                if count > max_rows:
                    raise InsertValueError('Too many rows for update')
            
            # Выполняем обновление
            stmt = (
                update(model)
                .where(conditions)
                .values(**updates)
                .execution_options(synchronize_session="fetch")
            )
            result = session.execute(stmt)
            
            session.commit()
            log_info(f'conditions: {conditions} updated with values: {updates}', InfoType.UPDATE)
            return True
            
        except Exception as ex:

            session.rollback()
            log_error(ex)
            return False

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