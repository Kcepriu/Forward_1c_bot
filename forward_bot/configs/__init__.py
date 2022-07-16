from .config import TOKEN, NAME_BOT, NAME_SERVER, ADDITIONAL_ADDRESS, USER_1C, PASSWD_1C, WEBHOOK_URL, WEBHOOK_PREFIX

from .texts import Texts, texts
from .roles import Roles
from .templates import TEMPLATE_INFORMATION, TEMPLATE_EVENTS, TEMPLATE_DIFFERENCE
from .exceptions import (BotException, NoConnectionWith1c, NoAuthentication, NoValidationData)
from .text_answer_1c import TextAnswer1c
