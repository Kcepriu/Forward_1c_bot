import mongoengine as me
from datetime import datetime
from .status import STATUS_OPERATION

me.connect('forward_bot')

class User(me.Document):
    user_id = me.IntField(unique=True, required=True)
    name = me.StringField(max_length=255)
    telephone = me.StringField(min_length=10, max_length=12, regex='^[0-9]*$')
    status_operation = me.StringField(required=True, choices=STATUS_OPERATION, unique=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_user(cls, chat):
        user = cls.objects(user_id=chat.id)
        if not user:
            try:
                name = chat.last_name + ' ' + chat.first_name
            except:
                name = ""

            user = cls.objects.create(user_id=chat.id, name=name, status_operation='NOT_OPERATION')
        else:
            user = user[0]
        return user


class Text(me.Document):
    START_MESSAGE = 'start_message',
    OTHER_MESSAGE = 'others_message',
    PHOTO_MESSAGE = 'photo_message',
    DOCUMENT_MESSAGE = 'document_message'

    TITLES_CONSTANT = (
        (START_MESSAGE, 'start message'),
        (OTHER_MESSAGE, 'others message'),
        (PHOTO_MESSAGE, 'photo message'),
        (DOCUMENT_MESSAGE, 'document message')
    )

    title = me.StringField(required=True, choices=TITLES_CONSTANT, unique=True)
    body = me.StringField(min_length=2, max_length=4096)

    @classmethod
    def get_body(cls, title_):
        _text = cls.objects(title=title_)
        if _text:
            return _text.body

        return 'Not text from  - ' + title_


    # text = 'Вітаємо. Ви підключилися до бота зберігання скана документів'

