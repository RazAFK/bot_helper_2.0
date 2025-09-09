import telebot, time, pprint
from settings.TOKEN import *
from db import *


abot = telebot.TeleBot(admin_token)



@abot.message_handler(commands=['stop']) 
def stop(message):
    if message.chat.id == 1634714523:
        abot.send_message(message.chat.id, 'Остановка')
        abot.stop_bot()
        exit()
    else:
        abot.send_message(message.chat.id, 'Недостаточно полномочий')


@abot.message_handler(commands=['start'])
def start(message):
    abot.send_message(message.chat.id, 'Hey')
    pprint.pprint(vars(message))

@abot.message_handler(content_types=['document'])
def start(message):
    abot.send_message(message.chat.id, 'file')
    pprint.pprint(vars(message))

@abot.message_handler(content_types=['photo'])
def start(message):
    abot.send_message(message.chat.id, message.json['date'])
    abot.send_message(message.chat.id, message.photo[0].file_id)

@abot.message_handler(commands=['senddocumen'])
def start(message):
    file_id = 'BQACAgIAAxkBAAMoaMAULXUB-qRRU3Bf0_k3_JtRTz8AAsN6AALrLwFKT4tPXRlCvSs2BA'
    abot.send_document(message.chat.id, file_id, caption='Hey thats your file')



@abot.message_handler(commands=['sendphoto'])
def start(message):
    file_id = 'AgACAgIAAxkBAAMhaMATdb7ZBH9fAxu-ywzxQ0lEDOkAAqf8MRuyYflJgzBa7HPGdBkBAAMCAANzAAM2BA'
    photo_id = 'AQADp_wxG7Jh-Ul4'
    abot.send_photo(message.chat.id, file_id, caption='Hey thats your file')

@abot.message_handler(commands=['animation'])
def start(message):
    file_id = message.animation[0].file_id
    abot.send_animation(message.chat.id, file_id)


if __name__ == "__main__":
    #try:
    abot.polling(none_stop=True)
    #except Exception as e:
    #    print(e)