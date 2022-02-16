class Texts():
    NO_CONNECT = 'NO_CONNECT'
    NO_AUTH = 'NO_AUTH'
    NO_ACCESS = 'NO_ACCESS'
    NO_FIND_RESULT = 'NO_FIND_RESULT'
    NO_FIND_INFORMATION = 'NO_FIND_INFORMATION'
    NO_FIND_EVENTS = 'NO_FIND_EVENTS'
    TEXT_START = 'TEXT_START'
    TEXT_START_FIND_CONTRAHENTS = 'TEXT_START_FIND_CONTRAHENTS'
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
    TEXT_OPERATION_FROM_CONTRAHENTS = 'TEXT_OPERATION_FROM_CONTRAHENTS'


    KB_BUTTON_FIND_CONTRAHENTS = 'KB_BUTTON_FIND_CONTRAHENTS'
    KB_BUTTON_FIND_TOVAR = 'KB_BUTTON_FIND_TOVAR'
    KB_BUTTON_SEND_INFORMATION_CONTRAHENTS = 'KB_BUTTON_SEND_INFORMATION_CONTRAHENTS'

    KB_BUTTON_SEND_ADM = 'KB_BUTTON_SEND_ADM'
    KB_BUTTON_CREATE_EVENT = 'KB_BUTTON_CREATE_EVENT'
    KB_BUTTON_CONTRAHENT_GET_EVENT = 'KB_BUTTON_CONTRAHENT_GET_EVENT'
    KB_BUTTON_COMPANY_GET_EVENT = 'KB_BUTTON_COMPANY_GET_EVENT'
    KB_BUTTON_CONTACT_PERSON_CANCELED = 'KB_BUTTON_CONTACT_PERSON_CANCELED'
    KB_BUTTON_CONTACT_PERSON_NO = 'KB_BUTTON_CONTACT_PERSON_NO'

    TITLES_CONSTANT = {NO_CONNECT: 'Не вдалося зʼєднатися з 1с',
         NO_AUTH: 'Про вас відсутні дані в 1с. Зверніться до адміністратора',
         NO_ACCESS: 'У вас бракує прав для такої операції',
         NO_FIND_RESULT: 'Не знайдено жодного контрагента з такою назвою',
         NO_FIND_INFORMATION: 'Дані про контрагента відсутні',
         NO_FIND_EVENTS: 'Подій не знайдено',
         TEXT_START: 'Виберіть потрібну операцію, натиснувши відповідну кнопку 👇',
         TEXT_START_FIND_CONTRAHENTS: '👇 Введіть назву контрагента, і відправте повідомлення',
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
         TEXT_OPERATION_FROM_CONTRAHENTS: 'Операції з контрагентом:',

         KB_BUTTON_FIND_CONTRAHENTS: '🔎 Пошук контрагента',
         KB_BUTTON_SEND_INFORMATION_CONTRAHENTS: 'Вивести інформацію про контрагнета',
         KB_BUTTON_FIND_TOVAR: '🔎 Пошук номенклатури',
         KB_BUTTON_CREATE_EVENT: 'Створити подію',
         KB_BUTTON_CONTRAHENT_GET_EVENT: 'Отримати події контрагента',
         KB_BUTTON_COMPANY_GET_EVENT: 'Отримати події компанії',
         KB_BUTTON_CONTACT_PERSON_CANCELED: 'Не створювати подію',
         KB_BUTTON_CONTACT_PERSON_NO: 'Без контактної особи',

         KB_BUTTON_SEND_ADM: 'Відправити запит адміністратору'
                       }

    @classmethod
    def get_body(cls, title_):
        _text = cls.TITLES_CONSTANT.get(title_, "")
        return _text


