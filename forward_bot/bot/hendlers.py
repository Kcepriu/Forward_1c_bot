from ..configs import TOKEN
from .service import Bot_1c
from ..db import User
from .keyboards import START_KB_AUTH
from ..configs import TEXTS

bot_instance = Bot_1c(TOKEN)

@bot_instance.message_handler(content_types=['text'], commands=['start'])
def start(message):
    user = User.get_user(chat=message.chat)

    # в message_1c зберігаються ролі користувача і список адимінів бота, куди можна відправляти запроси на авторизацію
    message_1c = bot_instance.autentification(user, False)
    if not message_1c:
        return
    bot_instance.generate_and_send_start_kb(user, message_1c)

# Натиснули пощук контраогнета
@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB_AUTH['find_company'])
def start_find_clients(message):
    user = User.get_user(chat=message.chat)
    # в message_1c зберігаються ролі користувача і список адимінів бота, куди можна відправляти запроси на авторизацію
    message_1c = bot_instance.autentification(user)
    if not message_1c:
        return

    bot_instance.send_start_find_clients(user, message_1c)
    print('find company')
    pass

@bot_instance.message_handler(content_types=['text'])
def only_message(message):
    user = User.get_user(chat=message.chat)
    # в message_1c зберігаються ролі користувача і список адимінів бота, куди можна відправляти запроси на авторизацію
    message_1c = bot_instance.autentification(user)
    if not message_1c:
        return

    print(message)
    #user = User.get_user(chat=message.chat)
    #bot_instance.send_message_from_type(user, Text.OTHER_MESSAGE)

