import telebot, time, threading
from settings.TOKEN import *
import settings.settings as sett
from db import *
from schedule_funcs import *


sbot = sett.sbot
create_db_and_tables()
create_temp_db_and_tables()


@sbot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id, 'Raz', 'Raz', 10)
    add_subject('math')
    add_theme(message.chat.id, 1, 'smth')
    theme = select_smth(Theme, (Theme.u_id==message.chat.id) & (Theme.status==0))[0]
    update_theme_teacher(theme.id, message.chat.id)
    update_theme_status(theme.id, 1)
    sbot.send_message(message.chat.id, 'Schedule running')

@sbot.message_handler(content_types=['text'])
def message_receiver(message):
    theme = select_smth(Theme, (Theme.u_id==message.chat.id) & (Theme.status==1))[0]
    write_message(message, theme.id, 2, 1, 0)
    print('new message')
    #sbot.send_message(message.chat.id, message.id)



scheduler_thread = threading.Thread(target=run_scheduler(scheduled_student_task))
scheduler_thread.daemon = True
scheduler_thread.start()


if __name__ == "__main__":
    print('start')
    #try:
    sbot.polling(none_stop=True)
    #except Exception as e:
    #    print(e)