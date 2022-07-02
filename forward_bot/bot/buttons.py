from ..configs import Texts


class Buttons:
    FIND_PARTNERS = 'FIND_PARTNERS'
    FIND_PRODUCT = 'FIND_PRODUCT'
    SEND_ADMIN = 'SEND_ADMIN'
    QR_DOCUMENTS = 'QR_DOCUMENTS'

    ALL_BUTTON = {
        FIND_PARTNERS: Texts.get_body(Texts.KB_BUTTON_FIND_PARTNERS),  # Пошук контрагентів
        FIND_PRODUCT: Texts.get_body(Texts.KB_BUTTON_FIND_PRODUCT),  # Пошук номенклатури
        SEND_ADMIN: Texts.get_body(Texts.KB_BUTTON_SEND_ADM),  # Відправити запит адміністратору'
        QR_DOCUMENTS: Texts.get_body(Texts.KB_BUTTON_QR_DOCUMENTS)
    }

    def __call__(self, name_button):
        return self.ALL_BUTTON[name_button]
