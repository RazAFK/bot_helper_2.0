import schedule, temp_db
from temp_db import *
from db import *
import time, telebot
from datetime import datetime, timedelta
from settings import *
from enum import Enum
from telebot.types import InputMediaPhoto, InputMediaDocument

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
    messages = select_message((Message.receiver==receiver) & (Message.send_time>=(datetime.now() - timedelta(seconds=(taker_delay)))) & (Message.parsed == False))
    #print(datetime.now() - timedelta(seconds=delay))
    #print(messages)
    if not(messages):
        return True
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
                        bot.send_message(theme.t_id, message.content[DataKeys.Root.Text])
                    else:
                        #creply = message.content[MP.TEXT]['reply'] - theme.t_raito + theme.u_raito
                        #bot.send_message(theme.u_id, 'Собеседник отправил сообщение которое не может быть переслано')
                        bot.send_message(theme.u_id, message.content[DataKeys.Root.Text])
                elif message.msg_type == 2:
                    # photos = [InputMediaPhoto(message.content[DataKeys.Root.Photo][DataKeys.Photo.photos_ids][0], caption=message.content[DataKeys.Root.Photo][DataKeys.Photo.caption])]
                    # if message.content[DataKeys.Root.Photo][DataKeys.Photo.number_of_photos]>1:
                    #     for photo_id in message.content[DataKeys.Root.Photo][DataKeys.Photo.photos_ids][1:]:
                    #         photos.append(InputMediaPhoto(photo_id))
                    # if receiver == 1:
                    #     # creply = message.content[MP.TEXT]['reply'] - theme.u_raito + theme.t_raito
                    #     # bot.send_message(theme.t_id, message.content[MP.TEXT][MP.TEXT], reply_to_message_id=creply)
                    #     bot.send_media_group(theme.t_id, photos)
                    # else:
                    #     #creply = message.content[MP.TEXT]['reply'] - theme.t_raito + theme.u_raito
                    #     #bot.send_message(theme.u_id, 'Собеседник отправил сообщение которое не может быть переслано')
                    #     bot.send_media_group(theme.u_id, photos)
                    print(*message.content[DataKeys.Root.Photo][DataKeys.Photo.photos_ids], sep='\n')
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



def write_message(message: telebot.types.Message, theme_id, sender, receiver, comand=0):
    '''
    Преобразование message из телеграм в строку таблицы temp

    sender: 0 - admin, 1 - teacher, 2 - student\n
    receiver: 0 - admin, 1 - teacher, 2 - student\n
    comand: 0 - message, 1 - new theme, 2 - close theme, 3 - turn off
    '''
    content = {}
    media_group_id = None
    if message.text!=None:
        content[DataKeys.Root.Text] = message.text
        msg_type = 1
    elif message.photo!=None:
        media_group_id = message.media_group_id
        same_media_group_message = select_message((Message.media_group_id == media_group_id) & (Message.media_group_id != None))
        photo = message.photo[-1]
        if len(same_media_group_message)>0:
            msg = same_media_group_message[0]
            content = msg.content
        else:
            caption = message.caption
            number_of_photos = 0
            content[DataKeys.Root.Photo] = {DataKeys.Photo.caption: caption, DataKeys.Photo.number_of_photos: number_of_photos, DataKeys.Photo.photos_ids: []}
        content[DataKeys.Root.Photo][DataKeys.Photo.photos_ids].append(photo.file_id)
        content[DataKeys.Root.Photo][DataKeys.Photo.number_of_photos] += 1
        msg_type = 2
    else:
        msg_type = 0
    
    if is_media_group_exist(media_group_id):
        update_message((Message.media_group_id == media_group_id), {'content': content})
    else:
        add_message(theme_id, sender, receiver, content, msg_type, media_group_id, comand)