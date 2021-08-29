import os
from .config import TOKEN
from .service import Bot_1c
from ..db import User, Text

bot_instance = Bot_1c(TOKEN)

@bot_instance.message_handler(content_types=['text'], commands=['start'])
def start(message):
    print(message)

    try:
        name = message.chat.last_name + ' ' + message.chat.first_name
    except:
        name = ""

    bot_instance.generate_and_send(message.chat.id, "Hello "+name)

    #user = User.get_user(chat=message.chat)
    #bot_instance.send_message_from_type(user, Text.START_MESSAGE)

@bot_instance.message_handler(content_types=['text'])
def only_message(message):
    print(message)
    #user = User.get_user(chat=message.chat)
    #bot_instance.send_message_from_type(user, Text.OTHER_MESSAGE)

@bot_instance.message_handler(content_types=['photo'])
def photo_message(message):
    pass
    user = User.get_user(chat=message.chat)
    bot_instance.send_message_from_type(user, Text.PHOTO_MESSAGE)


@bot_instance.message_handler(content_types=['document'])
def document_message(message):
    user = User.get_user(chat=message.chat)

    document = bot_instance.add_document(user, message)

    print(message.document)

    text = f'{Text.DOCUMENT_MESSAGE} - "{message.document.file_name}"'
    bot_instance.send_message_from_type(user, text)