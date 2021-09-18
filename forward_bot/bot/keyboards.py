from ..configs import Texts
class Keyboards():
    FIND_CONTRAHENTS = 'FIND_CONTRAHENTS'
    FIND_TOVAR = 'FIND_TOVAR'

    SEND_ADMIN = 'SEND_ADMIN'

    START_KB_AUTH = {
        FIND_CONTRAHENTS:   Texts.get_body(Texts.KB_BUTTON_FIND_CONTRAHENTS), #Пошук контрагентів
        FIND_TOVAR:   Texts.get_body(Texts.KB_BUTTON_FIND_TOVAR) #Пошук номенклатури
        }


    START_KB_NO_AUTH = {
        SEND_ADMIN:   Texts.get_body(Texts.KB_BUTTON_SEND_ADM) #Відправити запит адміністратору'
        }
