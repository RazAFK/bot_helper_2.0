echo = True
dbecho = False
debug = True

subjects = ['Математика',
            'Русский язык',
            'Алгебра', 
            'Геометрия', 
            'Физика', 
            'Информатика', 
            'Химия', 
            'Биология', 
            'Английский язык', 
            'Обществознание']
schools = ['МБОУ СОШ 6']
admins = ['1634714523', '994452801']

from settings.TOKEN import *
import telebot

sbot = telebot.TeleBot(student_token)
abot = telebot.TeleBot(admin_token)
tbot = telebot.TeleBot(teacher_token)

senders = {0: 'abot', 1: 'tbot', 2: 'sbot'}
data_folder = 'data_stash'

delay = 5 #seconds
taker_delay = delay+20