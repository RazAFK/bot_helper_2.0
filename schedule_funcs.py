import schedule, temp_db
from temp_db import *
from db import *
import time, telebot
from datetime import datetime, timedelta

#bot = telebot.TeleBot('admin_token')

#add_message(123, 1, 2, {"text":{"id":10}})
#print(datetime.now(tz=timezone.utc))
#print(select_message(Message.send_time>=(datetime.now() - timedelta(seconds=30)))[0].id)

def scheduled_task(bot: telebot.TeleBot, receiver, stime):
    '''
    Получение и отправка сообщений из таблицы

    receiver: 0 - admin, 1 - teacher, 2 - student
    stime: время между проверками(такое же как в планировщике)
    '''
    messages = select_message((Message.send_time>=(datetime.now() - timedelta(seconds=stime))) & (Message.receiver==receiver))
    print(messages)
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
                    if receiver == 1:
                        creply = message.content['text']['reply'] - theme.u_raito + theme.t_raito
                        bot.send_message(theme.t_id, message.content['text']['text'], reply_to_message_id=creply)
                    else:
                        creply = message.content['text']['reply'] - theme.t_raito + theme.u_raito
                        bot.send_message(theme.u_id, 'Собеседник отправио сообщение которое не может быть переслано')

                    


def run_scheduler(bot, receiver, stime):
    '''
    Запуск планировщика
    
    receiver: 0 - admin, 1 - teacher, 2 - student
    stime: время между проверками
    '''
    schedule.every(stime).seconds.do(scheduled_task(bot, receiver, stime))
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def write_message(message, sender, receiver, comand=0):
    '''
    Преобразование message из телеграм в строку таблицы temp

    sender: 0 - admin, 1 - teacher, 2 - student
    receiver: 0 - admin, 1 - teacher, 2 - student
    comand: 0 - message, 1 - new theme, 2 - close theme, 3 - turn off
    '''
    theme = Theme(select_smth(Theme, Theme.id == message.theme_id)[0])
    theme_id = theme.id
    content = {}
    if message.text!=None:
        content['text'] = message.text
        msg_type = 1
    elif message.photo!=None:
        pass
    add_message(theme_id, sender, receiver, {}, msg_type, comand)