from ..configs import TOKEN
from .service import Bot1c
from ..db import Partners
from .buttons import Buttons
from .lookups import *

bot_instance = Bot1c(TOKEN)
all_buttons = Buttons()


# Command START
@bot_instance.message_handler(content_types=['text'], commands=['start'])
def start(message):
    user = bot_instance.start_authentication(message.chat)
    if not user:
        return
    bot_instance.generate_and_send_start_kb(user)


# pressed the button FIND_PARTNERS
@bot_instance.message_handler(content_types=['text'],
                              func=lambda m: m.text == all_buttons(all_buttons.FIND_PARTNERS))
def start_find_clients(message):
    user = bot_instance.start_authentication(message.chat)
    if not user:
        return
    bot_instance.send_start_find_clients(user)


# pressed the button QR_DOCUMENTS
@bot_instance.message_handler(content_types=['text'],
                              func=lambda m: m.text == all_buttons(all_buttons.QR_DOCUMENTS))
def start_find_clients(message):
    user = bot_instance.start_authentication(message.chat)
    if not user:
        return
    bot_instance.send_start_qr_documents(user)


# Натиснули відправити запит адміну
@bot_instance.message_handler(content_types=['text'],
                              func=lambda m: m.text == all_buttons(all_buttons.SEND_ADMIN))
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


@bot_instance.message_handler(content_types=['photo'])
def get_image(message):
    user = bot_instance.start_authentication(message.chat)
    if not user:
        return

    bot_instance.start_qr_processing(user, message)

