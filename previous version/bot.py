import telebot
import sys
from TOKEN import token
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import time
from db import * 
from checks import *
from menu import *
import datetime
from funks import *

bot = telebot.TeleBot(token)

stopflag = True

db = data_base('users.db', 1)
db.init()

userstatus = db.userstatus
subjecttheme = db.subjecttheme




@bot.message_handler(commands=['stop']) 
def stop(message):
    if message.chat.id == 1634714523:
        bot.send_message(message.chat.id, 'Остановка')
        print('stopping')
        stopflag=False
        bot.stop_bot()
        db.close_connections()
        time.sleep(1)
        exit()
    else:
        bot.send_message(message.chat.id, 'Недостаточно полномочий')

@bot.message_handler(commands=['start'])
def start(message):
    if not(is_in_diolog(message, db)):
        if not(is_in_users(message, db)):
            bot.send_message(message.chat.id, f'{message.chat.username}Добро пожаловать новый пользователь!\nВведите своё НАСТОЯЩЕЕ имя')
            userstatus[message.chat.id] = 'registration'
            reg[message.chat.id] = True
        else:
            bot.send_message(message.chat.id, 'Вы уже зарегестрированы')
    else:
        cancel_menu(bot, message)

@bot.message_handler(commands=['help'])
def start(message):
    if not(is_in_diolog(message, db)):
        if not(is_in_users(message, db)):
            bot.send_message(message.chat.id, 'Я бот созданный для помощи в связи между учениками имеющими какие-то вопросы и учениками, которые готовы ответить на эти вопросы, для задачи вопроса перейди в /menu, а затем выберите задать вопрос')
            userstatus[message.chat.id] = 'registration'
            reg[message.chat.id] = True
        else:
            bot.send_message(message.chat.id, 'Привет! Этот бот нужен для связи с учеником, который готов тебе помочь подтянуть тебе знания. Для этого используй команду /menu и заполни мини-анкету, чтобы найти преподавателя как можно скорее.\n\nВажно!! В анкете указывать НАСТОЯЩЕЕ имя без нецензурной лексики, иначе ваш запрос будет удалён.')
    else:
        cancel_menu(bot, message)
    
@bot.message_handler(commands=['cancel'])
def cancel(message):
    if not(is_in_users(message, db)):
            bot.send_message(message.chat.id, 'Добро пожаловать новый пользователь!\nВведите своё имя')
            userstatus[message.chat.id] = 'registration'
            reg[message.chat.id] = True
    else:
        if is_in_diolog(message, db):
            cancel_menu(bot, message, 1)
        else:
            bot.send_message(message.chat.id, 'Вы не находитесь в диалоге')

