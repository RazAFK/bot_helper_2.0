import threading
import schedule
import time
import telebot
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, DateTime, String

# Настройка базы данных
Base = declarative_base()
engine = create_engine('sqlite:///your_database.db')

# Модель данных
class UserData(Base):
    __tablename__ = 'user_data'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    data = Column(String)
    user_id = Column(Integer)

# Функция для получения данных за последние 30 секунд
def get_recent_user_data():
    """Получить данные пользователей за последние 30 секунд"""
    with Session(engine) as session:
        time_threshold = datetime.now() - timedelta(seconds=30)
        
        query = select(UserData).where(
            UserData.timestamp >= time_threshold
        ).order_by(UserData.timestamp.desc())
        
        result = session.execute(query)
        recent_data = result.scalars().all()
        
        return recent_data

# Телеграм бот
TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

def scheduled_task():
    """Задача, выполняемая каждые 30 секунд"""
    try:
        recent_data = get_recent_user_data()
        
        if recent_data:
            print(f"Найдено {len(recent_data)} записей за последние 30 секунд:")
            for data in recent_data:
                print(f"Время: {data.timestamp}, Данные: {data.data}")
                
                # Можно отправить уведомление пользователю
                # bot.send_message(data.user_id, f"Новые данные: {data.data}")
        else:
            print("Нет новых данных за последние 30 секунд")
            
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")

def run_scheduler():
    """Запуск планировщика"""
    schedule_funcs.every(30).seconds.do(scheduled_task)
    
    while True:
        schedule_funcs.run_pending()
        time.sleep(1)

# Запуск планировщика в отдельном потоке
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

# Обработчики бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Бот запущен и мониторит БД каждые 30 секунд!")

@bot.message_handler(commands=['recent'])
def send_recent_data(message):
    """Команда для получения последних данных"""
    try:
        recent_data = get_recent_user_data()
        if recent_data:
            response = f"Последние данные ({len(recent_data)} записей):\n"
            for data in recent_data:
                response += f"• {data.timestamp}: {data.data}\n"
        else:
            response = "Нет данных за последние 30 секунд"
        
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

if __name__ == "__main__":
    # Создаем таблицы если их нет
    Base.metadata.create_all(engine)
    
    print("Бот запущен...")
    bot.polling(none_stop=True)