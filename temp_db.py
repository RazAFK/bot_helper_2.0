import sqlalchemy
from sqlalchemy import create_engine, event, Column, Integer, String, ForeignKey, Table, DateTime, Boolean, select, update, JSON
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Mapped, mapped_column, scoped_session

from contextlib import contextmanager
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from log import log_error, log_info, InfoType, log_temp, log_temp_error
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
    theme_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sender: Mapped[int] = mapped_column(Integer, nullable=False)#0 - admin, 1 - teacher, 2 - student
    receiver: Mapped[int] = mapped_column(Integer, nullable=False)#0 - admin, 1 - teacher, 2 - student
    content: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    send_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)

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
def add_message(theme_id, sender, receiver, content):
    with db_session() as session:  # Автоматический remove() при выходе
        new_message = Message(
            theme_id = theme_id,
            sender = sender,
            receiver = receiver,
            content = content
        )
        session.add(new_message)
        try:
            session.commit()
            log_temp(f'new message in theme {new_message.theme_id}, from {new_message.sender} to {new_message.receiver}', InfoType.TEMP)
            return True
        except Exception as ex:
            session.rollback()
            log_temp_error(ex)
            return False

#update(updates)
def update_message(conditions, updates, model=Message, max_rows=None):
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
            log_temp(f'conditions: {conditions} updated with values: {updates}', InfoType.UPDATE)
            return True
            
        except Exception as ex:

            session.rollback()
            log_temp_error(ex)
            return False

#dels
def del_message(message_id):
    with db_session() as session:
        message = session.get(Message, message_id)
        session.delete(message)
        try:
            session.commit()
            log_temp(f'user: {message.id}', InfoType.DEL)
            return True
        except Exception as ex:
            session.rollback()
            log_temp_error(ex)
            return False
        

#update(updates)
def select_message(conditions, model=Message):
    '''
    select
    
    conditions: for more complex conditions, use & as and, | as or \n
    '''
    with db_session() as session:
        try:
            # получаем объект
            stmt = (
                select(model)
                .where(conditions)
                .execution_options(synchronize_session="fetch")
            )
            result = session.scalars(stmt).all()
            return result
            
        except Exception as ex:

            session.rollback()
            log_temp_error(ex)
            return False