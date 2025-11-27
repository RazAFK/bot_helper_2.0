from telebot.types import InputMediaPhoto, InputMediaDocument, InputMediaAudio, InputMediaVideo, InputMediaAnimation
class msg_const:
    class types:
        undefind = 0
        text = 1 
        photo = 2
        document = 3
        voice = 4
        video = 5
        audio = 6
        different = 7
        gif = 8
    class comands:
        message = 0
        new_theme = 1
        close_theme = 2
        turn_off = 3
    class senders:
        admin = 0
        teacher = 1
        student = 2
    class receivers:
        admin = 0
        teacher = 1
        student = 2

    media_types = {
        types.audio: InputMediaAudio,
        types.document: InputMediaDocument,
        types.photo: InputMediaPhoto,
        types.video: InputMediaVideo,
        types.gif: InputMediaAnimation
    }
