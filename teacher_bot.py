import telebot, time, threading
from settings.TOKEN import *
from db import *
from schedule_funcs import *
import settings.settings as sett


tbot = sett.tbot

@tbot.message_handler(commands=['start'])
def start(message):
    tbot.send_message(message.chat.id, 'Schedule running')

@tbot.message_handler(content_types=['text'])
def message_receiver(message):
    theme = select_smth(Theme, (Theme.u_id==message.chat.id) & (Theme.status==1))[0]
    write_message(message, theme.id, 1, 2, tbot, 0)
    #sbot.send_message(message.chat.id, message.id)






if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler_teacher)
    scheduler_thread.daemon = True
    scheduler_thread.start()

# bot_thread  = threading.Thread(target=bot_polling)
# bot_thread .daemon = True
# bot_thread .start()

# while True:
#     pass
#try:
    tbot.polling(none_stop=True)
    #except Exception as e:
    #    print(e)