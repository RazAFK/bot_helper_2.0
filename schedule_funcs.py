import schedule, temp_db
from temp_db import *
from db import *
import time, telebot
from datetime import datetime, timedelta

bot = telebot.TeleBot('admin_token')

#add_message(123, 1, 2, {"text":{"id":10}})
#print(datetime.now(tz=timezone.utc))
#print(select_message(Message.send_time>=(datetime.now() - timedelta(seconds=30)))[0].id)

def scheduled_task(, receiver, stime):
    messages = select_message((Message.send_time>=(datetime.now() - timedelta(seconds=stime))) & (Message.receiver==receiver))
    for message in messages:
        if message.comand != 3:
            theme = select_smth(Theme, Theme.id == Message.theme_id)[0]
            if message.comand == 1:
                uraito = bot.send_message(theme.u_id, 'Вы начали диалог').message_id()
                rows_update(Theme, Theme.id == Message.theme_id, {'u_raito': uraito, 'status': 1})
            elif message.comand == 2:
                if receiver == 1:
                    bot.send_message(theme.t_id, 'Вы завершили диалог')
                    bot.send_message(theme.u_id, 'Собеседник завершил диалог')
                else:
                    bot.send_message(theme.u_id, 'Вы завершили диалог')
                    bot.send_message(theme.t_id, 'Собеседник завершил диалог')
                rows_update(Theme, Theme.id == Message.theme_id, {'status': 2})
            elif message.comand == 0:
                if message.msg_type == 0:
                    if receiver == 1:
                        bot.send_message(theme.t_id, 'Собеседник отправио сообщение которое не может быть переслано')
                    else:
                        bot.send_message(theme.u_id, 'Собеседник отправио сообщение которое не может быть переслано')
                elif message.msg_type == 1:
                    creply = message.content['text']['reply']-theme.
                    if receiver == 1:
                        bot.send_message(theme.t_id, message.content['text']['text'], reply_to_message_id=creply)
                    else:
                        bot.send_message(theme.u_id, 'Собеседник отправио сообщение которое не может быть переслано')

                    


def run_scheduler(bot, target, stime):
    '''Запуск планировщика'''
    schedule.every(stime).seconds.do(scheduled_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)