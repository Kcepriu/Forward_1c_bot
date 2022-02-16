from telebot import TeleBot
# from telebot.apihelper import ApiTelegramException
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           KeyboardButton)
from jinja2 import Template


from ..db import User, Contrahents, Status_Operation
from .keyboards import Keyboards
from .lookups import *

from ..request_from_1c import HTTP_1C
from ..configs import USER_1C, PASSWD_1C, NAME_BOT, NAME_SERVER, ADDITIONAL_ADRESS
from ..configs import Texts, Roles
from ..configs import TEMPLATE_INFORMATION, TEMPLATE_EVENTS

htt_1s_services = HTTP_1C(USER_1C, PASSWD_1C, NAME_BOT, NAME_SERVER, ADDITIONAL_ADRESS)


class Bot1c(TeleBot):
    @staticmethod
    def there_is_role(roles, role):
        if not roles:
            return
        return roles.get(role)

    @staticmethod
    def get_formating_information_from_contrahents(information):
        tm = Template(TEMPLATE_INFORMATION)
        format_text = tm.render(message=information)
        print(type(format_text))
        return format_text

    @staticmethod
    def get_formating_information_from_events(information):
        tm = Template(TEMPLATE_EVENTS)
        format_text = tm.render(message=information)
        return format_text

    def generate_and_send_start_kb(self, user: User):
        user.user_to_status(Status_Operation.NOT_OPERATION)
        kb = self.generate_start_kb(user)
        result = self.send_message(user.user_id, Texts.get_body(Texts.TEXT_START), reply_markup=kb)

        return result.message_id

    def generate_and_send(self, user_id, text: str):
        kb = self.generate_start_kb(user_id)
        result = self.send_message(user_id, text, reply_markup=kb)

        return result.message_id

    def generate_start_kb(self, user: User):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [KeyboardButton(button) for button in Keyboards.START_KB_AUTH.values()]
        kb.add(*buttons)

        return kb

    @staticmethod
    def generate_send_admin_kb():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [KeyboardButton(button) for button in Keyboards.START_KB_NO_AUTH.values()]
        kb.add(*buttons)

        return kb

    def send_start_find_clients(self, user: User):
        user.user_to_status(Status_Operation.FIND_CLIENTS)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_START_FIND_CONTRAHENTS),
                          reply_markup=ReplyKeyboardRemove())

    def send_start_find_tovar(self, user: User):
        user.user_to_status(Status_Operation.NOT_OPERATION)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_NOT_IMPLEMENTED),
                          reply_markup=ReplyKeyboardRemove())
        self.generate_and_send_start_kb(user)

    # Зробити запит про до 1с, чи може клієнт задавати питання. Якщо може, то отримати ролі
    def autentification(self, user: User, only_return_message=False):
        try:
            message_1c = htt_1s_services.get_autentification_1c(user)
        except Exception:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return

        if not message_1c:
            # Не вдалося зʼєднатися з 1с. Ругнулося там
            return

        elif only_return_message:
            return message_1c

        elif not message_1c.get("Authentication"):
            # користувая не включений в 1с
            self.send_not_autentification(user, Texts.get_body(Texts.NO_AUTH))
            return

        # elif check_access and not message_1c.get("Access"):
        #     # користувача нема прав
        #     self.send_not_autentification(user, Texts.get_body(Texts.NO_ACCESS))
        #     return

        return message_1c

    # Послати користувачу повідомлення, що він не аутентифікований.
    # Можливо відправити клавіатуру на запит про підтвердження дозволу в 1с
    def send_not_autentification(self, user: User, text: str):
        # Отут якщо є список адмінів бота. то треба намалювати клавіатуру, яка б відправляла запист адміну
        kb = Bot1c.generate_send_admin_kb()
        self.send_message(user.user_id, text, reply_markup=kb)

    def process_only_message(self, user: User, message_1c, text_message):
        if user.status_operation == Status_Operation.FIND_CLIENTS:
            self.process_find_contrahents(user, message_1c, text_message)

        elif user.status_operation == Status_Operation.CREATE_EVENT:
            self.process_create_event(user, message_1c, text_message)

        elif user.status_operation == Status_Operation.CHOICE_CONTACT_PERSON:
            # Треба сказати що треба вибрати контактну особу
            self.send_message(user.user_id, Texts.get_body(Texts.TEXT_CHOICE_CONTACT_PERSON),
                              reply_markup=ReplyKeyboardRemove())
            return False

        else:
            # Не знаходиться ні в одній із операцій. сказати про це
            # self.send_message(user.user_id, Texts.get_body(Texts.TEXT_NO_OPERATION),
            #                   reply_markup=ReplyKeyboardRemove())

            # поки зроблю щоб щукало контрагента
            self.process_find_contrahents(user, message_1c, text_message)

        return True


    def start_send_admin_message(self, user: User, message_1c):
        # Отут треба відправити повідомлення адмінам
        admins = message_1c.get('Admins')
        if admins:
            try:
                self.send_admin_message(user, admins)
            except Exception:
                pass

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_MESSAGE_ADMINS_SEND),
                          reply_markup=ReplyKeyboardRemove())

    def send_admin_message(self, user: User, admins):
        text = f'{Texts.get_body(Texts.TEXT_USER)} {user.name}  (id={user.user_id}) ' \
               f'{Texts.get_body(Texts.TEXT_ASKS_AUTH)}'

        for admin in admins:
            self.send_message(int(admin), text)

    def process_find_contrahents(self, user: User, message_1c, text_message):
        # Треба перевірити чи є права, якщо є то знайти контрагентів і вивести їх і вивести знову стартову клаву
        # Якщо прав нема, то написати це і висести стартову клаву
        if not Bot1c.there_is_role(message_1c.get('Role'), Roles.FINDS_CONTRAHENTS):
            self.send_message(user.user_id, Texts.get_body(Texts.NO_ACCESS),
                              reply_markup=ReplyKeyboardRemove())
            return

        try:
            contrahents_1c = htt_1s_services.get_find_contrahents(user, text_message)
        except Exception:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return

        contrahents = contrahents_1c.get('partners')

        if not contrahents:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_FIND_RESULT),
                              reply_markup=ReplyKeyboardRemove())
            return

        self.senf_list_contrahents(user, contrahents)

    def process_create_event(self, user: User, message_1c, text_message):
        # Треба перевірити чи є права, якщо є то знайти контрагентів і вивести їх і вивести знову стартову клаву
        # Якщо прав нема, то написати це і висести стартову клаву
        if not Bot1c.there_is_role(message_1c.get('Role'), Roles.FINDS_CONTRAHENTS):
            self.send_message(user.user_id, Texts.get_body(Texts.NO_ACCESS),
                              reply_markup=ReplyKeyboardRemove())
            return

        try:
            result = htt_1s_services.post_event(user, text_message)
        except Exception:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return
        # Змінимо статус
        user.user_to_status(Status_Operation.NOT_OPERATION)

        if not result.get('ЕventСreated', False):
            self.send_message(user.user_id, Texts.get_body(Texts.TEXT_EVENT_NOT_CREATED))
            return

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_EVENT_CREATED))

    def senf_list_contrahents(self, user: User, contrahents):
        kb = InlineKeyboardMarkup(row_width=1)
        buttons = []
        for id_client, name_client in contrahents.items():
            id_client = id_client.replace("_", "")
            buttons.append(
                InlineKeyboardButton(name_client, callback_data=f'{HENDLER_CONTRAHENTS}{SEPARATOR}{id_client}'))
            Contrahents.write_contrahent(id_client, name_client)

        kb.add(*buttons)

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_FIND_CLIENTS),
                          reply_markup=kb)

    def start_send_information_contrahents(self, user: User, id_client, message_id):
        self.delete_message(user.user_id, message_id)

        try:
            contrahent_1c = htt_1s_services.get_information_contrahent(user, id_client)
        except Exception:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return

        information_partner = contrahent_1c.get('partner')
        format_information = Bot1c.get_formating_information_from_contrahents(information_partner)

        # Інформація відсутня
        if not format_information:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_FIND_INFORMATION),
                              reply_markup=ReplyKeyboardRemove())
            self.generate_and_send_start_kb(user)
            return

        self.send_information_contrahents(user, id_client, format_information)

    def send_information_contrahents(self, user: User, id_client, format_information):
        kb = InlineKeyboardMarkup(row_width=2)

        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_CONTRAHENT_GET_EVENT),
                                    callback_data=f'{HENDLER_CONTRAHENT_GET_EVENT}{SEPARATOR}{id_client}'))
        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_COMPANY_GET_EVENT),
                                    callback_data=f'{HENDLER_COMPANY_GET_EVENT}{SEPARATOR}{id_client}'))

        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_CREATE_EVENT),
                                    callback_data=f'{HENDLER_EVENT}{SEPARATOR}{id_client}'))

        self.send_message(user.user_id, format_information,  parse_mode='html')

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_OPERATION_FROM_CONTRAHENTS), reply_markup=kb)

    # Отримуємо контактні особи контрагента
    def get_contact_person(self, user: User, id_client):
        try:
            information_1c = htt_1s_services.get_contact_person(user, id_client)
        except Exception:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return

        return information_1c.get('contact_person')

    # Створюємо клавіатуру з контактними особами контрагента
    def create_keyboard_contact_person(self, user: User, id_client):
        contact_persons = self.get_contact_person(user, id_client)

        if not contact_persons:
            return

        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_CONTACT_PERSON_NO),
                                    callback_data=f'{HENDLER_CONTACT_PERSON}{SEPARATOR}{id_client}{SEPARATOR}EMPTY'))

        for person in contact_persons:
            kb.add(InlineKeyboardButton(person.get('name'),
                        callback_data=f'{HENDLER_CONTACT_PERSON}{SEPARATOR}{id_client}{SEPARATOR}{person.get("id")}'))

        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_CONTACT_PERSON_CANCELED),
                        callback_data = f'{HENDLER_CONTACT_PERSON}{SEPARATOR}CANCELED{SEPARATOR}EMPTY'))

        return kb

    # Тикнули Створити подію
    def start_create_evetn(self, user: User, id_client, message_id):
        self.delete_message(user.user_id, message_id)
        keyboard_contact_person = self.create_keyboard_contact_person(user, id_client)
        if keyboard_contact_person:
            # Вивести кнопки вибору контактних осіб
            self.send_keyboard_contact_person(user, id_client, keyboard_contact_person)
        else:
            # Відправити повідомлення про створення події
            self.send_message_create_event(user, id_client)

    # Відпраляємо у чат повідомлення що треба вводити тексчт події
    def send_message_create_event(self, user: User, id_client, id_contact_person=''):
        user.user_to_status(Status_Operation.CREATE_EVENT, id_client, id_contact_person)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_START_CREATED_EVENT),
                          reply_markup=ReplyKeyboardRemove())

    # Відправляємо кнопки вибору контаткни осіб у чат
    def send_keyboard_contact_person(self, user: User, id_client, kb: InlineKeyboardMarkup):
        user.user_to_status(Status_Operation.CHOICE_CONTACT_PERSON, id_client)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_CHOICE_CONTACT_PERSON),
                          reply_markup=kb)
    #Тикнули по кнопці контакної особи контрагоента
    def clic_contact_person(self, user: User, id_client, id_contact_person, message_id):
        self.delete_message(user.user_id, message_id)

        if id_client == 'CANCELED':
            self.generate_and_send_start_kb(user)
            return

        id_contact_person = id_contact_person if id_contact_person != 'EMPTY' else ''
        self.send_message_create_event(user, id_client, id_contact_person)


    def start_send_information_event_contrahents(self, user: User, id_client, message_id, company=False):
        self.delete_message(user.user_id, message_id)

        try:
            events_1c = htt_1s_services.get_events(user, id_client, company)
        except Exception:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return

        information_events = events_1c.get('events')

        # Інформація відсутня
        if not information_events:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_FIND_EVENTS),
                              reply_markup=ReplyKeyboardRemove())
            self.generate_and_send_start_kb(user)
            return

        for event in information_events:
            format_information = Bot1c.get_formating_information_from_events(event)
            self.send_message(user.user_id, format_information, parse_mode='html')


if __name__ == '__main__':
    pass

# result = HTTP_1C.get_autentification_1c(user)
# result = HTTP_1C.get_find_contrahents(user, "веранда")
# result = htt_1s_services.get_information_contrahent(user, "000069431")
