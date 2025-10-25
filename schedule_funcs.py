import schedule, temp_db
from temp_db import *
from db import *
import time, telebot
from datetime import datetime, timedelta
from settings import *

#bot = telebot.TeleBot('admin_token')

#add_message(123, 1, 2, {"text":{"id":10}})
#print(datetime.now(tz=timezone.utc))
#print(select_message(Message.send_time>=(datetime.now() - timedelta(seconds=30)))[0].id)


def scheduled_admin_task():
    scheduled_task(abot, 0)

def scheduled_teacher_task():
    scheduled_task(tbot, 1)

def scheduled_student_task():
    scheduled_task(sbot, 2)

def scheduled_task(bot: telebot.TeleBot, receiver, stime=delay):
    '''
    Получение и отправка сообщений из таблицы

    receiver: 0 - admin, 1 - teacher, 2 - student
    stime: время между проверками(такое же как в планировщике)
    '''
    messages = select_message((Message.send_time>=(datetime.now() - timedelta(seconds=stime))) & (Message.receiver==receiver))
    if not(messages):
        #print('no recent')
        return True
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
                        bot.send_message(theme.t_id, 'Собеседник отправил сообщение которое не может быть переслано')
                    else:
                        bot.send_message(theme.u_id, 'Собеседник отправил сообщение которое не может быть переслано')
                elif message.msg_type == 1:
                    if receiver == 1:
                        creply = message.content['text']['reply'] - theme.u_raito + theme.t_raito
                        bot.send_message(theme.t_id, message.content['text']['text'], reply_to_message_id=creply)
                    else:
                        creply = message.content['text']['reply'] - theme.t_raito + theme.u_raito
                        bot.send_message(theme.u_id, 'Собеседник отправил сообщение которое не может быть переслано')




def run_scheduler(task, stime=delay):
    '''
    Запуск планировщика
    
    receiver: 0 - admin, 1 - teacher, 2 - student
    stime: время между проверками
    '''
    schedule.every(stime).seconds.do(task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def write_message(message, theme_id, sender, receiver, comand=0):
    '''
    Преобразование message из телеграм в строку таблицы temp

    sender: 0 - admin, 1 - teacher, 2 - student
    receiver: 0 - admin, 1 - teacher, 2 - student
    comand: 0 - message, 1 - new theme, 2 - close theme, 3 - turn off
    '''
    content = {}
    if message.text!=None:
        content['text'] = message.text
        msg_type = 1
    elif message.photo!=None:
        pass
    add_message(theme_id, sender, receiver, content, msg_type, comand)