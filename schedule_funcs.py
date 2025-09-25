import schedule, temp_db
from temp_db import *
import time, telebot
from datetime import datetime, timedelta


#add_message(123, 1, 2, {"text":{"id":10}})
#print(datetime.now(tz=timezone.utc))
#print(select_message(Message.send_time>=(datetime.now() - timedelta(seconds=30)))[0].id)

def scheduled_task(bot, target, stime):
    messages = select_message(Message.send_time>=(datetime.now() - timedelta(seconds=stime)))
    for message in messages:
        if message.msg_type == '':
            



def run_scheduler(bot, target, stime):
    '''Запуск планировщика'''
    schedule.every(stime).seconds.do(scheduled_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)