import telebot
import sys
from TOKEN import token
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import time
from old.database import * 

bot = telebot.TeleBot(token)

udb = user_database('users.db', 1)
tdb = teachers_database('users.db', 1)
sdb = subjects_database('users.db', 1)
tmdb = themes_database('users.db', 1)
jdb = joinedts_database('users.db', 1)
schdb = schools_database('users.db', 1)
adb = admins_database('users.db', 1)

udb.init()
tdb.init()
sdb.init()
tmdb.init()
jdb.init()
schdb.init()
adb.init()


def is_in_themes(id):
    us = tmdb.select(id)
    us = us[0][0] if us!=None else 0
    tch = tmdb.select(id)
    tch = tch[0][0] if tch!=None else 0
    return us or tch

def is_in_users(id):
    there = udb.selectwhere(id)
    if there==None:
        return False
    return len(there)>0

def is_in_teachers(id):
    there = tdb.selectwhere(id)
    if there==None:
        return False
    return len(there)>0

def is_admin(id):
    there = adb.selectwhere(id)
    if there == None:
        return False
    return len(there)>0

def teachmenu(message, admin=0):
    if admin:
        markup_tch = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton(text='Назад', callback_data=f'back')
        is_active = InlineKeyboardButton(text='Активен/Неактивен', callback_data=f'active')
        find = InlineKeyboardButton(text='Задать вопрос', callback_data=f'find')
        markup_tch.add(back)
        markup_tch.row(is_active, find)
        return markup_tch
    else:
        markup_tch = InlineKeyboardMarkup(row_width=1)
        is_active = InlineKeyboardButton(text='Активен/Неактивен', callback_data=f'active')
        find = InlineKeyboardButton(text='Задать вопрос', callback_data=f'find')
        markup_tch.row(is_active, find)
        return markup_tch

def usermenu(message, admin=0):
    if admin:
        markup_us = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton(text='Назад', callback_data=f'back')
        find = InlineKeyboardButton(text='Задать вопрос', callback_data=f'find')
        turn = InlineKeyboardButton(text='Стать преподавателем', callback_data=f'turn')
        markup_us.add(back)
        markup_us.row(find, turn)
        return markup_us
    else:
        markup_us = InlineKeyboardMarkup(row_width=1)
        find = InlineKeyboardButton(text='Задать вопрос', callback_data=f'find')
        turn = InlineKeyboardButton(text='Стать преподавателем', callback_data=f'turn')
        markup_us.add(find, turn)
        return markup_us

def preadminmenu(message):
    admin = InlineKeyboardButton(text='Админ панель', callback_data=f'adminmenu')
    if is_in_teachers(message.chat.id):
        markup_tchadm = InlineKeyboardMarkup(row_width=2)
        teacher = InlineKeyboardButton(text='Обычный функционал', callback_data=f'teachermenu')
        markup_tchadm.add(teacher, admin)
        return markup_tchadm
    else:
        markup_usadm = InlineKeyboardMarkup(row_width=2)
        user = InlineKeyboardButton(text='Обычный функционал', callback_data=f'usermenu')
        markup_usadm.add(user, admin)
        return markup_usadm

def adminmenu(message):
    markup_admin = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton(text='Назад', callback_data=f'back')
    takeuser = InlineKeyboardButton(text='Получить пользователей', callback_data=f'takeusers')
    deluser = InlineKeyboardButton(text='Удалить пользователя', callback_data=f'deluser')
    taketeacher = InlineKeyboardButton(text='Получить преподавателей', callback_data=f'taketeach')
    delteacher = InlineKeyboardButton(text='Удалить преподавателя', callback_data=f'delteach')
    requests = InlineKeyboardButton(text='Заявки в преподаватели', callback_data=f'takereq')
    activethemes = InlineKeyboardButton(text='Активные темы', callback_data=f'takethemes#1')
    inactivethemes = InlineKeyboardButton(text='Неактивные темы', callback_data=f'takethemes#0')
    addadmin = InlineKeyboardButton(text='Добавить админа', callback_data=f'addadmin')
    deladmin = InlineKeyboardButton(text='Удаление админа', callback_data=f'deladmin')
    markup_admin.add(back, takeuser, deluser, taketeacher, delteacher, requests)
    markup_admin.row(activethemes, inactivethemes)
    markup_admin.add(addadmin, deladmin)
    return markup_admin