@bot.message_handler(commands=['menu'])
def menu(message):
    if not(is_in_users(message, db)):
        bot.send_message(message.chat.id, 'Добро пожаловать новый пользователь!\nВведите своё имя')
        userstatus[message.chat.id] = 'registration'
        reg[message.chat.id] = True
    else:
        if not(is_in_diolog(message, db)):
            if is_admin(message, db):
                markup = preadminmenu()
            else:
                markup = menus(message, db)
            bot.send_message(message.chat.id, 'Выберите меню', reply_markup=markup)
        else:
            cancel_menu(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    data = call.data.split('#')
    if data[0]=='new':
        db.insertUser(call.message.chat.id, str(call.message.chat.username), data[1], int(data[2]))
        db.insertEnterTime(call.message.chat.id)
        if is_teacher(call.message, db):
            db.update(call.message.chat.id, 'name', data[1], 'teacher')
            db.update(call.message.chat.id, 'username', call.message.chat.username, 'teacher')
        bot.edit_message_text('Готово, вызовите /menu для активации меню функционала бота', call.message.chat.id, call.message.id)
        userstatus.pop(call.message.chat.id, None)
    elif data[0]=='canceldiolog':
        if int(data[1]):
            other_id = takeotherid(call.message.chat.id, db)
            db.updatethemeend(call.message.chat.id)
            db.updateThemesDT(call.message.chat.id, 'end')
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(other_id, 'Диалог завершён')
            bot.send_message(call.message.chat.id, 'Диалог завершён')
            userstatus.pop(call.message.chat.id, None)
            userstatus.pop(other_id, None)
        else:
            bot.delete_message(call.message.chat.id, call.message.id)
    elif data[0]=='messagedelete':
                bot.delete_message(call.message.chat.id, call.message.id)
    if not(is_in_users(call.message, db)):
        bot.send_message(call.message.chat.id, 'Добро пожаловать новый пользователь!\nВведите своё имя')
        userstatus[call.message.chat.id] = 'registration'
        reg[call.message.chat.id] = True
    else:
        if not(is_in_diolog(call.message, db)):  
            adminaction = InlineKeyboardMarkup(row_width=1)
            useraction = InlineKeyboardMarkup(row_width=1)
            admin = InlineKeyboardButton(text='Назад', callback_data=f'adminmenu')
            user = InlineKeyboardButton(text='Назад', callback_data=f'menu')
            adminaction.add(admin)
            useraction.add(user)
            if data[0]=='menu':
                markup = menus(call.message, db)
                bot.edit_message_text('Выберите действие', call.message.chat.id, call.message.id, reply_markup=markup)
            elif data[0]=='find':
                havetheme = db.selectthemefindbyid(call.message.chat.id)
                if havetheme==None:
                    if len(data)==1:
                        userclass = int(db.selectwhere(call.message.chat.id, 'user', 'class')[0][0])
                        subjects = db.selectall('subject')
                        for subject in subjects:
                            if userclass<7:
                                if subject[1]=='Математика' or subject[1]=='Русский язык':
                                    useraction.add(InlineKeyboardButton(text=f'{subject[1]}', callback_data=f'find#{subject[0]}'))
                            else:
                                if subject[1]!='Математика':
                                    useraction.add(InlineKeyboardButton(text=f'{subject[1]}', callback_data=f'find#{subject[0]}'))
                            
                        bot.edit_message_text('Выберите предмет к которому относится ваша тема', call.message.chat.id, call.message.id, reply_markup=useraction)
                    else:
                        subjecttheme[call.message.chat.id] = [data[1], call.message.id]
                        bot.edit_message_text('Введите вопрос или тему', call.message.chat.id, call.message.id)
                        userstatus[call.message.chat.id] = 'themeenter'
                        reg[call.message.chat.id] = True
                else:
                    delete = InlineKeyboardButton(text='Удалить', callback_data=f'delete')
                    useraction.add(delete)
                    bot.edit_message_text('У вас уже есть заданный вопрос, чтобы задать новый нужно удалить старый', call.message.chat.id, call.message.id, reply_markup=useraction)
            elif data[0]=='delete':
                db.deletethemefind(call.message.chat.id)
                bot.edit_message_text('Ваш вопрос удалён теперь вы можете задать новый', call.message.chat.id, call.message.id, reply_markup=useraction)
            elif data[0]=='change':
                name = db.selectwhere(call.message.chat.id, 'user', 'name')
                name = name[0][0] if name!=None else 'Вас не существует'
                bot.send_message(call.message.chat.id, f'Ваше текущее имя: {name}\nВведите своё имя')
                userstatus[call.message.chat.id] = 'namechange'
                reg[call.message.chat.id] = True
            elif data[0]=='changeclass':
                if len(data)==1:
                    clas = db.selectwhere(call.message.chat.id, 'user', 'class')
                    clas = clas[0][0] if clas!=None else 'У вас ещё нет класса'
                    for i in range(5,12):
                        cl = InlineKeyboardButton(text=f'{i}', callback_data=f'changeclass#{i}')
                        useraction.add(cl)
                    bot.edit_message_text(f'Ваше текущее имя: {clas}\nВыберите свой класс обучения', call.message.chat.id, call.message.id, reply_markup=useraction)
                else:
                    db.update(call.message.chat.id, 'class', data[1], 'user')
                    db.update(call.message.chat.id, 'class', data[1], 'teacher')
                    bot.edit_message_text('Готово', call.message.chat.id, call.message.id, reply_markup=useraction)
            elif data[0]=='takename':
                name = db.selectwhere(call.message.chat.id, 'user', 'name')
                name = name[0][0] if name!=None else 'Вас не существует'
                bot.send_message(call.message.chat.id, f'Ваше текущее имя: {name}')
            elif data[0]=='active' and is_teacher(call.message, db):
                teachersbusy = db.selectwhere(call.message.chat.id, 'teacher', 'is_busy')
                busy = int(teachersbusy[0][0])
                if busy:
                    db.update(call.message.chat.id, 'is_busy', 0, 'teacher')
                    bot.edit_message_text(f'Теперь вы неактивны', call.message.chat.id, call.message.id, reply_markup=useraction)
                else:
                    db.update(call.message.chat.id, 'is_busy', 1, 'teacher')
                    bot.edit_message_text(f'Теперь вы активны', call.message.chat.id, call.message.id, reply_markup=useraction)           
            elif data[0]=='accepttheme':
                theme = db.selectthemefindbyid(data[1])[0]
                if theme[0]==0:
                    msgtext = f'Тема этого диалога:\n{theme[3]}\n'
                    db.updatefindingTheme(data[1], call.message.chat.id)
                    db.updateThemesDT(data[1], 'answer', call.message.chat.id)
                    bot.edit_message_text(f'{msgtext}Дождитесь уточняющих вопросов или напишите ответ в этом чате', call.message.chat.id, call.message.id)
                    bot.send_message(int(data[1]), f'{msgtext}Дождитесь пока собеседник ответит или отправте уточняющие вопросы в этот чат')
                else:
                    bot.edit_message_text('На эту тему кто-то уже ответил', call.message.chat.id, call.message.id   )
            elif data[0]=='turn':
                if is_teacher(call.message, db):
                    bot.send_message(call.message.chat.id, 'Ваша заявка уже есть в системе, дождитесь её обработки')
                else:
                    if len(data)==3 and data[1]=='add':
                        try:
                            user = db.selectwhere(call.message.chat.id, 'user')[0]
                            s_ids = data[2].split('$')
                            for s_id in s_ids:
                                db.insertJoinTS(call.message.chat.id, int(s_id))
                            db.insertTeacher(user[0], user[1], user[2], user[3], user[4])
                            bot.edit_message_text(f'Ваша заявка будет рассмотрена в ближайшее время', call.message.chat.id, call.message.id, reply_markup=useraction)
                        except:
                            bot.edit_message_text(f'Во время подачи заявки вы были удалены администратором, пожалуйста попробуйте снова', call.message.chat.id, call.message.id, reply_markup=useraction)
                    else:
                        if len(data)!=1:
                            s_ids = data[1].split('$')
                            msgsubjects=''
                            for s_id in s_ids:
                                subject = db.selectwhere(s_id, 'subject', 'subject', 's_id')
                                msgsubjects+=subject[0][0]+', '
                            end = InlineKeyboardButton(text=f'Закончить выбор предметов', callback_data=f'turn#add#{data[1]}')
                            useraction.add(end)
                            subjects = db.selectall('subject')
                            for subject in subjects:
                                if subject[1] not in msgsubjects:
                                    markupsubject = InlineKeyboardButton(text=f'{subject[1]}', callback_data=f'turn#{data[1]+"$"+str(subject[0])}')
                                    useraction.add(markupsubject)
                            bot.edit_message_text(f'Текущие предметы:\n{msgsubjects[:-2]}', call.message.chat.id, call.message.id, reply_markup=useraction)
                        else:
                            subjects = db.selectall('subject')
                            for subject in subjects:
                                markupsubject = InlineKeyboardButton(text=f'{subject[1]}', callback_data=f'turn#{subject[0]}')
                                useraction.add(markupsubject)
                            bot.edit_message_text('Выберите предмет', call.message.chat.id, call.message.id, reply_markup=useraction)
            elif data[0]=='preadminmenu':
                markup = preadminmenu()
                bot.edit_message_text('Выберите меню', call.message.chat.id, call.message.id, reply_markup=markup)
            elif data[0]=='adminmenu' and is_admin(call.message, db):
                markup = adminmenu()
                bot.edit_message_text('Выберите действие', call.message.chat.id, call.message.id, reply_markup=markup)
            elif data[0]=='user' and is_admin(call.message, db):
                if len(data)>2:
                    if int(data[3]):
                        db.delete(data[2], 'user')
                        bot.send_message(data[2], 'Ваш аккаунт был удалён из-за неподобающего имени пользователя')
                    else:
                        db.update(data[2], 'warn', 1, 'user')
                        bot.send_message(data[2], 'Измените имя пользователя, или ваш аккаунт будет удалён')
                users=db.selectall('user')
                if len(users)>0 if users!=None else users!=None:
                    msgtext = f'id @username name class warn\n' if data[1]=='take' else '@username warn'
                    if data[1]=='take':
                        for user in users:
                            msgtext+=f'{user[0]} @{user[1]} {user[2]} {user[3]} {user[5]}\n'
                    elif data[1]=='del':
                        for user in users:
                            us = InlineKeyboardButton(text=f'@{user[1]} {user[5]}\n', callback_data=f'confirm#user#{user[0]}')
                            adminaction.add(us)
                    bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=adminaction)
                else:
                    bot.edit_message_text('Список пуст', call.message.chat.id, call.message.id, reply_markup=adminaction)
            elif data[0]=='teach' and is_admin(call.message, db):
                if data[1]=='req':
                    if len(data)>2:
                        if int(data[3]):
                            db.update(data[2], 'is_confirmed', 1, 'teacher')
                            bot.send_message(data[2], 'Ваша заявка принята')
                        else:
                            db.delete(data[2], 'teacher')
                            db.delete(data[2], 'joinTS')
                            bot.send_message(data[2], 'Ваша заявка откланена')
                    teachers = db.selectteachersconfirmed(0)
                    if len(teachers)>0 if teachers!=None else teachers!=None:
                        msgtext='id @username class subjects'
                        for teacher in teachers:
                            tch = InlineKeyboardButton(text=f'{teacher[0]} {teacher[1]}  {teacher[3]}', callback_data=f'confirm#req#{teacher[0]}#{teacher[2]}#{teacher[1]}')
                            adminaction.add(tch)
                        bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=adminaction)
                    else:
                        bot.edit_message_text('Заявки отсутствуют', call.message.chat.id, call.message.id, reply_markup=adminaction)
                else:
                    if len(data)>2:
                        db.delete(data[2], 'teacher')
                        db.delete(data[2], 'joinTS')
                        bot.send_message(data[2], 'Вы больше не преподаватель')
                    teachers = db.selectteachersconfirmed(1)
                    if len(teachers)>0 if teachers!=None else teachers!=None:
                        msgtext=f'id username name class subjects\n' if data[1]=='take' else '@username class'
                        if data[1]=='take':
                            for teacher in teachers:
                                msgsubjects = ''
                                subjects = db.selectteacherssubjects(teacher[0])
                                for subject in subjects:
                                    msgsubjects+=subject[0]+', '
                                msgtext +=f'{teacher[0]} @{teacher[1]} {teacher[2]} {teacher[3]}\n{msgsubjects[:-2]}\n'
                        elif data[1]=='del':
                            for teacher in teachers:
                                tch = InlineKeyboardButton(text=f'@{teacher[1]} {teacher[3]}', callback_data=f'confirm#teach#{teacher[0]}#{teacher[2]}#{teacher[1]}')
                                adminaction.add(tch)
                        bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=adminaction)
                    else:
                        bot.edit_message_text('Список пуст', call.message.chat.id, call.message.id, reply_markup=adminaction)
            elif data[0]=='takethemes' and is_admin(call.message, db): 
                msgtext = 'Учитель Ученик Предмет\nТема\n'
                themes = db.selectthemeall(int(data[1]))
                if len(themes)>0 if themes!=None else themes!=None:
                    for theme in themes:
                        teacher = db.selectwhere(theme[0], 'teacher', 'username')
                        teacher = '@' + teacher[0][0] if teacher!=None else 'Пока не найден'
                        user = db.selectwhere(theme[1], 'user', 'username')[0][0]
                        subject = db.selectwhere(theme[2], 'subject', 'subject', 's_id')[0][0]
                        msgtext+=f'* {teacher} @{user} {subject}\n{theme[3]}\nДата и время отправки/ответа/окончания вопроса:\n{theme[5]} / {theme[6]} / {theme[7]}\n'
                else:
                    msgtext = 'Список пуст'
                bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=adminaction)
            elif data[0]=='subj' and is_admin(call.message, db):
                if data[1]!='add':
                    if len(data)>2:
                        db.delete(data[2], 'subject')
                    subjects=db.selectall('subject')
                    if len(subjects)>0 if subjects!=None else subjects!=None:
                        msgtext = 'id subject\n'
                        if data[1]=='take':
                            for subject in subjects:
                                msgtext+=f'{subject[0]} {subject[1]}\n'
                        elif data[1]=='del':
                            for subject in subjects:
                                us = InlineKeyboardButton(text=f'{subject[0]} {subject[1]}\n', callback_data=f'confirm#subj#{subject[0]}#{subject[1]}')
                                adminaction.add(us)
                        bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=adminaction)
                    else:
                        bot.edit_message_text('Список пуст', call.message.chat.id, call.message.id, reply_markup=adminaction)
                else:
                    bot.send_message(call.message.chat.id, 'Введите название предмета')
                    userstatus[call.message.chat.id] = 'addingsubject'
                    reg[call.message.chat.id] = True
            elif data[0]=='admin' and is_admin(call.message, db):
                if data[1]!='add':
                    if len(data)>2:
                        if int(data[2])!=1634714523:
                            db.delete(data[2], 'admin')
                            if int(data[2])!=0: bot.send_message(data[2], 'Вы больше не администратор')
                        else:
                            bot.answer_callback_query(callback_query_id=call.id, text='Нельзя', show_alert=False)
                    admins=db.selectall('admin')
                    if len(admins)>0 if admins!=None else admins!=None:
                        msgtext = 'id username\n'
                        if data[1]=='take':
                            for admin in admins:
                                user= db.selectwhere(admin[0], 'user', 'username')
                                username = user[0][0] if user!=None else 'Пользователь удалён'
                                msgtext+=f'{admin[0]} @{username}\n'
                        elif data[1]=='del':
                            for admin in admins:
                                user= db.selectwhere(admin[0], 'user', 'username')
                                username = user[0][0] if user!=None else 'Пользователь удалён'
                                us = InlineKeyboardButton(text=f'{admin[0]} @{username}', callback_data=f'confirm#admin#{admin[0]}#{username}')
                                adminaction.add(us)
                        bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=adminaction)
                    else:
                        bot.edit_message_text('Список пуст', call.message.chat.id, call.message.id, reply_markup=adminaction)
                else:
                    bot.send_message(call.message.chat.id, 'Введите id или username(начиная с @) админа')
                    userstatus[call.message.chat.id] = 'addingadmin'
                    reg[call.message.chat.id] = True
            elif data[0]=='confirm' and is_admin(call.message, db):
                action = InlineKeyboardMarkup(row_width=2)
                back = InlineKeyboardButton(text='Назад', callback_data=f'{data[1]}#del')
                if data[1]=='user':
                    user = db.selectwhere(data[2], 'user')
                    if user==None:
                        action.add(back)
                        bot.edit_message_text(f'Удаление отменено, пользователь отсутствует', call.message.chat.id, call.message.id, reply_markup=action)
                    else:
                        user = user[0]
                        confirm = InlineKeyboardButton(text='Подтвердить', callback_data=f'user#del#{data[2]}#{user[5]}')
                        action.row(back, confirm)
                        bot.edit_message_text(f'Удаление @{user[1]} {user[2]} {user[3]} {user[5]}', call.message.chat.id, call.message.id, reply_markup=action)
                elif data[1]=='teach':
                    confirm = InlineKeyboardButton(text='Подтвердить', callback_data=f'teach#del#{data[2]}')
                    action.row(back, confirm)
                    msgsubjects = ''
                    subjects = db.selectteacherssubjects(data[2])
                    for subject in subjects:
                        msgsubjects+=subject[0]+', '
                    bot.edit_message_text(f'Удаление {data[2]} @{data[4]} {data[3]}\n{msgsubjects[:-2]}', call.message.chat.id, call.message.id, reply_markup=action)
                elif data[1]=='subj':
                    confirm = InlineKeyboardButton(text='Подтвердить', callback_data=f'subj#del#{data[2]}')
                    action.row(back, confirm)
                    bot.edit_message_text(f'Удаление {data[2]} {data[3]}', call.message.chat.id, call.message.id, reply_markup=action)
                elif data[1]=='admin':
                    confirm = InlineKeyboardButton(text='Подтвердить', callback_data=f'admin#del#{data[2]}')
                    action.row(back, confirm)
                    bot.edit_message_text(f'Удаление {data[2]} @{data[3]}\n', call.message.chat.id, call.message.id, reply_markup=action)
                elif data[1]=='req':
                    back = InlineKeyboardButton(text='Назад', callback_data=f'teach#req')
                    confirm = InlineKeyboardButton(text='Подтвердить', callback_data=f'teach#req#{data[2]}#1')
                    decline = InlineKeyboardButton(text='Отклонить', callback_data=f'teach#req#{data[2]}#0')
                    action.add(back)
                    action.row(decline, confirm)
                    msgsubjects = ''
                    subjects = db.selectteacherssubjects(data[2])
                    for subject in subjects:
                        msgsubjects+=subject[0]+', '
                    bot.edit_message_text(f'Подтверждение заявки {data[2]} @{data[4]} {data[3]}\n{msgsubjects[:-2]}', call.message.chat.id, call.message.id, reply_markup=action)
        else:
            cancel_menu(bot, call.message)
        
            


