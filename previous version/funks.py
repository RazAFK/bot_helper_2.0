import telebot
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import time
from checks import *
from db import *

def informteachers(u_id, db, bot):
    theme = db.selectthemefindbyid(u_id)[0]
    user = db.selectwhere(u_id, 'user')[0]
    msgtheme = f'Класс: {user[3]}\nТема:\n{theme[3]}'
    t_ids = db.selectwhere(theme[2], 'joinTS', 't_id', 's_id')
    if t_ids!=None:
        for t_id in t_ids:
            teacher = db.selectwhere(t_id[0], 'teacher')[0]
            if int(teacher[3])>=int(user[3]) and int(teacher[5]):
                markup = InlineKeyboardMarkup(row_width=1)
                delete = InlineKeyboardButton(text='Отклонить', callback_data=f'messagedelete')
                accept = InlineKeyboardButton(text='Принять', callback_data=f'accepttheme#{user[0]}')
                markup.add(delete, accept)
                bot.send_message(int(t_id[0]), msgtheme, reply_markup=markup)
    else:
        bot.send_message(u_id, 'Сейчас нет преподавателей готовых принять ваш запрос')

def takeotherid(id, db):
    theme = db.selectactivethemebyid(id)
    if theme!=None:
        theme = theme[0]
        if int(theme[0])==id:
            return int(theme[1])
        else:
            return int(theme[0])
    else:
        return id