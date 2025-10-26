from db import *
from temp_db import *
import db, temp_db
from log import log_info, log_error, log_temp, log_temp_error
from errors import *
import telebot
from settings.settings import sbot

#create_db_and_tables()

#add_subject('geometry')
#update(Subject, Subject.id==1, {'id': 'MATH'}, 1)
#temp_db.create_db_and_tables()
#print(add_message(1, 0, 1, {"text":{"text": "abcd","message_id": 123}, "photo":{"id": "123asd"}}))
#print(select_message(Message.id==1)[0].content['text']['text'])

import threading, time, datetime

def infinite_worker():
    while True:
        if datetime.datetime.now().second%10==0:
            sbot.send_message(1634714523, f'from second thread: {datetime.datetime.now()}')
            time.sleep(1)
# Создаем демон-поток
thread = threading.Thread(target=infinite_worker)
thread.daemon = True  # Ключевой параметр!
thread.start()

print("🚀 Главный поток запущен")
print("⏹️  Нажмите Ctrl+C для остановки")

try:
    # Главный поток что-то делает
    for i in range(5):
        sbot.send_message(1634714523, f'from main thread: {datetime.datetime.now()}')
        time.sleep(10)
    print("✅ Главный поток завершил работу")
except KeyboardInterrupt:
    print("\n🛑 Получен Ctrl+C")