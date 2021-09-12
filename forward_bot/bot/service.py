from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           KeyboardButton)

from ..db import User, Text
from .keyboards import  START_KB_AUTH, START_KB_NO_AUTH

from ..request_from_1c import HTTP_1C
from ..configs import USER_1C, PASSWD_1C, NAME_BOT, NAME_SERVER, ADDITIONAL_ADRESS
from ..configs import TEXTS
from ..db import STATUS_OPERATION

htt_1s_services = HTTP_1C(USER_1C, PASSWD_1C, NAME_BOT, NAME_SERVER, ADDITIONAL_ADRESS)

class Bot_1c(TeleBot):

   def generate_and_send_start_kb(self, user: User, message_1c):
       print(message_1c)
       kb = self.generate_start_kb(user)
       result = self.send_message(user.user_id, TEXTS.get('TEXT_START'), reply_markup=kb)

       return result.message_id

   def generate_and_send(self, user_id, text: str):
      kb = self.generate_start_kb(user_id)
      result = self.send_message(user_id, text, reply_markup=kb)

      return result.message_id

   def generate_start_kb(self, user: User):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [KeyboardButton(button) for button in START_KB_AUTH.values()]

        kb.add(*buttons)

        return kb
   def send_start_find_clients(self, user: User, message_1c):
       user.status_operation = STATUS_OPERATION.NOT_OPERATION
       user.save()

       self.send_message(user.user_id, TEXTS.get('TEXT_START_FIND_CONTRAHENTS'), reply_markup=ReplyKeyboardRemove())

   #Зробити запит про до 1с, чи може клієнт задавати питання. Якщо може, то отримати ролі
   def autentification(self, user:User, check_access=True):
       message_1c = htt_1s_services.get_autentification_1c(user)
       try:
           message_1c = htt_1s_services.get_autentification_1c(user)
       except:
           self.send_message(user.user_id, TEXTS.get('NO_CONNECT'))
           return

       if not message_1c:
           # Не вдалося зʼєднатися з 1с. Ругнулося там
           return

       elif not message_1c.get("Authentication"):
           # користувая не включений в 1с
           self.send_not_autentification(user, message_1c, TEXTS.get('NO_AUTH'))
           return

       # elif check_access and not message_1c.get("Access"):
       #     # користувача нема прав
       #     self.send_not_autentification(user, message_1c, TEXTS.get('NO_ACCESS'))
       #     return

       return message_1c

   #Послати користувачу повідомлення, що він не аутентифікований.
   #Можливо відправити клавіатуру на запит про підтвердження дозволу в 1с
   def send_not_autentification(self, user:User, message_1c, text: str):
       #Отут якщо є список адмінів бота. то треба намалювати клавіатуру, яка б відправляла запист адміну
       self.send_message(user.user_id, text, reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
   pass

# result = HTTP_1C.get_autentification_1c(user)
# result = HTTP_1C.get_find_contrahents(user, "веранда")
# result = htt_1s_services.get_information_contrahent(user, "000069431")