@bot.message_handler(commands=['start'])
def start(message):
    if is_in_themes(message.chat.id):
        bot.send_message(message.chat.id, "Для взаимодействия с функционалом бота завершите диалог(вернуться к нему позже будет нельзя)")
    else:
        if not(is_in_users(message.chat.id)):
            bot.send_message(message.chat.id, 'Введите имя')
        else:
            bot.send_message(message.chat.id, "Вы уже зарегестрированы")

@bot.message_handler(commands=['cancel'])
def cancel(message):
    if is_in_themes(message.chat.id):
        markup_cancel = InlineKeyboardMarkup()
        yes = InlineKeyboardButton(text='Да', callback_data=f'canceldiolog#1')
        no = InlineKeyboardButton(text='Нет', callback_data=f'canceldiolog#0')
        markup_cancel.add(yes, no)
        bot.send_message(message.chat.id, 'Вы точно хотите завершить диалог? Это действие нельзя будет отменить', reply_markup=markup_cancel)
    else:
        bot.send_message(message.chat.id, 'Вы не находитесь в диалоге')
        if not(is_in_users(message.chat.id)):
            bot.send_message(message.chat.id, 'Введите имя')
        else:
            bot.send_message(message.chat.id, "Вы уже зарегестрированы")
@bot.message_handler(commands=['menu'])
def menu(message):
    if is_in_themes(message.chat.id):
        bot.send_message(message.chat.id, "Для взаимодействия с функционалом бота завершите диалог(вернуться к нему позже будет нельзя)")
    else:
        if not(is_in_users(message.chat.id)):
            bot.send_message(message.chat.id, 'Введите имя')
        else:
            if is_admin(message.chat.id):
                markup_preadm = preadminmenu(message)
                bot.send_message(message.chat.id, 'Выберите меню', reply_markup=markup_preadm)
            else:
                if is_in_teachers(message.chat.id):
                    markup_teach = teachmenu(message)
                    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup_teach)
                else:
                    markup_user = usermenu(message)
                    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup_user)

