import telebot, time, pprint, db, temp_db
from settings.TOKEN import *
from db import *
from temp_db import *
from telebot.types import InputMediaPhoto, InputMediaDocument
import settings.settings as sett
import telebot.types

abot = sett.abot








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
    abot.send_message(message.chat.id, abot.send_message(message.chat.id, 'Hey').message_id)
    pprint.pprint(vars(message))

@abot.message_handler(content_types=['document'])
def start(message):
    abot.send_message(message.chat.id, 'file')
    pprint.pprint(vars(message))

@abot.message_handler(content_types=['photo'])
def start(message: telebot.types.Message):
    # downloaded_file = abot.download_file(abot.get_file(message.photo[-1].file_id).file_path)
    # with open('photo.jpg', 'wb') as file:
    #     file.write(downloaded_file)
    # for photo in photos:
    #     abot.send_message(message.chat.id, f'{photo.file_id}')
    #     abot.send_photo(message.chat.id, photo.file_id)
    print(message.photo[0].file_id)

@abot.message_handler(commands=['senddocumen'])
def start(message):
    document_id = 'BQACAgIAAxkBAAMoaMAULXUB-qRRU3Bf0_k3_JtRTz8AAsN6AALrLwFKT4tPXRlCvSs2BA'
    abot.send_document(message.chat.id, document_id, caption='Hey thats your file')



@abot.message_handler(commands=['sendphoto'])
def start(message):
    photos = [{'file_id': 'AgACAgIAAxkBAANxaRWQuXlJwk2O9lfZAWNYvjYv400AAmYOaxuf7alIbfLkVh4eQl0BAAMCAANzAAM2BA', 'file_unique_id': 'AQADZg5rG5_tqUh4', 'file_size': 1599, 'width': 51, 'height': 90},
    {'file_id': 'AgACAgIAAxkBAANxaRWQuXlJwk2O9lfZAWNYvjYv400AAmYOaxuf7alIbfLkVh4eQl0BAAMCAANtAAM2BA', 'file_unique_id': 'AQADZg5rG5_tqUhy', 'file_size': 18718, 'width': 180, 'height': 320},
    {'file_id': 'AgACAgIAAxkBAANxaRWQuXlJwk2O9lfZAWNYvjYv400AAmYOaxuf7alIbfLkVh4eQl0BAAMCAAN4AAM2BA', 'file_unique_id': 'AQADZg5rG5_tqUh9', 'file_size': 64871, 'width': 450, 'height': 800},
    {'file_id': 'AgACAgIAAxkBAANxaRWQuXlJwk2O9lfZAWNYvjYv400AAmYOaxuf7alIbfLkVh4eQl0BAAMCAAN5AAM2BA', 'file_unique_id': 'AQADZg5rG5_tqUh-', 'file_size': 109511, 'width': 720, 'height': 1280}]
    for photo in photos:
        abot.send_message(message.chat.id, f'{photo['file_id']}\nnexe\n{photo['file_unique_id']}')
        abot.send_photo(message.chat.id, photo['file_id'])
        abot.send_photo(message.chat.id, photo['file_unique_id'])


@abot.message_handler(commands=['sendgroup'])
def start(message):
    photo_id = 'AgACAgIAAxkBAAMhaMATdb7ZBH9fAxu-ywzxQ0lEDOkAAqf8MRuyYflJgzBa7HPGdBkBAAMCAANzAAM2BA'
    #photo_id = 'AQADp_wxG7Jh-Ul4'
    document_id = 'BQACAgIAAxkBAAMoaMAULXUB-qRRU3Bf0_k3_JtRTz8AAsN6AALrLwFKT4tPXRlCvSs2BA'
    #abot.send_photo(message.chat.id, photo_id, caption='Hey thats your file')
    #abot.send_media_group(message.chat.id, [InputMediaDocument(document_id, caption='here is your documents``'),InputMediaDocument(document_id, caption='here is your documents``')])
    abot.send_media_group(message.chat.id, [InputMediaPhoto(photo_id, caption='here is your photos')])#,InputMediaPhoto(photo_id), InputMediaPhoto(photo_id), InputMediaPhoto(photo_id)


if __name__ == "__main__":
    #try:
    abot.polling(none_stop=True)
    #except Exception as e:
    #    print(e)