reg = db.is_writing
@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if not(is_in_diolog(message, db)):
        if (message.chat.id in userstatus) and userstatus[message.chat.id]=='registration' and reg[message.chat.id]:
            classchoice(message, bot)
            userstatus.pop(message.chat.id, None)
            reg[message.chat.id]=False
        elif (message.chat.id in userstatus) and userstatus[message.chat.id]=='addingsubject' and reg[message.chat.id]:
            db.insertSubject(message.text)
            userstatus.pop(message.chat.id, None)
            reg[message.chat.id]=False
        elif (message.chat.id in userstatus) and userstatus[message.chat.id]=='namechange' and reg[message.chat.id]:
            
            db.update(message.chat.id, 'name', message.text, 'user')
            db.update(message.chat.id, 'warn', 0, 'user')
            if is_teacher(message, db):
                db.update(message.chat.id, 'name', message.text, 'teacher')
                db.update(message.chat.id, 'username', message.chat.username, 'teacher')
            bot.send_message(message.chat.id, 'Готово')
            userstatus.pop(message.chat.id, None)
            reg[message.chat.id]=False
        elif (message.chat.id in userstatus) and userstatus[message.chat.id]=='addingadmin' and reg[message.chat.id]:
            id = message.text
            if message.text[0]=='@':
                user = db.selectwhere(message.text[1:], 'user', 'id', 'username')
                id = user[0][0] if user!=None else 0
            db.insertAdmin(id)
            if int(id)!=0: bot.send_message(int(id), 'Вы назначены администратором')
            userstatus.pop(message.chat.id, None)
            reg[message.chat.id]=False
        elif (message.chat.id in userstatus) and userstatus[message.chat.id]=='themeenter' and reg[message.chat.id]:
            useraction = InlineKeyboardMarkup(row_width=1)
            user = InlineKeyboardButton(text='Назад', callback_data=f'menu')
            useraction.add(user)
            theme=message.text
            db.insertTheme(message.chat.id, subjecttheme[message.chat.id][0], theme=theme)
            db.updateThemesDT(message.chat.id, 'start')
            informteachers(message.chat.id, db, bot)
            bot.edit_message_text('Готово', message.chat.id, subjecttheme[message.chat.id][1], reply_markup=useraction)
            userstatus.pop(message.chat.id, None)
            reg[message.chat.id]=False
    else:
        id = message.chat.id
        id = takeotherid(id, db)
        bot.send_message(id, message.text)


if __name__ == "__main__":
    #while stopflag:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
    #    db.close_connections()
