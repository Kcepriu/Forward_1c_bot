from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           KeyboardButton)
from jinja2 import Template


from ..db import User
from .keyboards import Keyboards
from .lookups import SEPARATOR, HENDLER_CONTRAHENTS,HENDLER_EVENT

from ..request_from_1c import HTTP_1C
from ..configs import USER_1C, PASSWD_1C, NAME_BOT, NAME_SERVER, ADDITIONAL_ADRESS
from ..configs import Texts, Roles
from ..db import Status_Operation
from ..configs import TEMPLATE_INFORMATION

htt_1s_services = HTTP_1C(USER_1C, PASSWD_1C, NAME_BOT, NAME_SERVER, ADDITIONAL_ADRESS)

class Create_Text():
    @classmethod
    def generete_information_from_contrahents(cls, information):
        result = f'*Назва*: {information.get("name")}\n' \
                 f'*Повна назва*: {information.get("full_name")}\n' \
                 f'{cls.generate_information_from_contacts(information.get("contacts"))}\n\n' \
                 f'{cls.generate_information_from_contact_persons(information.get("contact_persons"), 3)}'

        return result

    @classmethod
    def generate_information_from_contact_persons(cls, contact_persons, indent=0):
        result = ''
        for item in contact_persons:
            result += ("" if len(result) == 0 else "\n") + \
                      f'{" "*(indent+3)}*{item.get("post")}*: {item.get("name")}\n'+ \
                      f'{cls.generate_information_from_contacts(item.get("contacts", indent+3))}\n'


        result = f'{" "*(indent)}*Контакні особи:*\n'+result

        return result

    @classmethod
    def generate_information_from_contacts(cls, contacts, indent=0):
        result = ""
        for item in contacts:
            result += ("" if len(result) == 0 else "\n") +f'{" "*(indent+3)}*{item.get("type")}*: {item.get("contact")}'

        return f'{" "*indent}*Контактна інформація:*\n{result}'

class Bot_1c(TeleBot):
    @staticmethod
    def there_is_role(roles, role):
        if not roles:
            return
        return roles.get(role)

    @staticmethod
    def get_formating_information_from_contrahents(information):
        # print(information)
        # create_text = Create_Text()
        # format_text = create_text.generete_information_from_contrahents(information)
        tm = Template(TEMPLATE_INFORMATION)
        format_text = tm.render(message=information)
        return format_text

    def generate_and_send_start_kb(self, user: User, message_1c):
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

    def send_start_find_clients(self, user: User, message_1c):
        user.user_to_status(Status_Operation.FIND_CLIENTS)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_START_FIND_CONTRAHENTS),
                          reply_markup=ReplyKeyboardRemove())

    def send_start_find_tovar(self, user: User, message_1c):
        user.user_to_status(Status_Operation.NOT_OPERATION)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_NOT_IMPLEMENTED),
                          reply_markup=ReplyKeyboardRemove())
        self.generate_and_send_start_kb(user, message_1c)

    # Зробити запит про до 1с, чи може клієнт задавати питання. Якщо може, то отримати ролі
    def autentification(self, user: User, check_access=True, only_return_message=False):
        try:
            message_1c = htt_1s_services.get_autentification_1c(user)
        except:
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
        kb = Bot_1c.generate_send_admin_kb()
        self.send_message(user.user_id, text, reply_markup=kb)

    def process_only_message(self, user: User, message_1c, text_message):
        if user.status_operation == Status_Operation.FIND_CLIENTS:
            self.process_find_contrahents(user, message_1c, text_message)
        elif user.status_operation == Status_Operation.CREATE_EVENT:
            self.process_create_event(user, message_1c, text_message)
        else:
            # Не знаходиться ні в одній із операцій. сказати про це
            self.send_message(user.user_id, Texts.get_body(Texts.TEXT_NO_OPERATION),
                              reply_markup=ReplyKeyboardRemove())

    def start_send_admin_message(self, user: User, message_1c):
        # Отут треба відправити повідомлення адмінам
        admins = message_1c.get('Admins')
        if admins:
            try:
                self.send_admin_message(user, admins)
            except:
                pass

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_MESSAGE_ADMINS_SEND),
                          reply_markup=ReplyKeyboardRemove())

    def send_admin_message(self, user: User, admins):
        text = f'{Texts.get_body(Texts.TEXT_USER)} {user.name}  (id={user.user_id}) {Texts.get_body(Texts.TEXT_ASKS_AUTH)}'

        for admin in admins:
            self.send_message(int(admin), text)

    def process_find_contrahents(self, user: User, message_1c, text_message):
        # Треба перевірити чи є права, якщо є то знайти контрагентів і вивести їх і вивести знову стартову клаву
        # Якщо прав нема, то написати це і висести стартову клаву
        if not Bot_1c.there_is_role(message_1c.get('Role'), Roles.FINDS_CONTRAHENTS):
            self.send_message(user.user_id, Texts.get_body(Texts.NO_ACCESS),
                              reply_markup=ReplyKeyboardRemove())
            return

        try:
            contrahents_1c = htt_1s_services.get_find_contrahents(user, text_message)
        except:
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
        if not Bot_1c.there_is_role(message_1c.get('Role'), Roles.FINDS_CONTRAHENTS):
            self.send_message(user.user_id, Texts.get_body(Texts.NO_ACCESS),
                              reply_markup=ReplyKeyboardRemove())
            return
        try:
            result = htt_1s_services.post_event(user, text_message)
        except:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return

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

        kb.add(*buttons)

        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_FIND_CLIENTS),
                          reply_markup=kb)

    def start_send_information_contrahents(self, user:User, message_id, id_client, message_1c):
        contrahent_1c = htt_1s_services.get_information_contrahent(user, id_client)
        try:
            contrahent_1c = htt_1s_services.get_information_contrahent(user, id_client)
        except:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_CONNECT))
            return

        information_partner = contrahent_1c.get('partner')
        format_information = Bot_1c.get_formating_information_from_contrahents(information_partner)

        #print(format_information)

        # Інформація відсутня
        if not format_information:
            self.send_message(user.user_id, Texts.get_body(Texts.NO_FIND_INFORMATION),
                              reply_markup=ReplyKeyboardRemove())
            self.generate_and_send_start_kb(user, message_1c)
            return

        self.send_information_contrahents(user, message_id, id_client, message_1c, format_information)

    def send_information_contrahents(self, user:User, message_id, id_client, message_1c, format_information):
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(InlineKeyboardButton(Texts.get_body(Texts.KB_BUTTON_CREATE_EVENT), callback_data=f'{HENDLER_EVENT}{SEPARATOR}{id_client}'))

        self.send_message(user.user_id, format_information,
                          reply_markup=kb, parse_mode='html')

    def start_create_evetn(self, user:User, message_id, id_client, message_1c):
        user.user_to_status(Status_Operation.CREATE_EVENT, id_client)
        self.send_message(user.user_id, Texts.get_body(Texts.TEXT_START_CREATED_EVENT),
                          reply_markup=ReplyKeyboardRemove())



if __name__ == '__main__':
    pass

# result = HTTP_1C.get_autentification_1c(user)
# result = HTTP_1C.get_find_contrahents(user, "веранда")
# result = htt_1s_services.get_information_contrahent(user, "000069431")
