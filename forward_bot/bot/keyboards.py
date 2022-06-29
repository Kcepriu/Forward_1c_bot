from ..configs import Texts


class Keyboards:
    FIND_PARTNERS = 'FIND_PARTNERS'
    FIND_PRODUCT = 'FIND_PRODUCT'

    SEND_ADMIN = 'SEND_ADMIN'

    START_KB_AUTH = {
        FIND_PARTNERS:   Texts.get_body(Texts.KB_BUTTON_FIND_PARTNERS) #Пошук контрагентів
        # , FIND_PRODUCT:   Texts.get_body(Texts.KB_BUTTON_FIND_PRODUCT) #Пошук номенклатури
        }

    START_KB_NO_AUTH = {
        SEND_ADMIN:   Texts.get_body(Texts.KB_BUTTON_SEND_ADM) #Відправити запит адміністратору'
        }