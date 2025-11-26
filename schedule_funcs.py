import schedule, temp_db
from temp_db import *
from db import *
import time, telebot
from datetime import datetime, timedelta
from settings import *
from enum import Enum
from telebot.types import InputMediaPhoto, InputMediaDocument
from message_class import Parsed_message
import os

class DataKeys:
    class Root:
        Text = 'text' #text has only text and nothing else
        Photo = 'photo'
    class Photo:
        caption = 'caption'
        number_of_photos = 'number_of_photos'
        photos_ids = 'photos_ids'


def scheduled_admin_task():
    scheduled_task(abot, 0)

def scheduled_teacher_task():
    scheduled_task(tbot, 1)

def scheduled_student_task():
    scheduled_task(sbot, 2)

def scheduled_task(bot: telebot.TeleBot, receiver):
    '''
    Получение и отправка сообщений из таблицы

    receiver: 0 - admin, 1 - teacher, 2 - student
    '''
    msgs = select_message((Message.receiver==receiver) & (Message.send_time>=(datetime.now() - timedelta(seconds=(taker_delay)))) & (Message.parsed == False))
    #print(datetime.now() - timedelta(seconds=delay))
    #print(messages)
    if not(msgs):
        return True
    
    messages = []
    for msg in msgs:
        message = Parsed_message(msg.id, msg.theme_id, msg.sender, msg.receiver, msg.content_id, msg.caption, msg.send_time, msg.comand, msg.msg_type, msg.parsed, msg.media_group_id)
        if not(message in messages):
            messages.append(message)
        else:
            messages[messages.index(message)].add_id(msg.content_id)
            set_message_as_sended(msg.id)
            

    #print(*messages, sep='\n')


    for message in messages:
        if message.comand != 3:
            theme = select_smth(Theme, (Theme.id == message.theme_id))
            #print(theme)
            if not(theme): continue
            theme = theme[0]
            if message.comand == 1:
                uraito = bot.send_message(theme.u_id, 'Вы начали диалог').message_id()
                rows_update(Theme, Theme.id == message.theme_id, {'u_raito': uraito, 'status': 1})
            elif message.comand == 2:
                if receiver == 1:
                    bot.send_message(theme.t_id, 'Вы завершили диалог')
                    bot.send_message(theme.u_id, 'Собеседник завершил диалог')
                else:
                    bot.send_message(theme.u_id, 'Вы завершили диалог')
                    bot.send_message(theme.t_id, 'Собеседник завершил диалог')
                rows_update(Theme, Theme.id == message.theme_id, {'status': 2})
            elif message.comand == 0:
                if message.msg_type == 0:
                    if receiver == 1:
                        bot.send_message(theme.t_id, 'Собеседник отправил сообщение которое не может быть переслано')
                    else:
                        bot.send_message(theme.u_id, 'Собеседник отправил сообщение которое не может быть переслано')
                elif message.msg_type == 1:
                    if receiver == 1:
                        # creply = message.content[MP.TEXT]['reply'] - theme.u_raito + theme.t_raito
                        # bot.send_message(theme.t_id, message.content[MP.TEXT][MP.TEXT], reply_to_message_id=creply)
                        bot.send_message(theme.t_id, message.content_ids[0])
                    else:
                        #creply = message.content[MP.TEXT]['reply'] - theme.t_raito + theme.u_raito
                        #bot.send_message(theme.u_id, 'Собеседник отправил сообщение которое не может быть переслано')
                        bot.send_message(theme.u_id, message.content_ids[0])
                elif message.msg_type == 2:
                    photos = [InputMediaPhoto(load_file(message.content_ids[0], message.sender), caption=message.caption)]
                    if len(message.content_ids)>1:
                        for photo_id in message.content_ids[1:]:
                            photos.append(InputMediaPhoto(load_file(photo_id, message.sender)))
                    if receiver == 1:
                        # creply = message.content[MP.TEXT]['reply'] - theme.u_raito + theme.t_raito
                        # bot.send_message(theme.t_id, message.content[MP.TEXT][MP.TEXT], reply_to_message_id=creply)
                        bot.send_media_group(theme.t_id, photos)
                    else:
                        #creply = message.content[MP.TEXT]['reply'] - theme.t_raito + theme.u_raito
                        #bot.send_message(theme.u_id, 'Собеседник отправил сообщение которое не может быть переслано')
                        bot.send_media_group(theme.u_id, photos)
                    #print(*message.content_ids, sep='\n')
                elif message.msg_type == 3:
                    pass
        set_message_as_sended(message.id)


def run_scheduler_student():
    '''
    Запуск планировщика ученика
    '''
    schedule.every(delay).seconds.do(scheduled_student_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_scheduler_teacher():
    '''
    Запуск планировщика преподавателя
    '''
    schedule.every(delay).seconds.do(scheduled_teacher_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_scheduler_admin():
    '''
    Запуск планировщика админа
    '''
    schedule.every(delay).seconds.do(scheduled_admin_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


def save_file(file_id, bot: telebot.TeleBot, sender):
    data_sender_path = os.path.join(data_folder, senders[sender])
    os.makedirs(data_sender_path, exist_ok=True)
    file_info = bot.get_file(file_id)
    dwld_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(data_sender_path, file_id)
    try:
        with open(file_path, 'wb') as file:
            file.write(dwld_file)
        log_temp(f'new data_file: {file_id} from {senders[sender]}')
        return True
    except Exception as e:
        log_temp_error(e)
        return False

def load_file(file_id, sender):
    data_sender_path = os.path.join(data_folder, senders[sender])
    file_path = os.path.join(data_sender_path, file_id)
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        log_temp_error(e)
        return False

def write_message(message: telebot.types.Message, theme_id, sender, receiver, bot: telebot.TeleBot, comand=0):
    '''
    Преобразование message из телеграм в строку таблицы temp

    sender: 0 - admin, 1 - teacher, 2 - student\n
    receiver: 0 - admin, 1 - teacher, 2 - student\n
    comand: 0 - message, 1 - new theme, 2 - close theme, 3 - turn off
    '''
    media_group_id = None
    if message.text!=None:
        content_id = message.text
        msg_type = 1
    elif message.photo!=None:
        media_group_id = message.media_group_id
        content_id = message.photo[-1].file_id
        caption = message.caption
        if save_file(content_id, bot, sender):
            msg_type = 2
        else:
            content_id = 'Error while saving file'
            msg_type = 1
    else:
        content_id = 'None type message'
        msg_type = 0
    add_message(theme_id, sender, receiver, content_id, caption, msg_type, media_group_id, comand)