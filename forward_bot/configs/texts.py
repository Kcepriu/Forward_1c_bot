class Texts:
    NO_CONNECT = 'NO_CONNECT'
    NO_AUTH = 'NO_AUTH'
    NO_ACCESS = 'NO_ACCESS'
    NO_FIND_RESULT = 'NO_FIND_RESULT'
    NO_FIND_INFORMATION = 'NO_FIND_INFORMATION'
    NO_FIND_EVENTS = 'NO_FIND_EVENTS'
    TEXT_START = 'TEXT_START'
    TEXT_START_FIND_PARTNERS = 'TEXT_START_FIND_PARTNERS'
    TEXT_NO_OPERATION = 'TEXT_NO_OPERATION'
    TEXT_NOT_IMPLEMENTED = 'TEXT_NOT_IMPLEMENTED'
    TEXT_MESSAGE_ADMINS_SEND = 'TEXT_MESSAGE_ADMINS_SEND'
    TEXT_USER = 'TEXT_USER'
    TEXT_ASKS_AUTH = 'TEXT_ASKS_AUTH'
    TEXT_FIND_CLIENTS = 'TEXT_FIND_CLIENTS'
    TEXT_START_CREATED_EVENT = 'TEXT_START_CREATED_EVENT'
    TEXT_EVENT_CREATED = 'TEXT_EVENT_CREATED'
    TEXT_EVENT_NOT_CREATED = 'TEXT_EVENT_NOT_CREATED'
    TEXT_CHOICE_CONTACT_PERSON = 'TEXT_CHOICE_CONTACT_PERSON'
    TEXT_OPERATION_FROM_PARTNERS = 'TEXT_OPERATION_FROM_PARTNERS'
    TEXT_SEND_QR_IMAGE = 'TEXT_SEND_QR_IMAGE'
    TEXT_FAILED_QR_PROCESSING = 'TEXT_FAILED_QR_PROCESSING'
    TEXT_UNKNOWN_ERROR = 'TEXT_UNKNOWN_ERROR'
    TEXT_FOR_DOCUMENT = 'TEXT_FOR_DOCUMENT'
    TEXT_FLAG_IN_SET = 'TEXT_FLAG_IN_SET'
    TEXT_FLAG_NO_SET = 'TEXT_FLAG_NO_SET'

    KB_BUTTON_FIND_PARTNERS = 'KB_BUTTON_FIND_PARTNERS'
    KB_BUTTON_FIND_PRODUCT = 'KB_BUTTON_FIND_PRODUCT'
    KB_BUTTON_SEND_INFORMATION_PARTNERS = 'KB_BUTTON_SEND_INFORMATION_PARTNERS'

    KB_BUTTON_SEND_ADM = 'KB_BUTTON_SEND_ADM'
    KB_BUTTON_CREATE_EVENT = 'KB_BUTTON_CREATE_EVENT'
    KB_BUTTON_PARTNER_GET_EVENT = 'KB_BUTTON_PARTNER_GET_EVENT'
    KB_BUTTON_COMPANY_GET_EVENT = 'KB_BUTTON_COMPANY_GET_EVENT'
    KB_BUTTON_CONTACT_PERSON_CANCELED = 'KB_BUTTON_CONTACT_PERSON_CANCELED'
    KB_BUTTON_CONTACT_PERSON_NO = 'KB_BUTTON_CONTACT_PERSON_NO'
    KB_BUTTON_QR_DOCUMENTS = 'KB_BUTTON_QR_DOCUMENTS'

    ERROR_1C_QR_STRUCTURE = 'ERROR_1C_QR_STRUCTURE'
    ERROR_1C_QR_COMPARISON = 'ERROR_1C_QR_COMPARISON'
    ERROR_1C_QR_MARK_SETTING = 'ERROR_1C_QR_MARK_SETTING'
    ERROR_1C_QR_FIND_DOCUMENT = 'ERROR_1C_QR_FIND_DOCUMENT'
    ERROR_1C_QR_FIND_PARTNER = 'ERROR_1C_QR_FIND_PARTNER'

    TYPE_DIFFERENCE_1C_NUMBER = 'TYPE_DIFFERENCE_1C_NUMBER'
    TYPE_DIFFERENCE_1C_SUMMA = 'TYPE_DIFFERENCE_1C_SUMMA'
    TYPE_DIFFERENCE_1C_DATE = 'TYPE_DIFFERENCE_1C_DATE'
    TYPE_DIFFERENCE_1C_PARTNER = 'TYPE_DIFFERENCE_1C_PARTNER'

    TITLES_CONSTANT = {NO_CONNECT: 'Не вдалося зʼєднатися з 1с',
                       NO_AUTH: 'Про вас відсутні дані в 1с. Зверніться до адміністратора',
                       NO_ACCESS: 'У вас бракує прав для такої операції',
                       NO_FIND_RESULT: 'Не знайдено жодного контрагента з такою назвою',
                       NO_FIND_INFORMATION: 'Дані про контрагента відсутні',
                       NO_FIND_EVENTS: 'Подій не знайдено',
                       TEXT_START: 'Виберіть потрібну операцію, натиснувши відповідну кнопку 👇',
                       TEXT_START_FIND_PARTNERS: '👇 Введіть назву контрагента, і відправте повідомлення',
                       TEXT_NO_OPERATION: 'Не вірна команда',
                       TEXT_NOT_IMPLEMENTED: 'Не реалізовано',
                       TEXT_MESSAGE_ADMINS_SEND: 'Повідомлення адміністратору відправлено',
                       TEXT_USER: 'Користувач',
                       TEXT_ASKS_AUTH: 'проcить авторизувати його в системі',
                       TEXT_FIND_CLIENTS: 'Знайдені контрагенти:',
                       TEXT_START_CREATED_EVENT: '👇 Введіть текст події',
                       TEXT_EVENT_CREATED: 'Подію створено!',
                       TEXT_EVENT_NOT_CREATED: 'Помилка створення події',
                       TEXT_CHOICE_CONTACT_PERSON: '👇 Виберіть контактну особу, для створення події',
                       TEXT_OPERATION_FROM_PARTNERS: 'Операції з контрагентом:',
                       TEXT_SEND_QR_IMAGE: 'Відправте QR код видаткової',
                       TEXT_FAILED_QR_PROCESSING: 'Не вдалося розпізнати QR код',
                       TEXT_UNKNOWN_ERROR: 'Невідома помилка',
                       TEXT_FOR_DOCUMENT: 'Для документу',
                       TEXT_FLAG_IN_SET: 'встановлено позначку отримання оригіналу',
                       TEXT_FLAG_NO_SET: 'Помилка!!! Документ не відмічено.',

                       KB_BUTTON_FIND_PARTNERS: '🔎 Пошук контрагента',
                       KB_BUTTON_SEND_INFORMATION_PARTNERS: 'Вивести інформацію про контрагнета',
                       KB_BUTTON_FIND_PRODUCT: '🔎 Пошук номенклатури',
                       KB_BUTTON_CREATE_EVENT: 'Створити подію',
                       KB_BUTTON_PARTNER_GET_EVENT: 'Отримати події контрагента',
                       KB_BUTTON_COMPANY_GET_EVENT: 'Отримати події компанії',
                       KB_BUTTON_CONTACT_PERSON_CANCELED: 'Не створювати подію',
                       KB_BUTTON_CONTACT_PERSON_NO: 'Без контактної особи',

                       KB_BUTTON_SEND_ADM: 'Відправити запит адміністратору',
                       KB_BUTTON_QR_DOCUMENTS: 'QR видаткової',

                       ERROR_1C_QR_STRUCTURE: 'Невірна структура QR',
                       ERROR_1C_QR_COMPARISON: 'В 1с в даний документ внесено змінени. '
                                               'Через це автоматичне відмітка не можлива.',
                       ERROR_1C_QR_MARK_SETTING: 'Не вдалося відмітити документ в 1с',
                       ERROR_1C_QR_FIND_DOCUMENT: 'В 1с не вдалося знайти такий документ',
                       ERROR_1C_QR_FIND_PARTNER: 'В 1с не вдалося знайти контрагента, вказаново в QR',

                       TYPE_DIFFERENCE_1C_NUMBER: 'Відрізняється номер документу',
                       TYPE_DIFFERENCE_1C_SUMMA: 'Відрізняється сума документу',
                       TYPE_DIFFERENCE_1C_DATE: 'Відрізняється дата документу',
                       TYPE_DIFFERENCE_1C_PARTNER: 'Відрізняється контрагент'
                       }

    @classmethod
    def get_body(cls, title_):
        _text = cls.TITLES_CONSTANT.get(title_, "")
        return _text

    def __call__(self, title_):
        return self.get_body(title_)


texts = Texts()
