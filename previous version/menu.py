import telebot
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import time
from checks import *

def cancel_menu(bot, message, is_cnacel=0):
    markup_cancel = InlineKeyboardMarkup()
    if is_cnacel:
        yes = InlineKeyboardButton(text='Да', callback_data=f'canceldiolog#1')
        no = InlineKeyboardButton(text='Нет', callback_data=f'canceldiolog#0')
        markup_cancel.add(yes, no)
        bot.send_message(message.chat.id, 'Вы точно хотите завершить диалог? Это действие нельзя будет отменить', reply_markup=markup_cancel)
    else:
        yes = InlineKeyboardButton(text='Завершить', callback_data=f'canceldiolog#1')
        no = InlineKeyboardButton(text='Продолжить', callback_data=f'canceldiolog#0')
        markup_cancel.add(yes, no)
        bot.send_message(message.chat.id, "Для взаимодействия с функционалом бота нужно завершить диалог. Это действие нельзя отменить", reply_markup=markup_cancel)


def menus(message, db):
    markup = InlineKeyboardMarkup(row_width=1)
    find = InlineKeyboardButton(text='Задать вопрос', callback_data=f'find')
    delete = InlineKeyboardButton(text='Удалить последний вопрос', callback_data=f'delete')
    change = InlineKeyboardButton(text='Изменить имя', callback_data=f'change')
    takename = InlineKeyboardButton(text='Получить имя', callback_data=f'takename')
    changeclass = InlineKeyboardButton(text='Изменить класс', callback_data=f'changeclass')
    if is_teacher(message, db):
        activetext = ''
        teachersbusy = db.selectwhere(message.chat.id, 'teacher', 'is_busy')
        busy = int(teachersbusy[0][0])
        if not(busy):
            activetext = 'активным'
        else:
            activetext = 'неактивным'
        is_active = InlineKeyboardButton(text=f'Стать {activetext}', callback_data=f'active')
        if is_admin(message, db):
            back = InlineKeyboardButton(text='Назад', callback_data=f'preadminmenu')
            markup.add(back)
        markup.add(is_active, find, delete)
        markup.add(change, takename, changeclass)
        return markup
    else:
        turn = InlineKeyboardButton(text='Стать преподавателем', callback_data=f'turn')
        if is_admin(message, db):
            back = InlineKeyboardButton(text='Назад', callback_data=f'preadminmenu')
            markup.add(back)
        markup.add(find, delete, turn)
        markup.add(change, takename, changeclass)
        return markup

def preadminmenu():
    admin = InlineKeyboardButton(text='Админ панель', callback_data=f'adminmenu')
    markup_usadm = InlineKeyboardMarkup(row_width=2)
    menu = InlineKeyboardButton(text='Обычный функционал', callback_data=f'menu')
    markup_usadm.add(menu, admin)
    return markup_usadm

def adminmenu():
    markup_admin = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton(text='Назад', callback_data=f'preadminmenu')

    takeuser = InlineKeyboardButton(text='Получить пользователей', callback_data=f'user#take')
    deluser = InlineKeyboardButton(text='Удалить пользователя', callback_data=f'user#del')

    taketeacher = InlineKeyboardButton(text='Получить преподавателей', callback_data=f'teach#take')
    delteacher = InlineKeyboardButton(text='Удалить преподавателя', callback_data=f'teach#del')
    requests = InlineKeyboardButton(text='Заявки в преподаватели', callback_data=f'teach#req')

    activethemes = InlineKeyboardButton(text='Активные темы', callback_data=f'takethemes#1')
    inactivethemes = InlineKeyboardButton(text='Неактивные темы', callback_data=f'takethemes#0')
    searchingthemes = InlineKeyboardButton(text='Ищущие темы', callback_data=f'takethemes#-1')
    
    takesubject = InlineKeyboardButton(text='Получить предметы', callback_data=f'subj#take')
    addsubject = InlineKeyboardButton(text='Добавление предмета', callback_data=f'subj#add')
    delsubject = InlineKeyboardButton(text='Удаление предмета', callback_data=f'subj#del')
    '''
    addschool = InlineKeyboardButton(text='Добавить школу', callback_data=f'school#add')
    delschool = InlineKeyboardButton(text='Удаление школу', callback_data=f'school#del')
    '''

    takeadmin = InlineKeyboardButton(text='Получить админов', callback_data=f'admin#take')
    addadmin = InlineKeyboardButton(text='Добавить админа', callback_data=f'admin#add')
    deladmin = InlineKeyboardButton(text='Удаление админа', callback_data=f'admin#del')

    markup_admin.add(back, takeuser, deluser, taketeacher, delteacher, requests)
    markup_admin.row(activethemes, inactivethemes, searchingthemes)
    markup_admin.add(takesubject)
    markup_admin.row(addsubject, delsubject)
    markup_admin.add(takeadmin)
    markup_admin.row(addadmin, deladmin)
    return markup_admin


def classchoice(message, bot):
    markup_classchoice = InlineKeyboardMarkup(row_width=2)  
    for i in range(5,12):
        clas = InlineKeyboardButton(f'{i}', callback_data=f'new#{message.text}#{i}')
        markup_classchoice.add(clas)
    bot.send_message(message.chat.id, 'Выберите класс', reply_markup=markup_classchoice)