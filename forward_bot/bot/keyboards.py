from .buttons import Buttons
from .acl import Acl


class Keyboards:
    START_KB_AUTH = 'START_KB_AUTH'
    START_KB_NO_AUTH = 'START_KB_NO_AUTH'

    KB = {
        START_KB_AUTH: (Buttons.FIND_PARTNERS, Buttons.QR_DOCUMENTS),
        START_KB_NO_AUTH: (Buttons.SEND_ADMIN,)
    }

    @classmethod
    def get_kb(cls, name_kb, role: set):
        kb = [Buttons.ALL_BUTTON[button] for button in cls.KB.get(name_kb)
              if role & set(Acl.BUTTONS.get(button)) or not set(Acl.BUTTONS.get(button))]

        # for button in cls.KB.get(name_kb):
        #     nnew = role & set(Acl.BUTTONS.get(button))
        #     print('role', role)
        #     print('button', set(Acl.BUTTONS.get(button)))

        return kb
