from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           KeyboardButton)
from jinja2 import Template


from ..db import User, Partners, StatusOperation
from .keyboards import Keyboards
from .lookups import *

from ..request_from_1c import Http1c
from ..image import ImageQR

from ..configs import USER_1C, PASSWD_1C, NAME_BOT, NAME_SERVER, ADDITIONAL_ADDRESS
from ..configs import Texts
from ..configs import TEMPLATE_INFORMATION, TEMPLATE_EVENTS
from ..configs import NoConnectionWith1c, NoAuthentication, NoValidationData

http_1c_services = Http1c(USER_1C, PASSWD_1C, NAME_BOT, NAME_SERVER, ADDITIONAL_ADDRESS)


class Bot1c(TeleBot):
    @staticmethod
    def there_is_role(roles, role):
        if not roles:
            return
        return roles.get(role)

    @staticmethod
    def get_formatting_information_from_partners(information):
        tm = Template(TEMPLATE_INFORMATION)
        format_text = tm.render(message=information)
        return format_text

    @staticmethod
    def get_formatting_information_from_events(information):
        tm = Template(TEMPLATE_EVENTS)
        format_text = tm.render(message=information)
        return format_text

    @staticmethod
    def split_formatting_information(format_text):
        list_str = []
        while format_text:
            if len(format_text) < 4096:
                list_str.append(format_text)
                format_text = ''
            else:
                index = format_text.rindex('\n', 0, 4096)
                list_str.append(format_text[:index])
                format_text = format_text[index:]

        return list_str

    @staticmethod
    def not_access(answer):
        return not answer.get("Access", False)

    def generate_and_send_start_kb(self, user: User):
        user.user_to_status(StatusOperation.NOT_OPERATION)
        kb = self.generate_start_kb(user)
        result = self.send_message(user.user_id, Texts.get_body(Texts.TEXT_START), reply_markup=kb)

        return result.message_id

    def generate_and_send(self, user_id, text: str):
        kb = self.generate_start_kb(user_id)
        result = self.send_message(user_id, text, reply_markup=kb)

        return result.message_id

    @staticmethod
    def generate_start_kb(user: User):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [KeyboardButton(button) for button in Keyboards.get_kb(Keyboards.START_KB_AUTH, user.roles)]
        kb.add(*buttons)

        return kb

    @staticmethod
    def generate_send_admin_kb(user):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [KeyboardButton(button) for button in Keyboards.get_kb(Keyboards.START_KB_NO_AUTH, user.roles)]
        kb.add(*buttons)

        return kb

    def send_start_find_clients(self, user: User):
        user.user_to_status(StatusOperation.FIND_CLIENTS)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_START_FIND_PARTNERS),
                          reply_markup=ReplyKeyboardRemove())

    def send_start_find_tovar(self, user: User):
        user.user_to_status(StatusOperation.NOT_OPERATION)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_NOT_IMPLEMENTED),
                          reply_markup=ReplyKeyboardRemove())
        self.generate_and_send_start_kb(user)

    def start_authentication(self, message_chat, get_only_info=False):
        user = User.get_user(chat=message_chat)

        try:
            self.authentication(user, get_only_info)
        except NoAuthentication:
            return

        return user

    def authentication(self, user: User, get_only_info=False):
        # Зробити запит до 1с, чи може клієнт задавати питання. Якщо може, то отримати ролі
        try:
            message_1c = http_1c_services.get_authentication_1c(user)

            # запишемо в юзера список ориманих ролей, список адмінів і признак аутентифікації
            user.set_info_from_user(message_1c)

        except (NoConnectionWith1c, NoValidationData):
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            raise NoAuthentication

        if get_only_info:
            # Не треба ругатись що не аутентифіковано. Ми отримали список адмінів, куди можна відправити запрос
            return
        elif not user.authentication:
            # користувая не включений в 1с
            self.send_not_authentication(user, Texts.get_body(Texts.NO_AUTH))
            raise NoAuthentication

    # Послати користувачу повідомлення, що він не аутентифікований.
    # Можливо відправити клавіатуру на запит про підтвердження дозволу в 1с
    def send_not_authentication(self, user: User, text: str):
        kb = Bot1c.generate_send_admin_kb(user)
        self.send_message(user.user_id, text, reply_markup=kb)

    def process_only_message(self, user: User, text_message):
        if user.status_operation == StatusOperation.FIND_CLIENTS:
            self.process_find_partners(user, text_message)

        elif user.status_operation == StatusOperation.CREATE_EVENT:
            self.process_create_event(user, text_message)

        elif user.status_operation == StatusOperation.CHOICE_CONTACT_PERSON:
            # Треба сказати що треба вибрати контактну особу
            self.send_message(user.user_id, Texts.get_body(Texts.TEXT_CHOICE_CONTACT_PERSON),
                              reply_markup=ReplyKeyboardRemove())
            return False

        else:
            # Не знаходиться ні в одній із операцій. сказати про це
            # self.send_message(user.user_id, Texts.get_body(Texts.TEXT_NO_OPERATION),
            #                   reply_markup=ReplyKeyboardRemove())

            # поки зроблю щоб щукало контрагента
            self.process_find_partners(user, text_message)

        return True

    def start_send_admin_message(self, user: User):
        # Отут треба відправити повідомлення адмінам
        admins = user.admins_bot
        if admins:
            try:
                self.send_admin_message(user, admins)
            except ApiTelegramException:
                pass

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_MESSAGE_ADMINS_SEND),
                          reply_markup=ReplyKeyboardRemove())

    def send_admin_message(self, user: User, admins):
        text = f'{Texts.get_body(Texts.TEXT_USER)} {user.name}  (id={user.user_id}) ' \
               f'{Texts.get_body(Texts.TEXT_ASKS_AUTH)}'

        for admin in admins:
            self.send_message(int(admin), text)

    def process_find_partners(self, user: User, text_message):
        # Треба перевірити чи є права, якщо є то знайти контрагентів і вивести їх і вивести знову стартову клаву
        # Якщо прав нема, то написати це і висести стартову клаву

        try:
            partners_1c = http_1c_services.get_find_partner(user, text_message)
            if self.not_access(partners_1c):
                self.send_message(user.user_id, Texts.get_body(Texts.NO_ACCESS),
                                  reply_markup=ReplyKeyboardRemove())
                return

        except NoConnectionWith1c:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return
        except ApiTelegramException:
            return

        partners = partners_1c.get('partners')

        if not partners:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_FIND_RESULT),
                              reply_markup=ReplyKeyboardRemove())
            return

        self.send_list_partners(user, partners)

    def process_create_event(self, user: User, text_message):
        # Треба перевірити чи є права, якщо є то знайти контрагентів і вивести їх і вивести знову стартову клаву
        # Якщо прав нема, то написати це і висести стартову клаву

        try:
            result = http_1c_services.post_event(user, text_message)

            if self.not_access(result):
                self.send_message(user.user_id, Texts.get_body(Texts.NO_ACCESS),
                                  reply_markup=ReplyKeyboardRemove())
                return

        except NoConnectionWith1c:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return
        except ApiTelegramException:
            return
        # Змінимо статус
        user.user_to_status(StatusOperation.NOT_OPERATION)

        if not result.get('ЕventСreated', False):
            self.send_message(user.user_id, Texts.get_body(Texts.TEXT_EVENT_NOT_CREATED))
            return

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_EVENT_CREATED))

    def send_list_partners(self, user: User, partners):
        kb = InlineKeyboardMarkup(row_width=1)
        buttons = []
        for id_client, name_client in partners.items():
            id_client = id_client.replace("_", "")
            buttons.append(
                InlineKeyboardButton(name_client, callback_data=f'{HANDLER_PARTNER}{SEPARATOR}{id_client}'))
            Partners.write_partner(id_client, name_client)

        kb.add(*buttons)

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_FIND_CLIENTS),
                          reply_markup=kb)

    def start_send_information_partners(self, user: User, id_client, message_id):
        self.delete_message(user.user_id, message_id)

        try:
            partners_1c = http_1c_services.get_information_partner(user, id_client)
        except NoConnectionWith1c:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return

        information_partner = partners_1c.get('partner')
        format_information = Bot1c.get_formatting_information_from_partners(information_partner)

        # Інформація відсутня
        if not format_information:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_FIND_INFORMATION),
                              reply_markup=ReplyKeyboardRemove())
            self.generate_and_send_start_kb(user)
            return

        self.send_information_partners(user, id_client, format_information)

    def generate_keyboard_partner(self, id_client):
        kb = InlineKeyboardMarkup(row_width=2)

        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_PARTNER_GET_EVENT),
                                    callback_data=f'{HANDLER_PARTNER_GET_EVENT}{SEPARATOR}{id_client}'))
        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_COMPANY_GET_EVENT),
                                    callback_data=f'{HANDLER_COMPANY_GET_EVENT}{SEPARATOR}{id_client}'))

        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_CREATE_EVENT),
                                    callback_data=f'{HANDLER_EVENT}{SEPARATOR}{id_client}'))
        return kb

    def send_information_partners(self, user: User, id_client, format_information):
        kb = self.generate_keyboard_partner(id_client)

        list_information = self.split_formatting_information(format_information)
        for elem in list_information:
            self.send_message(user.user_id, elem,  parse_mode='html')

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_OPERATION_FROM_PARTNERS), reply_markup=kb)

    # Отримуємо контактні особи контрагента
    def get_contact_person(self, user: User, id_client):
        try:
            information_1c = http_1c_services.get_contact_person(user, id_client)
        except NoConnectionWith1c:
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
                                    callback_data=f'{HANDLER_CONTACT_PERSON}{SEPARATOR}{id_client}{SEPARATOR}EMPTY'))

        for person in contact_persons:
            kb.add(InlineKeyboardButton(person.get('name'),
                        callback_data=f'{HANDLER_CONTACT_PERSON}{SEPARATOR}{id_client}{SEPARATOR}{person.get("id")}'))

        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_CONTACT_PERSON_CANCELED),
                                    callback_data=f'{HANDLER_CONTACT_PERSON}{SEPARATOR}CANCELED{SEPARATOR}EMPTY'))

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
        user.user_to_status(StatusOperation.CREATE_EVENT, id_client, id_contact_person)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_START_CREATED_EVENT),
                          reply_markup=ReplyKeyboardRemove())

    # Відправляємо кнопки вибору контаткни осіб у чат
    def send_keyboard_contact_person(self, user: User, id_client, kb: InlineKeyboardMarkup):
        user.user_to_status(StatusOperation.CHOICE_CONTACT_PERSON, id_client)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_CHOICE_CONTACT_PERSON),
                          reply_markup=kb)

    # Тикнули по кнопці контакної особи контрагоента
    def clic_contact_person(self, user: User, id_client, id_contact_person, message_id):
        self.delete_message(user.user_id, message_id)

        if id_client == 'CANCELED':
            self.generate_and_send_start_kb(user)
            return

        id_contact_person = id_contact_person if id_contact_person != 'EMPTY' else ''
        self.send_message_create_event(user, id_client, id_contact_person)

    def start_send_information_event_partners(self, user: User, id_client, message_id, company=False):
        self.delete_message(user.user_id, message_id)

        try:
            events_1c = http_1c_services.get_events(user, id_client, company)
        except NoConnectionWith1c:
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
            format_information = Bot1c.get_formatting_information_from_events(event)
            self.send_message(user.user_id, format_information, parse_mode='html')

    def send_start_qr_documents(self, user: User):
        user.user_to_status(StatusOperation.WAIT_QR_DOCUMENTS)

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_SEND_QR_IMAGE),
                          reply_markup=ReplyKeyboardRemove())

    def get_information_with_qr(self, message):
        file_info = self.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = self.download_file(file_info.file_path)

        image_qr = ImageQR(byte_string=downloaded_file)

        barcode_data = image_qr.decode_barcodes()

        return barcode_data

    def get_information_with_1c(self, user: User, barcode_data):
        try:
            result = http_1c_services.post_document(user, barcode_data)

            if self.not_access(result):
                self.send_message(user.user_id, Texts.get_body(Texts.NO_ACCESS),
                                  reply_markup=ReplyKeyboardRemove())
                return

        except NoConnectionWith1c:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return
        except ApiTelegramException:
            return

        return result

    def start_qr_processing(self, user: User, message):
        barcode_data = self.get_information_with_qr(message)

        self.delete_message(user.user_id, message.message_id)
        user.user_to_status(StatusOperation.NOT_OPERATION)

        if not barcode_data:
            self.send_message(user.user_id, Texts.get_body(Texts.TEXT_FAILED_QR_PROCESSING),
                              reply_markup=ReplyKeyboardRemove())
            return

        compare_answer = self.get_information_with_1c(user, barcode_data)
        self.output_information_compare(user, compare_answer)

    def output_information_compare(self, user: User, information):
        if not information:
            # Вже ругнулося. Просто виходимо
            return

        answer = information.get('DocumentMarked')
        if not answer:
            # error
            return

        if answer.result:
            # Все ок. сказати що відмічено
            self.send_message(user.user_id, 'Получено')
        else:
            # сказати про помилку
            if answer.array_differences:
                # вивеси дані про дані порівняння
                pass



# Треба написати обработку результата з 1с. Там поже приходити Access=False. Значить 1с заборонив виконувати цю операцію
# Це після всіх звернень до 1с крім автонтифікації


if __name__ == '__main__':
    pass

# result = HTTP_1C.get_autentification_1c(user)
# result = HTTP_1C.get_find_contrahents(user, "веранда")
# result = htt_1s_services.get_information_contrahent(user, "000069431")
