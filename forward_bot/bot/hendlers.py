from ..configs import TOKEN
from .service import Bot_1c
from ..db import User
from .keyboards import Keyboards
from .lookups import SEPARATOR, HENDLER_CONTRAHENTS, HENDLER_EVENT

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
@bot_instance.message_handler(content_types=['text'],
                              func=lambda m: m.text == Keyboards.START_KB_AUTH[Keyboards.FIND_CONTRAHENTS])
def start_find_clients(message):
    user = User.get_user(chat=message.chat)
    # в message_1c зберігаються ролі користувача і список адимінів бота, куди можна відправляти запроси на авторизацію
    message_1c = bot_instance.autentification(user)
    if not message_1c:
        return

    bot_instance.send_start_find_clients(user, message_1c)


# Натиснули пощук Номенклатури
@bot_instance.message_handler(content_types=['text'],
                              func=lambda m: m.text == Keyboards.START_KB_AUTH[Keyboards.FIND_TOVAR])
def start_find_tovar(message):
    user = User.get_user(chat=message.chat)
    # в message_1c зберігаються ролі користувача і список адимінів бота, куди можна відправляти запроси на авторизацію
    message_1c = bot_instance.autentification(user)
    if not message_1c:
        return

    bot_instance.send_start_find_tovar(user, message_1c)


# Натиснули відправити запит адміну
@bot_instance.message_handler(content_types=['text'],
                              func=lambda m: m.text == Keyboards.START_KB_NO_AUTH[Keyboards.SEND_ADMIN])
def start_send_admin_message(message):
    user = User.get_user(chat=message.chat)
    message_1c = bot_instance.autentification(user, only_return_message=True)
    if not message_1c:
        return

    bot_instance.start_send_admin_message(user, message_1c)


@bot_instance.message_handler(content_types=['text'])
def only_message(message):
    user = User.get_user(chat=message.chat)
    # в message_1c зберігаються ролі користувача і список адимінів бота, куди можна відправляти запроси на авторизацію
    message_1c = bot_instance.autentification(user)
    if not message_1c:
        return
    bot_instance.process_only_message(user, message_1c, message.text)

    bot_instance.generate_and_send_start_kb(user, message_1c)


@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HENDLER_CONTRAHENTS)
def clic_contrahents(call):
    user = User.get_user(chat=call.message.chat)
    # в message_1c зберігаються ролі користувача і список адимінів бота, куди можна відправляти запроси на авторизацію
    message_1c = bot_instance.autentification(user)
    if not message_1c:
        return

    id_client = call.data.split(SEPARATOR)[1]
    bot_instance.start_send_information_contrahents(user, call.message.message_id, id_client, message_1c)


@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HENDLER_EVENT)
def clic_contrahents(call):
    user = User.get_user(chat=call.message.chat)
    # в message_1c зберігаються ролі користувача і список адимінів бота, куди можна відправляти запроси на авторизацію
    message_1c = bot_instance.autentification(user)
    if not message_1c:
        return

    id_client = call.data.split(SEPARATOR)[1]
    bot_instance.start_create_evetn(user, call.message.message_id, id_client, message_1c)