userstate={}
themes = {}
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    data = call.data.split('#')
    if data[0] == 'new':
        udb.insert(call.message.chat.id, call.message.chat.username, data[2], int(data[1]))
        bot.edit_message_text('Готово', call.message.chat.id, call.message.id)
        userstate.pop(call.message.chat.id, None)
    elif data[0] == 'canceldiolog':
        if int(data[1]):
            id = tmdb.select(call.message.chat.id)[0]
            print(tmdb.update(call.message.chat.id))
            bot.send_message(id[0], 'Диалог завершён')
            bot.send_message(id[1], 'Диалог завершён')
        bot.delete_message(call.message.chat.id, call.message.id)
    elif data[0]=='usermenu':
        markup_user = usermenu(call.message, 1)
        bot.edit_message_text('Выберите действие', call.message.chat.id, call.message.id, reply_markup=markup_user)
    elif data[0]=='teachermenu':
        markup_teach = teachmenu(call.message, 1)
        bot.edit_message_text('Выберите действие', call.message.chat.id, call.message.id, reply_markup=markup_teach)
    elif data[0]=='find':
        havetheme = udb.selectwhere(call.message.chat.id, 'havetheme')
        print(havetheme)
        if not(int(havetheme)):
            userstate[call.message.chat.id] = 'theme'
            bot.edit_message_text('Напишите тему или вопрос', call.message.chat.id, call.message.id)
        else:
            pass

    elif data[0]=='back':
        markup_admin = preadminmenu(call.message)
        bot.edit_message_text('Выберите меню', call.message.chat.id, call.message.id, reply_markup=markup_admin)
    elif data[0]=='adminmenu':
        markup_admin = adminmenu(call.message)
        bot.edit_message_text('Выберите действие', call.message.chat.id, call.message.id, reply_markup=markup_admin)
    elif data[0]=='takeusers':
        msgtext = 'id username name class warn\n'
        users = udb.selectall()
        markup_uback = InlineKeyboardMarkup(row_width=1)
        markup_uback.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
        for item in users:
            msgtext+=f'{item[0]} {item[1]} {item[2]} {item[3]} {item[5]}\n'
        bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=markup_uback)
    elif data[0]=='taketeach':
        msgtext = 'id username name class subjects is_busy\n'
        teachers = tdb.allteachers(1)
        markup_tback = InlineKeyboardMarkup(row_width=1)
        markup_tback.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
        if teachers!=None:
            for item in teachers:
                subjects = jdb.selectbytid(call.message.chat.id)
                subj = ''
                for sitem in subjects:
                    subj+=sitem[0]+', '
                msgtext+=f'{item[0]} {item[1]} {item[2]} {subj[:-2]} {item[5]}\n'
            bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=markup_tback)
        else:
            bot.edit_message_text('Список пуст', call.message.chat.id, call.message.id, reply_markup=markup_tback)
    
    elif data[0]=='deluser':
        users = udb.selectall()
        markup_users = InlineKeyboardMarkup(row_width=1)
        markup_users.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
        for item in users:
            user = InlineKeyboardButton(text=f'{item[0]} {item[2]} {item[5]}', callback_data=f'confirmdeluser#{item[0]}#{item[2]}')
            markup_users.add(user)
        if len(data)==1:
            bot.edit_message_text('id name warn', call.message.chat.id, call.message.id, reply_markup=markup_users)
        else:
            warn = udb.selectwhere(str(data[1]))[0][5]
            if int(warn):
                udb.delete(str(data[1]))
                users = udb.selectall()
                markup_users = InlineKeyboardMarkup(row_width=1)
                markup_users.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
                for item in users:
                    user = InlineKeyboardButton(text=f'{item[0]} {item[2]} {item[5]}', callback_data=f'confirmdeluser#{item[0]}#{item[2]}')
                    markup_users.add(user)
            else:
                udb.update(str(data[1]), 'warn', 1)
                bot.send_message(str(data[1]), 'Измените имя или ваш аккаунт будет удалён')
            bot.edit_message_text('id name warn', call.message.chat.id, call.message.id, reply_markup=markup_users)
    elif data[0]=='confirmdeluser':
        markup_confirm = InlineKeyboardMarkup(row_width=2)
        yes = InlineKeyboardButton(text='Подтвердить', callback_data=f'deluser#{data[1]}')
        no = InlineKeyboardButton(text='Назад', callback_data=f'deluser')
        markup_confirm.add(yes, no)
        bot.edit_message_text(f'Удаление пользователя\nid:{data[1]} name:{data[2]}', call.message.chat.id, call.message.id, reply_markup=markup_confirm)

    elif data[0]=='delteach':
        teachers = tdb.selectall()
        markup_teachers = InlineKeyboardMarkup(row_width=1)
        markup_dback = InlineKeyboardMarkup(row_width=1)
        markup_dback.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
        markup_teachers.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
        if teachers == None:
            bot.edit_message_text('Список пуст', call.message.chat.id, call.message.id, reply_markup=markup_dback)
        else:
            for item in teachers:
                teacher = InlineKeyboardButton(text=f'{item[0]} {item[2]}', callback_data=f'confirmdelteach#{item[0]}#{item[2]}')
                markup_teachers.add(teacher)
            if len(data)==1:
                bot.edit_message_text('id name', call.message.chat.id, call.message.id, reply_markup=markup_teachers)
            else:
                if int(data[1]):
                    #warn = udb.selectwhere(str(data[2]))[0][5]
                    #if bool(warn):
                    tdb.delete(str(data[2]))
                    teachers = tdb.selectall()
                    markup_teachers = InlineKeyboardMarkup(row_width=1)
                    if teachers == None:
                        bot.edit_message_text('Список пуст', call.message.chat.id, call.message.id, reply_markup=markup_dback)
                    else:
                        for item in teachers:
                            teacher = InlineKeyboardButton(text=f'{item[0]} {item[2]}', callback_data=f'confirmdelteach#{item[0]}#{item[2]}')
                            markup_teachers.add(teacher)
                        #else:
                        #    udb.update(str(data[2]), 'warn', 1)
                        #    bot.send_message(str(data[2]), 'Измените имя или ваш аккаунт будет удалён')
                        bot.edit_message_text('id name', call.message.chat.id, call.message.id, reply_markup=markup_teachers)
    elif data[0]=='confirmdelteach':
        markup_confirm = InlineKeyboardMarkup(row_width=2)
        yes = InlineKeyboardButton(text='Подтвердить', callback_data=f'delteach#1#{data[1]}')
        no = InlineKeyboardButton(text='Назад', callback_data=f'delteach#0#{data[1]}')
        markup_confirm.add(yes, no)
        bot.edit_message_text(f'Удаление учителя\nid:{data[1]} name:{data[2]}', call.message.chat.id, call.message.id, reply_markup=markup_confirm)

    elif data[0]=='takereq':
        if len(data)==1:
            requests = tdb.allteachers(0)
            markup_rback = InlineKeyboardMarkup(row_width=1)
            markup_rback.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
            if requests!=None:
                msgtext = 'id username name class subjecsts\n'
                
                for item in requests:
                    subjects = jdb.selectbytid(call.message.chat.id)
                    subj = ''
                    for sitem in subjects:
                        subj+=sitem[0]+', '
                    msgtext+=f'{item[0]} {item[1]} {item[2]} {item[3]} {subj[:-2]}\n'
                    markup_rback.add(InlineKeyboardButton(text=f'{item[0]} {item[1]}', callback_data=f'confirmreq#{item[0]}#{item[2]}'))
                bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=markup_rback)
            else:
                bot.edit_message_text('Заявки отсутствуют', call.message.chat.id, call.message.id, reply_markup=markup_rback)
        else:
            if int(data[1]):
                tdb.update(data[2], 'is_confirmed', 1)
            else:
                tdb.delete(data[2])
                bot.send_message(data[2], 'Ваша заявка отклонена')
            requests = tdb.allteachers(0)
            markup_rback = InlineKeyboardMarkup(row_width=1)
            markup_rback.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
            if requests!=None:
                msgtext = 'id username name class subjecsts\n'
                for item in requests:
                    subjects = jdb.selectbytid(call.message.chat.id)
                    subj = ''
                    for sitem in subjects:
                        subj+=sitem[0]+', '
                    msgtext+=f'{item[0]} {item[1]} {item[2]} {item[3]} {subj[:-2]}\n'
                    markup_rback.add(InlineKeyboardButton(text=f'{item[0]} {item[1]}', callback_data=f'confirmreq#{item[0]}#{item[2]}'))
                bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=markup_rback)
            else:
                bot.edit_message_text('Заявки отсутствуют', call.message.chat.id, call.message.id, reply_markup=markup_rback)

    elif data[0]=='confirmreq':
        markup_confirm = InlineKeyboardMarkup(row_width=1)
        yes = InlineKeyboardButton(text='Подтвердить', callback_data=f'takereq#1#{data[1]}')
        delete = InlineKeyboardButton(text='Удалить', callback_data=f'takereq#0#{data[1]}')
        no = InlineKeyboardButton(text='Назад', callback_data=f'takereq')
        markup_confirm.add(no)
        markup_confirm.row(yes, delete)
        bot.edit_message_text(f'Рассмотрение заявки\nid:{data[1]} name:{data[2]}', call.message.chat.id, call.message.id, reply_markup=markup_confirm)

    elif data[0]=='takethemes':
        markup_back = InlineKeyboardMarkup(row_width=1)
        markup_back.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
        if int(data[1]):
            themes = tmdb.selectwhere(1, where='status')
            if themes==None:
                bot.edit_message_text('Активных тем нет', call.message.chat.id, call.message.id, reply_markup=markup_back)
            else:
                msgtext = 'Активные темы'
                msgtext += 'Учитель ученик предмет тема\n'
                for them in themes:
                    teacher = tdb.selectwhere(them[0], 'name')
                    user = udb.selectwhere(them[1], 'name')
                    subject = sdb.selectwhere(them[2], 'subject', 's_id')
                    msgtext += f'{teacher} {user} {subject} {'-' if them[3]==None else them[3]}\n'
                    bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=markup_back)
        else:
            themes = tmdb.selectwhere(0, where='status')
            if themes==None:
                bot.edit_message_text('Неактивных тем нет', call.message.chat.id, call.message.id, reply_markup=markup_back)
            else:
                msgtext = 'Неактивные темы\n'
                msgtext += 'Учитель ученик предмет тема\n'
                for them in themes:
                    teacher = tdb.selectwhere(them[0], 'name')[0][0]
                    user = udb.selectwhere(them[1], 'name')[0][0]
                    subject = sdb.selectwhere(them[2], 'subject', 's_id')[0][0]
                    msgtext += f'{teacher} {user} {subject} {'-' if them[3]!=None else them[3]}\n'
                    bot.edit_message_text(msgtext, call.message.chat.id, call.message.id, reply_markup=markup_back)
    elif data[0]=='addadmin':
        users = udb.selectall()
        markup_users = InlineKeyboardMarkup(row_width=1)
        markup_users.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
        for item in users:
            user = InlineKeyboardButton(text=f'{item[0]} {item[2]}', callback_data=f'confirmaddadmin#{item[0]}#{item[2]}')
            markup_users.add(user)
        if len(data)==1:
            bot.edit_message_text('id name', call.message.chat.id, call.message.id, reply_markup=markup_users)
        else:
            adb.insert(str(data[1]))
            bot.edit_message_text('id name', call.message.chat.id, call.message.id, reply_markup=markup_users)
    elif data[0]=='confirmaddadmin':
        markup_confirm = InlineKeyboardMarkup(row_width=2)
        yes = InlineKeyboardButton(text='Подтвердить', callback_data=f'addadmin#{data[1]}')
        no = InlineKeyboardButton(text='Назад', callback_data=f'addadmin')
        markup_confirm.add(yes, no)
        bot.edit_message_text(f'Добавление админа\nid:{data[1]} name:{data[2]}', call.message.chat.id, call.message.id, reply_markup=markup_confirm)

    elif data[0]=='deladmin':
        admins = adb.selectall()
        markup_users = InlineKeyboardMarkup(row_width=1)
        markup_users.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
        for item in admins:
            user = udb.selectwhere(item[0], 'name')
            admin = InlineKeyboardButton(text=f'{item[0]} {user[0][0]}', callback_data=f'confirmdeladmin#{item[0]}')
            markup_users.add(admin)
        if len(data)==1:
            bot.edit_message_text('id name', call.message.chat.id, call.message.id, reply_markup=markup_users)
        else:
            adb.delete(str(data[1]))
            admins = adb.selectall()
            markup_users = InlineKeyboardMarkup(row_width=1)
            markup_users.add(InlineKeyboardButton(text=f'Назад', callback_data=f'adminmenu'))
            for item in admins:
                user = udb.selectwhere(item[0], 'name')
                admin = InlineKeyboardButton(text=f'{item[0]} {user[0][0]}', callback_data=f'confirmdeladmin#{item[0]}')
                markup_users.add(admin)
            bot.edit_message_text('id name', call.message.chat.id, call.message.id, reply_markup=markup_users)
    elif data[0]=='confirmdeladmin':
        markup_confirm = InlineKeyboardMarkup(row_width=2)
        yes = InlineKeyboardButton(text='Подтвердить', callback_data=f'deladmin#{data[1]}')
        no = InlineKeyboardButton(text='Назад', callback_data=f'deladmin')
        markup_confirm.add(yes, no)
        bot.edit_message_text(f'Удаление админа\nid:{data[1]}', call.message.chat.id, call.message.id, reply_markup=markup_confirm)



