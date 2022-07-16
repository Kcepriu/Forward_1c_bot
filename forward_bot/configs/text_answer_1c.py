from ..configs import texts


class TextAnswer1c:
    error_1c_qr = {
        'error_structure': texts(texts.ERROR_1C_QR_STRUCTURE),
        'error_comparison': texts(texts.ERROR_1C_QR_COMPARISON),
        'error_mark_setting': texts(texts.ERROR_1C_QR_MARK_SETTING),
        'error_find_document': texts(texts.ERROR_1C_QR_FIND_DOCUMENT),
        'error_find_partner': texts(texts.ERROR_1C_QR_FIND_PARTNER)
    }
    type_difference = {
        'number': texts(texts.TYPE_DIFFERENCE_1C_NUMBER),
        'summa': texts(texts.TYPE_DIFFERENCE_1C_SUMMA),
        'date': texts(texts.TYPE_DIFFERENCE_1C_DATE),
        'partner': texts(texts.TYPE_DIFFERENCE_1C_PARTNER)
    }

    @classmethod
    def get_text_structure(cls, type_name, name, default=''):
        return getattr(cls, type_name).get(name, default)
