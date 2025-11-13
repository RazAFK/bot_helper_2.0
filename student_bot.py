import telebot, time, threading
from settings.TOKEN import *
import settings.settings as sett
from db import *
from schedule_funcs import *


sbot = sett.sbot
create_db_and_tables()
create_temp_db_and_tables()

#def bot_polling():
@sbot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id, 'Raz', 'Raz', 10)
    add_subject('math')
    add_theme(message.chat.id, 1, 'smth')
    theme = select_smth(Theme, (Theme.u_id==message.chat.id) & (Theme.status==0))[0]
    update_theme_teacher(theme.id, message.chat.id)
    update_theme_status(theme.id, 1)
    sbot.send_message(message.chat.id, 'Schedule running')

@sbot.message_handler(content_types=['text', 'photo'])
def message_receiver(message: telebot.types.Message):
    #print('new message', datetime.now())
    theme = select_smth(Theme, (Theme.u_id==message.chat.id) & (Theme.status==1))[0]
    #print('catched', message.photo)
    write_message(message, theme.id, 2, 1, 0)
    #print('new write message', datetime.now())
    #sbot.send_message(message.chat.id, message.id)

# @sbot.message_handler(content_types=['photo'])
# def start(message):
#     sbot.send_message(message.chat.id, message.photo[0].file_id)






if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler_student)
    scheduler_thread.daemon = True
    scheduler_thread.start()

# bot_thread  = threading.Thread(target=bot_polling)
# bot_thread .daemon = True
# bot_thread .start()

# while True:
#     pass
#try:
    sbot.polling(none_stop=True)
    #except Exception as e:
    #    print(e)