@bot.message_handler(funk=lambda message: userstate[message.chat.id] == 'theme', content_types=['text'])
def handle_text_message(message):
    print('im working')
    userstate.pop(message.chat.id, None)
    subjects = sdb.selectall()
    markup_subjchoice = InlineKeyboardMarkup(row_width=2)
    for subj in subjects:
        subject = InlineKeyboardButton(subj[1], callback_data=f'findtheme')
        markup_subjchoice.add(subject)
    bot.send_message(message.chat.id, 'Выберите предмет к которому относится тема вопроса', reply_markup=markup_subjchoice)


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if not(is_in_users(message.chat.id)) and not(userstate[message.chat.id] == 'regist'):
        userstate[message.chat.id] = 'regist'
        markup_classchoice = InlineKeyboardMarkup(row_width=2)  
        for i in range(5,12):
            clas = InlineKeyboardButton(text=str(i), callback_data=f'new#{i}#{message.text}')
            markup_classchoice.add(clas)
        bot.send_message(message.chat.id, 'Выберите класс', reply_markup=markup_classchoice)
    elif userstate[message.chat.id] == 'theme':
        udb.update(message.chat.id, 'havetheme', 1)
        userstate.pop(message.chat.id, None)
        subjects = sdb.selectall()
        markup_subjchoice = InlineKeyboardMarkup(row_width=2)
        for subj in subjects:
            subject = InlineKeyboardButton(subj[1], callback_data=f'findtheme')
            markup_subjchoice.add(subject)
        bot.send_message(message.chat.id, 'Выберите предмет к которому относится тема вопроса', reply_markup=markup_subjchoice)
    msg = message
    if msg.text == 'ins':
        tmdb.insert(1113683801, 1634714523, 9)
    elif msg.text == 'del':
        udb.delete(msg.chat.id)
    elif msg.text == 'teach':
        tdb.insert(msg.chat.id, msg.from_user.username, 'Egor', 10)
    elif msg.text.split()[0] == 'addsub':
        jdb.insert(msg.chat.id, int(msg.text.split()[1]))
    print(msg.text, msg.chat.id, msg.from_user.username)


    


if __name__ == "__main__":
    while True:
        #try:
        bot.polling(none_stop=True)
        #except Exception as e:
         #   time.sleep(3)
         #   print(e)