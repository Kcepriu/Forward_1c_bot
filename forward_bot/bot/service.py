from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           KeyboardButton)

from ..db import User, Text
from .keyboards import  START_KB_AUTH, START_KB_NO_AUTH

class Bot_1c(TeleBot):
   def generate_and_send_start_kb(self, user: User, text: str):
      kb = self.generate_start_kb(user)
      result = self.send_message(user.user_id, text, reply_markup=kb)

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


if __name__ == '__main__':
   pass




