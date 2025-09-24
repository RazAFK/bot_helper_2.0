import telebot, time, pprint, db, temp_db
from settings.TOKEN import *
from db import *
from temp_db import *
from telebot.types import InputMediaPhoto, InputMediaDocument


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
    document_id = 'BQACAgIAAxkBAAMoaMAULXUB-qRRU3Bf0_k3_JtRTz8AAsN6AALrLwFKT4tPXRlCvSs2BA'
    abot.send_document(message.chat.id, document_id, caption='Hey thats your file')



@abot.message_handler(commands=['sendphoto'])
def start(message):
    photo_id = 'AgACAgIAAxkBAAMhaMATdb7ZBH9fAxu-ywzxQ0lEDOkAAqf8MRuyYflJgzBa7HPGdBkBAAMCAANzAAM2BA'
    #photo_id = 'AQADp_wxG7Jh-Ul4'
    abot.send_photo(message.chat.id, photo_id, caption='Hey thats your file')


@abot.message_handler(commands=['sendgroup'])
def start(message):
    photo_id = 'AgACAgIAAxkBAAMhaMATdb7ZBH9fAxu-ywzxQ0lEDOkAAqf8MRuyYflJgzBa7HPGdBkBAAMCAANzAAM2BA'
    #photo_id = 'AQADp_wxG7Jh-Ul4'
    document_id = 'BQACAgIAAxkBAAMoaMAULXUB-qRRU3Bf0_k3_JtRTz8AAsN6AALrLwFKT4tPXRlCvSs2BA'
    #abot.send_photo(message.chat.id, photo_id, caption='Hey thats your file')
    abot.send_media_group(message.chat.id, [InputMediaDocument(document_id, caption='here is your documents``'),InputMediaDocument(document_id, caption='here is your documents``')])
    abot.send_media_group(message.chat.id, [InputMediaPhoto(photo_id, caption='here is your photos'),InputMediaPhoto(photo_id), InputMediaPhoto(photo_id), InputMediaPhoto(photo_id)])


if __name__ == "__main__":
    #try:
    abot.polling(none_stop=True)
    #except Exception as e:
    #    print(e)