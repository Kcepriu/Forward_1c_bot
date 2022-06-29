from ..configs import TOKEN
from .service import Bot1c
from ..db import Partners
from .keyboards import Keyboards
from .lookups import *

bot_instance = Bot1c(TOKEN)


# Команда START
@bot_instance.message_handler(content_types=['text'], commands=['start'])
def start(message):
    user = bot_instance.start_authentication(message.chat)
    if not user:
        return

    bot_instance.generate_and_send_start_kb(user)


# Натиснули пощук контрагента
@bot_instance.message_handler(content_types=['text'],
                              func=lambda m: m.text == Keyboards.START_KB_AUTH[Keyboards.FIND_PARTNERS])
def start_find_clients(message):
    user = bot_instance.start_authentication(message.chat)
    if not user:
        return

    bot_instance.send_start_find_clients(user)


# # Натиснули пощук Номенклатури
# @bot_instance.message_handler(content_types=['text'],
#                               func=lambda m: m.text == Keyboards.START_KB_AUTH[Keyboards.FIND_TOVAR])
# def start_find_tovar(message):
#     user = User.get_user(chat=message.chat)
#     # в message_1c зберігаються ролі користувача і список адимінів бота, куди можна відправляти запроси на авторизацію
#     try:
#         bot_instance.authentication(user)
#     except NoAuthentication:
#         return
#
#     bot_instance.send_start_find_tovar(user, message_1c)


# Натиснули відправити запит адміну
@bot_instance.message_handler(content_types=['text'],
                              func=lambda m: m.text == Keyboards.START_KB_NO_AUTH[Keyboards.SEND_ADMIN])
def start_send_admin_message(message):
    user = bot_instance.start_authentication(message.chat, get_only_info=True)
    if not user:
        return

    bot_instance.start_send_admin_message(user)


# Просто написали деякий текст. Перевіримо в якому статусі знаходимося
@bot_instance.message_handler(content_types=['text'])
def only_message(message):
    user = bot_instance.start_authentication(message.chat)
    if not user:
        return

    if bot_instance.process_only_message(user, message.text):
        bot_instance.generate_and_send_start_kb(user)


#  Тикнули по кнопці контрагента
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HANDLER_PARTNER)
def clic_partners(call):
    user = bot_instance.start_authentication(call.message.chat)
    if not user:
        return

    id_client = call.data.split(SEPARATOR)[1]
    bot_instance.start_send_information_partners(user, id_client, call.message.message_id)


# створити подію
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HANDLER_EVENT)
def clic_create_event(call):
    user = bot_instance.start_authentication(call.message.chat)
    if not user:
        return

    id_client = call.data.split(SEPARATOR)[1]
    bot_instance.start_create_evetn(user, id_client, call.message.message_id)


#  Отримати події контрагента
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HANDLER_PARTNER_GET_EVENT)
def clic_get_events(call):
    user = bot_instance.start_authentication(call.message.chat)
    if not user:
        return

    id_client = call.data.split(SEPARATOR)[1]
    bot_instance.start_send_information_event_partners(user, id_client, call.message.message_id, company=False)

    partner = {id_client: Partners.get_partner(id_client)}
    bot_instance.send_list_partners(user, partner)


#  Отримати події компанії
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HANDLER_COMPANY_GET_EVENT)
def clic_get_events_all(call):
    user = bot_instance.start_authentication(call.message.chat)
    if not user:
        return

    id_client = call.data.split(SEPARATOR)[1]
    bot_instance.start_send_information_event_partners(user, id_client, call.message.message_id, company=True)

    partner = {id_client: Partners.get_partner(id_client)}
    bot_instance.send_list_partners(user, partner)


#  Тикнули по кнопці контактної особи
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HANDLER_CONTACT_PERSON)
def clic_contact_person(call):
    user = bot_instance.start_authentication(call.message.chat)
    if not user:
        return

    id_client = call.data.split(SEPARATOR)[1]
    id_contact_person = call.data.split(SEPARATOR)[2]

    bot_instance.clic_contact_person(user, id_client, id_contact_person, call.message.message_id)
